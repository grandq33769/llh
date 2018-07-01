import json
from argparse import ArgumentParser
from pprint import pprint

parser = ArgumentParser()
parser.add_argument('-f', '--file', dest='file',
                    help='Topo json file')
parser.add_argument('-v', '--village_file', dest='village_file',
                    help='.txt file with village name')
args = parser.parse_args()

FILE = args.file
VILLAGE = args.village_file
INDEX_DICT = {'collection':'VILLAGENAM',
              'tmp':'VILLNAME'}

with open(FILE, 'r') as rf:
    data = json.load(rf)

'''
pprint(data.keys())
scale = data['transform']['scale']
translate = data['transform']['translate']

def dePosition(position):
    return_position = []
    for idx, p in enumerate(position):
        return_position.append(p * scale[idx] + translate[idx])

    return return_position

def deArc(arc):
    return_arc = []
    acc_pt = list(arc[0])
    return_arc.append(dePosition(arc[0]))
    for pt in arc[1:]:
        print(acc_pt, pt)
        acc_pt = [x+pt[idx] for idx,x in enumerate(acc_pt)]
        return_arc.append(dePosition(acc_pt))

    return return_arc

pprint(data['arcs'][9074])
pprint(data['arcs'][9081])
pprint(deArc(data['arcs'][9097]))
pprint(data['arcs'][9098])
'''

# Read topojson FILE
check = set()
# pprint(data['objects']['layer1']['geometries'])
key = list(data['objects'].keys())[0]
for d in data['objects'][key]['geometries']:
    town_name = d['properties']['TOWNNAME']
    village_name = d['properties'][INDEX_DICT[key]]
    combine = town_name + village_name
    check.add(combine.replace(']','').replace('[',''))
 
    '''
    if  village_name == '王公里':
        print('Before:',d['arcs'][0])
        pprint(d)
        check.append(d)
    '''
   
# Read all data village name
villname = set()    
with open(VILLAGE, 'r') as rf:
    for name in rf.readlines():
        villname.add(name.replace('\n',''))
   
diff = villname.difference(check)
        
pprint(diff)
pprint(len(diff))
'''
with open('./tainan2.new.topo.json', 'w', encoding='unicode-escape') as wf:
    json.dump(data, wf)
'''
