import os
import json
import numpy as np
import copy

ROOT_DIR = os.path.abspath("../../")

def getRegion(imageV,type = 'ring'):
    goodRegions = []
    orderX = []
    #type = type.lower()
    it = iter(imageV)
    for region in it:
        #print(region)
        regAtt = region['region_attributes']
        shAtt = region['shape_attributes']
        if shAtt['name'] == 'polyline':
            goodRegions.append(region) #I removed checking for ring here because we use pollyline only for rings and it checkes before
            orderX.append(np.average(shAtt['all_points_x']))
    if not goodRegions:
        #print("No data")
        return None
    return {'goodRegions':goodRegions, 'orderX':(np.argsort(orderX))}

def linesToPolygons(input = os.path.join(ROOT_DIR,'Mask_RCNN/JSONtransform/testJSON.json'), output = os.path.join(ROOT_DIR,'Mask_RCNN/JSONtransform/testJSONresult.json')):

    newJ = {}
    shpAttrBase = {'name':'polygon'}
    with open(input,'r') as json_file:
        dct = json.load(json_file)
        for image, imageAtt in dct.items():
            #print("Which image:",' ',image)
            newJ[image] = {}
            for imageK, imageV in imageAtt.items():
                #print("imageKeys:",' ',imageK)
                if imageK == 'regions':
                    #print("unsortedRegions:",' ',imageV)
                    sortRegions = getRegion(imageV, type = 'ring')
                    if sortRegions == None:
                        #print("continue, no sortRegions")
                        continue;
                    #print("sortRegions:",' ',sortRegions)
                    #print('orderX: ',sortRegions['orderX'])
                    shpAtt = shpAttrBase.copy()
                    newJ[image]['regions'] = []
                    for i in range(len(sortRegions['orderX'])-1):
                        #print(i)
                        firstRegion = sortRegions['goodRegions'][sortRegions['orderX'][i]]['shape_attributes']
                        secondRegion = sortRegions['goodRegions'][sortRegions['orderX'][i+1]]['shape_attributes']
                        #print('firstRegion: ',firstRegion)
                        #print('secondRegion: ',secondRegion)
                        shpAtt['all_points_x'] = firstRegion['all_points_x'] + secondRegion['all_points_x'][::-1]
                        shpAtt['all_points_y'] = firstRegion['all_points_y'] + secondRegion['all_points_y'][::-1]
                        #print('newAtt: ',shpAtt)
                        regions = {'shape_attributes':shpAtt,'region_attributes':{'type':'RingBndy'}}
                        newJ[image]['regions'].append(copy.deepcopy(regions))
                else:
                    #print(imageV)
                    try:
                        newJ[image][imageK] = imageV
                    except:
                        print("can't append:",' ',imageK,",",imageV)
            with open(output,'w') as outfile:
                json.dump(newJ, outfile,indent=4)
    return newJ



#for conveniance run on all jsons in directory and merge them in one
##function takes input folder and take .json files, transforms them and export transformed files and complete combined file in the output folder 
##this is still not working :(
def transformallJSON(input_folder, output_folder):
    dic_all = {}
    for file in os.listdir(input_folder):
        if file.endswith(".json"):
            try:
                
                input = os.path.join(input_folder, file)
                output = os.path.join(output_folder,'transformed' + file)
                print(input)
                print(output)
                dic = polylinesToPolygonJSON.linesToPolygons(input = os.path.join(input_folder, file), output = os.path.join(output_folder,'transformed' + file))
                #print(len(dic))
                dic_all.update(dic)
                #print(len(dic_all))
            except:
                print('This failed:',file)
                pass
    filenames =[]
    for image, imageAtt in dic_all.items():
        print(imageAtt['filename'])
        filenames.append(imageAtt['filename'])
    return(dic_all, filenames)
    
    