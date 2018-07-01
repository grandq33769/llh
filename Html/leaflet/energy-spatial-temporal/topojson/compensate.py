import copy
import json
from argparse import ArgumentParser
from pprint import pprint

parser = ArgumentParser()
parser.add_argument('-v', '--village', dest='village',
                    help='.txt file contain data village')
parser.add_argument('-ot', '--original_topo', dest='ori_topo',
                    help='Original topo json file which missing village name')
parser.add_argument('-st', '--supplement_topo', dest='sup_topo',
                    help='Supplement topo json file to compensate the original one')
parser.add_argument('-ex', '--exclusive', dest='exclusive', default='',
                    help='.txt file contain village name for escaping')
parser.add_argument('-om', '--output_main', dest='output_main', default='output_main.json',
                    help='Output topo json main filename')
parser.add_argument('-os', '--output_supplement', dest='output_sup', default='output_sup.json',
                    help='Output topo json supplement filename')

args = parser.parse_args()
ORI_DATA = args.village
ORI_TOPO = args.ori_topo
SUP_TOPO = args.sup_topo
EXCLUSIVE = args.exclusive
OUTPUT_MAIN = args.output_main
OUTPUT_SUP = args.output_sup
INDEX_DICT = {'collection':'VILLAGENAM',
              'tmp':'VILLNAME'}


with open(ORI_DATA, 'r') as rf:
    villname = {n.replace('\n','') for n in rf.readlines()}
if EXCLUSIVE != '':    
    with open(EXCLUSIVE, 'r') as rf:
        EXCLUSIVE = {n.replace('\n','') for n in rf.readlines()}

print('Excluesive village:')
pprint(EXCLUSIVE)

def read_topo(topofile):
    '''
    Input: topofile path
    Output: dict for topofile
    '''
    with open(topofile, 'r') as rf:
        return_dict = json.load(rf)

    return return_dict

def read_villname_topo(topo):
    '''
    Input: topo dictionary load from json
    Output: set of village name included in topofile
    '''
    return_set = set()
    key = list(topo['objects'].keys())[0]

    for d in topo['objects'][key]['geometries']:
        town_name = d['properties']['TOWNNAME']
        village_name = d['properties'][INDEX_DICT[key]]
        combine = town_name + village_name
        return_set.add(combine.replace('[','').replace(']',''))

    return return_set

def remove_village_json(topo_dict, cand):
    '''
    Remove all candidate village name in topo_dict 
    Input:
        topo_dict: dict from loading json file
        cand: all village name needed to remove
    Output:
        return_dict: dict without cand village name
    '''
    return_dict = copy.deepcopy(topo_dict)
    key = list(topo_dict['objects'].keys())[0]
    contents = topo_dict['objects'][key]['geometries']
    new_contents = list()
    
    for d in contents:
        town_name = d['properties']['TOWNNAME']
        village_name = d['properties'][INDEX_DICT[key]]
        combine = town_name + village_name
        combine = combine.replace('[','').replace(']','')
        if combine not in cand:
            new_contents.append(d)

    return_dict['objects'][key]['geometries'] = new_contents

    return return_dict
    

if __name__ == '__main__':
    ori = read_topo(ORI_TOPO)
    sup = read_topo(SUP_TOPO)
    ori_vill = read_villname_topo(ori)
    sup_vill = read_villname_topo(sup)
    diff_ori_vill = ori_vill.difference(villname)
    diff_dov_exc = diff_ori_vill.difference(EXCLUSIVE)

    inter_sup_ori = sup_vill.intersection(ori_vill)

    diff_sup_ori = sup_vill.difference(ori_vill)
    diff_dso_vill = diff_sup_ori.difference(villname)

    print('Original')
    ori_new = remove_village_json(ori, diff_dov_exc)
    print(len(ori['objects']['collection']['geometries']),
          len(ori_new['objects']['collection']['geometries']))

    print('Supplement')
    sup_new = remove_village_json(sup, inter_sup_ori)
    sup_new = remove_village_json(sup_new, diff_dso_vill)
    print(len(sup['objects']['tmp']['geometries']),
          len(sup_new['objects']['tmp']['geometries']))

    with open(OUTPUT_MAIN, 'w') as wf:
        json.dump(ori_new, wf)
        
    with open(OUTPUT_SUP, 'w') as wf:
        json.dump(sup_new, wf)

    print('Still missing village:')
    pprint(villname.difference(ori_vill).difference(sup_vill))
