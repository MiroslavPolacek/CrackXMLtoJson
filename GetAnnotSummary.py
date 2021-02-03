"""
Load annotation json file and save txt file with summary of data structure.

To run on my mac:
cd /Users/miroslav.polacek/github/CrackXMLtoJson &&
conda activate TreeRingCNNtest &&
python3 GetAnnotSummary.py
"""
import os
import json
import shutil

print("LOADING JSON FILE")
#PATH_JSON = "/Volumes/MiroAllLife/TreeRingDatasetsBackUp/treering_new/train/via_region_data_transformed.json" # New training set
#PATH_JSON = "/Volumes/MiroAllLife/TreeRingDatasetsBackUp/treering_new/val/via_region_data_transformed.json" # New val set
#PATH_JSON = "/Volumes/MiroAllLife/TreeRingDatasetsBackUp/treering_old/train/via_region_data_transformed.json" # Old train set
PATH_JSON = "/Volumes/MiroAllLife/TreeRingDatasetsBackUp/treering_old/val/via_region_data_transformed.json" # Old val set
#PATH_JSON = "/Users/miroslav.polacek/github/TreeRingCracksCNN/Mask_RCNN/datasets/treering_mini/val/via_region_data_transformed.json"
PATH_OUTPUT = os.path.split(PATH_JSON)[0]
print("DATA LOADED")
annot = json.load(open(PATH_JSON))
#print(annot['filename'])

image_names= [imageAtt['filename'] for image, imageAtt in annot.items()]
n_images = len(image_names)
print(n_images)

annot = list(annot.values())
rings = []
cracks = []
im_cracks = []
for a in annot:
    rings_and_cracks = [r['region_attributes']['type'] for r in a['regions']]
    rings_string = [i for i in rings_and_cracks if i=="RingBndy"]
    rings.extend(rings_string)
    cracks_string = [i for i in rings_and_cracks if i=="CrackPoly"]
    cracks.extend(cracks_string)
    if len(cracks_string) > 0:
        im_cracks.append(1)


n_rings = len(rings)
n_cracks = len(cracks)
n_im_cracks = sum(im_cracks)


log_file = os.path.join(PATH_OUTPUT, "dataset_log.txt")
with open(log_file, 'w') as f:
    print("Run on this file: {}.".format(PATH_JSON), file=f)
    print("File contains {} images.".format(n_images), file=f)
    print("In this dataset there are {} rings, {} cracks and {} images containing cracks.".format(n_rings, n_cracks, n_im_cracks ), file=f)
