import pandas as pd
import json


def askFileName():
    input_file_name = input("What's your translation file name?")
    if len(input_file_name) < 6:input_file_name = 'satisfied'
    file_path = 'translationfile/' + input_file_name + '.xlsx'
    return file_path

def getExcel(file_path):
    df = pd.read_excel(file_path, 0)
    df = df.dropna(how='all').dropna(axis=1, how='all')
    return df.to_dict('records')

def makeSortedTable(origintable, original_lang):
    transTable = sorted(origintable, key = lambda k: len(k[original_lang]), reverse = True)
    return transTable

file_path = askFileName()
dicf = getExcel(file_path)
# print(dicf)

with open('template.json', 'r') as infile:
    template = json.load(infile)


template += dicf

print(json.dumps(template, indent = 4))


with open('template.json', 'w') as outfile:
    json.dump(template, outfile)


# print(json.dumps(template, indent = 4))

# print(transTable)
