from fastapi import APIRouter, Depends
from typing import List

# db
from sqlalchemy.orm import Session

from ..util.images.image_save import calc_item_url,bad_fname_hash
from ..dependencies import valid_content_length, get_nas, get_images_db

router = APIRouter(
    prefix="/images",
    tags=["images"],
    #dependencies=[Depends()]
)


# files (images + form data)
from fastapi import File, UploadFile, Form
import shutil



# use as endpoint for multiple images in parallel fashion for uploads
@router.post("/upload", status_code=201)
async def upload_image(
    image: UploadFile = File(...),
    nas:str = Depends(get_nas),
    images_db:Session = Depends(get_images_db)):
    """
    Endpoint for image upload. 

    - Multi image upload performed by frontend iterating calls to this endpoint.
    """

    # background tasks to perform:

    # calculate image location
    url = calc_item_url(filehash=bad_fname_hash(image.filename),nas=nas) 
    # save to that location because we're going to ASSUME its safe (its not)

    with open(f"{url}","wb") as buffer:
        shutil.copyfileobj(image.file,buffer)



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
