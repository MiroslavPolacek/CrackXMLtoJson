"""
This script loads and cleans up annotations from xml file. Then checks images from Tasks and move images that were sussesfully
annotated to train folder and adds json for exactly these images. Should save number of images, rings and cracks in dataset.

To run on my mac:
cd /Users/miroslav.polacek/github/CrackXMLtoJson &&
conda activate TreeRingCNN &&
python3 CleanAndMoveTrainData.py

"""
import os
import json
import shutil
import XMLtoJSON #this is my function that should be in the same forlder

# Specify the paths to images, xml files and where the 'train' or 'val' folder should be created
PATH_IMAGES = "/Volumes/MiroAllLife/Plot_8/Tasks_2ndRound"
PATH_XML = "/Volumes/MiroAllLife/Plot_8/XML_annotations_2ndRound"
PATH_OUTPUT = "/Users/miroslav.polacek/github/TreeRingCracksCNN/Mask_RCNN/datasets/treering/train"
BUFFER = 30 #how much to buffer polyline when creating polygon

# load and transform all xml annotations
dic_all = {}
for xmlfile in os.listdir(PATH_XML):
    if xmlfile.endswith(".xml") and not xmlfile.startswith("._"):
        #print(file)
        try:
            dic = XMLtoJSON.XMLtoJSON(Path_xml = os.path.join(PATH_XML, xmlfile), buffer = BUFFER)
            dic_all.update(dic)
        except:
            print('This failed:',xmlfile) #needs to go in log
            pass
print("Annotated images in all XMLs", len(dic_all)) #might also go in log


# get list of image names in annotations
annotated_image_names = [imageAtt['filename'] for image, imageAtt in dic_all.items()]
"""
all_annotated_image_names = []
for image, imageAtt in dic_all.items():
    all_annotated_image_names.append(imageAtt['filename'])
"""
# remove images with empty regions from the annotated images list
"""
# This seemed pointless and we create the regions in XMLtoJSON function
# check if each image have something in regions
empty_regions_img = []
for image, imageAtt in dic_all.items():
    try:
        #print(imageAtt['filename'])
        print(imageAtt['regions'])
    except:
        empty_regions_img.append(imageAtt['filename'])
        pass
print("These images in xml files have empty regions", empty_regions_img) # should also be in log
# annotated_image_names = [x for x in all_annotated_image_names if all_annotated_image_names not in empty_regions_img]
"""
# move images that are in annotations to the output folder
all_images_paths = []
all_images_names = []
for path, subdirs, files in os.walk(PATH_IMAGES):
    for filename in files:
        all_images_paths.append(os.path.join(path, filename))
        all_images_names.append(filename)
print("All images in tasks", len(all_images_names))
moved_images = []
for img_path in all_images_paths:
    img_filename = os.path.basename(img_path)
    if img_filename in annotated_image_names[:200]:
        moved_images.append(img_filename)
        img_out = os.path.join(PATH_OUTPUT, img_filename)
        shutil.copy(img_path, img_out) #did not work without obvious reason :(
print("Images that were moved in train data:", len(moved_images))
# save json of annotated images in output folder
img_in_folder = os.listdir(PATH_OUTPUT)
dic_subset = {}
for image, imageAtt in dic_all.items():
    if imageAtt['filename'] in img_in_folder:
        dic_subset[image] = imageAtt
    else:
        next
#print(dic_subset)
output = os.path.join(PATH_OUTPUT,'via_region_data_transformed.json')

with open(output,'w') as outfile:
                json.dump(dic_subset, outfile,indent=4)
print("Json was saved")
# save a log file with all basic data of the run, number of images, rings and cracks
