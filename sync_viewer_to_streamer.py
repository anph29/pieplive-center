import os
import platform
import shutil

#
cwd = os.getcwd().replace("\\", "/")
osname = platform.system()
#
VIEWER_SRC = f"{cwd}/viewer/src/"
VIEWER_UTIL = f"{VIEWER_SRC}utils/"
VIEWER_MODEL = f"{VIEWER_SRC}models/"
VIEWER_MODULE = f"{VIEWER_SRC}modules/"
#
STREAM_SRC = f"{cwd}/streamer/src/"
STREAM_UTIL = f"{STREAM_SRC}utils/"
STREAM_MODEL = f"{STREAM_SRC}models/"
STREAM_MODULE = f"{STREAM_SRC}modules/"
#
commands = [
    # util
    f"{VIEWER_UTIL}__init__.py#anph#{STREAM_UTIL}__init__.py",
    f"{VIEWER_UTIL}helper.py#anph#{STREAM_UTIL}helper.py",
    f"{VIEWER_UTIL}scryto.py#anph#{STREAM_UTIL}scryto.py",
    f"{VIEWER_UTIL}ftype.py#anph#{STREAM_UTIL}ftype.py",
    f"{VIEWER_UTIL}store.py#anph#{STREAM_UTIL}store.py",
    f"{VIEWER_UTIL}firebase.py#anph#{STREAM_UTIL}firebase.py",
    f"{VIEWER_UTIL}zip_helper.py#anph#{STREAM_UTIL}zip_helper.py"
    # model
    ,
    f"{VIEWER_MODEL}__init__.py#anph#{STREAM_MODEL}__init__.py",
    f"{VIEWER_MODEL}http_model.py#anph#{STREAM_MODEL}http_model.py",
    f"{VIEWER_MODEL}l500_model.py#anph#{STREAM_MODEL}l500_model.py",
    f"{VIEWER_MODEL}n100_model.py#anph#{STREAM_MODEL}n100_model.py",
    f"{VIEWER_MODEL}q170_model.py#anph#{STREAM_MODEL}q170_model.py",
    f"{VIEWER_MODEL}p300_model.py#anph#{STREAM_MODEL}p300_model.py",
    f"{VIEWER_MODEL}l300_model.py#anph#{STREAM_MODEL}l300_model.py",
]
for command in commands:
    shutil.copyfile(*command.split("#anph#"))

