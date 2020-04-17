import os
import uuid

from PIL import Image


def rename_image(old_filename):
    ext = os.path.splitext(old_filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


def resize_photo(filename):
    filein = './Life/static/photos/%s' %(filename)
    img = Image.open(filein)
    width = 80
    height = 80
    out = img.resize((width, height), Image.ANTIALIAS)
    fileout = './Life/static/photos/s_%s' %(filename)
    out.save(fileout)
    return 's_%s' %(filename)