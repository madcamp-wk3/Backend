from pydantic import BaseModel

# Define the model for metadata associated with the uploaded image
class ImageMetadata(BaseModel):
    username: str
    description: str