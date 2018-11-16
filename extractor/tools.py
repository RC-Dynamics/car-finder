import json
import buyacar

def read_json_element(site, id):
    arquivo_json = open(site + '.json','r')
    dados_json = json.load(arquivo_json)
    data = dados_json[str(id)]
    return data
def read_json(site):
    try:
        arquivo_json = open(site + '.json','r')
        dados_json = json.load(arquivo_json)
        return dados_json
    except:
        return {}
def write_json(site, id,mileage, exterior_color, price, transmission, title):
    data = {
        'Title': title,
        'Price': price,
        'Exterior Color' : exterior_color,
        'Mileage' : mileage,
        'Transmission': transmission
        }
    data_dic = read_json(site)
    data_dic[str(id)] = data
    data_dic = json.dumps(data_dic, indent=4, sort_keys=False)

    arquivo_json = open(site + '.json','w')
    arquivo_json.write(data_dic)
    arquivo_json.close