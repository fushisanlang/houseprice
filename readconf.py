
import configparser

def ReadConf(section, item_key):
    conf_file = "conf.ini"
    cf = configparser.ConfigParser()
    cf.read(conf_file)

    item_value = cf.get(section, item_key)
    return item_value