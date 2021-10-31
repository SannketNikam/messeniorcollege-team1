import requests as r
import sys

uid = sys.argv[1]
otp = sys.argv[2]
txnId = sys.argv[3]

dict = {
    "uid" : uid,
    "vid" : "",
    "txnId" : txnId,
    "otp" : otp
}
print(dict)