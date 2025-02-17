import yaml
import os
from typing import Dict


config: Dict = None

working_dir = os.getcwd()
application_yml_path = working_dir + "/resources/application.yml"


with open(application_yml_path, "r") as ymlfile:
    config = yaml.load(ymlfile.read(), Loader=yaml.Loader)
