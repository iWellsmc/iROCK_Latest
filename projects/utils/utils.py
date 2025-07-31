from base64 import b64encode
from PIL import Image
import os
def generateImage():
    img = Image.new("RGB", (800, 1280), (255, 255, 255))
    img.save("image.png", "PNG")
    with open('image.png', "rb") as image_file:
        encoded_string = b64encode(image_file.read())
        decodeimage = encoded_string.decode("utf-8")
        add_base = 'data:image/png;base64,' + decodeimage
    os.remove('image.png')
    return add_base