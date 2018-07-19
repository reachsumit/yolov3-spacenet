#!/bin/bash

# This script will request one GPU device and 1 CPU core

#SBATCH --account=mscagpu
#SBATCH --job-name=darknet
#SBATCH --output=logout_%j.txt
#SBATCH --error=logerr_%j.txt
#SBATCH --time=48:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --partition=mscagpu
#SBATCH --gres=gpu:1
#SBATCH --mem-per-cpu=90000


# if your executable was built with CUDA, be sure to load the correct CUDA module:
module purge
module load darknet

#
# your GPU-based executable here
#
# Below is the old command syntax
#darknet detector train obj.data yolo-obj.cfg darknet53.conv.74

# download pre-trained network from here
# wget https://pjreddie.com/media/files/darknet53.conv.74
darknet detector train voc.data yolov3-voc.cfg darknet53.conv.74

# Use below syntax to continue training
#darknet detector train voc.data yolov3-voc.cfg backup/yolov3-voc_900.weights

# Use below syntax to test
#darknet detector test voc.data yolov3-voc.cfg backup/yolov3-voc_900.weights test.jpg
