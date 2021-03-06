# imgurer

A functioning image repository API and frontend with upload and similar(duplicate) image search capabilities.

## installation

NOTE:

- using virtualenvwrapper is recommended
- currently environment variables are required
  - --> defaults are supplied in postactivate.txt

```txt
create a virtual environment in current directory
activate virtual environment 



NOTE: using virtualenvwrapper is recommended
  create environment variables as per postactivate.txt (unset in predeactivate.txt)
  https://virtualenvwrapper.readthedocs.io/en/latest/scripts.html?highlight=postactivate#postactivate



copy repository
install requirements
(optionally) "chmod +x run" to >more easily start server
run server and navigate to >localhost (127.0.0.1:8000/)
127.0.0.1:8000/docs for directly interfacing with the API
```

Python only (no venvwrapper) installation using bash

```bash
python3 -m venv './imgurer'
source bin/activate
git clone https://github.com/zzpz/imgurer.git
cd imgurer

set -o allexport
source postactivate.txt
set +o allexport

pip install -r requirements
uvicorn imgurer.main:app --reload
```

## requirements

imgurer will currently write files to local disk, if this is restricted expect errors
virtualenvwrapper allows for pre and post activation hooks (setting env variables such as $DB_URL)

## Usage

- The application is accessible through both API calls and a frontend on local host.
- User creation is only accessible through the /docs API backend

### Future areas of development

- [x] refactor to external db (:elephant: sql)
- [ ] refactor of image storage from local to CDN/NAS
- [ ] external image store(s)
- [ ] user login and cookied credentials
- [ ] frontend framework (react/vue/etc)
- [ ] parsing image exif data on upload
- [ ] migration to postgres
- [ ] extending models to link user and images

### notes

- images uploaded are stored on disk as both a thumbnail and the original
  - be mindful of filling a harddrive while uploading

- on server reload the ability to search files already uploaded is lost
  - accessing </images/rebuildBKT> will rebuild the search tree
  - the tree can be rebuilt from the search page

- search for similarity is done via a 128bit dhash comparison
  - this is more accurately a search for 'duplicate' images
  - a more sophisticated comparison should then be used for less false positives

- file uploads are not validated
  - size is not checked in headers
  - files are not chunked for upload

- images are bucketed to multiple folders with a hashed name to allow for enormous image sets

- frontend javascript and html is a mess and little to none is re-used

- ***this is in no way safe for a production environment***
