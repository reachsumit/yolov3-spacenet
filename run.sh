source activate py27
python generate_old_bounding_boxes.py
source deactivate
python logistics.py
python generate_yolo_bounding_boxes.py
python post_processing.py
