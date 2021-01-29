import PySimpleGUI as sg
from configparser import ConfigParser


lang_dict = {'English':'en', 'Chinese':'zh', 'Korean':'ko', 'French':'fr', 'German':'de', 'Russian':'ru', 'Japanese':'ja', 'Polish': 'pl', 'Spanish':'es', 'Italian':'it', 'Vietnamese': 'vi', 'Arabic':'ar', 'Dutch':'nl', 'Indonesian':'id', 'Portuguese':'pt', 'Swedish':'sv', 'Thai':'th', 'Turkish':'tr', 'Chinese(Simplified)': 'zh_Hans', 'Chinese(Traditional)': 'zh_Hant', 'Norwegian': 'no'}
lang_list = ['English', 'Chinese', 'Korean', 'French', 'German', 'Russian', 'Japanese', 'Polish', 'Spanish', 'Italian', 'Vietnamese', 'Arabic', 'Dutch', 'Indonesian', 'Portuguese', 'Swedish', 'Thai', 'Turkish', 'Chinese(Simplified)', 'Chinese(Traditional)', 'Norwegian']
chinese_lang_dict = {'English':'英语', 'Chinese':'中文', 'Korean':'韩语', 'French':'法语', 'German':'德语', 'Russian':'俄语', 'Japanese':'日语', 'Polish': '波兰语', 'Spanish':'西班牙语', 'Italian':'意大利语', 'Vietnamese': '越南语', 'Arabic':'阿拉伯语', 'Dutch':'荷兰语', 'Indonesian':'印度尼西亚语', 'Portuguese':'葡萄牙语', 'Swedish':'瑞典语', 'Thai':'泰语', 'Turkish':'土耳其语', 'Chinese(Simplified)': '简体中文', 'Chinese(Traditional)': '繁体中文', 'Norwegian': '挪威语'}



def updateConfig(k, content):
    config_object['SURVEYINFO'][k] = content
    with open('config.ini', 'w') as c:
        config_object.write(c)


#Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")
surveyinfo = config_object["SURVEYINFO"]
apiinfo = config_object["APIINFO"]

destination_lang_infile = surveyinfo['destination_lang']
original_lang_infile = surveyinfo['original_lang']
excel_file_path_infile = surveyinfo['excel_file_path']


sg.theme('DarkAmber')

layout = [[sg.Text('Please enter the following translation information:')],
          [sg.Text('Please enter the language list you want to translate into:')],
          [sg.InputText(f'{destination_lang_infile}')],
          [sg.Text('Please enter the language to translate from:')],
          [sg.InputText(f'{original_lang_infile}')],
          [sg.Text('Translation File:')],
          [sg.Input(f'{excel_file_path_infile}'), sg.FileBrowse()],
          [sg.Submit(), sg.Cancel()]]

window = sg.Window('Translation Substitution', layout)

event, values = window.read()



while True:
    destination_lang_entered = values[0].strip().split(' ')
    original_lang_entered = values[1].strip()
    excel_file_path_entered = values[2].strip()
    print(original_lang_entered, destination_lang_entered, excel_file_path_entered)

    langs = destination_lang_entered.copy()
    langs.append(original_lang_entered)

    if event in  (None, 'Cancel'):
        break
    if event == 'Submit':
        for lang in langs:
            try:
                lang_dict[lang]
            except:
                sg.Popup(f'{lang} is a unsupported language. Please try again.')
                continue



window.close()

updateConfig('original_lang', original_lang_entered)
updateConfig('destination_lang', ' '.join(destination_lang_entered))
updateConfig('excel_file_path', excel_file_path_entered)


# print(event)
# print(values)

print(f'You clicked {event}')
print(f'You chose filenames {values[0]}, {values[1]}, {values[2]}')
