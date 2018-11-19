import tools
import buyacar
import kbb
import marbles
import kijiji
import munstermanauto
import usedcars
import cars
import time

sites = ["buyacar","kbb","kijiji","marbles","munstermanauto","usedcars","cars"]
count = 0
for item in sites:
    site = tools.read_json_element("sitepool",item)
    #print(site)
    for id in range(len(site)):
        
        if(item == "buyacar"):
            print(str(site[str(count)]))
            buyacar.extrator(str(site[str(count)]), count) 
        if(item == "kbb"):
            print(str(site[str(count)]))
            kbb.extrator(str(site[str(count)]), count) 
        if(item == "kijiji"):
            kijiji.extrator(str(site[str(count)]), count) 
        if(item == "marbles"):
            marbles.extrator(str(site[str(count)]), count) 
        if(item == "munstermanauto"):
            munstermanauto.extrator(str(site[str(count)]), count) 
        if(item == "usedcars"):
            usedcars.extrator(str(site[str(count)]), count) 
        if(item == "cars"):
            cars.extrator(str(site[str(count)]), count) 
        print(count)
        print(" ")
        count += 1
        #time.sleep(2)