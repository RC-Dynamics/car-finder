import tools
import buyacar

sites = tools.read_json_element('buyacar', "site")

#buyacar.POK()
#print(sites)
for id in range(len(sites)):
    buyacar.extrator(str(sites[str(id)]), id) 
#write_json('buyacar',1, "1000", "Blue", "$50k","Automatic", "Good Car")