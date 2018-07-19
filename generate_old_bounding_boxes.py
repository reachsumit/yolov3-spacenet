# coding: utf-8
import os
import configparser
import geojson_to_pixel_arr

config = configparser.ConfigParser()
config.read('config.ini')

tif_path = config['FILE_PATHS']['TIF_PATH']
geojson_path = config['FILE_PATHS']['GEOJSON_PATH']

if __name__ == "__main__":
    for raster in os.listdir(tif_path):
        if raster.endswith(".tif"):
            tif_file = os.path.splitext(raster)[0][15:]
            geojson_file = geojson_path+"buildings_"+tif_file+".geojson"
            if os.path.isfile(geojson_file):
                try:
                    pixel_coords, _ = geojson_to_pixel_arr.geojson_to_pixel_arr(tif_path+raster,geojson_file)
                except:
                    print("Some exception occured in parsing geojson file: {}.".format(geojson_file))
                    continue
                mylist = []
                mylist.append(0)
                for building in pixel_coords:
                    # first convert polygon to rectangle
                    c1 = [x[0] for x in building]
                    c2 = [x[1] for x in building]
                    bbox = [[min(c1),min(c2)],[min(c1),max(c2)],[max(c1),max(c2)],[max(c1),min(c2)],[min(c1),min(c2)]]
                    # find height and width of this rectangle
                    for point in bbox[1:-1]:
                        if point[0] == bbox[0][0]:
                            height = abs(point[1]-bbox[0][1])
                        if point[1] == bbox[0][1]:
                            width = abs(point[0]-bbox[0][0])
                        # find center point of this rectangle    
                        if point[0] != bbox[0][0] and point[1] != bbox[0][1]:
                            x1 = bbox[0][0]
                            y1 = bbox[0][1]
                            x2 = point[0]
                            y2 = point[1]
                            x_center = int((bbox[0][0]+point[0])/2)
                            y_center = int((bbox[0][1]+point[1])/2)
                    mylist.append([x1, y1, x2, y2])
                if not os.path.exists("old_style_boxes_txt"):
                    os.mkdir("old_style_boxes_txt")
                with open("old_style_boxes_txt/"+os.path.splitext(raster)[0]+".txt", 'w') as thefile:
                    for index, item in enumerate(mylist):
                        if index==0:
                            thefile.write("0\n")
                        else:
                            thefile.write("{} {} {} {}\n".format(item[0], item[1], item[2], item[3]))
            else:
                print("geojson corresponding to {} doesn't exist.".format(raster))
    print("Old style bounding boxes created!")

