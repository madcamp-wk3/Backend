from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from models import ImageMetadata
import os
from datetime import datetime
import uuid

# Create FastAPI instance
app = FastAPI()

# Create an uploads directory if it doesn't exist
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.post("/api/upload-image")
async def upload_image(
    username: str = Form(...),                # Metadata field (username)
    description: str = Form(...),            # Metadata field (description)
    image: UploadFile = File(...)            # The image file itself
):
    """
    API endpoint to handle image uploads with metadata (username, description).
    """

    # Validate file type (e.g., only allow JPEG and PNG)
    if image.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG and PNG are allowed.")

    # Generate a unique filename for the uploaded image
    unique_filename = f"{uuid.uuid4()}_{image.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    # Save the image file
    with open(file_path, "wb") as buffer:
        buffer.write(await image.read())

    # Generate a response that matches your Android `UploadResponse`
    response = {
        "id": str(uuid.uuid4()),  # Generate a unique ID
        "createdAt": datetime.now().isoformat(),  # Current timestamp
        "username": username,
        "description": description,
        "filename": unique_filename  # Save the unique filename
    }
    return JSONResponse(response)