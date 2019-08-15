import sys
import hashlib
import re
import time


def createToken(input, keysIgnor=[]):
    try:
        if "token" in input:
            del input["token"]
        #
        input["v"] = "v1"
        input["keyToken"] = "Piepme2017"  #
        #
        sorted_key = sorted(input)

        def lambdaX(v):
            return f"{v}={input[v]}" if v not in keysIgnor else ""

        #
        maped_ls = map(lambdaX, sorted_key)
        paramStr = "&".join(list(maped_ls))
        #
        return hash_md5(paramStr)
    except:
        print(sys.exc_info())


def createTokenV2(input, isRecursive=False):
    try:
        if "token" in input:
            del input["token"]

        if isRecursive is False:
            input["v"] = "v1"
            input["keyToken"] = "Piepme2017"  #

        sorted_key = sorted(input)

        def lambdaX(v):
            return (
                f"{v}={input[v]}"
                if type(input[v]) is not dict
                else createTokenV2(input[v], True)
            )

        maped_ls = map(lambdaX, sorted_key)
        paramStr = "&".join(list(maped_ls))

        return paramStr if isRecursive else hash_md5(paramStr)
    except:
        print(sys.exc_info())


def createTokenV3(input, isRecursive=False):
    try:
        if "token" in input:
            del input["token"]

        if isRecursive is False:
            input["v"] = "v1"
            input["keyToken"] = "Piepme2017"
        sorted_key = sorted(input)

        # improve non-charater from v2
        def lambdaX(v):
            if type(input[v]) is not dict:
                after_regex = re.sub(r"[^a-zA-Z0-9]", "", str(input[v]))
                return f"{v}={after_regex}"
            else:
                return createTokenV3(input[v], True)

        maped_ls = map(lambdaX, sorted_key)
        paramStr = "&".join(list(maped_ls))
        #
        if not isRecursive:
            print(paramStr, "paramStr")
        return paramStr if isRecursive else hash_md5(paramStr)
    except:
        print(sys.exc_info())


def hash_md5_with_time(s):
    timestamp = time.time()
    return hash_md5(s + str(timestamp))


def hash_md5(s):
    s = s.encode("utf-8")
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()


# // ---------------------------------------------------------------------------------------------
# aesDecryptWithKey(cipherData, $key) {
#     try {//remove special character
#       if ($key === 'OFF') return cipherData
#       let rtVal = ''
#       if (!!cipherData) {
#         cipherData = cipherData.replace(/\n|\r|\t/g, "").replace(/ /g, '+')
#         const key = CryptoJS.enc.Utf8.parse($key),
#           decrypted = CryptoJS.AES.decrypt(cipherData, key, { iv: key })
#         try {
#           rtVal = decrypted.toString(CryptoJS.enc.Utf8)
#         } catch (err) {
#           if (err) rtVal = decrypted.toString()
#         }
#       }
#       return rtVal.trim()
#     } catch (error) {
#       console.log('-->cipherData', cipherData, '-->key', $key)
#       console.log('descrypt->', error)
#     }
#   }

#   aesEncryptWithKey(message, $key) {
#     if ($key === 'OFF')
#       return message
#     const key = CryptoJS.enc.Utf8.parse($key),
#       cipherData = CryptoJS.AES.encrypt(message, key, { iv: key })
#     return cipherData.toString()
#   }
# // ---------------------------------------------------------------------------------------------
# aesDecryptDef(cipherData) {
#     try {//remove special character
#       cipherData = cipherData.replace(/\n|\r|\t/g, "").replace(/ /g, '+')
#       const key = CryptoJS.enc.Utf8.parse(this.AES_KEY),
#         iv = CryptoJS.enc.Utf8.parse(this.AES_IV),
#         decrypted = CryptoJS.AES.decrypt(cipherData, key, { iv })
#       let rtVal = ''
#       try {
#         rtVal = decrypted.toString(CryptoJS.enc.Utf8)
#       } catch (err) {
#         if (err) rtVal = decrypted.toString()
#       }
#       return rtVal.trim()

#     } catch (error) {
#       console.log('-->cipherData', cipherData, '-->key', $key)
#       console.log('descrypt->', error)
#     }
#   }

#   aesEncryptDef(message) {
#     const key = CryptoJS.enc.Utf8.parse(this.AES_KEY),
#       iv = CryptoJS.enc.Utf8.parse(this.AES_IV),
#       cipherData = CryptoJS.AES.encrypt(message, key, { iv })
#     return cipherData.toString()
#   }
