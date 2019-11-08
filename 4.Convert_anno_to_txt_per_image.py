import glob
import json
import argparse
import os


def anno_to_txt_for_training(anno):
    for ann in anno:
        file_name = ann['img_path'].split('/')[-1]
        img_w, img_h = ann['img_size']
        
        for idx, obj in enumerate(ann):
            if idx < 2: continue
            box = ann[obj]['box']    
            value = ann[obj]['value']
            
            cx = round(((box[2] + box[0]) / 2)/img_w, 6)
            cy = round(((box[3] + box[1]) / 2)/img_h, 6)
            box_w = round((box[2] - box[0])/img_w, 6)
            box_h = round((box[3] - box[1])/img_h, 6)
            
            data = [str(value), str(cx), str(cy), str(box_w), str(box_h)]
            data = ' '.join(data)
        
            with open('labels/'+file_name+'.txt', 'a') as f:
                f.write(data)
                f.write('\n')
                 




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--anno-file', type=str, default='', help='annotaion file')
    opt = parser.parse_args()
    
    path = opt.anno_file
    
    with open(path, 'r') as f:
        annos = json.load(f)
    
    
    anno_to_txt_for_training(annos)