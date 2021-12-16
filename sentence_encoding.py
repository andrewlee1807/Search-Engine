import nltk
# import numpy as np
import re
from nltk import featstruct
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk import ngrams
import re
import pickle
lemmatizer = WordNetLemmatizer()



with open('bag_word.txt','rb') as f:
    Pronoun_BOW = pickle.load(f)

Noun_BOW = {"device": ["device"],
            "display": ["display", "screen", "resolution", "size", "height", "width", "length", "diameter", "dimension"], 
            "camera": ["camera"], 
            "price": ["price", "fee", "worth", "value", "cost"], 
            # "memory": ["memory", "ram", ""], 
            "battery": ["battery", "life", "working"]}
ADJ_BOW = {"more": ["more", "big", "high", "great", "good", "large", "long", "above"], 
            "less": ["small", "less", "short", "few", "low", "under", "below"]}

Unit_BOW = {
        "display": ["inch", "cm", "mm", "hz"], 
        "camera": ["mp"], 
        "price": ["usd"], 
        # "memory": ["gb", "g"], 
        "battery": ["mah"]}

# for key in Noun_BOW:
#     for syn in wordnet.synsets(key):
#         for lm in syn.lemmas():
#                 Noun_BOW[key].append(lm.name())#adding into synonyms

def get_syn(word, BOW):
    for key in BOW:
        if(word in BOW[key]):
            return key
    return None

def encoding(list_of_tokens):
    priority = {"END": 100, "NNP": 0, "NN": 3, "JJ": 2, "RB": 2, "CD": 1}
    encode_dict = {"device": [0, 0, 0],
                    "display": [0, 0, 0],
                    "camera": [0, 0, 0],
                    "price": [0, 0, 0],
                    "battery": [0, 0, 0],
                    "popularity": [10000, 0, 0.05]}
                    # "memory": [0, 0, 0],}
    list_of_tokens.append(("", "END"))
    temp_queue = []
    for token in list_of_tokens:
        if(len(temp_queue) == 0 or 
                (priority[temp_queue[-1][1]] >= priority[token[1]])):
            temp_queue.append(token)
        else: #priority is small
            weight = 0
            value = ""
            sign = 0
            key = ""
            for sub_token in temp_queue:
                if(sub_token[1] == "NN"): 
                    if(sub_token[0].lower() in Pronoun_BOW):
                        sub_token[1] = "NNP"
                    else:
                        syn = get_syn(sub_token[0], BOW=Noun_BOW)
                        if(syn != None):
                            key = syn
                            weight += 1
                            encode_dict[key][-1] = weight

                if(sub_token[1] == "NNP"): 
                    t = sub_token[0].lower()
                    if(t in Pronoun_BOW):
                        value += (" " + t)
                        value = value.strip()
                        key = "device"
                        weight += 1

                elif(sub_token[1] == "JJ" or sub_token[1] == "RB"):
                    contraints = get_syn(sub_token[0], BOW=ADJ_BOW)
                    if(contraints == "less"): sign = -1
                    elif(contraints == "more"): sign = 1

                elif(sub_token[1] == "CD"): #prior = 3
                    num = re.findall(r"[-+]?\d*\.\d+|\d+", sub_token[0])[0]
                    unit = sub_token[0].split(num)[-1]
                    value = float(num)
                    weight += 1
                    if(unit != num): #contain unit
                        get_key = get_syn(unit, BOW=Unit_BOW) 
                        if(get_key != None):
                            key = get_key
        
            if(key != ""):
                encode_dict[key] = [value, sign, weight]
            temp_queue = [token]
                       
    return encode_dict           
            

def sentence_encoding(sentence):
    #preprocessing

    #remove non-asscii
    sentence = sentence.encode("ascii", errors="ignore").decode()
    #remove space
    sentence = sentence.strip()
    sentence = re.sub(' +', ' ', sentence)
    # print(sentence)
    #tokenizer
    tokens = nltk.word_tokenize(sentence)
    # print(tokens)

    #pos
    pos = nltk.pos_tag(tokens)
    # print(pos)
    #remove un-necessary word
    pos = [tag for tag in pos if (tag[1] in ['CD', 'JJ', 'JJR', 'JJS', 
                                            'NN', 'NNS', 'NNP', 'NNPS', 
                                            'RB', 'RBR', 'RBS',])]
                                            # 'VB', 'VBD', 'VBN', 'VBP', 'VBG', 'VBPZ'])]
    # print(pos)
    lemmatized_pos = []
    for p in pos:
        if(p[1] in ["JJ", "JJR", "JJS"]):
            lemmatized_pos.append([lemmatizer.lemmatize(p[0], pos="a"), "JJ"])
        elif(p[1] in ['NN', 'NNS']):
            lemmatized_pos.append([lemmatizer.lemmatize(p[0], pos="n"), "NN"])
        elif(p[1] in ['RB', 'RBR', 'RBS']):
            lemmatized_pos.append([lemmatizer.lemmatize(p[0], pos="r"), "RB"])
        # elif(p[1] in ['VB', 'VBD', 'VBN', 'VBP', 'VBG', 'VBPZ']):
        #     lemmatized_pos.append((lemmatizer.lemmatize(p[0], pos="v"), "VB"))
        else:
            lemmatized_pos.append(p)

    # print(lemmatized_pos)
    #
    encode_dict = encoding(lemmatized_pos)
    Features = [encode_dict[key][0] for key in encode_dict]
    Weights = [encode_dict[key][2] for key in encode_dict]
    Contraints = [encode_dict[key][1] for key in encode_dict]
    
    return Features, Weights, Contraints

if __name__ == "__main__":

    sample = "Samsung S21 phone larger than 5.0inch,   good cameras,  and cost less than 500USD, and battery around 4000mah   "
    code = sentence_encoding(sample)
    print(code)