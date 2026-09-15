# Implement Direct-to-Cloud Uploads for Supabase Storage

This plan outlines the steps to bypass Vercel's 4.5 MB serverless payload limit by implementing Direct-to-Cloud Uploads. The browser will upload the study material files directly to a Supabase Storage bucket, and Django will only store the reference URL.

## User Review Required
> [!IMPORTANT]
> **Supabase S3 Credentials Needed:**
> To implement this, you will need to create a Storage Bucket in Supabase (e.g., named `study-materials`) and obtain your Supabase S3 credentials. I will need:
> - `AWS_ACCESS_KEY_ID`
> - `AWS_SECRET_ACCESS_KEY`
> - `AWS_STORAGE_BUCKET_NAME`
> - `AWS_S3_ENDPOINT_URL` (usually `https://<your-project-id>.supabase.co/storage/v1/s3`)
> 
> *Do not paste them in the chat if you want to keep them secret. You can just set them in your Vercel Environment Variables and local `.env`.*

> [!WARNING]
> **Database Schema Change:**
> We will need to change the `file` field on the `StudyMaterial` model from a local `FileField` to a `URLField` (or configure `django-storages`). Since Vercel is read-only, using a `URLField` that points to the Supabase Storage URL is the cleanest approach.

## Proposed Changes

### 1. Backend: Boto3 & Presigned URLs
- Install `boto3`.
- Create a new Django view `generate_presigned_url` that uses `boto3` to generate an S3 presigned PUT URL for Supabase Storage.
- Return the presigned URL and the final public accessible URL to the frontend.

### 2. Frontend: JS Upload Interception
- Modify `templates/quiz/study_material.html`.
- Intercept the upload form submission using JavaScript.
- Step 1: Request a presigned URL from the new Django endpoint.
- Step 2: Use `fetch()` with `PUT` to upload the file directly to Supabase (bypassing Vercel).
- Step 3: Once successful, submit the form to Django, passing the Supabase file URL instead of the actual file payload.

### 3. Backend: Model & Service Updates
- Update `StudyMaterial` model in `quiz/models.py` (and `quiz/study_models.py` if used) to store a `file_url` instead of a local `FileField`.
- Update `quiz/views.py` `upload_study_material` to accept the URL string and create the database record.
- Update `quiz/services.py` `extract_text_from_file()` to download the file from the URL to the temporary Vercel folder (`/tmp/`) before parsing the text (PDF/DOCX).

## Verification Plan
### Manual Verification
- Attempt to upload a PDF file larger than 5 MB locally.
- Verify that the file uploads to the Supabase Storage bucket.
- Verify that the AI Exam generation successfully downloads the file from the bucket and extracts the text without hitting Vercel's payload or read-only filesystem limits.
