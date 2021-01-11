# imgurer

Image upload 
- [ ] one + bulk
    - [ ] POST
- [ ] enormous (1000's)
    - [ ] Websocket?
    - [ ] partial uploader?
    - [ ] ???


Users
- [x] CRUD
- [ ] link to images
- [ ] auth / access
    - [x] web tokens
        - [ ] permissioning
            - [ ] delete
            - [ ] view
    - [ ] websockets auth?


Image validation / check
- [ ] parse + validate types / size?
- [ ] put through some kind of moderation middleman? (rekognition / etc)

Image storage

- write to disk
    - [ ] tree file/folder structure
        - user/images???
        - user/hash/hash/images?
        - hash/hash/images?
        - [ ] two users upload same image??? store 1,10,1000's same?
        - [ ] hash collisions?
    - [ ] difference hash
        - [ ] difference hash stored in DB
        - [ ] later compare / search on similarity of imagehash?
- entry to database
    - [ ] url
        - from hash? from SOME kind of hashing function?
        - hash + incrementing number?
        - incremementing numbers and hope noone maps directory? 
    - [ ] link to user
        - many to many mapping
    - [ ] features / tags
        - extract features at upload
        - add tags if permissioned?
        - add tags if logged in?
- write to disk
    - [ ] naive folder destination
    - [ ] NAS
    - [ ] CDN?
    - [ ] thumbnail
        - [ ] create thumbnail
        - [ ] store thumbnail
        - [ ] serve thumbnail in place of original