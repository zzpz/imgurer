from fastapi import APIRouter
from typing import List

router = APIRouter()


# files (images + form data)
from fastapi import File, UploadFile, Form
import shutil #for now



# use as endpoint for multiple images in parallel fashion for uploads
@router.post("/image", tags=["images"], status_code=201)
async def upload_image(image: UploadFile = File(...)):
    """
    Endpoint for image upload.
    """
    destination_folder = "./NAS/"
    with open(f"{destination_folder}desination.png","wb") as buffer:
        shutil.copyfileobj(image.file,buffer)

    return {"filename": image.filename, "content_type":image.content_type, "file":image.file}


# which is better? I feel like single endpoint for a given request is best until we flood with too many users connecting?
# good problems to have i guess
@router.post("/images",tags=["images"])
async def upload_images(images: List[UploadFile] = File(...)):
    destination_folder = "./NAS/"
    for image in images:
        with open(f"{destination_folder}{image.filename}","wb") as buffer:
            shutil.copyfileobj(image.file,buffer)