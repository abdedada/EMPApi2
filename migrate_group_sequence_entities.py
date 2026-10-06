"""Create group/sequence tables and migrate groups to reusable teams."""

from sqlalchemy import inspect

from database import Base, engine
import models  # noqa: F401 - registers the entity models on Base.metadata


ENTITY_TABLES = ("groups", "group_students", "note_groupes", "sequences")


def _migrate_legacy_groups() -> None:
    inspector = inspect(engine)
    group_columns = {column["name"] for column in inspector.get_columns("groups")}
    note_columns = {column["name"] for column in inspector.get_columns("note_groupes")}
    if "classe_id" in group_columns and "seance_id" in note_columns:
        return

    with engine.connect() as conn:
        group_rows = conn.exec_driver_sql("SELECT * FROM groups").mappings().all()
        assignments = conn.exec_driver_sql(
            """
            SELECT gs.group_id, s.classe_id
            FROM group_students AS gs
            JOIN students AS s ON s.id = gs.student_id
            """
        ).all()
        session_classes = {}
        if "seance_id" in group_columns:
            session_classes = dict(
                conn.exec_driver_sql(
                    """
                    SELECT s.id, lines.classe_id
                    FROM seances AS s
                    JOIN timetable_lines AS lines ON lines.id = s.timetable_line_id
                    """
                ).all()
            )

    classes_by_group = {}
    for group_id, classe_id in assignments:
        classes_by_group.setdefault(group_id, set()).add(classe_id)
    for row in group_rows:
        group_id = row["id"]
        if "classe_id" in group_columns and row["classe_id"] is not None:
            classe_id = row["classe_id"]
        elif "seance_id" in group_columns and row["seance_id"] in session_classes:
            classe_id = session_classes[row["seance_id"]]
        else:
            inferred_classes = classes_by_group.get(group_id, set())
            if len(inferred_classes) != 1:
                raise RuntimeError(
                    f"Cannot determine a unique class for group {group_id}; "
                    "assign it to a class before migrating."
                )
            classe_id = next(iter(inferred_classes))
        classes_by_group[group_id] = {classe_id}

    note_rows = []
    with engine.connect() as conn:
        note_rows = conn.exec_driver_sql("SELECT * FROM note_groupes").mappings().all()

    raw_connection = engine.raw_connection()
    cursor = raw_connection.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys=OFF")
        cursor.execute("BEGIN IMMEDIATE")
        cursor.execute(
            """
            CREATE TABLE groups_new (
                id INTEGER NOT NULL PRIMARY KEY,
                nom VARCHAR NOT NULL,
                classe_id INTEGER NOT NULL,
                created_at DATETIME,
                FOREIGN KEY(classe_id) REFERENCES classes(id)
            )
            """
        )
        for row in group_rows:
            cursor.execute(
                """
                INSERT INTO groups_new (id, nom, classe_id, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (row["id"], row["nom"], next(iter(classes_by_group[row["id"]])), row.get("created_at")),
            )
        cursor.execute(
            """
            CREATE TABLE note_groupes_new (
                id INTEGER NOT NULL PRIMARY KEY,
                group_id INTEGER NOT NULL,
                seance_id INTEGER NOT NULL,
                note FLOAT NOT NULL,
                remarques TEXT,
                created_at DATETIME,
                CONSTRAINT uq_note_groupe_seance UNIQUE (group_id, seance_id),
                FOREIGN KEY(group_id) REFERENCES groups_new(id),
                FOREIGN KEY(seance_id) REFERENCES seances(id)
            )
            """
        )
        for row in note_rows:
            seance_id = row.get("seance_id")
            if seance_id is None:
                if "seance_id" not in group_columns:
                    raise RuntimeError(
                        f"Cannot determine the session for legacy group note {row['id']}."
                    )
                seance_id = next(
                    group["seance_id"] for group in group_rows if group["id"] == row["group_id"]
                )
            cursor.execute(
                """
                INSERT INTO note_groupes_new
                    (id, group_id, seance_id, note, remarques, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    row["id"],
                    row["group_id"],
                    seance_id,
                    row["note"],
                    row.get("remarques"),
                    row.get("created_at"),
                ),
            )
        cursor.execute("DROP TABLE note_groupes")
        cursor.execute("DROP TABLE groups")
        cursor.execute("ALTER TABLE groups_new RENAME TO groups")
        cursor.execute("ALTER TABLE note_groupes_new RENAME TO note_groupes")
        cursor.execute("CREATE INDEX ix_groups_id ON groups (id)")
        cursor.execute("CREATE INDEX ix_groups_classe_id ON groups (classe_id)")
        cursor.execute("CREATE INDEX ix_note_groupes_id ON note_groupes (id)")
        raw_connection.commit()
    except Exception:
        raw_connection.rollback()
        raise
    finally:
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
        raw_connection.close()


def _allow_unassigned_students() -> None:
    assignment_columns = inspect(engine).get_columns("group_students")
    group_id_column = next(column for column in assignment_columns if column["name"] == "group_id")
    if group_id_column["nullable"]:
        return

    raw_connection = engine.raw_connection()
    cursor = raw_connection.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys=OFF")
        cursor.execute("BEGIN IMMEDIATE")
        cursor.execute(
            """
            CREATE TABLE group_students_new (
                id INTEGER NOT NULL PRIMARY KEY,
                group_id INTEGER,
                student_id INTEGER NOT NULL,
                seance_id INTEGER NOT NULL,
                CONSTRAINT uq_student_group_seance UNIQUE (student_id, seance_id),
                FOREIGN KEY(group_id) REFERENCES groups(id),
                FOREIGN KEY(student_id) REFERENCES students(id),
                FOREIGN KEY(seance_id) REFERENCES seances(id)
            )
            """
        )
        cursor.execute(
            """
            INSERT INTO group_students_new (id, group_id, student_id, seance_id)
            SELECT id, group_id, student_id, seance_id FROM group_students
            """
        )
        cursor.execute("DROP TABLE group_students")
        cursor.execute("ALTER TABLE group_students_new RENAME TO group_students")
        cursor.execute("CREATE INDEX ix_group_students_id ON group_students (id)")
        raw_connection.commit()
    except Exception:
        raw_connection.rollback()
        raise
    finally:
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
        raw_connection.close()


def migrate_group_sequence_entities() -> None:
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    missing_tables = [name for name in ENTITY_TABLES if name not in existing_tables]

    if missing_tables:
        required_parent_tables = {"seances", "students", "chapitres"}
        missing_parents = required_parent_tables - existing_tables
        if missing_parents:
            raise RuntimeError(
                "Cannot create group/sequence tables; required tables are missing: "
                + ", ".join(sorted(missing_parents))
            )
        tables = [Base.metadata.tables[name] for name in ENTITY_TABLES]
        Base.metadata.create_all(bind=engine, tables=tables, checkfirst=True)

    _migrate_legacy_groups()
    _allow_unassigned_students()

    inspector = inspect(engine)
    expected_columns = {
        "groups": {"id", "nom", "classe_id", "created_at"},
        "group_students": {"id", "group_id", "student_id", "seance_id"},
        "note_groupes": {"id", "group_id", "seance_id", "note", "remarques", "created_at"},
        "sequences": {
            "id", "seance_id", "type", "duree", "contenu", "chapitre_id", "created_at"
        },
    }
    table_names = set(inspector.get_table_names())
    for table_name, expected in expected_columns.items():
        if table_name not in table_names:
            raise RuntimeError(f"Migration did not create table '{table_name}'")
        actual = {column["name"] for column in inspector.get_columns(table_name)}
        missing_columns = expected - actual
        if missing_columns:
            raise RuntimeError(
                f"Table '{table_name}' is incomplete; missing columns: "
                + ", ".join(sorted(missing_columns))
            )
    assignment_columns = {
        column["name"]: column
        for column in inspector.get_columns("group_students")
    }
    if not assignment_columns["group_id"]["nullable"]:
        raise RuntimeError("The group_students.group_id column must allow NULL assignments.")

    print("Migration completed: reusable groups and per-session group grades are ready.")


if __name__ == "__main__":
    migrate_group_sequence_entities()
