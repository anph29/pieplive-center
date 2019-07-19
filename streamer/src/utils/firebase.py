from .pyrebase import pyrebase

my_stream = None

def config():
    return pyrebase.initialize_app({
        "apiKey": "AIzaSyCMSM_EJFrQ9K8zb6FFDtonppI_zOI1YZc",
        "authDomain":  "piepme-161803.firebaseapp.com",
        "databaseURL": "https://piepme-161803.firebaseio.com",
        "storageBucket": "piepme-161803.appspot.com",
        # "serviceAccount": "path/to/serviceAccountCredentials.json"
    })
