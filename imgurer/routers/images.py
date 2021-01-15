from fastapi import APIRouter, Depends
from typing import List
from ..util.images import image_save
from ..dependencies import valid_content_length

router = APIRouter(
    prefix="/images",
    tags=["images"]
)


# files (images + form data)
from fastapi import File, UploadFile, Form
import shutil #for now



# use as endpoint for multiple images in parallel fashion for uploads
@router.post("/upload", status_code=201)
async def upload_image(image: UploadFile = File(...)):
    """
    Endpoint for image upload.
    """

    # background tasks to perform:

    # calculate image location
    # save to that location
    # create a shrinked version --> thumbnail and save
    # calculate dhash @ 64bit
    # calculate details and insert into database --> CRUD

    destination_folder = "./NAS/"
    with open(f"{destination_folder}desination.png","wb") as buffer:
        shutil.copyfileobj(image.file,buffer)


    return {"filename": image.filename, "content_type":image.content_type, "file":image.file}

@router.get("/similar",tags=["search"], status_code=400)
def similar_images_ti(image: UploadFile=File(...)):
    """
        Endpoint for either uploading an image and returning its similar or selecting an image and returning its similar
        not sure yet folks
    """
    return {"filename": image.filename, "content_type":image.content_type, "file":image.file}

    # find all image_hash in database that are "similar enough" to this image_hash

#TODO: provide search of database for similar 


