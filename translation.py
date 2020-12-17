import polib
import csv
import pandas as pd


def getExcel(excel_file_path):
    df = pd.read_excel(excel_file_path, 0)
    df = df.dropna(how='all').dropna(axis=1, how='all')
    return df.to_dict('records')

def makeSortedTable(origintable, original_lang):
    transTable = sorted(origintable, key = lambda k: len(k[original_lang]), reverse = True)
    return transTable

# replace everything key with values in the string
def replaceDict(dict, str):
    for k, v in dict.items():
        if k in str:
            str = str.replace(k, v)
    return str


lang_list = ['English', 'Chinese', 'Korean', 'French', 'German', 'Russian', 'Japanese', 'Polish', 'Spanish', 'Italian', 'Vietnamese', 'Arabic', 'Dutch', 'Indonesian', 'Portuguese', 'Swedish', 'Thai', 'Turkish', 'Origin', 'Chinese1']
lang_dict = {'English':'en', 'Chinese':'zh', 'Korean':'ko', 'French':'fr', 'German':'de', 'Russian':'ru', 'Japanese':'ja', 'Polish': 'pl', 'Spanish':'es', 'Italian':'it', 'Vietnamese': 'vi', 'Arabic':'ar', 'Dutch':'nl', 'Indonesian':'id', 'Portuguese':'pt', 'Swedish':'sv', 'Thai':'th', 'Turkish':'tr'}
lang_shortdic = {'EN':'English', 'ZH':'Chinese', 'KO':'Korean', 'SV':'Swedish', 'PL':'Polish', 'NL':'Dutch', 'ID':'Indonesian', 'ES':'Spanish', 'JA':'Japanese', 'TR':'Turkish', 'VI':'Vietnamese', 'FR':'French', 'DE':'German', 'IT':'Italian', 'RU':'Russian', 'PT':'Portuguese', 'TH':'Thai', 'AR':'Arabic'}
sub_dict = {'English':'Please enter a whole number between {0} and {1}.',
            'Chinese1':'请输入{0}和{1}之间的整数。',
            'Korean':'{0}에서 {1} 사이의 정수를 입력하십시오.',
            'French':'Veuillez saisir un nombre entier entre {0} et {1}.',
            'German':'Bitte geben Sie eine ganze Zahl zwischen {0} und {1} ein.',
            'Russian':'Пожалуйста, введите целое число между {0} и {1}.',
            'Japanese':' {0}と{1}の間に整数を入力してください。',
            'Polish': 'Proszę wpisać całą liczbę pomiędzy {0} a {1}.',
            'Spanish':'Por favor, introduzca un número entero entre {0} y {1}.',
            'Italian':'Inserire un numero intero compreso tra {0} e {1}.',
            'Vietnamese': 'Vui lòng nhập một số nguyên từ {0} đến {1}.',
            'Origin': '请输入{0}和{1}之间的整数。'
            }

#Determine and test the two languages to translate between
while True:
    destination_lang = input('Please enter the language to translate into:')
    destination_lang = destination_lang.strip().split()
    print(destination_lang)
    if all(x in lang_dict for x in destination_lang) == False:
        print('Unsupported language appears, please try again.')
    else:
        break


while True:
    original_lang = input('Please enter the language to translate from:')
    if original_lang not in lang_list:
        print('Unsupported language, please try again.')
    else:
        break



# ask for excel file name and load into sorted dictionary
excel_file_name = input("What's your translation file name?")
excel_file_path = excel_file_name + '.xlsx'
if len(excel_file_path) < 6:excel_file_path = 'questions.xlsx'

excelfile = getExcel(excel_file_path)
transTable = makeSortedTable(excelfile, original_lang)



#load and parse HTML substitution files and make a dictionary from it.
html_usable_dict = {}

with open('HTMLsub.csv', 'r', newline='') as htmlreader:
    for row in htmlreader:
        row = row.strip().split(',')
        html_usable_dict[row[1]] = row[0]


#Substitute translation
print('--------Start substituting sentences--------')

for deslang in destination_lang:
    po = polib.pofile('translation_' + lang_dict[deslang] + '.po')
    # print(po)
    for row in transTable:
        for entry in po:
            origin = replaceDict(html_usable_dict, entry.msgid)
            if row[original_lang] in origin:
                print('Original: '+row[original_lang]+'\nMSGID: '+entry.msgid + '\nDestination: ' + row[deslang])
                if entry.msgstr == '':
                    entry.msgstr = origin.replace(row[original_lang], row[deslang])
                else:
                    entry.msgstr = entry.msgstr.replace(row[original_lang], row[deslang])
                print('Substitute to: '+ entry.msgstr)

    for entry in po:
        if entry.msgid == sub_dict[original_lang]: entry.msgstr = sub_dict[deslang]

    po.save(excel_file_name + '_finished_translation_' + deslang + '.po')

print('--------End substituting sentences--------')
