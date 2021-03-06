import rawpy
import imageio
import glob
import os
import sys
import multiprocessing as mp
import time
import argparse

def convert(f):
    print ('Processing --> ' + f)
    with rawpy.imread(f) as raw:
        rgb = raw.postprocess(use_camera_wb=True)
    fileName = os.path.splitext(f)[0] + '.jpg'
    fileName = fileName.replace(sys.argv[1],'')
    newFileName = sys.argv[1] + 'converted/' + fileName
    imageio.imsave(newFileName, rgb)

def main():
    parser = argparse.ArgumentParser(description='Quickly converts .ARW files to jpg')
    parser.add_argument('-n', '--numb_cores', type=int, help = 'Restrict the number of cores to use', default =(mp.cpu_count()-1))
    parser.add_argument('-d', '--debug', action='store_true', help = 'enable debugging mode')
    parser.add_argument('folder_name')
    args = parser.parse_args()

    if(args.debug):
        print(args)

    files = glob.glob(args.folder_name +'*.ARW')
    num_photos = len(files)
    print ('nr ARW founded --> ' + str(num_photos))

    if num_photos > 0:
        if not os.path.exists(args.folder_name + 'converted/'):
            os.makedirs(args.folder_name + 'converted/')

        start = time.time()
        if(args.numb_cores != 1):
            with mp.Pool(args.numb_cores) as p:
                p.map(convert, files)
        else:
            for f in files:
                convert(f)
                
        if (args.debug):
            print('Conversion finished, took {} sec'.format(time.time()-start))

if __name__ == "__main__":
    main()