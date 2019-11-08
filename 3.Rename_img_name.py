import os 
import glob
import json
import argparse


def remove_img(unique_path):
    nope = []
    
    img_file = glob.glob('content_img/'+month+'/'+'*.*')
    for img in img_file:
        if not img in unique_path:
            if os.path.isfile(img):
                os.remove(img)
                nope.append(img)
                print('remove!', img)

    print('Removed Images :', len(nope))
                


def Check_double_img(anno):
    unique_path = []
    unique_anno = []
    for ano in anno:
        if not ano['img_path'] in unique_path:
            unique_path.append(ano['img_path'])
            unique_anno.append(ano)
        else:
            continue
            
    remove_img(unique_path)
        
    return unique_anno
         

def Rename_file_name(unique_anno):
    for idx, uni_anno in enumerate(unique_anno):
        ori_img_name = uni_anno['img_path']
        new_img_name = 'content_img/'+month+'/media_'+str(idx)+'.'+ori_img_name.split('.')[-1]
        
        os.rename(ori_img_name, new_img_name)
        
        uni_anno['img_path'] = new_img_name
        print('Renamed....', uni_anno['img_path'])
    
    
    with open('content_log/'+'annotation_'+month+'_uni.json', 'w') as f:
        json.dump(unique_anno, f, ensure_ascii=False, indent='\t')

         
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--anno-path', type=str, default='', help='annotation path')
    opt = parser.parse_args()
    
    path = opt.anno_path
    month = path.split('.')[0].split('_')[-1]
    
    with open(path,'r') as f:
        anno = json.load(f)
    
    unique_anno = Check_double_img(anno)
    Rename_file_name(unique_anno)
    