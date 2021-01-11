# imgurer

Image upload 
    - [ ] one + bulk
        - [ ] POST
    - [ ] enormous (1000's)
        - [ ] Websocket?
        - [ ] partial uploader?
        - [ ] ???


Users
- [ ] CRUD
- [ ] link to images
- [ ] auth / access
    - [ ] web tokens
    - [ ] websockets auth?


Image validation / check
    - [ ] parse + validate types?
    - [ ] put through some kind of moderation middleman? (rekognition / etc)

Image storage
    - [ ] hash
        - [ ] filename? image contents? rgb channels? 
        - [ ] what is most unique? 
            - [ ] author + content + salt ?
    - entry to database
        - [ ] url from hash
        - [ ] link to user
        - [ ] features /  tags / etc
    - write to disk
        - [ ] tree file/folder structure 
            - [ ] hash collisions?
        - [ ] NAS
        - [ ] CDN?
        - [ ] thumbnail    
            - [ ] create thumbnail
            - [ ] store thumbnail
            - [ ] serve thumbnail