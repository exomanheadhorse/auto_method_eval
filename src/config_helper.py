import yaml
import os
from typing import Dict
from database_helper import DatabaseHelper


class ConfigHelper(object):
    def __init__(self) -> None:
        self.db_info_map = dict()
        self.log_info_map = dict()

    @staticmethod
    def load_from_dict(key, dict, property):
        for k, v in dict[key].items():
            property.setdefault(k, v)
    
    def load_config(self):
        cur_path = os.path.dirname(os.path.realpath(__file__))
        yaml_path = os.path.join(cur_path, "../etc/config.yaml")

        if not os.path.exists(yaml_path):
            raise Exception("%s not found!" % yaml_path)

        f = open(yaml_path, 'r', encoding='utf-8')
        cft = f.read()

        d = yaml.load(cft, Loader=yaml.FullLoader)

        self.db_info_map = d['db']
        self.log_info_map = d['log']


if __name__ == '__main__':
    c = ConfigHelper()
    c.load_config()
    print(c.db_info_map.get('cdn_mat').get('password'))
    print(c.log_info_map)