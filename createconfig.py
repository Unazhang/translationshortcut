from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()

#Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG
config_object["SURVEYINFO"] = {
    "destination_lang": "English",
    "original_lang": "Chinese",
    "excel_file_name": "testtrans",
    "surveyname": "testtrans",
    "excel_file_path": " "
}

config_object["APIINFO"] = {
    "YOUR_ACCESS_TOKEN": "Enter your own token here"
}

#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)
