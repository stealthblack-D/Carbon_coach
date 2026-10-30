#!/usr/bin/env bash
# deploy_cloud_run.sh - One-command deployment of Carbon Coach to Google Cloud Run
set -e

SERVICE_NAME="carbon-coach"
REGION="asia-south1" # Mumbai, India (low latency for Indian campuses)

echo "🚀 Deploying ${SERVICE_NAME} to Google Cloud Run in ${REGION}..."

# Ensure Google Cloud project is set
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: No GCP Project configured. Run 'gcloud config set project <PROJECT_ID>'"
    exit 1
fi

echo "📦 Project ID: ${PROJECT_ID}"

# Deploy directly from source to Cloud Run
gcloud run deploy "${SERVICE_NAME}" \
    --source . \
    --platform managed \
    --region "${REGION}" \
    --allow-unauthenticated \
    --port 8080 \
    --set-env-vars="GEMINI_MODEL=gemini-2.5-flash" \
    --min-instances 0 \
    --max-instances 10

echo "✅ Deployment successful! Service URL:"
gcloud run services describe "${SERVICE_NAME}" --platform managed --region "${REGION}" --format="value(status.url)"
