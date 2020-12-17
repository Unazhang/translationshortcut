import pandas as pd
import json


def askFileName():
    file_path = input("What's your translation file name?") + '.xlsx'
    if len(file_path) < 6:file_path = 'questions.xlsx'
    return file_path

def getExcel(file_path):
    df = pd.read_excel(file_path, 0)
    df = df.dropna(how='all').dropna(axis=1, how='all')
    return df.to_dict('records')

def makeSortedTable(origintable, original_lang):
    transTable = sorted(origintable, key = lambda k: len(k[original_lang]), reverse = True)
    return transTable

file_path = 'gog.xlsx'
df = getExcel(file_path)

with open('template.json', 'w') as outfile:
    json.dump(df, outfile)

# with open('template.json', 'r') as infile:
#     template = json.load(infile)
#
# print(json.dumps(template, indent = 4))

# print(transTable)
