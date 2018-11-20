import json
import tools

data = tools.read_json("index")
data = json.dumps(data, indent=0, sort_keys=False)
arquivo_json = open('normal.json','w')
arquivo_json.write(data)
arquivo_json.close
data = tools.read_json("index")

base = 0
for key, value in data.iteritems():
    base = 0
    #print("another list")
    for item in value:
        #print("ant",item['doc'])
        item['doc'] = item['doc'] - base
        base = item['doc'] + base
        #print("pos",item['doc'])
        #print(" ")

data = json.dumps(data, indent=0, sort_keys=False)

arquivo_json = open('sub.json','w')
arquivo_json.write(data)
arquivo_json.close