from PIL import Image, ImageDraw, ImageFont
from IPython import display
import glob
import json
import argparse
import os


def Draw_annotaion_box(annos):
    fnt = ImageFont.truetype('bahnschrift.ttf',size=20)
    for ann in annos:
        img_path = ann['img_path']
        img = Image.open(img_path)
        
        frame = img.copy()
        draw = ImageDraw.Draw(frame)
        for idx, obj in enumerate(ann):
            if idx < 2: continue
            
            box = ann[obj]['box']
            value = ann[obj]['value']
            
            draw.rectangle(box, outline=(255,0,0), width = 3)
            draw.text((box[0]+5,box[1]+5),  value, font=fnt, fill=(255,0,0))
        
        frame.save('content_img/'+path.split('_')[-1].split('.')[0]+'_with_box/'+img_path.split('/')[-1])
        print('Image saved....,'+img_path)
                           

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--anno-file', type=str, default='', help='annotaion file')
    opt = parser.parse_args()
    
    path = opt.anno_file
    
    with open(path, 'r') as f:
        annos = json.load(f)
    
    Draw_annotaion_box(annos)
