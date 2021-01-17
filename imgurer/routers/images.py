from fastapi import APIRouter, Depends, Request, status
from fastapi.templating import Jinja2Templates
from typing import List, Optional

# files (images + form data)
from fastapi import File, UploadFile, Form
from ..util.image_save import (
    calc_item_url,
    bad_fname_hash,
    parse_image,
    SingletonSearchTree,
)
from ..schemas import ImageCreate, ImageOut, MultiImageOut

# db
from sqlalchemy.orm import Session
from ..crud import (
    create_image,
    get_image,
    get_bkt_reload_images,
    get_images,
    browse_images,
)

# disk
import shutil

# dependency
from ..dependencies import valid_content_length, get_nas, get_images_db, get_thumbs_nas
from .users import get_current_user

# Front end
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException


router = APIRouter(
    prefix="/images",
    # tags=["images"],
    # dependencies=[Depends()]
)


templates = Jinja2Templates(directory="templates")


# use as endpoint for multiple images in parallel fashion for uploads
@router.post("/upload", tags=["images"], status_code=201)
async def upload_image(
    image: UploadFile = File(...),
    nas: str = Depends(get_nas),
    thumbs: str = Depends(get_thumbs_nas),
    images_db: Session = Depends(get_images_db),
):
    """
    Endpoint for image upload.

    - Multi image upload performed by frontend iterating calls to this endpoint.
    """

    # background tasks to perform:

    # calculate image location
    url = calc_item_url(filehash=bad_fname_hash(image.filename), nas=nas)

    # save to that location because we're going to ASSUME its safe (its not - we check nothing)
    with open(f"{url}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # pass off to a worker queue and have another process handle it from here?
    db_image = create_image(
        images_db, parse_image(image_url=url, filename=image.filename)
    )
    # TODO: image.xxx : keeping file open longer than necessary?

    # create a shrinked version --> thumbnail and save
    # calculate dhash @ 64bit
    # calculate details and insert into database --> CRUD

    # insert into bkTree with id as stored details?
    SST = SingletonSearchTree.get_instance()
    SST.update_bkTree(bits=int(db_image.dhash128), id=db_image.id)

    return {
        "filename": db_image.filename,
        "content_type": image.content_type,
        "id": db_image.id,
    }


@router.post("/similar", tags=["search"], status_code=200, response_model=MultiImageOut)
async def similar_images_to(image_id: int, db: Session = Depends(get_images_db)):
    """
    Endpoint for and image id
    - returning its similar images' ID and urls
    """
    db_image = get_image(images_db=db, id=image_id)
    if not db_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find image",
            headers={"WWW-Authenticate": "Bearer"},
        )
    SST = SingletonSearchTree.get_instance()
    fastfilter: [int] = SST.search_bkTree(bits=int(db_image.dhash128), id=db_image.id)
    # similar will always return at least 1 id (the file itself if it exists)

    similar_imgs = get_images(images_db=db, ids=fastfilter)
    # here we could filter further using a more accurate similarity function

    return similar_imgs


@router.get("/rebuildBKT", tags=["development"], status_code=200)
def rebuild_BKT(db: Session = Depends(get_images_db)):
    """
    # this is for development because of some design decisions
    We have issues because our search tree is stored in the server process's scope
    - it wipes the poor guy once we make any change to a file while developing
    - I don't know how to get the server to call an 'on startup do this' function or where i'd put it atm
    - So there's this bandaid for now

    """
    SST = SingletonSearchTree.get_instance()
    images_to_load = get_bkt_reload_images(db)
    for image in images_to_load:
        SST.update_bkTree(int(image.dhash128), image.id)


@router.get("/upload", tags=["development"])
async def html_upload(request: Request):
    """
    returns /upload template
    """
    return templates.TemplateResponse(
        "upload.html", {"request": request}  # TODO: staticfiles
    )


@router.get("/search", tags=["development"])
async def html_search(request: Request):
    """
    returns /search template
    """
    return templates.TemplateResponse(
        "search.html", {"request": request}  # TODO: staticfiles
    )


@router.get("/browse", tags=["development"])
async def html_browse(request: Request):
    """
    returns /browse template
    """
    return templates.TemplateResponse(
        "browse.html", {"request": request}  # TODO: staticfiles
    )


@router.get("/browsing", status_code=200, response_model=MultiImageOut)
async def browse(db: Session = Depends(get_images_db)):
    images_to_browse = browse_images(images_db=db)

    return images_to_browse


@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "home.html", {"request": request}  # TODO: staticfiles
    )
