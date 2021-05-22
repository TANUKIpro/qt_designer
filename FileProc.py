import sys
import os

class FileProc:
    def __init__(self):
        pass

    def getContentsList(self, to_contents, img_type):
        contents  = os.listdir(to_contents)
        images_list = [f for f in contents if (os.path.isfile(os.path.join(to_contents, f)) and f.endswith(img_type))]
        return images_list