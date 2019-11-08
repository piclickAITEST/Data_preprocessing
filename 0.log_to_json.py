import glob
import json
import argparse
import os


def list_to_json(log_path):
    print('Loading log_file......')
    with open(log_path, 'rb') as f:
        log = f.read()
    log_split = log.split(b'\n')
      
    error_log = []
    success_log = []
    for idx, log in enumerate(log_split):
        try:
            log_json = json.loads(log)
            success_log.append(log_json)
        except:
            error_log.append(idx)

    # Check log len
    print('--success_log.....',len(success_log))
    print('--error_log.....',len(error_log))
    print('--Total_log.....',len(success_log)+len(error_log))
    return success_log


def get_google_api_info(logs_json, new_log_path):
    
    annotation = []

    for idx, log in enumerate(logs_json):
        anno = {}
        if 'http' in log['c_img_url']:
            path = log['c_img_url']
        else:
            path = 'https:'+log['c_img_url']
            
        anno['img_path'] = path
        boxes = log['data']['responses'][0]['productSearchResults']['productGroupedResults']
        for idx,box in enumerate(boxes):
            value = {}
            xyxy= box['boundingPoly']['normalizedVertices']
            try:
                label = box['objectAnnotations'][0]['name']
            except:
                continue
            value['label'] = label
            value['xyxy'] = xyxy
            anno['obj_'+str(idx)] = value

        annotation.append(anno)
    
    #Bounding box가 없는 이미지 제거 process
    error_list = []
    success_list = []
    for anno in annotation:
        if len(anno) == 1:
            continue
        else:
            success_list.append(anno)

    # final success list = 8975        
    print('--Total_annotation_count......', len(success_list))
    
    
    with open(new_log_path,'w') as f:
        json.dump(success_list, f, ensure_ascii=False, indent='\t')
    print('--Saved annotation :', new_log_path)

    return annotation
    



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default='', help='log dir path')
    opt = parser.parse_args()
    
    path = opt.path
    

    log_path = glob.glob(opt.path+'*.log')
    for path in log_path:
        print('==================',path,'==================')
        dir_path = path.split('/')[0]+'/'+path.split('/')[1]+'_json/'
        log_name = path.split('/')[-1].split('.')[0]+'.json'
        new_log_path = dir_path+log_name
        print("check log exist", new_log_path)
        if os.path.isfile(new_log_path):
            print("already Done")
            continue
        
        logs_json = list_to_json(path)
        google_api_result = get_google_api_info(logs_json, new_log_path)
    
    
