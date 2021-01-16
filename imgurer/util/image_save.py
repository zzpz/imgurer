from pathlib import Path
from typing import Optional
from PIL import Image
from ..schemas import ImageCreate
import pybktree
import collections


def userhash(username:str):
    """
        simplistic way to bucket usernames so they don't all wind up in A/aardvark,apple,antelope
        not sure of the implications for on disk / cache misses for reading / etc
        it's just building a way to allow for many many many accounts and images on one disk
        it could just as easily be username first 3 letters then/username?
        probably shouldn't use username itself in path
    """
    simple_hash = username[:3]
    return simple_hash

def bad_fname_hash(filename:str)->str:
    """
        non cryptographic hash to bucket files
    """
    hash = 'abcdefghijklmnopqrstuvwxyz'
    pos = 0
    for c in filename:
        pos += ord(c)
    return f"{hash[pos%26]}{hash[pos%19%26]}{hash[pos%7%26]}{hash[pos%13%26]}{hash[pos%23%26]}{hash[pos%27%26]}"

def calc_item_url(filehash: str, nas: str,username:Optional[str] = None)->str:
    """
        calculates the url for where a given file (image) should be stored on disk
        handles collisions in filenames at that location
        database should update after

        TODO: a better way if I somehow had all files already? feels like i have to do this to avoid race conditions 
    """
    #calculate image url (path pattern)
    if username :
    # ensure dir exists
        dir_path = f"{nas}/{userhash(username)}/{username}/{filehash[:2]}/{filehash[2:4]}"
        ensure_dir(dir_path)
        path_pattern = f"{userhash(username)}/{username}/{filehash[:2]}/{filehash[2:4]}/{filehash}_%s.jpg"
    else: 
        dir_path = f"{nas}/nouser/{filehash[:2]}/{filehash[2:4]}"
        ensure_dir(dir_path)
        path_pattern = f"{nas}/nouser/{filehash[:2]}/{filehash[2:4]}/{filehash}_%s.jpg"


    # calc path

    url = next_file_path(path_pattern)


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
    # means I need to sort a basic user login / auth front end

    return url

def ensure_dir(dir_path: str):
    """
        If directory does not exist we need to make it,
        can't async or race condition on file create
    """
    path = Path(dir_path)
    Path.mkdir(path, parents=True, exist_ok=True)     #fails silently

def next_file_path(path_pattern: str)->str:
    """
        Finds the next free filepath in sequentially named list of files

        e.g. path_pattern = 'abc/username/abc/def/foobar_%s.jpg':

        abc/username/abc/def/foobar_1.jpg
        abc/username/abc/def/foobar_2.jpg
        abc/username/abc/def/foobar_3.jpg

        exponential search - https://en.wikipedia.org/wiki/Exponential_search

        TODO: could we just store them all together and use symlinks? 
        would need Path.resolve
    """    
    # assume directory exists for now (we'll make it if we have to prior to this func)   
    i = 1

    # exponential search the directory  
    while Path(path_pattern % i).exists():
        i = i * 2

    # eventually i is larger than the largest foobar_n.jpg that exists
    # this gives us an interval between the 'last' i (i/2) and the 'current' i (i)
    # it is an interval (a..b] that can be searched using binary search (ordered list)
    a,b = (i//2, i)
    while a + 1 < b: #binary search backwards
        c = (a+b) // 2
        a,b = (c,b) if Path(path_pattern % c).exists() else (a,c)
    return path_pattern % b


#could just pip install dhash but I wanted to learn it first
def difference_hash_n_bits(image:Image,hash_size: int = 8,row:bool = True, col:bool = True)->(int,int):
    """
        # Hash_size must be same as shrink_and_greyscale do not call one without the other?
        http://www.hackerfactor.com/blog/?/archives/529-Kind-of-Like-That.html

        Difference hash produces a string representing the relative gradients between adjacent pixels in an image.
        This can be compared against other images' hashes using a string-distance comparison (hamming distance) to determine how similar they are.
        There are a number of variants namely in the resizing.

        Briefly:

        - Difference hash works on gradients 
        - Downsize it to a NxN thumbnail (9x9 == 64 bits)
        - Convert the image to grayscale

        - Produce a 64-bit “row hash”: a 1 bit means the pixel intensity is increasing in the x direction, 0 means it’s decreasing
        -   optionally
        -   Do the same to produce a 64-bit “column hash” in the y direction
        -   Combine the two values to produce the final 128-bit hash value
        - e.g.  11111111101110101011111110101010111
        - e.g.  01011111101111110111101011111101101
        
        Compare the hashes to determine how many bits are different, a threshold of <10 is a candidate for being a duplicate
        - Comparison is its own challenge at scale
        https://benhoyt.com/writings/duplicate-image-detection/
    """

    #future we could only perform row_hash or only col_hash and use as fast filter for phash
        
    # compare pixels of each row then of each column
    row_hash = 0
    col_hash = 0
    for y in range(hash_size):
        for x in range(hash_size):
            left = image.getpixel((y,x))
            right = image.getpixel((y+1,x))
            row_bit = left < right #shif row hash left 1, OR with bit
            row_hash = row_hash <<1 | row_bit

            up = left
            down = image.getpixel((y,x+1))
            col_bit = up < down
            col_hash = col_hash << 1 | col_bit #shift col hash left 1, OR with bit
            # we can now calc just row or just col with any size of hash using this bit flip pattern !!! 

    
    #close image now we're done with it? no. close outside of function and do everything we want with it first

    return (row_hash,col_hash) #lets us use either or or concat later or compare separate
       
def get_num_bits_different(hash1, hash2)->int:
    """
    https://github.com/benhoyt/dhash/blob/master/dhash.py
    Calculate number of bits different between two hashes
    >>> get_num_bits_different(0x4bd1, 0x4bd1)
    0
    >>> get_num_bits_different(0x4bd1, 0x5bd2)
    3
    >>> get_num_bits_different(0x0000, 0xffff)
    16
    """
    return bin(hash1 ^ hash2).count('1') 





def shrink_and_greyscale(image_url:str,hash_size:int = 8)->Image:
    # assume that the provided url will be an image location
    # could be saved then picked up separately in batches
    image = Image.open(image_url)
    image = image.convert('L').resize((hash_size + 1, hash_size+1), Image.ANTIALIAS, )
    return image

def make_thumbnail(image_url:str):
    """
        Makes a thumbnail of the target url
    """
    MAX_SIZE = (100,100)

    thumb_path :str = ''
    #better
    with Path(image_url) as p:
        with Image.open(p) as img:
            img.thumbnail(MAX_SIZE)
            img = img.convert('RGB')
            p = 'NAS/thumbs/' / p.relative_to('NAS/nouser/')
            thumb_path = p
            ensure_dir(p.parent)
            img.save(thumb_path)
    return str(thumb_path)

def parse_image(image_url:str, filename:str)->ImageCreate:
    """
    helper function to call a number of image processing functions
    """

    # this is probably a better option?
        # as it closes file and contains it all in this context
    # with Image.open(Path(image_url)) as img:

    thumb_url = make_thumbnail(image_url)
    img = shrink_and_greyscale(image_url)
    row_hash,col_hash = difference_hash_n_bits(img)
    dhash128 = ((row_hash<<32) | col_hash) #concat together
 

    img_create = ImageCreate(
        filename = filename,
        url=image_url,
        thumb_url=thumb_url,
        dhash128=dhash128
        )
    return img_create



    

class SingletonSearchTree():
    """
        singleton class to store all of our images. seems like a poor design decision.
    """
    __instance__ = None
    TreeImage = collections.namedtuple('TreeImage','bits id')
    
    def item_distance(x:TreeImage,y:TreeImage):
        return pybktree.hamming_distance(x.bits, y.bits)
    
    tree=pybktree.BKTree(item_distance)


    def __init__(self):
        """
        Constructor
        """
        if SingletonSearchTree.__instance__ is None:
            SingletonSearchTree.__instance__ = self
        else:
            raise Exception("Singleton --> use SingletonSearchTree.get_instance()")


    
    @staticmethod
    def get_instance():
        """
        static method to fetch instance
        """
        if not SingletonSearchTree.__instance__:
            SingletonSearchTree()
        return SingletonSearchTree.__instance__

    def update_bkTree(self,bits:int, id:int):
        """
            wrapper to get and add to tree for a given image maintaining its id as reference in tree
            - distance is default 8
        """
        bkt: pybktree.BKTree = self.tree
        bkt.add(self.TreeImage(bits,id))

    def search_bkTree(self,bits:int, distance:int = 8, id : Optional[int] = None):
        """
            wrapper to get and search tree for 'similar' images
            - distance is default 8
        """
        bkt: pybktree.BKTree = self.tree
        found = bkt.find(self.TreeImage(bits,id),distance)
        print(found)
        return(found)






