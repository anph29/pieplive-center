import pyrebase
firebase = pyrebase.initialize_app({
    "apiKey": "AIzaSyCMSM_EJFrQ9K8zb6FFDtonppI_zOI1YZc",
    "authDomain":  "piepme-161803.firebaseapp.com",
    "databaseURL": "https://piepme-161803.firebaseio.com",
    "storageBucket": "piepme-161803.appspot.com",
    # "serviceAccount": "path/to/serviceAccountCredentials.json"
})
db = firebase.database()
auth = firebase.auth()



def stream_handler(message):
    print(message)
    my_stream.close()


my_stream = db.child("messenger_Client").stream(stream_handler)
