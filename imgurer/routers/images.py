from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from typing import List, Optional
# files (images + form data)
from fastapi import File, UploadFile, Form
from ..util.image_save import calc_item_url, bad_fname_hash,parse_image,SingletonSearchTree
from ..schemas import ImageCreate,ImageOut
# db
from sqlalchemy.orm import Session
from ..crud import create_image
# disk
import shutil
# dependency
from ..dependencies import valid_content_length, get_nas, get_images_db, get_thumbs_nas
# Front end
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/images",
    tags=["images"],
    #dependencies=[Depends()]
)



templates = Jinja2Templates(directory="templates")




# use as endpoint for multiple images in parallel fashion for uploads
@router.post("/upload", status_code=201)
async def upload_image(
    image: UploadFile = File(...),
    nas:str = Depends(get_nas),
    thumbs:str = Depends(get_thumbs_nas),
    images_db:Session = Depends(get_images_db)):
    """
    Endpoint for image upload. 

    - Multi image upload performed by frontend iterating calls to this endpoint.
    """

    # background tasks to perform:

    # calculate image location
    url = calc_item_url(filehash=bad_fname_hash(image.filename),nas=nas)
     

    # save to that location because we're going to ASSUME its safe (its not - we check nothing)
    with open(f"{url}","wb") as buffer:
        shutil.copyfileobj(image.file,buffer)

    # pass off to a worker queue and have another process handle it from here?
    db_image = create_image(images_db,parse_image(url))
        # create a shrinked version --> thumbnail and save
        # calculate dhash @ 64bit
        # calculate details and insert into database --> CRUD
    
    # insert into bkTree with id as stored details?
    SST = SingletonSearchTree.get_instance()
    SST.update_bkTree(bits=int(db_image.dhash128),id=db_image.id)


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

@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html",{ #TODO: staticfiles
        "request": request
    })

@router.get("/upload")
async def read_upload(request: Request):
    """
    i'm not up for building a front end 
    """
    return templates.TemplateResponse("upload.html",{ #TODO: staticfiles
        "request": request
    })

@router.get("/search")
async def read_search(request: Request):
    """
    i'm not up for building a front end
    """
    return templates.TemplateResponse("upload.html",{ #TODO: staticfiles
        "request": request
    })

@router.get("/browse")
async def read_search(request: Request):
    """
    i'm not up for building a front end
    """
    return templates.TemplateResponse("upload.html",{ #TODO: staticfiles
        "request": request
    })
