import requests
import json
import html
import sys
import pandas as pd
from functools import lru_cache
from configparser import ConfigParser
# import GUI


lang_dict = {'English':'en', 'Chinese':'zh', 'Korean':'ko', 'French':'fr', 'German':'de', 'Russian':'ru', 'Japanese':'ja', 'Polish': 'pl', 'Spanish':'es', 'Italian':'it', 'Vietnamese': 'vi', 'Arabic':'ar', 'Dutch':'nl', 'Indonesian':'id', 'Portuguese':'pt', 'Swedish':'sv', 'Thai':'th', 'Turkish':'tr', 'Chinese(Simplified)': 'zh_Hans', 'Chinese(Traditional)': 'zh_Hant', 'Norwegian': 'no'}
lang_list = ['English', 'Chinese', 'Korean', 'French', 'German', 'Russian', 'Japanese', 'Polish', 'Spanish', 'Italian', 'Vietnamese', 'Arabic', 'Dutch', 'Indonesian', 'Portuguese', 'Swedish', 'Thai', 'Turkish', 'Chinese(Simplified)', 'Chinese(Traditional)', 'Norwegian']
chinese_lang_dict = {'English':'英语', 'Chinese':'中文', 'Korean':'韩语', 'French':'法语', 'German':'德语', 'Russian':'俄语', 'Japanese':'日语', 'Polish': '波兰语', 'Spanish':'西班牙语', 'Italian':'意大利语', 'Vietnamese': '越南语', 'Arabic':'阿拉伯语', 'Dutch':'荷兰语', 'Indonesian':'印度尼西亚语', 'Portuguese':'葡萄牙语', 'Swedish':'瑞典语', 'Thai':'泰语', 'Turkish':'土耳其语', 'Chinese(Simplified)': '简体中文', 'Chinese(Traditional)': '繁体中文', 'Norwegian': '挪威语'}

#problem

# TODO
# interface
# for a specific locale


class Monkey():
    def __init__(self, YOUR_ACCESS_TOKEN):
        # connect to server
        self.s = requests.Session()
        self.s.headers.update({
          "Authorization": "Bearer %s" % YOUR_ACCESS_TOKEN,
          "Content-Type": "application/json"
        })

    @lru_cache(maxsize=256)
    def getSurveyId(self, surveyname):
        #get survey id
        url = f"https://api.surveymonkey.com/v3/surveys?title={surveyname}"
        sur = self.s.get(url).json()
        # print(json.dumps(sur, indent = 4))
        for i in range(len(sur['data'])):
            print(i, sur['data'][i]['nickname'])
        try:
            index = int(input("Which of the surveys above are you referring? ENTER the number."))
        except:
            print("Please enter a NUMBER")
        self.survey_id = sur['data'][index]['id']
        return self.survey_id

    @lru_cache(maxsize=256)
    def getLangResponse(self, survey_id, langcode):
        langResponse = self.s.get('https://api.surveymonkey.com/v3/surveys/{}/languages/{}'.format(survey_id, langcode))
        self.langjson = langResponse.json()
        return self.langjson

    def postLangTranslation(self, survey_id, langcode, jtext):
        self.postr = self.s.post('https://api.surveymonkey.com/v3/surveys/{}/languages/{}'.format(survey_id, langcode), json=jtext)
        print("About to post to this address:" + 'https://api.surveymonkey.com/v3/surveys/{}/languages/{}'.format(survey_id, langcode))
        return self.postr

    def patchLangTranslation(self, survey_id, langcode, jtext):
        self.patchr = self.s.patch('https://api.surveymonkey.com/v3/surveys/{}/languages/{}'.format(survey_id, langcode), json=jtext)
        return self.patchr

    def deleteLangTranslation(self, survey_id, langcode):
        self.deleter = self.s.delete('https://api.surveymonkey.com/v3/surveys/{}/languages/{}'.format(survey_id, langcode))
        return self.deleter

    def getCollectorURL(self, survey_id):
        self.cURL = self.s.get(f'https://api.surveymonkey.com/v3/surveys/{survey_id}/collectors?include=url').json()
        url = self.cURL['data'][0]['url'] + "?fpid=[fpid_value]"
        print("Your list of links are:")
        print(chinese_lang_dict[original_lang] + " , " + url)
        for lang in destination_lang:
            print(chinese_lang_dict[lang] + " , " + url + "&lang=" + lang_dict[lang])
        return url

    def postCollectorURL(self, survey_id):
        jtext = {"type": "weblink"}
        self.posturl = self.s.post(f'https://api.surveymonkey.com/v3/surveys/{survey_id}/collectors', json = jtext)
        print("A new collector has been added.")

    def getLanguages(self, survey_id):
        getlang = self.s.get(f"https://api.surveymonkey.com/v3/surveys/{survey_id}/languages")
        print("Currently available languages:")
        print(getlang.json())






def getExcel(excel_file_path):
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



#Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")
surveyinfo = config_object["SURVEYINFO"]
apiinfo = config_object["APIINFO"]
#
#
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

print(destination_lang)


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

with open('template.json', 'r') as infile:
    template = json.load(infile)

excel_file_path = 'translationfile/' + excel_file_name + '.xlsx'
excelfile = getExcel(excel_file_path)
excelfile += template
# print(excelfile)
transTable = makeSortedTable(excelfile, original_lang)

# print(transTable)

with open('test.json', 'w') as f:
    json.dump(transTable, f)



Ask for survey name, get survey id and make connection
surveyname = input(f"Please enter your the name of your survey. Press ENTER if the survey name is {surveyinfo['surveyname']}.").strip()
if len(surveyname) < 2:
    surveyname = surveyinfo['surveyname']
else:
    updateConfig('surveyname', surveyname)

print(surveyname)

m = Monkey(apiinfo["YOUR_ACCESS_TOKEN"])
survey_id = m.getSurveyId(surveyname)
print(f"The survey id is {m.survey_id}.")
# current_languages = m.getLanguages(survey_id)

# sys.exit()


#loop through the downloaded dic and substitute.

for deslang in destination_lang:
    print(f"Start substituting for {deslang}")
    langcode = lang_dict[deslang]
    clear_previous_trans = m.deleteLangTranslation(survey_id, langcode)

    langjson = m.getLangResponse(survey_id, langcode)


    # print("This is what's pulled from survey monkey:")
    # print(json.dumps(langjson, indent = 4))

    payload = {}
    payload['translations'] = langjson['translations']


    for row in transTable:
        for line in payload['translations']:
            origin_in_web = str(line['default']).strip()
            origin_in_file = str(row[original_lang]).strip()
            destination_in_file = str(row[deslang]).strip()

            if origin_in_file in origin_in_web:
                # print('Match Found.\nOriginal in File: '+origin_in_file+'\nOriginal in Web: '+origin_in_web +'\nAbout to Change to: ' + destination_in_file)
                if line['translation'] == '':
                    # print('No translation found, create new and replace.')
                    line['translation'] = origin_in_web.replace(origin_in_file, destination_in_file)
                else:
                    # print('Found existing translation, start replace existing translation.')
                    line['translation'] = line['translation'].replace(origin_in_file, destination_in_file)
                # print('Current version of translation:\n'+ line['translation'] + '\nResource ID is:\n' + line["resource_id"])

    payload["enabled"] = True

# deal with the escaping characters

    for line in payload['translations']:
        line['default'] = line['default'].replace('&', '&amp;')
        line['default'] = line['default'].replace('“', '&ldquo;').replace('”', '&rdquo;')


    # for line in payload['translations']:
    #     print(line['translation'])
    #     print(line['resource_id'])

    print(f"End substituting for {deslang} and start uploading.")

    # print("This is what's about to be uploaded:")
    # print(json.dumps(payload, indent = 4))



    #post back the new translation
    postr = m.postLangTranslation(m.survey_id, langcode, payload)
    print("Status Code:" + str(postr.status_code))
    if postr.status_code != 200:
        print("An error occured!\n" + "Error Code: " + str(postr.status_code))
        # print(json.dumps(postr.json(), indent = 4))
        print(postr.json()["error"]["message"])
        sys.exit()
    else:
        print(f"End uploading for {deslang}.")

    # print(json.dumps(postr.json(), indent=4), postr.status_code)

    # patchr = m.patchLangTranslation(m.survey_id, langcode, payload)
    # print(json.dumps(patchr.json(), indent=4), patchr.status_code)


# get collector and create a list of links

url = m.getCollectorURL(survey_id)
# if url.status_code != 200:
#     m.postCollectorURL(survey_id)
#     url = m.getCollectorURL(survey_id)

print("All Done!")
