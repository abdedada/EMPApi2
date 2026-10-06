@echo off
REM Script pour lancer l'API EMC

cls
echo ════════════════════════════════════════════════════════════════
echo.
echo  ✅ Easy Manager Classe (EMC) v2.0.0
echo.
echo ════════════════════════════════════════════════════════════════
echo.

REM Activer l'environnement virtuel
call .venv\Scripts\activate.bat

REM Lancer l'API FastAPI
echo 🚀 Lancement de l'API FastAPI sur http://localhost:8000...
echo.
echo 📖 Documentation API: http://localhost:8000/docs
echo Appuyez sur Ctrl+C pour arrêter le serveur.
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
