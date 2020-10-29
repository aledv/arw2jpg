import imageio
import os
import sys

def convert(f):
    print ('Processing --> ' + f)
    with rawpy.imread(f) as raw:
        rgb = raw.postprocess(use_camera_wb=True)
    fileName = os.path.splitext(f)[0] + '.jpg'
    fileName = fileName.replace(sys.argv[1],'')
    newFileName = sys.argv[1] + 'converted/' + fileName
    imageio.imsave(newFileName, rgb)