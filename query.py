from itertools import count
from sentence_encoding import sentence_encoding
from product_extraction import product_from_dict
import json
from nltk.translate.bleu_score import sentence_bleu
import numpy as np

with open(r"phone.json", encoding='utf-8') as json_file:
    data = json.load(json_file)

    # Print the type of data variable
    print("Type:", type(data))
    list_device = product_from_dict(data)
    database = {}
    for i in range(0, len(list_device), 2): #I dont know why overlap data
        device = list_device[i]
        camera = device.main_camera.single
        price = device.battery.price
        
        # battery = device.battery
        if(device.device.product_name == None):
            continue
        
        name = device.device.brand +  (" " + ' '.join(device.device.product_name))
        porpular = device.popularity.love
        display = device.display.size
        # memory = device.memory
        if(np.any(np.array([camera, price, porpular, display]) == -1)):
            continue
        database.update({i: [name.strip().lower(), display, camera, porpular, price]})
    
    min_display = min([database[k][1] for k in database ])
    max_display = max([database[k][1] for k in database ])
    min_camera = min([database[k][2] for k in database ])
    max_camera = max([database[k][2] for k in database ])
    min_popular = min([database[k][3] for k in database ])
    max_popular = max([database[k][3] for k in database ])
    min_price = min([database[k][4] for k in database ])
    max_price = max([database[k][4] for k in database ])
    print(min_display, max_display, min_camera, max_camera, min_popular, max_popular, min_price, max_price)
    
def query(request, database):

    Features, Weights, Contraints = request
    similarity = {}
    
    min_array = np.array([min_display, min_camera, min_popular, min_price])
    max_min_array = np.array([max_display, max_camera, max_popular, max_price]) - np.array([min_display, min_camera, min_popular, min_price])
    for key in database:
        cons = np.array(Contraints[1:5])
        device = database[key]
        
        
        y = (np.array(Features[1:5]) - min_array) / max_min_array
        x = (np.array(device[1:]) - min_array) / max_min_array
        
        if(np.any((cons * (x - y)) < 0)):
            continue
        BLEU = sentence_bleu([device[0].split(" ")], Features[0].split(" "), weights=(1, 0, 0, 0))
        scores = (x - y) * (x - y)
        scores = np.append(1 - BLEU, scores)
        w = np.array(Weights[0:5])
        w = w/w.sum()
        weighted_sum = (w * scores).sum()   
        similarity.update({key: weighted_sum})

    ranking = dict(sorted(similarity.items(), key=lambda item: item[1]))
  
    return ranking

if __name__ == "__main__":

    sample = "  What Samsung S21 phone with \xe5 display more than 5.0 inches,   good cameras,  and price less than 500USD, and battery around 4000mah   "
    request = sentence_encoding(sample)
    ranking = query(request, database=database)
    top_k_result = 10
    count = 0
    for key in ranking: 
        print(database[key])
        if(count > top_k_result): break
        count += 1