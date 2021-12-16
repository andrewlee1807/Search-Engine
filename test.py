import urllib.request as urllib2
import json
import pysolr
import copy

with open('template.json') as json_file:
  template = json.load(json_file)
  key_list_1 = []
  key_list_2 = []
  for key in template:
    key_list_1.append(key)
    for key_2 in template[key]:
      key_list_2.append(key_2)
  print(key_list_1)
  print(key_list_2)

spec_page = "Full phone specifications"
start_spec = "Network"
end_spec = r"Disclaimer. We can not guarantee that the information on this page is 100% correct"

connection = urllib2.urlopen(r'http://localhost:8983/solr/phone/select?q=*:*&q.op=AND&indent=true&df=title&fq=phone%20specifications&rows=2147483647&wt=json')
#solr = pysolr.Solr('http://localhost:8983/solr/smartphone/select?q=mobile&wt=json')
# response = eval(solr.read())
# print(response)
# response = eval(connection.read())
# print(response)
response = json.load(connection)
print(response['response']['numFound'], "documents found.")

# Print the name of each document.
Database = []
for document in response['response']['docs']:
  print("--------------------------------------")
  content = document['content'][0]
  split_contents = content.split("\n")
  first_line = split_contents[0]
  if(spec_page in first_line):
    
    new_template = copy.deepcopy(template)
    # new_template = template
    Database.append(new_template)
    
    print(first_line)
    model_name = first_line.split("-")[0]
    new_template["DEVICE"] = model_name
    key_1 = None
    for i in range(len(split_contents) - 1):
      line = split_contents[i]
     
      if("hits" in line):
        hits = line.split("hits")
        new_template["POPULARITY"]["Click"] = hits[0]
      if("Become a fan" in line):
        new_template["POPULARITY"]["Love"] = split_contents[i - 1]

      next_line = split_contents[i + 1]
      if(line.upper() in key_list_1):
        key_1 = line.upper()
      if(key_1 == "OPINIONS"):
        continue #skip for now
        # new_template[key_1].append(next_line)
      elif(line in key_list_2):
        key = line
        new_template[key_1][key] = next_line

    Database.append(new_template)
    
# print(Database)
# save database
with open("phone.json", 'w', encoding='utf-8') as f:
  json.dump(Database, f, ensure_ascii=False, indent=4)


