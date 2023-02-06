import json,requests,uuid,math,datetime
from decouple import config
from dbcon import table

class sms:
    #initialize the HostPinacle Variables
    def __init__(self):
      self.HPApiKey = config('HPApiKey')
      self.HPUserID  = config('HPUserID')
      self.HPPassword = config('HPPassword')
      self.HPSenderID = config('HPSenderID')
    
    #This function is Called to Submit Outgoing Curl Requests
    def submit_request(self,url,postData):
      headers = {
          "apikey": self.HPApiKey,
          "cache-control": "no-cache",
          "Content-Type": "application/x-www-form-urlencoded",
        }
      response = requests.post(url, data=postData, headers=headers)
      return response
   
   #this Function is Called to Get the SMS Balance from HostPinnacle
    def getBalance(self):
      postData = {
        "userid" : self.HPUserID,
        "password" : self.HPPassword,
        "output" : "json"
      }
      response = requests.get(EndPoints('HPSMS.HP_ACCOUNTSTATUS'),params = postData)
      return response.text

   #This Function is called to Get Message Delivery Status From HostPinnacle
    def msgStatus(self,msgTransID):
      postData = {
        "userid" : self.HPUserID,
        "password" : self.HPPassword,
        "output" : "json",
        "uuid" : msgTransID
      }
      response = requests.get(EndPoints('HPSMS.HP_MSGSTATUS'),params = postData)
      return response.text
    
    #This Function is Called to Send SMS Message
    def sendSMS(self,sendBody):
      msgId = uuid.uuid1().time_low #Generate unique Message ID
      postData = {
        "userid" : self.HPUserID,
        "password" : self.HPPassword,
        "mobile" : sendBody["phoneNo"],
        "msg" : sendBody["msg"],
        "senderid" : self.HPSenderID,
        "msgType" : "text",
        "duplicatecheck" : "true",
        "sendMethod" : "quick",
        "output" : "json",
        "msgId" : msgId
      }
      db = table("sms_outbox_hostpins") # Initialize Table 
      smsUnits = len(sendBody["msg"]) / int(config('smsLength'))
      
      response = self.submit_request(EndPoints('HPSMS.HP_SENDSMS'),postData)
      response  = json.loads(response.text)
      msgItem = {
          'short_code' : self.HPSenderID,
          'phone' : sendBody["phoneNo"],
          'message' : sendBody["msg"],
          'msgid' :  msgId,
          'sms_length' : len(sendBody["msg"]),
          'sms_units'  : math.ceil(smsUnits),
          'transactionId'  : response["transactionId"],
          'send_status'  : response["status"],
          'statusCode'  : response["statusCode"],
          'reason'  : response["reason"],
          'response_message'  : response["reason"]
      }
      db.create(msgItem)
      return response
  
# This function is called to Get the Current Time
def now():
  curtime = datetime.datetime.now()
  return curtime.isoformat()

#Get End Point URLS EndPoints.json
def EndPoints(PointName):
  nodePoint = PointName.split('.')
  try:
      with open('EndPoints.json', 'r') as f:
            pointList = json.load(f)
  except KeyError:
        return False
  if nodePoint[0] in pointList:
      nodeList = pointList[nodePoint[0]]
      return nodeList[nodePoint[1]]
  else:
      return 'Invalid EndPoint'