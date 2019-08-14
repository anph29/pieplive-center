from .pyrebase import pyrebase
from . import store
from requests.exceptions import HTTPError
from src.models import N100_model


def getFirebase():
    return pyrebase.initialize_app(
        {
            "apiKey": "AIzaSyCMSM_EJFrQ9K8zb6FFDtonppI_zOI1YZc",
            "authDomain": "piepme-161803.firebaseapp.com",
            "databaseURL": "https://piepme-161803.firebaseio.com",
            "storageBucket": "piepme-161803.appspot.com",
            # "serviceAccount": "path/to/serviceAccountCredentials.json"
        }
    )


def config():
    try:
        firebase = getFirebase()
        auth = firebase.auth()
        authen = auth.sign_in_with_custom_token(store._get("tokenfb"))
        store._set("firebaseAuth", authen)
        return firebase.database()
    except:
        # print(e, '--firebase error--')
        return refreshToken()


def refreshToken():
    try:
        firebase = getFirebase()
        auth = firebase.auth()
        res = getTokenFromSession()
        if not res:
            return False
        store._set("tokenfb", res["tokenfb"])
        authen = auth.sign_in_with_custom_token(res["tokenfb"])
        store._set("firebaseAuth", authen)
        return firebase.database()
    except:
        return False


def getTokenFromSession():
    n100 = N100_model()
    res = n100.f5fb_login_viewer(
        {
            "NV117": store._get("NV117"),  # PiepMeID
            "NV125": store._get("NV125"),  # Token
            "LOGIN": store._get("NV101"),
        }
    )
    if res["status"] == "success":
        if res["elements"] == -3:
            return False
        else:
            return res["elements"]


def startObserverActivedBu(callback):
    activedBu = store.getCurrentActiveBusiness()
    if bool(activedBu):
        db = config()
        if bool(db):
            firebaseAuth = store._get("firebaseAuth")
            return db.child(f"l500/{activedBu}").stream(
                callback, token=firebaseAuth["idToken"]
            )


def makeChangePresenter(pl500):
    activedBu = store.getCurrentActiveBusiness()
    if bool(activedBu):
        db = config()
        if bool(db):
            firebaseAuth = store._get("firebaseAuth")
            db.child(f"l500/{activedBu}/PRESENTER").set(
                pl500, token=firebaseAuth["idToken"]
            )


def setP300AfterStartStream(data):
    activedBu = store.getCurrentActiveBusiness()
    if bool(activedBu):
        db = config()
        if bool(db):
            firebaseAuth = store._get("firebaseAuth")
            db.child(f"l500/{activedBu}/P300").set(data, token=firebaseAuth["idToken"])

   
