"""
This script loads and cleans up annotations from xml file. Then checks images from Tasks and move images that were sussesfully
annotated to train folder and adds json for exactly these images. Should save number of images, rings and cracks in dataset.

To run on my mac:
cd /Users/miroslav.polacek/github/CrackXMLtoJson &&
conda activate TreeRingCNNtest &&
python3 CleanAndMoveTrainDataCombineWithTheOld.py
"""
import os
import json
import shutil
import XMLtoJSON # this is my function that should be in the same forlder

# Specify the paths to images, xml files and where the 'train' or 'val' folder should be created
PATH_IMAGES_NEW = "/Volumes/MiroAllLife/Plot_8/Tasks_2ndRound"
PATH_IMAGES_OLD = "/Volumes/MiroAllLife/Annotations/Tasks"
PATH_XML_NEW = "/Volumes/MiroAllLife/Plot_8/XML_annotations_2ndRound"
PATH_XML_OLD = "/Volumes/MiroAllLife/Annotations/AnnotationsOldDatasetWithCracks"
#PATH_OUTPUT = "/Users/miroslav.polacek/github/TreeRingCracksCNN/Mask_RCNN/datasets/treering/val"
PATH_OUTPUT = "/Volumes/MiroAllLife/TreeRingDatasetsBackUp/treering/train"
PATH_OLD_VAL_JSON = "/Volumes/MiroAllLife/Annotations/old_val/via_region_data_transformed.json"
BUFFER = 30 #how much to buffer polyline when creating polygon

# load and transform all xml annotations from old and new dataset
dic_all = {}
for xmlfile in os.listdir(PATH_XML_NEW):
    if xmlfile.endswith(".xml") and not xmlfile.startswith("._"):
        #print(file)
        try:
            dic = XMLtoJSON.XMLtoJSON(Path_xml = os.path.join(PATH_XML_NEW, xmlfile), buffer = BUFFER)
            dic_all.update(dic)
        except:
            print('This failed:',xmlfile) #needs to go in log
            pass
for xmlfile in os.listdir(PATH_XML_OLD):
    if xmlfile.endswith(".xml") and not xmlfile.startswith("._"):
        #print(file)
        try:
            dic = XMLtoJSON.XMLtoJSON(Path_xml = os.path.join(PATH_XML_OLD, xmlfile), buffer = BUFFER)
            dic_all.update(dic)
        except:
            print('This failed:',xmlfile) #needs to go in log
            pass


print("Annotated images in all XMLs", len(dic_all)) #might also go in log


# get list of image names in annotations
annotated_image_names = [imageAtt['filename'] for image, imageAtt in dic_all.items()]

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
## get names and paths to all images of both new and old datset
all_images_paths = []
all_images_names = []
for path, subdirs, files in os.walk(PATH_IMAGES_NEW):
    for filename in files:
        all_images_paths.append(os.path.join(path, filename))
        all_images_names.append(filename)
for path, subdirs, files in os.walk(PATH_IMAGES_OLD):
    for filename in files:
        all_images_paths.append(os.path.join(path, filename))
        all_images_names.append(filename)
print("All images in tasks", len(all_images_names))

## get a list of images in old validation dataset
list_old_val_img = json.load(open(PATH_OLD_VAL_JSON))
old_val_set_imnames = [imageAtt['filename'] for image, imageAtt in list_old_val_img.items()]
print("old_val_set_imnames", len(old_val_set_imnames))

## now move
moved_images = []
for img_path in all_images_paths:
    img_filename = os.path.basename(img_path)
    if img_filename in annotated_image_names and img_filename not in old_val_set_imnames and img_filename not in moved_images:
        moved_images.append(img_filename)
        img_out = os.path.join(PATH_OUTPUT, img_filename)
        shutil.copy(img_path, img_out)
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
## define function to cound the words in it
def word_count(str):
    counts = dict()
    words = str.split()
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts
##count the words
all_words = word_count(str(dic_subset)) #change to dic_subset

log_file = os.path.join(PATH_OUTPUT, "dataset_log.txt")
with open(log_file, 'w') as f:
    print("Annotated images in all XMLs {}".format(len(dic_all)), file=f)
    print("All images in tasks {}".format(len(all_images_names)), file=f)
    print("Images that were moved in this dataset: {}".format(len(moved_images)), file=f)
    print("In this dataset there are {} rings and {} cracks".format(all_words["'RingBndy'}},"], all_words["'CrackPoly'}},"] ), file=f)
