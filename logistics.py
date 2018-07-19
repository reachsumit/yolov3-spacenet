import os
from skimage import io
import shutil
import random
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
tif_path = config['FILE_PATHS']['TIF_PATH']
TEST_SIZE = float(config['PARAMS']['TEST_SIZE'])

if not os.path.exists("output"):
    os.mkdir("output")
    if not os.path.exists("output/data"):
        os.mkdir("output/data")

fname = []
for raster in os.listdir(tif_path):
    if raster.endswith(".tif"):
        print("Checkpoint 1")
        if raster.endswith(".tif"):
            im = io.imread(tif_path+raster)
            io.imsave("output/data/"+os.path.splitext(raster)[0]+".jpg", im)
            fname.append("data/"+os.path.splitext(raster)[0]+".jpg")

with open('output/data/train.txt', 'w') as thefile:
    for item in fname:
      thefile.write("%s\n" % item)

with open('output/data/test.txt', 'w') as thefile:
    for i in range(int(len(fname)*TEST_SIZE)):
      item = random.choice(fname)
      thefile.write("%s\n" % item)

fname = []
fname.append("building")
with open('output/data/obj.names', 'w') as thefile:
    for item in fname:
      thefile.write("%s\n" % item)

fname = []
fname.append("classes = 1")
fname.append("train  = data/train.txt")
fname.append("valid  = data/test.txt")
fname.append("names = data/obj.names")
fname.append("backup = backup/")
with open('output/voc.data', 'w') as thefile:
    for item in fname:
      thefile.write("%s\n" % item)

shutil.copy2("yolov3-voc.cfg","output/")
shutil.copy2("run.sbatch","output/")
print("Logistics done!")

