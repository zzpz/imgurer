from pathlib import Path




def userhash(username:str):
    """
    TODO: 
        simplistic way to bucket usernames so they don't all wind up in A/aardvark,apple,antelope
        not sure of the implications for on disk / cache misses for reading / etc
        it's just building a way to allow for many many many accounts and images on one disk
        it could just as easily be username first 3 letters then/username?
        probably shouldn't use username itself in path
    """
    simple_hash = username[:3]
    return  

def calc_item_url(username:str, image_hash: str):
    """
    TODO:
        calculate where a given uploaded file should be stored on disk
        handle collisions in filenames
        update reference in database accordingly
    """
    #calculate image url (path pattern)
    path_pattern = f"{userhash(username)}/{username}/{image_hash[:3]}/{image_hash[3:6]}/{image_hash}_%s.jpg"

    url = next_file_path(path_pattern)

    #calculate image url pattern
        # pattern:
        # userhash[:3]/username/filehash[:3]/filehash[3:6]/filehash_{0,1,2,3,4,5}.jpg

    # perform search for that url existing 
        # next_file_path(path_pattern)
        # exponential search - https://en.wikipedia.org/wiki/Exponential_search
        # go to the folder
            # search folder for value
            
                # if found
                    # find next available
                # write to disk
                # update database with url
                # move along
    
    # need username of who uploaded
    # means upload requires auth
    # means I need to sort a basic user login / auth

    return ""
    #userhash[:2]/username/filehash[:2]/filehash[3:6]/filehash_{0,1,2,3,4,5}.jpg




def next_file_path(path_pattern: str):
    """
        Finds the next free filepath in sequentially named list of files

        e.g. path_pattern = 'abc/username/abc/def/foobar_%s.jpg':

        abc/username/abc/def/foobar_1.jpg
        abc/username/abc/def/foobar_2.jpg
        abc/username/abc/def/foobar_3.jpg

        uses exponential search 
        exponential search - https://en.wikipedia.org/wiki/Exponential_search

        TODO: could we just store them all together and use symlinks? 
        would need Path.resolve
    """
    # if directory does not exist we need to make it
    Path.mkdir(dir_path, parents=True, exist_ok=True)

    
    # assume directory exists for now (we'll make it if we have to prior to write)   
    i = 1

    # exponential search the directory  
    while Path.exists(path_pattern % i):
        i = i * 2
    
    # eventually i is larger than the largest foobar_n.jpg that exists
    # this gives us an interval between the 'last' i (i/2) and the 'current' i (i)
    # it is an interval (a..b] that can be searched using binary search (ordered list)
    a,b = (i//2, i)
    while a + 1 < b: #binary search
        c = (a+b) // 2
        a,b = (c,b) if Path.exists(path_pattern % i) else (a,c)
    
    return path_pattern % b

