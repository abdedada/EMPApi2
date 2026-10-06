#!/usr/bin/env powershell
# Script de démarrage pour EMP API v2.0
# Lance le serveur FastAPI avec uvicorn

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║          EMP API v2.0 - FastAPI Server               ║" -ForegroundColor Cyan
Write-Host "║         Démarrage du serveur...                       ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Se placer dans le répertoire du script
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

# Vérifier requirements.txt
if (-not (Test-Path "requirements.txt")) {
    Write-Host "[ERREUR] Fichier requirements.txt non trouvé!" -ForegroundColor Red
    Write-Host "Assurez-vous d'être dans le répertoire correct du projet." -ForegroundColor Red
    Write-Host ""
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

# Afficher les informations
Write-Host "ℹ️  Répertoire: $(Get-Location)" -ForegroundColor Yellow
Write-Host "ℹ️  Python:" -ForegroundColor Yellow
python --version
Write-Host "ℹ️  Uvicorn:" -ForegroundColor Yellow
uvicorn --version
Write-Host ""

# Vérifier si le port est déjà utilisé
$portInUse = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Where-Object { $_.State -eq "Listen" }
if ($portInUse) {
    Write-Host "[ATTENTION] Le port 8000 est déjà utilisé!" -ForegroundColor Yellow
    Write-Host "Un autre processus l'utilise peut-être." -ForegroundColor Yellow
    Write-Host ""
    $response = Read-Host "Voulez-vous continuer quand même? (o/n)"
    if ($response -ne "o") {
        exit 1
    }
}

# Démarrer le serveur
Write-Host "🚀 Démarrage du serveur sur http://localhost:8000" -ForegroundColor Green
Write-Host "📖 Documentation Swagger: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "🧪 Tester l'API: python test_quick.py" -ForegroundColor Green
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Yellow
Write-Host ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000

Write-Host ""
Write-Host "Serveur arrêté." -ForegroundColor Cyan
Read-Host "Appuyez sur Entrée pour fermer cette fenêtre"

