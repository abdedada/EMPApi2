from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Table, Float, JSON, event, Time, UniqueConstraint, CheckConstraint, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# Association table pour la relation many-to-many entre Evaluation et Question
evaluation_question_association = Table(
    'evaluation_question',
    Base.metadata,
    Column('evaluation_id', Integer, ForeignKey('evaluations.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('questions.id'), primary_key=True)
)


class User(Base):
    """Modèle pour les utilisateurs"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)


# MODÈLES POUR LE SYSTÈME ÉDUCATIF

class SchoolYear(Base):
    """Modèle pour l'année scolaire"""
    __tablename__ = "school_years"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, unique=True, nullable=False, index=True)  # Ex: "2023-2024"
    startAt = Column(DateTime, nullable=False)
    endAt = Column(DateTime, nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    current = Column(Boolean, default=False, nullable=False)

    # Relations
    classes = relationship("Classe", back_populates="schoolYear", cascade="all, delete-orphan")
    timetables = relationship("Timetable", back_populates="schoolYear", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow)


class Classe(Base):
    """Modèle pour une classe"""
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)  # Ex: "1ère année"
    filiere = Column(String, nullable=False)  # Ex: "Informatique"
    schoolYear_id = Column(Integer, ForeignKey('school_years.id'), nullable=False)

    # Relations
    schoolYear = relationship("SchoolYear", back_populates="classes")
    students = relationship("Student", back_populates="classe", cascade="all, delete-orphan")
    evaluations = relationship("Evaluation", back_populates="classe", cascade="all, delete-orphan")
    groupes = relationship("Group", back_populates="classe", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        # Index composé pour l'unicité par année scolaire
        # Column('label', String),
        # Column('filiere', String),
        # Column('schoolYear_id', Integer),
    )


class Module(Base):
    """Modèle pour un module d'enseignement"""
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String, nullable=False)

    # Relations
    chapitres = relationship("Chapitre", back_populates="module", cascade="all, delete-orphan")
    evaluations = relationship("Evaluation", back_populates="module", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow)


class Chapitre(Base):
    """Modèle pour un chapitre du module"""
    __tablename__ = "chapitres"

    id = Column(Integer, primary_key=True, index=True)
    num = Column(Integer, nullable=False)
    titre = Column(String, nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)

    # Relations
    module = relationship("Module", back_populates="chapitres")
    questions = relationship("Question", back_populates="chapitre", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow)


class Question(Base):
    """Modèle pour une question d'examen"""
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    enonce = Column(String, nullable=False)
    type = Column(String, nullable=False)  # Ex: "QCM", "texte", "vrai/faux"
    content = Column(JSON, nullable=True)  # Contenu JSON (options, réponse attendue, etc)
    chapitre_id = Column(Integer, ForeignKey('chapitres.id'), nullable=False)
    points = Column(Float, default=1.0, nullable=False)

    # Relations
    chapitre = relationship("Chapitre", back_populates="questions")
    evaluations = relationship("Evaluation", secondary=evaluation_question_association, overlaps="questions")
    created_at = Column(DateTime, default=datetime.utcnow)


class Evaluation(Base):
    """Modèle pour une évaluation (examen)"""
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    num = Column(String, nullable=False, unique=True, index=True)  # Numéro/identifiant de l'examen
    date = Column(DateTime, nullable=False)
    classe_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=False)
    duree = Column(Integer, nullable=False)  # Durée en minutes
    type = Column(String, nullable=False)  # Ex: "examen", "contrôle"
    nbr_questions = Column(Integer, nullable=False)

    # Relations
    classe = relationship("Classe", back_populates="evaluations")
    module = relationship("Module", back_populates="evaluations")
    questions = relationship("Question", secondary=evaluation_question_association, overlaps="evaluations")
    reponses = relationship("Reponse", back_populates="evaluation", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow)


class Student(Base):
    """Modèle pour un étudiant"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    num = Column(String, nullable=False, index=True)  # Numéro étudiant
    idMassar = Column(String, nullable=True, unique=True, index=True)  # ID Massar (Maroc)
    nom = Column(String, nullable=False)
    sexe = Column(String, nullable=True)  # M (Masculin) ou F (Féminin)
    classe_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    photo = Column(String, nullable=True)
    enabled = Column(Boolean, default=True, nullable=False)
    changeEnabledAt = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relations
    classe = relationship("Classe", back_populates="students")
    reponses = relationship("Reponse", back_populates="student", cascade="all, delete-orphan")
    absences = relationship("Absence", back_populates="student", cascade="all, delete-orphan")
    participations = relationship("Participation", back_populates="student", cascade="all, delete-orphan")
    group_assignments = relationship("GroupStudent", back_populates="student", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow)

    @property
    def nombre_absences(self):
        return len(self.absences)

    @property
    def somme_notes_participation(self):
        return sum(participation.note or 0 for participation in self.participations)
    
    __table_args__ = (
        UniqueConstraint('num', 'classe_id', name='uq_student_num_classe'),
    )


class Reponse(Base):
    """Modèle pour une réponse d'étudiant à une évaluation"""
    __tablename__ = "reponses"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey('evaluations.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    content = Column(JSON, nullable=True)  # Réponses en JSON
    score = Column(Float, nullable=True)  # Score obtenu
    submittedAt = Column(DateTime, nullable=True)  # Date de soumission
    durationUsed = Column(Integer, nullable=True)  # Durée utilisée en secondes

    # Relations
    evaluation = relationship("Evaluation", back_populates="reponses")
    student = relationship("Student", back_populates="reponses")
    created_at = Column(DateTime, default=datetime.utcnow)


# ==================== SYSTÈME DE PRÉSENCE ET PARTICIPATION ====================

class Timetable(Base):
    """Modèle pour l'emploi du temps d'une classe pour une année scolaire"""
    __tablename__ = "timetables"

    id = Column(Integer, primary_key=True, index=True)
    schoolYear_id = Column(Integer, ForeignKey('school_years.id'), nullable=False)
    startAt = Column(DateTime, nullable=False)  # Début de l'emploi du temps
    endAt = Column(DateTime, nullable=False)    # Fin de l'emploi du temps

    # Relations
    schoolYear = relationship("SchoolYear", back_populates="timetables")
    timeTableLines = relationship("TimeTableLine", back_populates="timetable", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow)


class TimeTableLine(Base):
    """Modèle pour une ligne d'emploi du temps (créneau horaire récurrent)"""
    __tablename__ = "timetable_lines"

    id = Column(Integer, primary_key=True, index=True)
    timetable_id = Column(Integer, ForeignKey('timetables.id'), nullable=False)
    classe_id = Column(Integer, ForeignKey('classes.id'), nullable=False)
    startAt = Column(Time, nullable=False)      # Heure de début (ex: 09:00:00)
    endAt = Column(Time, nullable=False)        # Heure de fin (ex: 11:00:00)
    day = Column(Integer, nullable=False)       # Jour de la semaine (1=lundi, 2=mardi, ..., 7=dimanche)

    # Relations
    timetable = relationship("Timetable", back_populates="timeTableLines")
    classe = relationship("Classe")
    seances = relationship("Seance", back_populates="timeTableLine", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow)


class Seance(Base):
    """Modèle pour une séance de cours (réalisation d'une ligne d'emploi du temps)"""
    __tablename__ = "seances"

    id = Column(Integer, primary_key=True, index=True)
    timetable_line_id = Column(Integer, ForeignKey('timetable_lines.id'), nullable=False)
    date = Column(DateTime, nullable=False)     # Date et heure de la séance
    realise = Column(Boolean, default=False, nullable=False)  # Si la séance a eu lieu
    contenu = Column(Text, nullable=True)       # Contenu du cours (notes, matière couverte, etc)

    # Relations
    timeTableLine = relationship("TimeTableLine", back_populates="seances")
    absences = relationship("Absence", back_populates="seance", cascade="all, delete-orphan")
    participations = relationship("Participation", back_populates="seance", cascade="all, delete-orphan")
    group_assignments = relationship("GroupStudent", back_populates="seance", cascade="all, delete-orphan")
    group_notes = relationship("NoteGroupe", back_populates="seance", cascade="all, delete-orphan")
    sequences = relationship("Sequence", back_populates="seance", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow)


class Group(Base):
    """Groupe stable rattaché à une classe et réutilisable d'une séance à l'autre"""
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, nullable=False)
    classe_id = Column(Integer, ForeignKey("classes.id"), nullable=False, index=True)

    classe = relationship("Classe", back_populates="groupes")
    members = relationship("GroupStudent", back_populates="group", cascade="all, delete-orphan")
    notes = relationship("NoteGroupe", back_populates="group", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow)


class GroupStudent(Base):
    """Historique du groupe auquel appartient un étudiant pour chaque séance"""
    __tablename__ = "group_students"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    seance_id = Column(Integer, ForeignKey("seances.id"), nullable=False)

    group = relationship("Group", back_populates="members")
    student = relationship("Student", back_populates="group_assignments")
    seance = relationship("Seance", back_populates="group_assignments")

    __table_args__ = (
        UniqueConstraint("student_id", "seance_id", name="uq_student_group_seance"),
    )


class NoteGroupe(Base):
    """Note attribuée à un groupe pour sa séance"""
    __tablename__ = "note_groupes"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    seance_id = Column(Integer, ForeignKey("seances.id"), nullable=False)
    note = Column(Float, nullable=False)
    remarques = Column(Text, nullable=True)

    group = relationship("Group", back_populates="notes")
    seance = relationship("Seance", back_populates="group_notes")
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("group_id", "seance_id", name="uq_note_groupe_seance"),
    )


class SequenceType(str, PyEnum):
    COURS = "cours"
    EXERCICE = "exercice"
    TP = "tp"
    EVALUATION = "evaluation"
    AUTRE = "autre"


class Sequence(Base):
    """Séquence pédagogique réalisée pendant une séance"""
    __tablename__ = "sequences"

    id = Column(Integer, primary_key=True, index=True)
    seance_id = Column(Integer, ForeignKey("seances.id"), nullable=False, index=True)
    type = Column(
        SQLAlchemyEnum(
            SequenceType,
            values_callable=lambda enum_type: [item.value for item in enum_type],
            name="sequence_type",
        ),
        nullable=False,
    )
    duree = Column(Integer, nullable=False)  # Durée en minutes
    contenu = Column(Text, nullable=False)
    chapitre_id = Column(Integer, ForeignKey("chapitres.id"), nullable=False)

    seance = relationship("Seance", back_populates="sequences")
    chapitre = relationship("Chapitre")
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (CheckConstraint("duree > 0", name="ck_sequence_duree_positive"),)


class Absence(Base):
    """Modèle pour enregistrer l'absence d'un étudiant à une séance"""
    __tablename__ = "absences"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    seance_id = Column(Integer, ForeignKey('seances.id'), nullable=False)
    raison = Column(String, nullable=True)      # Motif de l'absence

    # Relations
    student = relationship("Student", back_populates="absences")
    seance = relationship("Seance", back_populates="absences")
    created_at = Column(DateTime, default=datetime.utcnow)


class Participation(Base):
    """Modèle pour enregistrer la participation d'un étudiant lors d'une séance"""
    __tablename__ = "participations"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    seance_id = Column(Integer, ForeignKey('seances.id'), nullable=False)
    note = Column(Float, nullable=True)         # Score de participation (ex: 0-5 ou 0-20)
    remarques = Column(Text, nullable=True)     # Observations sur la participation

    # Relations
    student = relationship("Student", back_populates="participations")
    seance = relationship("Seance", back_populates="participations")
    created_at = Column(DateTime, default=datetime.utcnow)


# Event listener pour mettre à jour changeEnabledAt quand enabled change
@event.listens_for(Student, 'before_update')
def receive_before_update(mapper, connection, target):
    """Mettre à jour changeEnabledAt quand la colonne enabled change"""
    from sqlalchemy.inspection import inspect
    
    # Obtenir l'état de l'objet
    insp = inspect(target)
    
    # Vérifier si la colonne 'enabled' a changé
    # Utiliser history pour vérifier les changements
    history = insp.attrs.enabled.history
    if history.has_changes():
        target.changeEnabledAt = datetime.utcnow()
