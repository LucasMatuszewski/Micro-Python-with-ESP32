# We can use this file to manualy deploy our API to Google Cloud Run (serverless container)
# If you have Google CLI instaled just type in the console: ./deploy.sh

# Since we have Google Cloud Build configured to trigger on GitHub push to master, we don't have to deploy manually

GOOGLE_PROJECT_ID=weather-station-esp32

# build an image and send it to Google Cloud Container Registry (which use a bucket to store images)
gcloud builds submit --tag gcr.io/$GOOGLE_PROJECT_ID/weather-api \
  --project=$GOOGLE_PROJECT_ID

# deploy created image to Google Cloud Run serverless container
gcloud run deploy weather-api \
  --image gcr.io/$GOOGLE_PROJECT_ID/weather-api \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated \
  --project=$GOOGLE_PROJECT_ID