from dbcon import table
from hostpinsms import *
from decouple import config
from dbcon import table

sms = sms()
sendBody = {
    "phoneNo" : "254743955713",
    "msg" : f"Niaje Boss wangu  I Believe You Have it"
}
response = sms.sendSMS(sendBody)
print(response)