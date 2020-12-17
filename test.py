from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()

#Assume we need 2 sections in the config file, let's call them USERINFO and SERVERCONFIG
config_object["SURVEYINFO"] = {
    "destination_lang": "English",
    "original_lang": "Chinese",
    "excel_file_name": "testtrans",
    "surveyname": "testtrans"
}

config_object["APIINFO"] = {
    "YOUR_ACCESS_TOKEN": "v8P3p2WMWTaZNSuDosmN1qypC85Ezdk3G0xtol2fun3iBGzfqV7EWbbPqA51R07wXZhyfi0fW4Ro2GXjFtzgNvH0g0dNOuSuwnbAjtz8CNY27XAfda3aWb9mzUr8vf71",
}

#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)
