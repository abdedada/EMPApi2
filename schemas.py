from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime, time
from typing import List, Any, Literal


# User Schemas
class UserBase(BaseModel):
    """Schéma de base pour les utilisateurs"""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Schéma pour créer un utilisateur"""
    password: str


class UserUpdate(BaseModel):
    """Schéma pour mettre à jour un utilisateur"""
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(UserBase):
    """Schéma pour retourner un utilisateur"""
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schéma pour le login"""
    username: str
    password: str


class Token(BaseModel):
    """Schéma pour le token JWT"""
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class RefreshTokenRequest(BaseModel):
    """Schéma pour renouveler un token d'accès"""
    refresh_token: str


class TokenData(BaseModel):
    """Schéma pour les données du token"""
    username: Optional[str] = None


# ==================== SCHÉMAS ÉDUCATIFS ====================

# SchoolYear Schemas
class SchoolYearBase(BaseModel):
    """Schéma de base pour une année scolaire"""
    label: str
    startAt: datetime
    endAt: datetime
    enabled: bool = True
    current: bool = False


class SchoolYearCreate(SchoolYearBase):
    """Schéma pour créer une année scolaire"""
    pass


class SchoolYearUpdate(BaseModel):
    """Schéma pour mettre à jour une année scolaire"""
    label: Optional[str] = None
    startAt: Optional[datetime] = None
    endAt: Optional[datetime] = None
    enabled: Optional[bool] = None
    current: Optional[bool] = None


class SchoolYear(SchoolYearBase):
    """Schéma pour retourner une année scolaire"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Classe Schemas
class ClasseBase(BaseModel):
    """Schéma de base pour une classe"""
    label: str
    filiere: str
    schoolYear_id: int


class ClasseCreate(ClasseBase):
    """Schéma pour créer une classe"""
    pass


class ClasseUpdate(BaseModel):
    """Schéma pour mettre à jour une classe"""
    label: Optional[str] = None
    filiere: Optional[str] = None
    schoolYear_id: Optional[int] = None


class Classe(ClasseBase):
    """Schéma pour retourner une classe"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Module Schemas
class ModuleBase(BaseModel):
    """Schéma de base pour un module"""
    titre: str


class ModuleCreate(ModuleBase):
    """Schéma pour créer un module"""
    pass


class ModuleUpdate(BaseModel):
    """Schéma pour mettre à jour un module"""
    titre: Optional[str] = None


class Module(ModuleBase):
    """Schéma pour retourner un module"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Chapitre Schemas
class ChapitreBase(BaseModel):
    """Schéma de base pour un chapitre"""
    num: int
    titre: str
    module_id: int


class ChapitreCreate(ChapitreBase):
    """Schéma pour créer un chapitre"""
    pass


class ChapitreUpdate(BaseModel):
    """Schéma pour mettre à jour un chapitre"""
    num: Optional[int] = None
    titre: Optional[str] = None
    module_id: Optional[int] = None


class Chapitre(ChapitreBase):
    """Schéma pour retourner un chapitre"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Question Schemas
class QuestionBase(BaseModel):
    """Schéma de base pour une question"""
    enonce: str
    type: str
    content: Optional[dict] = None
    chapitre_id: int
    points: float = 1.0


class QuestionCreate(QuestionBase):
    """Schéma pour créer une question"""
    pass


class QuestionUpdate(BaseModel):
    """Schéma pour mettre à jour une question"""
    enonce: Optional[str] = None
    type: Optional[str] = None
    content: Optional[dict] = None
    chapitre_id: Optional[int] = None
    points: Optional[float] = None


class Question(QuestionBase):
    """Schéma pour retourner une question"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Evaluation Schemas
class EvaluationBase(BaseModel):
    """Schéma de base pour une évaluation"""
    num: str
    date: datetime
    classe_id: int
    module_id: int
    duree: int
    type: str
    nbr_questions: int


class EvaluationCreate(EvaluationBase):
    """Schéma pour créer une évaluation"""
    pass


class EvaluationUpdate(BaseModel):
    """Schéma pour mettre à jour une évaluation"""
    num: Optional[str] = None
    date: Optional[datetime] = None
    classe_id: Optional[int] = None
    module_id: Optional[int] = None
    duree: Optional[int] = None
    type: Optional[str] = None
    nbr_questions: Optional[int] = None


class Evaluation(EvaluationBase):
    """Schéma pour retourner une évaluation"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class EvaluationQuestionsSet(BaseModel):
    """Schéma pour définir les questions d'une évaluation"""
    question_ids: List[int]


# Student Schemas
class StudentBase(BaseModel):
    """Schéma de base pour un étudiant"""
    num: str
    idMassar: Optional[str] = None
    nom: str
    sexe: Optional[str] = None  # M ou F
    classe_id: int
    photo: Optional[str] = None
    enabled: bool = True


class StudentCreate(StudentBase):
    """Schéma pour créer un étudiant"""
    pass


class StudentUpdate(BaseModel):
    """Schéma pour mettre à jour un étudiant"""
    num: Optional[str] = None
    idMassar: Optional[str] = None
    nom: Optional[str] = None
    sexe: Optional[str] = None
    classe_id: Optional[int] = None
    photo: Optional[str] = None
    enabled: Optional[bool] = None


class Student(StudentBase):
    """Schéma pour retourner un étudiant"""
    id: int
    created_at: datetime
    changeEnabledAt: datetime
    nombre_absences: int
    somme_notes_participation: float

    class Config:
        from_attributes = True


# Reponse Schemas
class ReponseBase(BaseModel):
    """Schéma de base pour une réponse"""
    evaluation_id: int
    student_id: int
    content: Optional[dict] = None
    score: Optional[float] = None
    submittedAt: Optional[datetime] = None
    durationUsed: Optional[int] = None


class ReponseCreate(ReponseBase):
    """Schéma pour créer une réponse"""
    pass


class ReponseUpdate(BaseModel):
    """Schéma pour mettre à jour une réponse"""
    content: Optional[dict] = None
    score: Optional[float] = None
    submittedAt: Optional[datetime] = None
    durationUsed: Optional[int] = None


class Reponse(ReponseBase):
    """Schéma pour retourner une réponse"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== SCHÉMAS PRÉSENCE ET PARTICIPATION ====================

# Timetable Schemas
class TimetableBase(BaseModel):
    """Schéma de base pour un emploi du temps"""
    schoolYear_id: int
    startAt: datetime
    endAt: datetime


class TimetableCreate(TimetableBase):
    """Schéma pour créer un emploi du temps"""
    pass


class TimetableUpdate(BaseModel):
    """Schéma pour mettre à jour un emploi du temps"""
    schoolYear_id: Optional[int] = None
    startAt: Optional[datetime] = None
    endAt: Optional[datetime] = None


class Timetable(TimetableBase):
    """Schéma pour retourner un emploi du temps"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# TimeTableLine Schemas
class TimeTableLineBase(BaseModel):
    """Schéma de base pour une ligne d'emploi du temps"""
    timetable_id: int
    classe_id: int
    startAt: time  # Format HH:MM:SS (ex: "09:00:00") — Pydantic parse automatiquement
    endAt: time    # Format HH:MM:SS (ex: "11:00:00")
    day: int      # 1=lundi, 2=mardi, ..., 7=dimanche


class TimeTableLineCreate(TimeTableLineBase):
    """Schéma pour créer une ligne d'emploi du temps"""
    pass


class TimeTableLineUpdate(BaseModel):
    """Schéma pour mettre à jour une ligne d'emploi du temps"""
    timetable_id: Optional[int] = None
    classe_id: Optional[int] = None
    startAt: Optional[time] = None
    endAt: Optional[time] = None
    day: Optional[int] = None


class TimeTableLine(TimeTableLineBase):
    """Schéma pour retourner une ligne d'emploi du temps"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Seance Schemas
class SeanceBase(BaseModel):
    """Schéma de base pour une séance"""
    timetable_line_id: int
    date: datetime
    realise: bool = False
    contenu: Optional[str] = None


class SeanceCreate(SeanceBase):
    """Schéma pour créer une séance"""
    pass


class SeanceUpdate(BaseModel):
    """Schéma pour mettre à jour une séance"""
    timetable_line_id: Optional[int] = None
    date: Optional[datetime] = None
    realise: Optional[bool] = None
    contenu: Optional[str] = None


class Seance(SeanceBase):
    """Schéma pour retourner une séance"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Group Schemas
class GroupBase(BaseModel):
    """Schéma de base pour un groupe stable"""
    nom: str
    classe_id: int


class GroupCreate(GroupBase):
    pass


class GroupUpdate(BaseModel):
    nom: Optional[str] = None


class Group(GroupBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class GroupStudent(BaseModel):
    id: int
    group_id: Optional[int]
    student_id: int
    seance_id: int

    class Config:
        from_attributes = True


# NoteGroupe Schemas
class NoteGroupeBase(BaseModel):
    group_id: int
    seance_id: int
    note: float
    remarques: Optional[str] = None


class NoteGroupeCreate(NoteGroupeBase):
    pass


class NoteGroupeUpdate(BaseModel):
    note: Optional[float] = None
    remarques: Optional[str] = None


class NoteGroupe(NoteGroupeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Sequence Schemas
class SequenceBase(BaseModel):
    seance_id: int
    type: Literal["cours", "exercice", "tp", "evaluation", "autre"]
    duree: int = Field(gt=0)
    contenu: str
    chapitre_id: int


class SequenceCreate(SequenceBase):
    pass


class SequenceUpdate(BaseModel):
    seance_id: Optional[int] = None
    type: Optional[Literal["cours", "exercice", "tp", "evaluation", "autre"]] = None
    duree: Optional[int] = Field(default=None, gt=0)
    contenu: Optional[str] = None
    chapitre_id: Optional[int] = None


class Sequence(SequenceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Absence Schemas
class AbsenceBase(BaseModel):
    """Schéma de base pour une absence"""
    student_id: int
    seance_id: int
    raison: Optional[str] = None


class AbsenceCreate(AbsenceBase):
    """Schéma pour créer une absence"""
    pass


class AbsenceUpdate(BaseModel):
    """Schéma pour mettre à jour une absence"""
    student_id: Optional[int] = None
    seance_id: Optional[int] = None
    raison: Optional[str] = None


class Absence(AbsenceBase):
    """Schéma pour retourner une absence"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Participation Schemas
class ParticipationBase(BaseModel):
    """Schéma de base pour une participation"""
    student_id: int
    seance_id: int
    note: Optional[float] = None
    remarques: Optional[str] = None


class ParticipationCreate(ParticipationBase):
    """Schéma pour créer une participation"""
    pass


class ParticipationUpdate(BaseModel):
    """Schéma pour mettre à jour une participation"""
    student_id: Optional[int] = None
    seance_id: Optional[int] = None
    note: Optional[float] = None
    remarques: Optional[str] = None


class Participation(ParticipationBase):
    """Schéma pour retourner une participation"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
