import json

with open('test.json', 'r') as f:
    file = json.load(f)

print(json.dumps(file, indent = 4))

for dic in file:
    print(dic['Chinese(Traditional)'])
