import os
import shutil

yolo_box_files = os.listdir("yolo_style_boxes_txt")

for file in yolo_box_files:
    shutil.move("yolo_style_boxes_txt/"+file, "output/data/"+file)

os.remove("data_list.txt")

shutil.rmtree("yolo_style_boxes_txt")
shutil.rmtree("old_style_boxes_txt")

shutil.make_archive("output", 'zip', 'output')
print("Post processing done! Upload output.zip to RCC.")
print("You can also delete the output directory now.")
