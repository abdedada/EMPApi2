"""
Migration SQLite pour aligner la table `timetables` avec le modèle actuel.

But:
- Supprimer l'ancienne colonne `classe_id` (héritée d'un ancien schéma)
- Conserver les données existantes
- Garder la clé étrangère `schoolYear_id`
"""

from sqlalchemy import inspect, text
from database import engine


def migrate_timetables_table() -> None:
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print("=" * 60)
    print("Migration de la table timetables")
    print("=" * 60)

    if "timetables" not in tables:
        print("[INFO] Table 'timetables' absente. Aucune migration requise.")
        return

    columns = inspector.get_columns("timetables")
    column_names = [col["name"] for col in columns]
    print(f"[INFO] Colonnes actuelles: {column_names}")

    # Schéma attendu par models.py
    expected_columns = {"id", "schoolYear_id", "startAt", "endAt", "created_at"}

    # Si la colonne legacy n'existe plus, on sort proprement.
    if "classe_id" not in column_names and set(column_names) == expected_columns:
        print("[OK] Schéma déjà à jour. Aucune migration nécessaire.")
        return

    with engine.connect() as conn:
        try:
            # SQLite: on reconstruit la table pour retirer les anciennes colonnes.
            conn.execute(text("PRAGMA foreign_keys=OFF"))
            conn.execute(text("BEGIN"))

            conn.execute(
                text(
                    """
                    CREATE TABLE timetables_new (
                        id INTEGER NOT NULL PRIMARY KEY,
                        schoolYear_id INTEGER NOT NULL,
                        startAt DATETIME NOT NULL,
                        endAt DATETIME NOT NULL,
                        created_at DATETIME,
                        FOREIGN KEY(schoolYear_id) REFERENCES school_years(id)
                    )
                    """
                )
            )

            # Copie uniquement des colonnes utiles; created_at peut être absent en legacy.
            if "created_at" in column_names:
                conn.execute(
                    text(
                        """
                        INSERT INTO timetables_new (id, schoolYear_id, startAt, endAt, created_at)
                        SELECT id, schoolYear_id, startAt, endAt, created_at
                        FROM timetables
                        """
                    )
                )
            else:
                conn.execute(
                    text(
                        """
                        INSERT INTO timetables_new (id, schoolYear_id, startAt, endAt)
                        SELECT id, schoolYear_id, startAt, endAt
                        FROM timetables
                        """
                    )
                )

            conn.execute(text("DROP TABLE timetables"))
            conn.execute(text("ALTER TABLE timetables_new RENAME TO timetables"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS ix_timetables_id ON timetables (id)"))

            conn.execute(text("COMMIT"))
            print("[OK] Migration appliquée avec succès.")

        except Exception as exc:
            conn.execute(text("ROLLBACK"))
            print(f"[ERREUR] Migration annulée: {exc}")
            raise
        finally:
            conn.execute(text("PRAGMA foreign_keys=ON"))

    # Vérification post-migration
    new_columns = [col["name"] for col in inspect(engine).get_columns("timetables")]
    print(f"[INFO] Colonnes après migration: {new_columns}")


if __name__ == "__main__":
    migrate_timetables_table()

