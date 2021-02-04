import polib
import csv
import pandas as pd
from configparser import ConfigParser



def getExcel(excel_file_name):
    excel_file_path = 'translationfile/' + excel_file_name + '.xlsx'
    df = pd.read_excel(excel_file_path, 0, header = 0)
    df = df.dropna(how='all').dropna(axis=1, how='all')
    df.columns = df.columns.str.strip()
    df.rename(columns={"Chinese (Simplified)": "Chinese(Simplified)", "Chinese (Traditional)": "Chinese(Traditional)"}, inplace=True)
    return df.to_dict('records')

def makeSortedTable(origintable, original_lang):
    transTable = sorted(origintable, key = lambda k: len(k[original_lang]), reverse = True)
    return transTable

def updateConfig(k, content):
    config_object['SURVEYINFO'][k] = content
    with open('config.ini', 'w') as c:
        config_object.write(c)

# replace everything key with values in the string
def replaceDict(dict, str):
    for k, v in dict.items():
        if k in str:
            str = str.replace(k, v)
    return str


lang_list = ['English', 'Chinese', 'Korean', 'French', 'German', 'Russian', 'Japanese', 'Polish', 'Spanish', 'Italian', 'Vietnamese', 'Arabic', 'Dutch', 'Indonesian', 'Portuguese', 'Swedish', 'Thai', 'Turkish', 'Chinese(Simplified)', 'Chinese(Traditional)']
lang_dict = {'English':'en', 'Chinese':'zh', 'Korean':'ko', 'French':'fr', 'German':'de', 'Russian':'ru', 'Japanese':'ja', 'Polish': 'pl', 'Spanish':'es', 'Italian':'it', 'Vietnamese': 'vi', 'Arabic':'ar', 'Dutch':'nl', 'Indonesian':'id', 'Portuguese':'pt', 'Swedish':'sv', 'Thai':'th', 'Turkish':'tr', 'Chinese(Simplified)': 'zh_Hans', 'Chinese(Traditional)': 'zh_Hant'}
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


config_object = ConfigParser()
config_object.read("config.ini")
surveyinfo = config_object["SURVEYINFO"]
apiinfo = config_object["APIINFO"]


#Determine and test the two languages to translate between
while True:
    destination_lang_infile = surveyinfo['destination_lang']
    destination_lang_entered = input(f'Please enter the language list you want to translate into. Press ENTER if the destination language is {destination_lang_infile}.')
    #  {surveyinfo['destination_lang']}
    if len(destination_lang_entered)< 1:
        destination_lang = destination_lang_infile.strip().split(',')
        break
    else:
        destination_lang = destination_lang_entered.strip().split()
        if "(Simplified)" in destination_lang:
            destination_lang = [x for x in destination_lang if x != "Chinese" and x != "(Simplified)"]
            destination_lang += ["Chinese(Simplified)"]
        if "(Traditional)" in destination_lang:
            destination_lang = [x for x in destination_lang if x != "Chinese" and x != "(Traditional)"]
            destination_lang += ["Chinese(Traditional)"]
        if all(x in lang_dict for x in destination_lang) == False:
            print('Unsupported language appears, please try again.')
            print(destination_lang)
        else:
            updateConfig('destination_lang', ','.join(destination_lang))
            break


while True:
    original_lang_infile = surveyinfo['original_lang']
    original_lang = input(f'Please enter the language to translate from. Press ENTER if the original language is {original_lang_infile}.')
    #  {surveyinfo['original_lang']}
    if len(original_lang)< 1:
        original_lang = original_lang_infile
        break
    elif original_lang not in lang_list:
        print('Unsupported language, please try again.')
    else:
        # if original_lang = "Chinese(Simplified)": original_lang = "Chinese"
        updateConfig('original_lang', original_lang)
        break



# ask for excel file name and load into sorted dictionary
excel_file_name = input(f"Please enter your translation excel file name? Press ENTER if the file name is {surveyinfo['excel_file_name']}.")
if len(excel_file_name)< 1:
    excel_file_name = surveyinfo['excel_file_name']
else:
    updateConfig('excel_file_name', excel_file_name)

excelfile = getExcel(excel_file_name)
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

    # for entry in po:
    #     if entry.msgid == sub_dict[original_lang]: entry.msgstr = sub_dict[deslang]

    po.save(excel_file_name + '_finished_translation_' + deslang + '.po')

print('--------End substituting sentences--------')
