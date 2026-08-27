# Google Cloud Run Deployment Script (PowerShell)
# All Things Agentic Hackathon

$PROJECT_ID = "automentor-hackathon"
$REGION = "us-central1"
$SERVICE_NAME = "automentor-api"

Write-Host "🚀 Iniciando deploy do AutoMentor AI no Google Cloud Run..." -ForegroundColor Cyan

# 1. Configurar Projeto GCP
gcloud config set project $PROJECT_ID

# 2. Build e Deploy direto no Cloud Run
gcloud run deploy $SERVICE_NAME `
    --source . `
    --region $REGION `
    --platform managed `
    --allow-unauthenticated `
    --set-env-vars "DEMO_MODE=true"

Write-Host "✓ Deploy concluído com sucesso no Cloud Run!" -ForegroundColor Green
