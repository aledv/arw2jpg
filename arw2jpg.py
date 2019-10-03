import rawpy
import imageio
import glob
import os
import sys

files = glob.glob(sys.argv[1]+'*.ARW')
num_photos = len(files)
print ('nr ARW founded --> ' + str(num_photos))

if num_photos > 0:

    if not os.path.exists(sys.argv[1] + 'converted/'):
        os.makedirs(sys.argv[1] + 'converted/')

    for f in files:
        print ('Processing --> ' + f)
        with rawpy.imread(f) as raw:
            rgb = raw.postprocess()
        fileName = os.path.splitext(f)[0] + '.jpg'
        fileName = fileName.replace(sys.argv[1],'')
        newFileName = sys.argv[1] + 'converted/' + fileName
        imageio.imsave(newFileName, rgb)

print('Conversion finished')

