from sqlalchemy.orm import Session, selectinload
import bcrypt
import models
from models import User
from schemas import UserCreate, UserUpdate


def get_password_hash(password: str) -> str:
    """Hacher un mot de passe"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifier un mot de passe"""
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())



# User CRUD
def get_user(db: Session, user_id: int):
    """Obtenir un utilisateur par ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    """Obtenir un utilisateur par nom d'utilisateur"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    """Obtenir un utilisateur par email"""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Obtenir la liste des utilisateurs"""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    """Créer un nouvel utilisateur"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate):
    """Mettre à jour un utilisateur"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user.dict(exclude_unset=True)
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """Supprimer un utilisateur"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


# ==================== SCHOOL YEAR CRUD ====================

def create_school_year(db: Session, school_year):
    """Créer une nouvelle année scolaire"""
    db_school_year = models.SchoolYear(**school_year.dict())
    db.add(db_school_year)
    db.commit()
    db.refresh(db_school_year)
    return db_school_year


def get_school_year(db: Session, school_year_id: int):
    """Obtenir une année scolaire par ID"""
    return db.query(models.SchoolYear).filter(models.SchoolYear.id == school_year_id).first()


def get_school_years(db: Session, skip: int = 0, limit: int = 100):
    """Lister toutes les années scolaires"""
    return db.query(models.SchoolYear).offset(skip).limit(limit).all()


def update_school_year(db: Session, school_year_id: int, school_year):
    """Mettre à jour une année scolaire"""
    db_school_year = get_school_year(db, school_year_id)
    if not db_school_year:
        return None
    update_data = school_year.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_school_year, field, value)
    db.commit()
    db.refresh(db_school_year)
    return db_school_year


def delete_school_year(db: Session, school_year_id: int):
    """Supprimer une année scolaire"""
    db_school_year = get_school_year(db, school_year_id)
    if not db_school_year:
        return False
    db.delete(db_school_year)
    db.commit()
    return True


# ==================== CLASSE CRUD ====================

def create_classe(db: Session, classe):
    """Créer une classe et ses quatorze groupes."""
    db_classe = models.Classe(**classe.dict())
    db.add(db_classe)
    db.flush()
    db.add_all(
        models.Group(nom=f"Groupe {number}", classe_id=db_classe.id)
        for number in range(1, 15)
    )
    db.commit()
    db.refresh(db_classe)
    return db_classe


def get_classe(db: Session, classe_id: int):
    """Obtenir une classe par ID"""
    return db.query(models.Classe).filter(models.Classe.id == classe_id).first()


def get_classes(db: Session, skip: int = 0, limit: int = 100):
    """Lister toutes les classes"""
    return db.query(models.Classe).offset(skip).limit(limit).all()


def get_classes_by_school_year(db: Session, school_year_id: int):
    """Lister les classes d'une année scolaire"""
    return db.query(models.Classe).filter(models.Classe.schoolYear_id == school_year_id).all()


def update_classe(db: Session, classe_id: int, classe):
    """Mettre à jour une classe"""
    db_classe = get_classe(db, classe_id)
    if not db_classe:
        return None
    update_data = classe.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_classe, field, value)
    db.commit()
    db.refresh(db_classe)
    return db_classe


def delete_classe(db: Session, classe_id: int):
    """Supprimer une classe"""
    db_classe = get_classe(db, classe_id)
    if not db_classe:
        return False
    db.delete(db_classe)
    db.commit()
    return True


# ==================== MODULE CRUD ====================

def create_module(db: Session, module):
    """Créer un nouveau module"""
    db_module = models.Module(**module.dict())
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module


def get_module(db: Session, module_id: int):
    """Obtenir un module par ID"""
    return db.query(models.Module).filter(models.Module.id == module_id).first()


def get_modules(db: Session, skip: int = 0, limit: int = 100):
    """Lister tous les modules"""
    return db.query(models.Module).offset(skip).limit(limit).all()


def update_module(db: Session, module_id: int, module):
    """Mettre à jour un module"""
    db_module = get_module(db, module_id)
    if not db_module:
        return None
    update_data = module.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_module, field, value)
    db.commit()
    db.refresh(db_module)
    return db_module


def delete_module(db: Session, module_id: int):
    """Supprimer un module"""
    db_module = get_module(db, module_id)
    if not db_module:
        return False
    db.delete(db_module)
    db.commit()
    return True


# ==================== CHAPITRE CRUD ====================

def create_chapitre(db: Session, chapitre):
    """Créer un nouveau chapitre"""
    db_chapitre = models.Chapitre(**chapitre.dict())
    db.add(db_chapitre)
    db.commit()
    db.refresh(db_chapitre)
    return db_chapitre


def get_chapitre(db: Session, chapitre_id: int):
    """Obtenir un chapitre par ID"""
    return db.query(models.Chapitre).filter(models.Chapitre.id == chapitre_id).first()


def get_chapitres(db: Session, skip: int = 0, limit: int = 100):
    """Lister tous les chapitres"""
    return db.query(models.Chapitre).offset(skip).limit(limit).all()


def get_chapitres_by_module(db: Session, module_id: int):
    """Lister les chapitres d'un module"""
    return db.query(models.Chapitre).filter(models.Chapitre.module_id == module_id).all()


def update_chapitre(db: Session, chapitre_id: int, chapitre):
    """Mettre à jour un chapitre"""
    db_chapitre = get_chapitre(db, chapitre_id)
    if not db_chapitre:
        return None
    update_data = chapitre.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_chapitre, field, value)
    db.commit()
    db.refresh(db_chapitre)
    return db_chapitre


def delete_chapitre(db: Session, chapitre_id: int):
    """Supprimer un chapitre"""
    db_chapitre = get_chapitre(db, chapitre_id)
    if not db_chapitre:
        return False
    db.delete(db_chapitre)
    db.commit()
    return True


# ==================== QUESTION CRUD ====================

def create_question(db: Session, question):
    """Créer une nouvelle question"""
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_question(db: Session, question_id: int):
    """Obtenir une question par ID"""
    return db.query(models.Question).filter(models.Question.id == question_id).first()


def get_questions(db: Session, skip: int = 0, limit: int = 100):
    """Lister toutes les questions"""
    return db.query(models.Question).offset(skip).limit(limit).all()


def get_questions_by_chapitre(db: Session, chapitre_id: int):
    """Lister les questions d'un chapitre"""
    return db.query(models.Question).filter(models.Question.chapitre_id == chapitre_id).all()


def get_questions_by_evaluation(db: Session, evaluation_id: int):
    """Lister les questions d'une évaluation"""
    return db.query(models.Question).join(models.evaluation_question_association).filter(models.evaluation_question_association.c.evaluation_id == evaluation_id).all()


def get_questions_by_module(db: Session, module_id: int):
    """Lister toutes les questions d'un module"""
    return db.query(models.Question).join(models.Chapitre).filter(models.Chapitre.module_id == module_id).all()


def set_evaluation_questions(db: Session, evaluation_id: int, question_ids: list[int]):
    """Définir les questions d'une évaluation"""
    # Vérifier que l'évaluation existe
    evaluation = get_evaluation(db, evaluation_id)
    if not evaluation:
        return None
    
    # Supprimer les associations existantes
    db.execute(models.evaluation_question_association.delete().where(models.evaluation_question_association.c.evaluation_id == evaluation_id))
    
    # Ajouter les nouvelles associations
    for question_id in question_ids:
        # Vérifier que la question existe
        question = get_question(db, question_id)
        if question:
            db.execute(models.evaluation_question_association.insert().values(evaluation_id=evaluation_id, question_id=question_id))
    
    db.commit()
    return evaluation


def update_question(db: Session, question_id: int, question):
    """Mettre à jour une question"""
    db_question = get_question(db, question_id)
    if not db_question:
        return None
    update_data = question.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_question, field, value)
    db.commit()
    db.refresh(db_question)
    return db_question


def delete_question(db: Session, question_id: int):
    """Supprimer une question"""
    db_question = get_question(db, question_id)
    if not db_question:
        return False
    db.delete(db_question)
    db.commit()
    return True


# ==================== EVALUATION CRUD ====================

def create_evaluation(db: Session, evaluation):
    """Créer une nouvelle évaluation"""
    db_evaluation = models.Evaluation(**evaluation.dict())
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation


def get_evaluation(db: Session, evaluation_id: int):
    """Obtenir une évaluation par ID"""
    return db.query(models.Evaluation).filter(models.Evaluation.id == evaluation_id).first()


def get_evaluations(db: Session, skip: int = 0, limit: int = 100):
    """Lister toutes les évaluations"""
    return db.query(models.Evaluation).offset(skip).limit(limit).all()


def get_evaluations_by_classe(db: Session, classe_id: int):
    """Lister les évaluations d'une classe"""
    return db.query(models.Evaluation).filter(models.Evaluation.classe_id == classe_id).all()


def get_evaluations_by_module(db: Session, module_id: int):
    """Lister les évaluations d'un module"""
    return db.query(models.Evaluation).filter(models.Evaluation.module_id == module_id).all()


def update_evaluation(db: Session, evaluation_id: int, evaluation):
    """Mettre à jour une évaluation"""
    db_evaluation = get_evaluation(db, evaluation_id)
    if not db_evaluation:
        return None
    update_data = evaluation.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_evaluation, field, value)
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation


def delete_evaluation(db: Session, evaluation_id: int):
    """Supprimer une évaluation"""
    db_evaluation = get_evaluation(db, evaluation_id)
    if not db_evaluation:
        return False
    db.delete(db_evaluation)
    db.commit()
    return True


# ==================== STUDENT CRUD ====================

def create_student(db: Session, student):
    """Créer un nouvel étudiant ou mettre à jour s'il existe déjà"""
    existing_student = db.query(models.Student).filter(
        models.Student.num == student.num,
        models.Student.classe_id == student.classe_id
    ).first()
    
    if existing_student:
        # Mettre à jour l'étudiant existant avec les nouvelles données
        update_data = student.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing_student, field, value)
        db.commit()
        db.refresh(existing_student)
        return existing_student
    
    # Créer un nouvel étudiant
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_student(db: Session, student_id: int):
    """Obtenir un étudiant par ID"""
    return db.query(models.Student).options(
        selectinload(models.Student.absences),
        selectinload(models.Student.participations),
    ).filter(models.Student.id == student_id).first()


def get_students(db: Session, skip: int = 0, limit: int = 100):
    """Lister tous les étudiants"""
    return db.query(models.Student).options(
        selectinload(models.Student.absences),
        selectinload(models.Student.participations),
    ).offset(skip).limit(limit).all()


def get_students_by_classe(db: Session, classe_id: int):
    """Lister les étudiants d'une classe"""
    return db.query(models.Student).options(
        selectinload(models.Student.absences),
        selectinload(models.Student.participations),
    ).filter(models.Student.classe_id == classe_id).all()


def update_student(db: Session, student_id: int, student):
    """Mettre à jour un étudiant"""
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    update_data = student.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: int):
    """Supprimer un étudiant"""
    db_student = get_student(db, student_id)
    if not db_student:
        return False
    db.delete(db_student)
    db.commit()
    return True


# ==================== REPONSE CRUD ====================

def create_reponse(db: Session, reponse):
    """Créer une nouvelle réponse"""
    db_reponse = models.Reponse(**reponse.dict())
    db.add(db_reponse)
    db.commit()
    db.refresh(db_reponse)
    return db_reponse


def get_reponse(db: Session, reponse_id: int):
    """Obtenir une réponse par ID"""
    return db.query(models.Reponse).filter(models.Reponse.id == reponse_id).first()


def get_reponses(db: Session, skip: int = 0, limit: int = 100):
    """Lister toutes les réponses"""
    return db.query(models.Reponse).offset(skip).limit(limit).all()


def get_reponses_by_evaluation(db: Session, evaluation_id: int):
    """Lister les réponses d'une évaluation"""
    return db.query(models.Reponse).filter(models.Reponse.evaluation_id == evaluation_id).all()


def get_reponses_by_student(db: Session, student_id: int):
    """Lister les réponses d'un étudiant"""
    return db.query(models.Reponse).filter(models.Reponse.student_id == student_id).all()


def update_reponse(db: Session, reponse_id: int, reponse):
    """Mettre à jour une réponse"""
    db_reponse = get_reponse(db, reponse_id)
    if not db_reponse:
        return None
    update_data = reponse.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_reponse, field, value)
    db.commit()
    db.refresh(db_reponse)
    return db_reponse


def delete_reponse(db: Session, reponse_id: int):
    """Supprimer une réponse"""
    db_reponse = get_reponse(db, reponse_id)
    if not db_reponse:
        return False
    db.delete(db_reponse)
    db.commit()
    return True


# ==================== TIMETABLE CRUD ====================

def create_timetable(db: Session, timetable):
    """Créer un nouvel emploi du temps"""
    db_timetable = models.Timetable(**timetable.dict())
    db.add(db_timetable)
    db.commit()
    db.refresh(db_timetable)
    return db_timetable


def get_timetable(db: Session, timetable_id: int):
    """Obtenir un emploi du temps par ID"""
    return db.query(models.Timetable).filter(models.Timetable.id == timetable_id).first()


def get_timetables(db: Session, skip: int = 0, limit: int = 100):
    """Lister tous les emplois du temps"""
    return db.query(models.Timetable).offset(skip).limit(limit).all()


def get_timetables_by_classe(db: Session, classe_id: int):
    """Lister les emplois du temps d'une classe via les lignes d'emploi du temps"""
    return (
        db.query(models.Timetable)
        .join(models.TimeTableLine, models.TimeTableLine.timetable_id == models.Timetable.id)
        .filter(models.TimeTableLine.classe_id == classe_id)
        .distinct()
        .all()
    )


def get_timetables_by_school_year(db: Session, school_year_id: int):
    """Lister les emplois du temps d'une année scolaire"""
    return db.query(models.Timetable).filter(models.Timetable.schoolYear_id == school_year_id).all()


def update_timetable(db: Session, timetable_id: int, timetable):
    """Mettre à jour un emploi du temps"""
    db_timetable = get_timetable(db, timetable_id)
    if not db_timetable:
        return None
    update_data = timetable.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_timetable, field, value)
    db.commit()
    db.refresh(db_timetable)
    return db_timetable


def delete_timetable(db: Session, timetable_id: int):
    """Supprimer un emploi du temps"""
    db_timetable = get_timetable(db, timetable_id)
    if not db_timetable:
        return False
    db.delete(db_timetable)
    db.commit()
    return True


# ==================== TIMETABLE LINE CRUD ====================

def create_timetable_line(db: Session, timetable_line):
    """Créer une nouvelle ligne d'emploi du temps"""
    db_timetable_line = models.TimeTableLine(**timetable_line.dict())
    db.add(db_timetable_line)
    db.commit()
    db.refresh(db_timetable_line)
    return db_timetable_line


def get_timetable_line(db: Session, timetable_line_id: int):
    """Obtenir une ligne d'emploi du temps par ID"""
    return db.query(models.TimeTableLine).filter(models.TimeTableLine.id == timetable_line_id).first()


def get_timetable_lines(db: Session, skip: int = 0, limit: int = 100):
    """Lister toutes les lignes d'emploi du temps"""
    return db.query(models.TimeTableLine).offset(skip).limit(limit).all()


def get_timetable_lines_by_timetable(db: Session, timetable_id: int):
    """Lister les lignes d'un emploi du temps"""
    return db.query(models.TimeTableLine).filter(models.TimeTableLine.timetable_id == timetable_id).all()


def get_timetable_lines_by_classe(db: Session, classe_id: int):
    """Lister les lignes d'emploi du temps d'une classe"""
    return db.query(models.TimeTableLine).filter(models.TimeTableLine.classe_id == classe_id).all()


def update_timetable_line(db: Session, timetable_line_id: int, timetable_line):
    """Mettre à jour une ligne d'emploi du temps"""
    db_timetable_line = get_timetable_line(db, timetable_line_id)
    if not db_timetable_line:
        return None
    update_data = timetable_line.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_timetable_line, field, value)
    db.commit()
    db.refresh(db_timetable_line)
    return db_timetable_line


def delete_timetable_line(db: Session, timetable_line_id: int):
    """Supprimer une ligne d'emploi du temps"""
    db_timetable_line = get_timetable_line(db, timetable_line_id)
    if not db_timetable_line:
        return False
    db.delete(db_timetable_line)
    db.commit()
    return True


# ==================== SEANCE CRUD ====================

def create_seance(db: Session, seance):
    """Créer une séance avec la répartition précédente de sa classe si disponible."""
    seance_data = seance.dict()
    timetable_line = get_timetable_line(db, seance_data["timetable_line_id"])
    if not timetable_line:
        raise ValueError("Timetable line not found")

    classe_id = timetable_line.classe_id
    previous_seance = (
        db.query(models.Seance)
        .join(models.TimeTableLine)
        .filter(
            models.TimeTableLine.classe_id == classe_id,
            models.Seance.date < seance_data["date"],
        )
        .order_by(models.Seance.date.desc(), models.Seance.id.desc())
        .first()
    )
    previous_groups = {}
    if previous_seance:
        previous_assignments = db.query(models.GroupStudent).filter(
            models.GroupStudent.seance_id == previous_seance.id
        ).all()
        if any(assignment.group_id is not None for assignment in previous_assignments):
            previous_groups = {
                assignment.student_id: assignment.group_id
                for assignment in previous_assignments
            }

    db_seance = models.Seance(**seance.dict())
    db.add(db_seance)
    db.flush()
    students = db.query(models.Student).filter(
        models.Student.classe_id == classe_id,
        models.Student.enabled.is_(True),
    ).all()
    db.add_all(
        models.GroupStudent(
            student_id=student.id,
            seance_id=db_seance.id,
            group_id=previous_groups.get(student.id),
        )
        for student in students
    )
    db.commit()
    db.refresh(db_seance)
    return db_seance


def get_seance(db: Session, seance_id: int):
    """Obtenir une séance par ID"""
    return db.query(models.Seance).filter(models.Seance.id == seance_id).first()


def get_seances(db: Session, skip: int = 0, limit: int = 100):
    """Lister toutes les séances"""
    return db.query(models.Seance).offset(skip).limit(limit).all()


def get_seances_by_timetable_line(db: Session, timetable_line_id: int):
    """Lister les séances d'une ligne d'emploi du temps"""
    return db.query(models.Seance).filter(models.Seance.timetable_line_id == timetable_line_id).all()


def update_seance(db: Session, seance_id: int, seance):
    """Mettre à jour une séance"""
    db_seance = get_seance(db, seance_id)
    if not db_seance:
        return None
    update_data = seance.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_seance, field, value)
    db.commit()
    db.refresh(db_seance)
    return db_seance


def delete_seance(db: Session, seance_id: int):
    """Supprimer une séance"""
    db_seance = get_seance(db, seance_id)
    if not db_seance:
        return False
    db.delete(db_seance)
    db.commit()
    return True


# ==================== ABSENCE CRUD ====================

def create_absence(db: Session, absence):
    """Créer une nouvelle absence"""
    db_absence = models.Absence(**absence.dict())
    db.add(db_absence)
    db.commit()
    db.refresh(db_absence)
    return db_absence


def get_absence(db: Session, absence_id: int):
    """Obtenir une absence par ID"""
    return db.query(models.Absence).filter(models.Absence.id == absence_id).first()


def get_absences(db: Session, skip: int = 0, limit: int = 100):
    """Lister toutes les absences"""
    return db.query(models.Absence).offset(skip).limit(limit).all()


def get_absences_by_student(db: Session, student_id: int):
    """Lister les absences d'un étudiant"""
    return db.query(models.Absence).filter(models.Absence.student_id == student_id).all()


def get_absences_by_seance(db: Session, seance_id: int):
    """Lister les absences d'une séance"""
    return db.query(models.Absence).filter(models.Absence.seance_id == seance_id).all()


def update_absence(db: Session, absence_id: int, absence):
    """Mettre à jour une absence"""
    db_absence = get_absence(db, absence_id)
    if not db_absence:
        return None
    update_data = absence.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_absence, field, value)
    db.commit()
    db.refresh(db_absence)
    return db_absence


def delete_absence(db: Session, absence_id: int):
    """Supprimer une absence"""
    db_absence = get_absence(db, absence_id)
    if not db_absence:
        return False
    db.delete(db_absence)
    db.commit()
    return True


# ==================== PARTICIPATION CRUD ====================

def create_participation(db: Session, participation):
    """Créer une nouvelle participation"""
    db_participation = models.Participation(**participation.dict())
    db.add(db_participation)
    db.commit()
    db.refresh(db_participation)
    return db_participation


def get_participation(db: Session, participation_id: int):
    """Obtenir une participation par ID"""
    return db.query(models.Participation).filter(models.Participation.id == participation_id).first()


def get_participations(db: Session, skip: int = 0, limit: int = 100):
    """Lister toutes les participations"""
    return db.query(models.Participation).offset(skip).limit(limit).all()


def get_participations_by_student(db: Session, student_id: int):
    """Lister les participations d'un étudiant"""
    return db.query(models.Participation).filter(models.Participation.student_id == student_id).all()


def get_participations_by_seance(db: Session, seance_id: int):
    """Lister les participations d'une séance"""
    return db.query(models.Participation).filter(models.Participation.seance_id == seance_id).all()


def update_participation(db: Session, participation_id: int, participation):
    """Mettre à jour une participation"""
    db_participation = get_participation(db, participation_id)
    if not db_participation:
        return None
    update_data = participation.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_participation, field, value)
    db.commit()
    db.refresh(db_participation)
    return db_participation


def delete_participation(db: Session, participation_id: int):
    """Supprimer une participation"""
    db_participation = get_participation(db, participation_id)
    if not db_participation:
        return False
    db.delete(db_participation)
    db.commit()
    return True


# ==================== GROUP CRUD ====================

def create_group(db: Session, group):
    if not db.query(models.Classe).filter(models.Classe.id == group.classe_id).first():
        return None
    db_group = models.Group(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group


def get_group(db: Session, group_id: int):
    return db.query(models.Group).filter(models.Group.id == group_id).first()


def get_groups(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    seance_id: int = None,
    student_id: int = None,
    classe_id: int = None,
    nom: str = None,
):
    query = db.query(models.Group)
    if classe_id is not None:
        query = query.filter(models.Group.classe_id == classe_id)
    if seance_id is not None:
        class_id_for_seance = (
            db.query(models.TimeTableLine.classe_id)
            .join(models.Seance, models.Seance.timetable_line_id == models.TimeTableLine.id)
            .filter(models.Seance.id == seance_id)
            .scalar_subquery()
        )
        query = query.filter(models.Group.classe_id == class_id_for_seance)
    if student_id is not None:
        if seance_id is not None:
            query = query.join(
                models.GroupStudent,
                models.GroupStudent.group_id == models.Group.id,
            ).filter(models.GroupStudent.seance_id == seance_id)
        else:
            query = query.join(models.GroupStudent)
        query = query.filter(models.GroupStudent.student_id == student_id)
    if nom:
        query = query.filter(models.Group.nom.ilike(f"%{nom}%"))
    return query.distinct().order_by(models.Group.id).offset(skip).limit(limit).all()


def get_groups_by_seance(db: Session, seance_id: int, skip: int = 0, limit: int = 100):
    return get_groups(db, skip=skip, limit=limit, seance_id=seance_id)


def update_group(db: Session, group_id: int, group):
    db_group = get_group(db, group_id)
    if not db_group:
        return None
    for field, value in group.dict(exclude_unset=True).items():
        setattr(db_group, field, value)
    db.commit()
    db.refresh(db_group)
    return db_group


def delete_group(db: Session, group_id: int):
    db_group = get_group(db, group_id)
    if not db_group:
        return False
    db.delete(db_group)
    db.commit()
    return True


def assign_student_to_group(db: Session, group_id: int, student_id: int, seance_id: int):
    db_group = get_group(db, group_id)
    if not db_group:
        return None, "Group not found"

    db_student = get_student(db, student_id)
    if not db_student:
        return None, "Student not found"
    db_seance = get_seance(db, seance_id)
    if not db_seance:
        return None, "Session not found"
    if db_student.classe_id != db_seance.timeTableLine.classe_id:
        return None, "Student does not belong to the class for this session"
    if db_student.classe_id != db_group.classe_id:
        return None, "Student does not belong to this group's class"

    existing = db.query(models.GroupStudent).filter(
        models.GroupStudent.student_id == student_id,
        models.GroupStudent.seance_id == seance_id,
    ).first()
    if existing:
        existing.group_id = group_id
        db.commit()
        db.refresh(existing)
        return existing, None

    assignment = models.GroupStudent(
        group_id=group_id,
        student_id=student_id,
        seance_id=seance_id,
    )
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment, None


def get_group_students(
    db: Session,
    group_id: int,
    skip: int = 0,
    limit: int = 100,
    student_id: int = None,
    seance_id: int = None,
):
    query = db.query(models.GroupStudent).filter(models.GroupStudent.group_id == group_id)
    if student_id is not None:
        query = query.filter(models.GroupStudent.student_id == student_id)
    if seance_id is not None:
        query = query.filter(models.GroupStudent.seance_id == seance_id)
    return query.order_by(models.GroupStudent.id).offset(skip).limit(limit).all()


def remove_student_from_group(db: Session, group_id: int, student_id: int, seance_id: int):
    assignment = db.query(models.GroupStudent).filter(
        models.GroupStudent.group_id == group_id,
        models.GroupStudent.student_id == student_id,
        models.GroupStudent.seance_id == seance_id,
    ).first()
    if not assignment:
        return False
    assignment.group_id = None
    db.commit()
    return True


# ==================== NOTE GROUPE CRUD ====================

def create_note_groupe(db: Session, note_groupe):
    assignment = db.query(models.GroupStudent).filter(
        models.GroupStudent.group_id == note_groupe.group_id,
        models.GroupStudent.seance_id == note_groupe.seance_id,
    ).first()
    if not assignment:
        return None
    db_note_groupe = models.NoteGroupe(**note_groupe.dict())
    db.add(db_note_groupe)
    db.commit()
    db.refresh(db_note_groupe)
    return db_note_groupe


def get_note_groupe(db: Session, note_groupe_id: int):
    return db.query(models.NoteGroupe).filter(models.NoteGroupe.id == note_groupe_id).first()


def get_notes_groupe(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    group_id: int = None,
    seance_id: int = None,
    note_min: float = None,
    note_max: float = None,
):
    query = db.query(models.NoteGroupe).join(models.Group)
    if group_id is not None:
        query = query.filter(models.NoteGroupe.group_id == group_id)
    if seance_id is not None:
        query = query.filter(models.NoteGroupe.seance_id == seance_id)
    if note_min is not None:
        query = query.filter(models.NoteGroupe.note >= note_min)
    if note_max is not None:
        query = query.filter(models.NoteGroupe.note <= note_max)
    return query.order_by(models.NoteGroupe.id).offset(skip).limit(limit).all()


def get_note_groupe_by_group(db: Session, group_id: int, seance_id: int):
    return db.query(models.NoteGroupe).filter(
        models.NoteGroupe.group_id == group_id,
        models.NoteGroupe.seance_id == seance_id,
    ).first()


def update_note_groupe(db: Session, note_groupe_id: int, note_groupe):
    db_note_groupe = get_note_groupe(db, note_groupe_id)
    if not db_note_groupe:
        return None
    for field, value in note_groupe.dict(exclude_unset=True).items():
        setattr(db_note_groupe, field, value)
    db.commit()
    db.refresh(db_note_groupe)
    return db_note_groupe


def delete_note_groupe(db: Session, note_groupe_id: int):
    db_note_groupe = get_note_groupe(db, note_groupe_id)
    if not db_note_groupe:
        return False
    db.delete(db_note_groupe)
    db.commit()
    return True


# ==================== SEQUENCE CRUD ====================

def create_sequence(db: Session, sequence):
    db_sequence = models.Sequence(**sequence.dict())
    db.add(db_sequence)
    db.commit()
    db.refresh(db_sequence)
    return db_sequence


def get_sequence(db: Session, sequence_id: int):
    return db.query(models.Sequence).filter(models.Sequence.id == sequence_id).first()


def get_sequences(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    seance_id: int = None,
    chapitre_id: int = None,
    type: str = None,
    contenu: str = None,
):
    query = db.query(models.Sequence)
    if seance_id is not None:
        query = query.filter(models.Sequence.seance_id == seance_id)
    if chapitre_id is not None:
        query = query.filter(models.Sequence.chapitre_id == chapitre_id)
    if type is not None:
        query = query.filter(models.Sequence.type == type)
    if contenu:
        query = query.filter(models.Sequence.contenu.ilike(f"%{contenu}%"))
    return query.order_by(models.Sequence.id).offset(skip).limit(limit).all()


def get_sequences_by_seance(db: Session, seance_id: int, skip: int = 0, limit: int = 100):
    return get_sequences(db, skip=skip, limit=limit, seance_id=seance_id)


def update_sequence(db: Session, sequence_id: int, sequence):
    db_sequence = get_sequence(db, sequence_id)
    if not db_sequence:
        return None
    for field, value in sequence.dict(exclude_unset=True).items():
        setattr(db_sequence, field, value)
    db.commit()
    db.refresh(db_sequence)
    return db_sequence


def delete_sequence(db: Session, sequence_id: int):
    db_sequence = get_sequence(db, sequence_id)
    if not db_sequence:
        return False
    db.delete(db_sequence)
    db.commit()
    return True
