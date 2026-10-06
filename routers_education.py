# Fichier router pour les endpoints éducatifs
# À importer dans main.py

from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
import schemas
from auth import get_current_user

router = APIRouter(prefix="/api/education", tags=["Education"])


def get_db():
    """Dépendance pour obtenir la session DB"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== SCHOOL YEAR ENDPOINTS ====================

@router.post("/school-years/", response_model=schemas.SchoolYear)
def create_school_year(
    school_year: schemas.SchoolYearCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer une nouvelle année scolaire"""
    return crud.create_school_year(db, school_year)


@router.get("/school-years/", response_model=list[schemas.SchoolYear])
def list_school_years(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister toutes les années scolaires"""
    return crud.get_school_years(db, skip=skip, limit=limit)


@router.get("/school-years/{school_year_id}", response_model=schemas.SchoolYear)
def get_school_year_detail(
    school_year_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir une année scolaire par ID"""
    db_school_year = crud.get_school_year(db, school_year_id)
    if not db_school_year:
        raise HTTPException(status_code=404, detail="SchoolYear not found")
    return db_school_year


@router.put("/school-years/{school_year_id}", response_model=schemas.SchoolYear)
def update_school_year_detail(
    school_year_id: int,
    school_year: schemas.SchoolYearUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour une année scolaire"""
    db_school_year = crud.update_school_year(db, school_year_id, school_year)
    if not db_school_year:
        raise HTTPException(status_code=404, detail="SchoolYear not found")
    return db_school_year


@router.delete("/school-years/{school_year_id}")
def delete_school_year_detail(
    school_year_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer une année scolaire"""
    success = crud.delete_school_year(db, school_year_id)
    if not success:
        raise HTTPException(status_code=404, detail="SchoolYear not found")
    return {"message": "SchoolYear deleted successfully"}


# ==================== CLASSE ENDPOINTS ====================

@router.post("/classes/", response_model=schemas.Classe)
def create_classe(
    classe: schemas.ClasseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer une nouvelle classe"""
    return crud.create_classe(db, classe)


@router.get("/classes/", response_model=list[schemas.Classe])
def list_classes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister toutes les classes"""
    return crud.get_classes(db, skip=skip, limit=limit)


@router.get("/classes/school-year/{school_year_id}", response_model=list[schemas.Classe])
def list_classes_by_school_year(
    school_year_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les classes d'une année scolaire"""
    return crud.get_classes_by_school_year(db, school_year_id)


@router.get("/classes/{classe_id}", response_model=schemas.Classe)
def get_classe_detail(
    classe_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir une classe par ID"""
    db_classe = crud.get_classe(db, classe_id)
    if not db_classe:
        raise HTTPException(status_code=404, detail="Classe not found")
    return db_classe


@router.put("/classes/{classe_id}", response_model=schemas.Classe)
def update_classe_detail(
    classe_id: int,
    classe: schemas.ClasseUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour une classe"""
    db_classe = crud.update_classe(db, classe_id, classe)
    if not db_classe:
        raise HTTPException(status_code=404, detail="Classe not found")
    return db_classe


@router.delete("/classes/{classe_id}")
def delete_classe_detail(
    classe_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer une classe"""
    success = crud.delete_classe(db, classe_id)
    if not success:
        raise HTTPException(status_code=404, detail="Classe not found")
    return {"message": "Classe deleted successfully"}


# ==================== MODULE ENDPOINTS ====================

@router.post("/modules/", response_model=schemas.Module)
def create_module(
    module: schemas.ModuleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer un nouveau module"""
    return crud.create_module(db, module)


@router.get("/modules/", response_model=list[schemas.Module])
def list_modules(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister tous les modules"""
    return crud.get_modules(db, skip=skip, limit=limit)


@router.get("/modules/{module_id}", response_model=schemas.Module)
def get_module_detail(
    module_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir un module par ID"""
    db_module = crud.get_module(db, module_id)
    if not db_module:
        raise HTTPException(status_code=404, detail="Module not found")
    return db_module


@router.put("/modules/{module_id}", response_model=schemas.Module)
def update_module_detail(
    module_id: int,
    module: schemas.ModuleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour un module"""
    db_module = crud.update_module(db, module_id, module)
    if not db_module:
        raise HTTPException(status_code=404, detail="Module not found")
    return db_module


@router.delete("/modules/{module_id}")
def delete_module_detail(
    module_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer un module"""
    success = crud.delete_module(db, module_id)
    if not success:
        raise HTTPException(status_code=404, detail="Module not found")
    return {"message": "Module deleted successfully"}


# ==================== CHAPITRE ENDPOINTS ====================

@router.post("/chapitres/", response_model=schemas.Chapitre)
def create_chapitre(
    chapitre: schemas.ChapitreCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer un nouveau chapitre"""
    return crud.create_chapitre(db, chapitre)


@router.get("/chapitres/", response_model=list[schemas.Chapitre])
def list_chapitres(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister tous les chapitres"""
    return crud.get_chapitres(db, skip=skip, limit=limit)


@router.get("/chapitres/module/{module_id}", response_model=list[schemas.Chapitre])
def list_chapitres_by_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les chapitres d'un module"""
    return crud.get_chapitres_by_module(db, module_id)


@router.get("/chapitres/{chapitre_id}", response_model=schemas.Chapitre)
def get_chapitre_detail(
    chapitre_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir un chapitre par ID"""
    db_chapitre = crud.get_chapitre(db, chapitre_id)
    if not db_chapitre:
        raise HTTPException(status_code=404, detail="Chapitre not found")
    return db_chapitre


@router.put("/chapitres/{chapitre_id}", response_model=schemas.Chapitre)
def update_chapitre_detail(
    chapitre_id: int,
    chapitre: schemas.ChapitreUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour un chapitre"""
    db_chapitre = crud.update_chapitre(db, chapitre_id, chapitre)
    if not db_chapitre:
        raise HTTPException(status_code=404, detail="Chapitre not found")
    return db_chapitre


@router.delete("/chapitres/{chapitre_id}")
def delete_chapitre_detail(
    chapitre_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer un chapitre"""
    success = crud.delete_chapitre(db, chapitre_id)
    if not success:
        raise HTTPException(status_code=404, detail="Chapitre not found")
    return {"message": "Chapitre deleted successfully"}


# ==================== QUESTION ENDPOINTS ====================

@router.post("/questions/", response_model=schemas.Question)
def create_question(
    question: schemas.QuestionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer une nouvelle question"""
    return crud.create_question(db, question)


@router.get("/questions/", response_model=list[schemas.Question])
def list_questions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister toutes les questions"""
    return crud.get_questions(db, skip=skip, limit=limit)


@router.get("/questions/chapitre/{chapitre_id}", response_model=list[schemas.Question])
def list_questions_by_chapitre(
    chapitre_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les questions d'un chapitre"""
    return crud.get_questions_by_chapitre(db, chapitre_id)


@router.get("/questions/evaluation/{evaluation_id}", response_model=list[schemas.Question])
def get_questions_by_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Récupérer les questions d'une évaluation"""
    return crud.get_questions_by_evaluation(db, evaluation_id)


@router.get("/questions/module/{module_id}", response_model=list[schemas.Question])
def get_questions_by_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Récupérer toutes les questions d'un module"""
    return crud.get_questions_by_module(db, module_id)


@router.post("/questions/evaluation/{evaluation_id}")
def set_evaluation_questions(
    evaluation_id: int,
    evaluation_questions: schemas.EvaluationQuestionsSet,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Définir les questions d'une évaluation"""
    evaluation = crud.set_evaluation_questions(db, evaluation_id, evaluation_questions.question_ids)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return {"message": "Questions set successfully for evaluation", "evaluation_id": evaluation_id}


@router.get("/questions/{question_id}", response_model=schemas.Question)
def get_question_detail(
    question_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir une question par ID"""
    db_question = crud.get_question(db, question_id)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@router.put("/questions/{question_id}", response_model=schemas.Question)
def update_question_detail(
    question_id: int,
    question: schemas.QuestionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour une question"""
    db_question = crud.update_question(db, question_id, question)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@router.delete("/questions/{question_id}")
def delete_question_detail(
    question_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer une question"""
    success = crud.delete_question(db, question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}


# ==================== EVALUATION ENDPOINTS ====================

@router.post("/evaluations/", response_model=schemas.Evaluation)
def create_evaluation(
    evaluation: schemas.EvaluationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer une nouvelle évaluation"""
    return crud.create_evaluation(db, evaluation)


@router.get("/evaluations/", response_model=list[schemas.Evaluation])
def list_evaluations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister toutes les évaluations"""
    return crud.get_evaluations(db, skip=skip, limit=limit)


@router.get("/evaluations/classe/{classe_id}", response_model=list[schemas.Evaluation])
def list_evaluations_by_classe(
    classe_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les évaluations d'une classe"""
    return crud.get_evaluations_by_classe(db, classe_id)


@router.get("/evaluations/module/{module_id}", response_model=list[schemas.Evaluation])
def list_evaluations_by_module(
    module_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les évaluations d'un module"""
    return crud.get_evaluations_by_module(db, module_id)


@router.get("/evaluations/{evaluation_id}", response_model=schemas.Evaluation)
def get_evaluation_detail(
    evaluation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir une évaluation par ID"""
    db_evaluation = crud.get_evaluation(db, evaluation_id)
    if not db_evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return db_evaluation


@router.put("/evaluations/{evaluation_id}", response_model=schemas.Evaluation)
def update_evaluation_detail(
    evaluation_id: int,
    evaluation: schemas.EvaluationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour une évaluation"""
    db_evaluation = crud.update_evaluation(db, evaluation_id, evaluation)
    if not db_evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return db_evaluation


@router.delete("/evaluations/{evaluation_id}")
def delete_evaluation_detail(
    evaluation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer une évaluation"""
    success = crud.delete_evaluation(db, evaluation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return {"message": "Evaluation deleted successfully"}


# ==================== STUDENT ENDPOINTS ====================

@router.post("/students/", response_model=schemas.Student)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer un nouvel étudiant"""
    return crud.create_student(db, student)


@router.get("/students/", response_model=list[schemas.Student])
def list_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister tous les étudiants"""
    return crud.get_students(db, skip=skip, limit=limit)


@router.get("/students/classe/{classe_id}", response_model=list[schemas.Student])
def list_students_by_classe(
    classe_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les étudiants d'une classe"""
    return crud.get_students_by_classe(db, classe_id)


@router.get("/students/{student_id}", response_model=schemas.Student)
def get_student_detail(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir un étudiant par ID"""
    db_student = crud.get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@router.put("/students/{student_id}", response_model=schemas.Student)
def update_student_detail(
    student_id: int,
    student: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour un étudiant"""
    db_student = crud.update_student(db, student_id, student)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@router.delete("/students/{student_id}")
def delete_student_detail(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer un étudiant"""
    success = crud.delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}


# ==================== REPONSE ENDPOINTS ====================

@router.post("/reponses/", response_model=schemas.Reponse)
def create_reponse(
    reponse: schemas.ReponseCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer une nouvelle réponse"""
    return crud.create_reponse(db, reponse)


@router.get("/reponses/", response_model=list[schemas.Reponse])
def list_reponses(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister toutes les réponses"""
    return crud.get_reponses(db, skip=skip, limit=limit)


@router.get("/reponses/evaluation/{evaluation_id}", response_model=list[schemas.Reponse])
def list_reponses_by_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les réponses d'une évaluation"""
    return crud.get_reponses_by_evaluation(db, evaluation_id)


@router.get("/reponses/student/{student_id}", response_model=list[schemas.Reponse])
def list_reponses_by_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les réponses d'un étudiant"""
    return crud.get_reponses_by_student(db, student_id)


@router.get("/reponses/{reponse_id}", response_model=schemas.Reponse)
def get_reponse_detail(
    reponse_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir une réponse par ID"""
    db_reponse = crud.get_reponse(db, reponse_id)
    if not db_reponse:
        raise HTTPException(status_code=404, detail="Reponse not found")
    return db_reponse


@router.put("/reponses/{reponse_id}", response_model=schemas.Reponse)
def update_reponse_detail(
    reponse_id: int,
    reponse: schemas.ReponseUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour une réponse"""
    db_reponse = crud.update_reponse(db, reponse_id, reponse)
    if not db_reponse:
        raise HTTPException(status_code=404, detail="Reponse not found")
    return db_reponse


@router.delete("/reponses/{reponse_id}")
def delete_reponse_detail(
    reponse_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer une réponse"""
    success = crud.delete_reponse(db, reponse_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reponse not found")
    return {"message": "Reponse deleted successfully"}


# ==================== TIMETABLE ENDPOINTS ====================

@router.post("/timetables/", response_model=schemas.Timetable)
def create_timetable(
    timetable: schemas.TimetableCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer un nouvel emploi du temps"""
    return crud.create_timetable(db, timetable)


@router.get("/timetables/", response_model=list[schemas.Timetable])
def list_timetables(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister tous les emplois du temps"""
    return crud.get_timetables(db, skip=skip, limit=limit)


@router.get("/timetables/classe/{classe_id}", response_model=list[schemas.Timetable])
def list_timetables_by_classe(
    classe_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les emplois du temps d'une classe"""
    return crud.get_timetables_by_classe(db, classe_id)


@router.get("/timetables/school-year/{school_year_id}", response_model=list[schemas.Timetable])
def list_timetables_by_school_year(
    school_year_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les emplois du temps d'une année scolaire"""
    return crud.get_timetables_by_school_year(db, school_year_id)


@router.get("/timetables/{timetable_id}", response_model=schemas.Timetable)
def get_timetable_detail(
    timetable_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir un emploi du temps par ID"""
    db_timetable = crud.get_timetable(db, timetable_id)
    if not db_timetable:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return db_timetable


@router.put("/timetables/{timetable_id}", response_model=schemas.Timetable)
def update_timetable_detail(
    timetable_id: int,
    timetable: schemas.TimetableUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour un emploi du temps"""
    db_timetable = crud.update_timetable(db, timetable_id, timetable)
    if not db_timetable:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return db_timetable


@router.delete("/timetables/{timetable_id}")
def delete_timetable_detail(
    timetable_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer un emploi du temps"""
    success = crud.delete_timetable(db, timetable_id)
    if not success:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return {"message": "Timetable deleted successfully"}


# ==================== TIMETABLE LINE ENDPOINTS ====================

@router.post("/timetable-lines/", response_model=schemas.TimeTableLine)
def create_timetable_line(
    timetable_line: schemas.TimeTableLineCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer une nouvelle ligne d'emploi du temps"""
    return crud.create_timetable_line(db, timetable_line)


@router.get("/timetable-lines/", response_model=list[schemas.TimeTableLine])
def list_timetable_lines(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister toutes les lignes d'emploi du temps"""
    return crud.get_timetable_lines(db, skip=skip, limit=limit)


@router.get("/timetable-lines/timetable/{timetable_id}", response_model=list[schemas.TimeTableLine])
def list_timetable_lines_by_timetable(
    timetable_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les lignes d'un emploi du temps"""
    return crud.get_timetable_lines_by_timetable(db, timetable_id)


@router.get("/timetable-lines/classe/{classe_id}", response_model=list[schemas.TimeTableLine])
def list_timetable_lines_by_classe(
    classe_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les lignes d'emploi du temps d'une classe"""
    return crud.get_timetable_lines_by_classe(db, classe_id)


@router.get("/timetable-lines/{timetable_line_id}", response_model=schemas.TimeTableLine)
def get_timetable_line_detail(
    timetable_line_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir une ligne d'emploi du temps par ID"""
    db_timetable_line = crud.get_timetable_line(db, timetable_line_id)
    if not db_timetable_line:
        raise HTTPException(status_code=404, detail="TimeTableLine not found")
    return db_timetable_line


@router.put("/timetable-lines/{timetable_line_id}", response_model=schemas.TimeTableLine)
def update_timetable_line_detail(
    timetable_line_id: int,
    timetable_line: schemas.TimeTableLineUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour une ligne d'emploi du temps"""
    db_timetable_line = crud.update_timetable_line(db, timetable_line_id, timetable_line)
    if not db_timetable_line:
        raise HTTPException(status_code=404, detail="TimeTableLine not found")
    return db_timetable_line


@router.delete("/timetable-lines/{timetable_line_id}")
def delete_timetable_line_detail(
    timetable_line_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer une ligne d'emploi du temps"""
    success = crud.delete_timetable_line(db, timetable_line_id)
    if not success:
        raise HTTPException(status_code=404, detail="TimeTableLine not found")
    return {"message": "TimeTableLine deleted successfully"}


# ==================== SEANCE ENDPOINTS ====================

@router.post("/seances/", response_model=schemas.Seance)
def create_seance(
    seance: schemas.SeanceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer une nouvelle séance"""
    if not crud.get_timetable_line(db, seance.timetable_line_id):
        raise HTTPException(status_code=404, detail="TimeTableLine not found")
    return crud.create_seance(db, seance)


@router.get("/seances/", response_model=list[schemas.Seance])
def list_seances(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister toutes les séances"""
    return crud.get_seances(db, skip=skip, limit=limit)


@router.get("/seances/timetable-line/{timetable_line_id}", response_model=list[schemas.Seance])
def list_seances_by_timetable_line(
    timetable_line_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les séances d'une ligne d'emploi du temps"""
    return crud.get_seances_by_timetable_line(db, timetable_line_id)


@router.get("/seances/{seance_id}", response_model=schemas.Seance)
def get_seance_detail(
    seance_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir une séance par ID"""
    db_seance = crud.get_seance(db, seance_id)
    if not db_seance:
        raise HTTPException(status_code=404, detail="Seance not found")
    return db_seance


@router.put("/seances/{seance_id}", response_model=schemas.Seance)
def update_seance_detail(
    seance_id: int,
    seance: schemas.SeanceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour une séance"""
    db_seance = crud.update_seance(db, seance_id, seance)
    if not db_seance:
        raise HTTPException(status_code=404, detail="Seance not found")
    return db_seance


@router.delete("/seances/{seance_id}")
def delete_seance_detail(
    seance_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer une séance"""
    success = crud.delete_seance(db, seance_id)
    if not success:
        raise HTTPException(status_code=404, detail="Seance not found")
    return {"message": "Seance deleted successfully"}


# ==================== ABSENCE ENDPOINTS ====================

@router.post("/absences/", response_model=schemas.Absence)
def create_absence(
    absence: schemas.AbsenceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer une nouvelle absence"""
    return crud.create_absence(db, absence)


@router.get("/absences/", response_model=list[schemas.Absence])
def list_absences(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister toutes les absences"""
    return crud.get_absences(db, skip=skip, limit=limit)


@router.get("/absences/student/{student_id}", response_model=list[schemas.Absence])
def list_absences_by_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les absences d'un étudiant"""
    return crud.get_absences_by_student(db, student_id)


@router.get("/absences/seance/{seance_id}", response_model=list[schemas.Absence])
def list_absences_by_seance(
    seance_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les absences d'une séance"""
    return crud.get_absences_by_seance(db, seance_id)


@router.get("/absences/{absence_id}", response_model=schemas.Absence)
def get_absence_detail(
    absence_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir une absence par ID"""
    db_absence = crud.get_absence(db, absence_id)
    if not db_absence:
        raise HTTPException(status_code=404, detail="Absence not found")
    return db_absence


@router.put("/absences/{absence_id}", response_model=schemas.Absence)
def update_absence_detail(
    absence_id: int,
    absence: schemas.AbsenceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour une absence"""
    db_absence = crud.update_absence(db, absence_id, absence)
    if not db_absence:
        raise HTTPException(status_code=404, detail="Absence not found")
    return db_absence


@router.delete("/absences/{absence_id}")
def delete_absence_detail(
    absence_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer une absence"""
    success = crud.delete_absence(db, absence_id)
    if not success:
        raise HTTPException(status_code=404, detail="Absence not found")
    return {"message": "Absence deleted successfully"}


# ==================== PARTICIPATION ENDPOINTS ====================

@router.post("/participations/", response_model=schemas.Participation)
def create_participation(
    participation: schemas.ParticipationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer une nouvelle participation"""
    return crud.create_participation(db, participation)


@router.get("/participations/", response_model=list[schemas.Participation])
def list_participations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister toutes les participations"""
    return crud.get_participations(db, skip=skip, limit=limit)


@router.get("/participations/student/{student_id}", response_model=list[schemas.Participation])
def list_participations_by_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les participations d'un étudiant"""
    return crud.get_participations_by_student(db, student_id)


@router.get("/participations/seance/{seance_id}", response_model=list[schemas.Participation])
def list_participations_by_seance(
    seance_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Lister les participations d'une séance"""
    return crud.get_participations_by_seance(db, seance_id)


@router.get("/participations/{participation_id}", response_model=schemas.Participation)
def get_participation_detail(
    participation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir une participation par ID"""
    db_participation = crud.get_participation(db, participation_id)
    if not db_participation:
        raise HTTPException(status_code=404, detail="Participation not found")
    return db_participation


@router.put("/participations/{participation_id}", response_model=schemas.Participation)
def update_participation_detail(
    participation_id: int,
    participation: schemas.ParticipationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour une participation"""
    db_participation = crud.update_participation(db, participation_id, participation)
    if not db_participation:
        raise HTTPException(status_code=404, detail="Participation not found")
    return db_participation


@router.delete("/participations/{participation_id}")
def delete_participation_detail(
    participation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Supprimer une participation"""
    success = crud.delete_participation(db, participation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Participation not found")
    return {"message": "Participation deleted successfully"}


# ==================== GROUP ENDPOINTS ====================

@router.post("/groups/", response_model=schemas.Group)
def create_group(
    group: schemas.GroupCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_group = crud.create_group(db, group)
    if not db_group:
        raise HTTPException(status_code=404, detail="Class not found")
    return db_group


@router.get("/groups/", response_model=list[schemas.Group])
def list_groups(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    seance_id: int = Query(default=None, gt=0),
    student_id: int = Query(default=None, gt=0),
    classe_id: int = Query(default=None, gt=0),
    nom: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_groups(
        db,
        skip=skip,
        limit=limit,
        seance_id=seance_id,
        student_id=student_id,
        classe_id=classe_id,
        nom=nom,
    )


@router.get("/groups/seance/{seance_id}", response_model=list[schemas.Group])
def list_groups_by_seance(
    seance_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    groups = crud.get_groups_by_seance(db, seance_id, skip=skip, limit=limit)
    return groups


@router.get("/groups/{group_id}", response_model=schemas.Group)
def get_group_detail(
    group_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_group = crud.get_group(db, group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group


@router.put("/groups/{group_id}", response_model=schemas.Group)
def update_group_detail(
    group_id: int,
    group: schemas.GroupUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_group = crud.update_group(db, group_id, group)
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group


@router.delete("/groups/{group_id}")
def delete_group_detail(
    group_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not crud.delete_group(db, group_id):
        raise HTTPException(status_code=404, detail="Group not found")
    return {"message": "Group deleted successfully"}


@router.post("/groups/{group_id}/students/{student_id}/seances/{seance_id}", response_model=schemas.GroupStudent)
def assign_student_to_group(
    group_id: int,
    student_id: int,
    seance_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    assignment, error = crud.assign_student_to_group(db, group_id, student_id, seance_id)
    if error in ("Group not found", "Student not found", "Session not found"):
        raise HTTPException(status_code=404, detail=error)
    if error:
        raise HTTPException(status_code=409, detail=error)
    return assignment


@router.get("/groups/{group_id}/students", response_model=list[schemas.GroupStudent])
def list_group_students(
    group_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    student_id: int = Query(default=None, gt=0),
    seance_id: int = Query(default=None, gt=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not crud.get_group(db, group_id):
        raise HTTPException(status_code=404, detail="Group not found")
    return crud.get_group_students(
        db,
        group_id,
        skip=skip,
        limit=limit,
        student_id=student_id,
        seance_id=seance_id,
    )


@router.delete("/groups/{group_id}/students/{student_id}/seances/{seance_id}")
def remove_student_from_group(
    group_id: int,
    student_id: int,
    seance_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not crud.remove_student_from_group(db, group_id, student_id, seance_id):
        raise HTTPException(status_code=404, detail="Group assignment not found")
    return {"message": "Student removed from group"}


# ==================== NOTE GROUPE ENDPOINTS ====================

@router.post("/notes-groupes/", response_model=schemas.NoteGroupe)
def create_note_groupe(
    note_groupe: schemas.NoteGroupeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not crud.get_group(db, note_groupe.group_id):
        raise HTTPException(status_code=404, detail="Group not found")
    if not crud.get_seance(db, note_groupe.seance_id):
        raise HTTPException(status_code=404, detail="Session not found")
    if crud.get_note_groupe_by_group(db, note_groupe.group_id, note_groupe.seance_id):
        raise HTTPException(status_code=409, detail="This group already has a grade for this session")
    db_note = crud.create_note_groupe(db, note_groupe)
    if not db_note:
        raise HTTPException(status_code=409, detail="Group has no members assigned for this session")
    return db_note


@router.get("/notes-groupes/", response_model=list[schemas.NoteGroupe])
def list_notes_groupe(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    group_id: int = Query(default=None, gt=0),
    seance_id: int = Query(default=None, gt=0),
    note_min: float = None,
    note_max: float = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if note_min is not None and note_max is not None and note_min > note_max:
        raise HTTPException(status_code=422, detail="note_min must be less than or equal to note_max")
    return crud.get_notes_groupe(
        db,
        skip=skip,
        limit=limit,
        group_id=group_id,
        seance_id=seance_id,
        note_min=note_min,
        note_max=note_max,
    )


@router.get("/notes-groupes/group/{group_id}", response_model=schemas.NoteGroupe)
def get_note_groupe_for_group(
    group_id: int,
    seance_id: int = Query(gt=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_note = crud.get_note_groupe_by_group(db, group_id, seance_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Group note not found")
    return db_note


@router.get("/notes-groupes/{note_groupe_id}", response_model=schemas.NoteGroupe)
def get_note_groupe_detail(
    note_groupe_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_note = crud.get_note_groupe(db, note_groupe_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Group note not found")
    return db_note


@router.put("/notes-groupes/{note_groupe_id}", response_model=schemas.NoteGroupe)
def update_note_groupe_detail(
    note_groupe_id: int,
    note_groupe: schemas.NoteGroupeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_note = crud.update_note_groupe(db, note_groupe_id, note_groupe)
    if not db_note:
        raise HTTPException(status_code=404, detail="Group note not found")
    return db_note


@router.delete("/notes-groupes/{note_groupe_id}")
def delete_note_groupe_detail(
    note_groupe_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not crud.delete_note_groupe(db, note_groupe_id):
        raise HTTPException(status_code=404, detail="Group note not found")
    return {"message": "Group note deleted successfully"}


# ==================== SEQUENCE ENDPOINTS ====================

@router.post("/sequences/", response_model=schemas.Sequence)
def create_sequence(
    sequence: schemas.SequenceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.create_sequence(db, sequence)


@router.get("/sequences/", response_model=list[schemas.Sequence])
def list_sequences(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    seance_id: int = Query(default=None, gt=0),
    chapitre_id: int = Query(default=None, gt=0),
    type: Literal["cours", "exercice", "tp", "evaluation", "autre"] = None,
    contenu: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_sequences(
        db,
        skip=skip,
        limit=limit,
        seance_id=seance_id,
        chapitre_id=chapitre_id,
        type=type,
        contenu=contenu,
    )


@router.get("/sequences/seance/{seance_id}", response_model=list[schemas.Sequence])
def list_sequences_by_seance(
    seance_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_sequences_by_seance(db, seance_id, skip=skip, limit=limit)


@router.get("/sequences/{sequence_id}", response_model=schemas.Sequence)
def get_sequence_detail(
    sequence_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_sequence = crud.get_sequence(db, sequence_id)
    if not db_sequence:
        raise HTTPException(status_code=404, detail="Sequence not found")
    return db_sequence


@router.put("/sequences/{sequence_id}", response_model=schemas.Sequence)
def update_sequence_detail(
    sequence_id: int,
    sequence: schemas.SequenceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_sequence = crud.update_sequence(db, sequence_id, sequence)
    if not db_sequence:
        raise HTTPException(status_code=404, detail="Sequence not found")
    return db_sequence


@router.delete("/sequences/{sequence_id}")
def delete_sequence_detail(
    sequence_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if not crud.delete_sequence(db, sequence_id):
        raise HTTPException(status_code=404, detail="Sequence not found")
    return {"message": "Sequence deleted successfully"}
