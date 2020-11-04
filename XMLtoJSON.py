


import xmltodict
import copy
from shapely import geometry


def XMLtoJSON(Path_xml, buffer = 30):

    # Load xml file as dic even if it is problematic one
    from xml.parsers.expat import ExpatError
    with open(Path_xml) as f:
        data = f.read()
        try:
            doc = xmltodict.parse(data)
        except ExpatError:
            doc = xmltodict.parse(data[3:])

    # dig in it to get all componenets and transform them to buffer points
    newJ = {}

    for key1, value1 in doc.items():

        for key2, value2 in value1.items():
            #get to task name to append to image name
            if key2 == 'meta':
                for metakey1, metavalue1 in value2.items():
                    if metakey1 =='task':
                        for metakey2, metavalue2 in metavalue1.items():
                            if metakey2 == 'name':
                                task_name = metavalue2
                                #print(task_name)


            #get to image name and annotations
            if key2 == 'image':
                for image_section in value2:
                    for key3, value3 in image_section.items():
                        #print(key3)
                        if key3 == '@name':
                            img_name = value3
                            #print(img_name)
                            task_image = task_name + '_' + img_name
                            newJ[task_image] = {}
                            newJ[task_image]['filename'] = img_name

                        if key3 == '@width':
                            img_width = value3
                        if key3 == '@height':
                            img_height = value3
                            newJ[task_image]['size'] = img_width + 'x' + img_height
                            newJ[task_image]['regions'] = []
                            newJ[task_image]['file_attributes'] = {}
                        if key3 == 'polygon':
                            try:
                                for hmkey, hmvalue in value3.items():
                                    if hmkey == '@points':
                                        bad_points = hmvalue
                                        #print(bad_points)
                                        bad_points_split = bad_points.split(';')

                                        linepoints = []
                                        for points in bad_points_split:
                                            points_split = points.split(',')
                                            point_xy = (float(points_split[0]), float(points_split[1]))
                                            linepoints.append(point_xy)
                                        shapely_polygon = geometry.Polygon(linepoints)
                                        points_x, points_y = shapely_polygon.exterior.xy

                                        shpAtt = {}
                                        shpAtt['all_points_x'] = points_x.tolist()
                                        shpAtt['all_points_y'] = points_y.tolist()
                                        #print(shpAtt['all_points_x'])

                                        regions = {'shape_attributes':shpAtt,'region_attributes':{'type':'CrackPoly'}}
                                        newJ[task_image]['regions'].append(copy.deepcopy(regions))

                            except:
                                for hm in value3:

                                    for polykey, polyvalue in hm.items():
                                        if polykey == '@points':
                                            bad_points = hmvalue
                                            #print(bad_points)
                                            bad_points_split = bad_points.split(';')

                                            linepoints = []
                                            for points in bad_points_split:
                                                points_split = points.split(',')
                                                point_xy = (float(points_split[0]), float(points_split[1]))
                                                linepoints.append(point_xy)
                                            shapely_polygon = geometry.Polygon(linepoints)
                                            points_x, points_y = shapely_polygon.exterior.xy

                                            shpAtt = {}
                                            shpAtt['all_points_x'] = points_x.tolist()
                                            shpAtt['all_points_y'] = points_y.tolist()
                                            #print(shpAtt['all_points_x'])

                                            regions = {'shape_attributes':shpAtt,'region_attributes':{'type':'CrackPoly'}}
                                            newJ[task_image]['regions'].append(copy.deepcopy(regions))


                        if key3 == 'polyline':
                            try:
                                for hmkey, hmvalue in value3.items():
                                    if hmkey == '@points':
                                        bad_points = hmvalue
                                        #print(bad_points)
                                        bad_points_split = bad_points.split(';')

                                        linepoints = []
                                        for points in bad_points_split:
                                            points_split = points.split(',')
                                            point_xy = (float(points_split[0]), float(points_split[1]))
                                            linepoints.append(point_xy)
                                        line = geometry.LineString(linepoints)
                                        #print(line)
                                        buffer_points = line.buffer(buffer, cap_style=1)
                                        #to make ends round use cap_style=1, 2 finishes it sharp at the end of the line ton prevent polygons to stick out of the picture

                                        ##correct those that are out of range of 2 and max-2 (height, width)
                                        height = float(img_height)-2
                                        width = float(img_width)-2

                                        coords = buffer_points.exterior.coords
                                        new_coords = []
                                        for i in range(len(coords)):
                                            coord = coords[i]
                                            x = coord[0]
                                            y = coord[1]
                                            if x <= width and x >= 2 and y <= height and y >= 2:
                                                new_coords.append(coord)
                                        new_polygon = geometry.Polygon(new_coords)


                                        points_x, points_y = new_polygon.exterior.xy

                                        shpAtt = {}
                                        shpAtt['all_points_x'] = points_x.tolist()
                                        shpAtt['all_points_y'] = points_y.tolist()
                                        #print(shpAtt['all_points_x'])

                                        regions = {'shape_attributes':shpAtt,'region_attributes':{'type':'RingBndy'}}
                                        newJ[task_image]['regions'].append(copy.deepcopy(regions))

                                #print(value3) # there is some probelm here in certan iteration i think in case there is only one line
                            except:
                                for hm in value3:

                                    for polykey, polyvalue in hm.items():
                                        if polykey == '@points':
                                            bad_points = polyvalue
                                            #print(bad_points)
                                            #transform them in shapely polygons and add buffer
                                            bad_points_split = bad_points.split(';')

                                            linepoints = []
                                            for points in bad_points_split:
                                                points_split = points.split(',')
                                                point_xy = (float(points_split[0]), float(points_split[1]))
                                                linepoints.append(point_xy)
                                            line = geometry.LineString(linepoints)
                                            #print(line)
                                            buffer_points = line.buffer(buffer, cap_style=1)
                                            #to make ends round use cap_style=1, 2 finishes it sharp at the end of the line ton prevent polygons to stick out of the picture


                                            ##correct those that are out of range of 2 and max-2 (height, width)
                                            height = float(img_height)-2
                                            width = float(img_width)-2

                                            coords = buffer_points.exterior.coords
                                            new_coords = []
                                            for i in range(len(coords)):
                                                coord = coords[i]
                                                x = coord[0]
                                                y = coord[1]
                                                if x <= width and x >= 2 and y <= height and y >= 2:
                                                    new_coords.append(coord)
                                            new_polygon = geometry.Polygon(new_coords)


                                            points_x, points_y = new_polygon.exterior.xy

                                            shpAtt = {}
                                            shpAtt['all_points_x'] = points_x.tolist()
                                            shpAtt['all_points_y'] = points_y.tolist()
                                            #print(shpAtt['all_points_x'])

                                            regions = {'shape_attributes':shpAtt,'region_attributes':{'type':'RingBndy'}}
                                            newJ[task_image]['regions'].append(copy.deepcopy(regions))

    return(newJ)
