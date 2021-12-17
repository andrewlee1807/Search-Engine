from flask import Flask, render_template, request
from sentence_encoding import sentence_encoding
from product_extraction import product_from_dict
import json
from nltk.translate.bleu_score import sentence_bleu
import numpy as np

global database, list_device
# LOAD DATABASE
with open(r"phone.json", encoding='utf-8') as json_file:
    data = json.load(json_file)

    # Print the type of data variable
    print("Type:", type(data))
    list_device = product_from_dict(data)
    database = {}
    for i in range(0, len(list_device), 2): #I dont know why overlap data
        device = list_device[i]
        camera = device.selfie_camera.single
        price = device.battery.price
        battery = device.battery.type
        
        if(device.device.product_name == None):
            continue
        name = device.device.brand +  (" " + ' '.join(device.device.product_name))
        porpular = device.popularity.love
        display = device.display.size
        # memory = device.memory
        if(np.any(np.array([camera, price, porpular, display, battery]) == -1)):
            continue

        database.update({i: [name.strip().lower(), display, camera, price, battery, porpular]})
    
    min_display = min([database[k][1] for k in database ])
    max_display = max([database[k][1] for k in database ])
    min_camera = min([database[k][2] for k in database ])
    max_camera = max([database[k][2] for k in database ])
    min_price = min([database[k][3] for k in database ])
    max_price = max([database[k][3] for k in database ])
    min_battery = min([database[k][4] for k in database ])
    max_battery = max([database[k][4] for k in database ])
    min_popular = min([database[k][5] for k in database ])
    max_popular = max([database[k][5] for k in database ])


def query(request):

    Features, Weights, Contraints = request
    similarity = {}
    
    min_array = np.array([min_display, min_camera, min_price, min_battery, min_popular])
    max_min_array = np.array([max_display, max_camera, max_price, max_battery, max_popular]) - min_array
    for key in database:
        n = 6
        cons = np.array(Contraints[1:])
        device = database[key]
        
        y = (np.array(Features[1:]) - min_array) / max_min_array
        x = (np.array(device[1:]) - min_array) / max_min_array
        
        if(np.any((cons * (x - y)) < 0)):
            continue
        BLEU = 0
        if (Features[0] != 0):
            BLEU = sentence_bleu([device[0].split(" ")], Features[0].split(" "), weights=(1, 0, 0, 0))
        scores = (x - y) * (x - y)
        scores = np.append(1 - BLEU, scores)
        w = np.array(Weights)
        w = w/w.sum()
        weighted_sum = (w * scores).sum()   
        similarity.update({key: weighted_sum})

    ranking = dict(sorted(similarity.items(), key=lambda item: item[1]))
  
    return ranking


app = Flask(__name__)

# # DB settings
# MONGO_URL = app.config['MONGO_URL']
# client = MongoClient(MONGO_URL)
# db = client["test"]
# col = db["Index"]
global t, top_k_result
top_k_result = 10
t = 1


@app.route('/', methods=['GET', 'POST'])
def index():
    """Return index.html
    """
    global t
    global top_k_result
    if request.method == 'POST':
        t = t + 1
        keyword = request.form['keyword']
        if keyword:
            # Call API to get list results
            req = sentence_encoding(keyword)
            ranking = query(req)
            count = 0
            search_results = []
            for key in ranking:
                print(database[key])
                search_results.append(list_device[key])
                if count > top_k_result: break
                count += 1
            return render_template(
                'index.html',
                products=search_results,  # Change query to appear the search RESULTS
                keyword=keyword)  # change keyword ~ search value
    return render_template('index.html')
