#!/usr/bin/env bash
# Google Cloud Run Deployment Script (Bash)
# All Things Agentic Hackathon

PROJECT_ID="automentor-hackathon"
REGION="us-central1"
SERVICE_NAME="automentor-api"

echo "🚀 Iniciando deploy do AutoMentor AI no Google Cloud Run..."

gcloud config set project $PROJECT_ID

gcloud run deploy $SERVICE_NAME \
    --source . \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --set-env-vars "DEMO_MODE=true"

echo "✓ Deploy concluído com sucesso no Cloud Run!"
