import os
import platform
import shutil
#
cwd = os.getcwd().replace("\\", "/")
osname = platform.system()
#
vwr_src = f"{cwd}/viewer/src/"
vwr_util = f"{vwr_src}utils/"
vwr_model = f"{vwr_src}models/"
vwr_module = f"{vwr_src}modules/"
#
str_src = f"{cwd}/streamer/src/"
str_util = f"{str_src}utils/"
str_model = f"{str_src}models/"
str_module = f"{str_src}modules/"
#
commands = [
    #util
      f"{vwr_util}__init__.py#anph#{str_util}__init__.py"
    ,  f"{vwr_util}helper.py#anph#{str_util}helper.py"
    , f"{vwr_util}scryto.py#anph#{str_util}scryto.py"
    , f"{vwr_util}ftype.py#anph#{str_util}ftype.py"
    , f"{vwr_util}store.py#anph#{str_util}store.py"
    , f"{vwr_util}firebase.py#anph#{str_util}firebase.py"
    , f"{vwr_util}zip_helper.py#anph#{str_util}zip_helper.py"
    #model
    , f"{vwr_model}http_model.py#anph#{str_model}http_model.py"
    , f"{vwr_model}l500_model.py#anph#{str_model}l500_model.py"
    , f"{vwr_model}n100_model.py#anph#{str_model}n100_model.py"
    , f"{vwr_model}q170_model.py#anph#{str_model}q170_model.py"
    #module
    #module
]
for command in commands:
    a, b = command.split('#anph#')
    shutil.copyfile(a, b)