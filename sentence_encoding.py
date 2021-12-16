import nltk
# import numpy as np
import re
from nltk import featstruct
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
# from nltk import ngrams
import re
lemmatizer = WordNetLemmatizer()


synonyms = {"device": [], "display": [], "camera": [], "popularity": [], "price": [], "memory": [], "battery": [],
             "less": [], "more": [], "around": []}
for key in synonyms:
    for syn in wordnet.synsets(key):
        for lm in syn.lemmas():
                synonyms[key].append(lm.name())#adding into synonyms

def check_synonym(word):
    for key in synonyms:
        if(word in synonyms[key]):
            return key
    return ""

print(check_synonym("monitor"))

def encoding(list_of_tokens):
    priority = {"END": 100, "NNP": 0, "NN": 3, "JJ": 2, "RB": 2, "CD": 1}
    encode_dict = {"device": [0, 0, 0],
                    "display": [0, 0, 0],
                    "camera": [0, 0, 0],
                    "popularity": [0, 0, 0],
                    "price": [0, 0, 0],
                    "memory": [0, 0, 0],
                    "battery": [0, 0, 0]}
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
                if(sub_token[1] == "NN"): #prior = 1
                    syn = check_synonym(sub_token[0])
                    if(syn != ""):
                        key = syn
                        weight += 1
                        encode_dict[key][-1] = weight

                elif(sub_token[1] == "NNP"): #prior = 0
                    value += (" " + sub_token[0])
                    value = value.strip().lower()
                    key = "device"
                    weight += 1
                elif(sub_token[1] == "JJ" or sub_token[1] == "RB"): #prior = 2
                    contraints = check_synonym(sub_token[0])
                    if(contraints == "less"): sign = -1
                    elif(contraints == "more"): sign = 1

                elif(sub_token[1] == "CD"): #prior = 3
                    num = re.findall(r"[-+]?\d*\.\d+|\d+", sub_token[0])[0]
                    # unit = sub_token[0].split(num)[-1]
                    value = float(num)
                    weight += 1
                    # if(unit != num): #contain unit
        
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
            lemmatized_pos.append((lemmatizer.lemmatize(p[0], pos="a"), "JJ"))
        elif(p[1] in ['NN', 'NNS']):
            lemmatized_pos.append((lemmatizer.lemmatize(p[0], pos="n"), "NN"))
        elif(p[1] in ['RB', 'RBR', 'RBS']):
            lemmatized_pos.append((lemmatizer.lemmatize(p[0], pos="r"), "RB"))
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

    sample = "  What Samsung S21 phone with \xe5 display more than 5.0 inches,   good cameras,  and price less than 500USD, and battery around 4000mah   "
    code = sentence_encoding(sample)
    print(code)