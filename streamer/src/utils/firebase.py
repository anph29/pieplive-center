from .pyrebase import pyrebase
from . import store 
from requests.exceptions import HTTPError
from src.models import N100_model
from src.constants import WS
from src.modules.login import Login

def getFirebase():
    return pyrebase.initialize_app({
        "apiKey": "AIzaSyCMSM_EJFrQ9K8zb6FFDtonppI_zOI1YZc",
        "authDomain":  "piepme-161803.firebaseapp.com",
        "databaseURL": "https://piepme-161803.firebaseio.com",
        "storageBucket": "piepme-161803.appspot.com",
        # "serviceAccount": "path/to/serviceAccountCredentials.json"
    })

def config():
    try:
        firebase = getFirebase()
        auth = firebase.auth()
        faketoken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJodHRwczovL2lkZW50aXR5dG9vbGtpdC5nb29nbGVhcGlzLmNvbS9nb29nbGUuaWRlbnRpdHkuaWRlbnRpdHl0b29sa2l0LnYxLklkZW50aXR5VG9vbGtpdCIsImlhdCI6MTU2Mzk2NTY1OSwiZXhwIjoxNTYzOTY5MjU5LCJpc3MiOiJmaXJlYmFzZS1hZG1pbnNkay1zMHJlY0BwaWVwbWUtMTYxODAzLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwic3ViIjoiZmlyZWJhc2UtYWRtaW5zZGstczByZWNAcGllcG1lLTE2MTgwMy5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsInVpZCI6IntcIkZPMTAwXCI6NDAzM30ifQ.WxN_PBGyrB3lFvF_5B2ZcyqWCLSPV0dmgy-jqbi0S5Kmp1AMeTeX3c_ud38oZFKEt6C31gHYBK4nwhmAowJg0aPsEgr0ZWstSHC6JCRaYQAKZLibk2U-BlSq-FL71y9-Yclx1vJyMb30hkNVd6PB1BzfLSSc7WYmy0aJ3QKEUJGqLjaaW1_p9eOF3gA_vYSt8oOVbRNwtZR4vC5se7RG-zpXmCHyjYvVdMTNiLUPIxb4zsFq0D9ISEI_CneSfzgto5nMF73HjhDIdn8Ek6uq3csfzhEgvT5ibm_5nGmlkyoReQY4T48J5HbyHmpKL4mEXT6k8Vv9A1pBH3C7YvT9Xw'
        authen = auth.sign_in_with_custom_token(store._get('tokenfb'))
        store._set('firebaseAuth', authen)
        return firebase.database()
    except HTTPError as e:
        # print(e, '--firebase error--')
        return refreshToken()

def refreshToken():
    try:
        firebase = getFirebase()
        auth = firebase.auth()
        res = getTokenFromSession()
        store._set('tokenfb', res['tokenfb'])
        authen = auth.sign_in_with_custom_token(res['tokenfb'])
        store._set('firebaseAuth', authen)
        return firebase.database()
    except:
        login = Login()
        login.logout()

def getTokenFromSession():
    n100 = N100_model()
    res = n100.f5fb_login_viewer({
        'NV117': store._get('NV117'), # PiepMeID
        'NV125': store._get('NV125'), # Token
        'LOGIN': store._get('NV101')
    })

    if res[WS.STATUS] == WS.SUCCESS:
        if res[WS.ELEMENTS] == -3:
            login = Login()
            login.logout()
            return None
        else:
            return res[WS.ELEMENTS]

