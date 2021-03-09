import configparser
import os

def get_config(section, key):
    config = configparser.ConfigParser()
    path = "config.conf"
    config.read(path)
    return config.get(section, key)
