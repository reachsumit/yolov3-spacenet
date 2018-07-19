import os
import shutil
import random
import configparser
from osgeo import gdal
import subprocess

config = configparser.ConfigParser()
config.read('config.ini')
tif_path = config['FILE_PATHS']['TIF_PATH']
TEST_SIZE = float(config['PARAMS']['TEST_SIZE'])

if not os.path.exists("output"):
    os.mkdir("output")
    if not os.path.exists("output/data"):
        os.mkdir("output/data")

fname = []
for raster in os.listdir('old_style_boxes_txt'):
    srcRaster = gdal.Open(tif_path+os.path.splitext(raster)[0]+".tif")
    outputRaster = "output/data/"+os.path.splitext(raster)[0]+".jpg"

    cmd = ['gdal_translate', '-ot', 'Byte', '-of', 'JPEG', '-co', 'PHOTOMETRIC=rgb']
    scaleList = []
    for bandId in range(srcRaster.RasterCount):
        bandId = bandId+1
        band=srcRaster.GetRasterBand(bandId)
        min = band.GetMinimum()
        max = band.GetMaximum()

        # if not exist minimum and maximum values
        if min is None or max is None:
            (min, max) = band.ComputeRasterMinMax(1)
        cmd.append('-scale_{}'.format(bandId))
        cmd.append('{}'.format(0))
        cmd.append('{}'.format(max))
        cmd.append('{}'.format(0))
        cmd.append('{}'.format(255))

    cmd.append(tif_path+os.path.splitext(raster)[0]+".tif")
    cmd.append(outputRaster)
    print(cmd)
    subprocess.call(cmd)
    os.remove("output/data/"+os.path.splitext(raster)[0]+".jpg.aux.xml")
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

