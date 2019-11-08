import glob
import json
import argparse
import os
import urllib.request


def merge_json(json_path):
    print('Merge json data.....')
    js_list = []
    month = str(opt.path.split('/')[1].split('_')[0])
    print(month)
    for js in json_path:
        with open(js, 'r') as f:
            js_file = json.load(f)

        js_list = js_list + js_file
    

    return js_list
        

def download_image(merge_data):
    print('Starting download Images.....')
    
    success_list = []
    error_list = []
    
    print('Total Images:', len(merge_data))
    for idx, data in enumerate(merge_data):
        
        img_url = 'content_img/'+opt.path.split('/')[1].split('_')[0]+'/'+data['img_path'].split('/')[-1]
        img_url = img_url.split('?')[0]
        if os.path.exists(img_url):
            #print(idx,'Image is already saved')
            continue
        try:
            urllib.request.urlretrieve(data['img_path'], img_url)
            success_list.append(idx)
            print(idx, data['img_path'])
        except:
            print('ERROR', data['img_path'])
            error_list.append(idx)
            pass
    
    print('success_count_is',len(success_list))
    print('error_count_is',len(error_list)) 
    
                      



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='', help='log dir path')
    opt = parser.parse_args()
    
    json_path = glob.glob(opt.path+'*.json')
    print('Total json file count is', len(json_path))
    
    merge_data = merge_json(json_path)
    download_image(merge_data)
     