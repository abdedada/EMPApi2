@echo off
REM Script de démarrage rapide pour EMP API v2.0
REM Lance le serveur FastAPI

title EMP API v2.0 - FastAPI Server
color 0A

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║          EMP API v2.0 - FastAPI Server               ║
echo ║         Démarrage du serveur...                       ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Se placer dans le répertoire du projet
cd /d "%~dp0"

REM Vérifier que requirements.txt existe
if not exist "requirements.txt" (
    echo [ERREUR] Fichier requirements.txt non trouvé!
    echo Assurez-vous d'être dans le répertoire correct du projet.
    pause
    exit /b 1
)

REM Afficher les informations
echo ℹ️  Répertoire: %cd%
echo ℹ️  Python:
python --version
echo ℹ️  Uvicorn:
uvicorn --version
echo.

REM Démarrer le serveur
echo 🚀 Démarrage du serveur sur http://localhost:8000
echo.
echo Appuyez sur Ctrl+C pour arrêter le serveur
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause

