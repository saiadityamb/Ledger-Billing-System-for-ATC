from firebase import Firebase
config = {
 "apiKey": "AIzaSyC2mR0apOvm8V-P2Rx-JVpPRNuv9Zt_ipw",
  "authDomain": "ashish-trading-company.firebaseapp.com",
  "databaseURL": "https://ashish-trading-company-default-rtdb.firebaseio.com",
  "projectId": "ashish-trading-company",
  "storageBucket": "ashish-trading-company.appspot.com",
  "messagingSenderId": "962173488570",
  "appId": "1:962173488570:web:cb96903e29df15a06de183",
  'measurementId': "G-FDTF6ZDJEZ"
 }

def noquote(s):
    return s
firebase = Firebase(config)
db = firebase.database()

# bhai = ['sai','shikhar','om','parth','srujana','siddh','devesh']
# for i in bhai:
#     data = {
#         "name":i
#     }
#     db.child("Users").push(data)

mbsa = db.child("Users").order_by_child("name").limit_to_first(3).get()
print(mbsa.val())