import sys
import requests as r
import uuid
import sys

txnId = uuid.uuid4().hex
with open('txnId','w') as f:
    f.write(txnId)
uid = sys.argv[1]

dict = {"uid": uid,
        "vid": "",
        "txnId" : txnId
}
req = r.post("https://stage1.uidai.gov.in/onlineekyc/getOtp/",json=dict)
print(req.content.decode())
