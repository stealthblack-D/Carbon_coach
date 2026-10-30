@echo off
REM deploy_cloud_run.bat - Deploy Carbon Coach to Google Cloud Run from Windows

set SERVICE_NAME=carbon-coach
set REGION=asia-south1

echo =======================================================
echo  Deploying %SERVICE_NAME% to Google Cloud Run (%REGION%)
echo =======================================================

call gcloud run deploy %SERVICE_NAME% ^
    --source . ^
    --platform managed ^
    --region %REGION% ^
    --allow-unauthenticated ^
    --port 8080 ^
    --set-env-vars="GEMINI_MODEL=gemini-2.5-flash" ^
    --min-instances 0 ^
    --max-instances 10

if %ERRORLEVEL% EQU 0 (
    echo.
    echo =======================================================
    echo  Deployment completed successfully!
    echo =======================================================
    call gcloud run services describe %SERVICE_NAME% --platform managed --region %REGION% --format="value(status.url)"
) else (
    echo.
    echo [ERROR] Cloud Run deployment encountered an error.
)
