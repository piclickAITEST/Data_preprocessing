import glob
import json
import argparse
import os
import urllib.request
from PIL import Image


def change_img_path(merge_json):
    json_list =[]
    no_img = []
    print('Merge annotaion is', len(merge_json))
    for m_json in merge_json:
        new_json = {}
        img_name = m_json['img_path'].split('/')[-1]
        dir_name = opt.merge_json.split('_')[-1].split('.')[0]
        img_path = 'content_img/'+dir_name+os.sep+img_name
        if os.path.exists(img_path):
            im = Image.open(img_path)
            im_w, im_h = im.size #width, height
            new_json['img_path'] = img_path
            new_json['img_size'] = [im_w, im_h]
        else:
            no_img.append(m_json['img_path'])
            continue
        
        
        for idx, obj in enumerate(m_json): 
            obj_value ={}
            if idx == 0: continue
            
            try:
                x1 = m_json[obj]['xyxy'][0]['x'] * im_w 
            except:
                x1 = 0
            try:
                y1 = m_json[obj]['xyxy'][0]['y'] * im_h 
            except:
                y1 = 0
            try:    
                x3 = m_json[obj]['xyxy'][2]['x'] * im_w 
            except:
                x3 = 1
            try:
                y3 = m_json[obj]['xyxy'][2]['y'] * im_h 
            except:
                y3 = 1
                
            box = [x1, y1, x3, y3]
            
            obj_value['box'] = box
            obj_value['value'] = m_json[obj]['label']
        
            new_json[obj] = obj_value
        
        json_list.append(new_json)
    
    print('Total annotation is', len(json_list))
    print('No image count :', len(no_img))
    file_name = 'content_log/annotation_'+str(opt.merge_json.split('_')[-1].split('.')[0])+'.json'
    print('file_name :', file_name)
    with open(file_name, 'w') as f:
        json.dump(json_list, f, ensure_ascii=False, indent='\t')
    
    print('Annotation is saved :', file_name)
        
    return json_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--merge-json', type=str, default='', help='merge json file')
    opt = parser.parse_args()
    
    with open(opt.merge_json, 'r') as f:
        merge_json = json.load(f)
    
    json_anno_list = change_img_path(merge_json)
     