
import json
import webbrowser
from flask import Flask,render_template,request,redirect,url_for,make_response
from firebase import Firebase
from datetime import date
import random
import datetime
# import pdfkit
# path_wkhtmltopdf = 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'
# config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
app = Flask(__name__)
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


firebase = Firebase(config)
db = firebase.database()
def handle_catch(caller, on_exception):
    try:
         return caller()
    except:
         return on_exception

# Python3 code to remove whitespace
def remove_lower(string):
    return string.replace(" ", "").lower()

@app.route("/")
def main():
    return render_template("index.html")
@app.route('/WholeSellers',methods=['GET','POST'])
def WholeSellers():
    result = db.child("WholeSellers").get()
    return render_template('WholeSellers.html',result = result,handle_catch = handle_catch)
@app.route('/WholeSellerStocks',methods=['GET','POST'])
def WholeSellerStocks():
    result = db.child("WholeSellers").get()
    return render_template('WholeSellerStocks.html',result = result,handle_catch = handle_catch)
@app.route('/Customers',methods=['GET','POST'])
def Customers():
    return render_template('Customers.html',handle_catch = handle_catch)
@app.route('/NewTruckEntry',methods=['GET','POST'])
def NewTruckEntry():
    if request.method == 'POST':
        truck_no = request.form.get("truck_no")
        date_of_arrival = request.form.get("date_of_arrival")
        data = {
            "truck_no":remove_lower(truck_no),
            "is_wholeseller":0,
            'main_data':{
            'item':' ',
            'no_of_items': 0,
            'detail_items':{
                'trial':1
            },
         
        }
        }
        db.child("__NewTruckEntry__").child("in_stock").child(str(date_of_arrival)).push(data)
        truck_data = db.child("__NewTruckEntry__").child("in_stock").get().val()
        return render_template('NewTruckEntry.html',truck_data = truck_data,handle_catch = handle_catch)
    truck_data = db.child("__NewTruckEntry__").child("in_stock").get().val()
    return render_template('NewTruckEntry.html',truck_data = truck_data, handle_catch = handle_catch)


@app.route("/truck/<string:truck_date_uid>/<string:date>",methods=['GET','POST'])
def truck_date_uid(truck_date_uid,date):
    if request.method == 'POST':
        data = request.form.get('All_JSON_DATA')
        json_data = json.loads(data)
        WholeSellers = db.child("WholeSellers").get()
        mdata = db.child("__NewTruckEntry__").child("in_stock").child(date).child(truck_date_uid).get().val()
        if mdata is not None:
            db.child("__NewTruckEntry__").child("in_stock").child(date).child(truck_date_uid).child("main_data").update(json_data)
            truck_details = db.child("__NewTruckEntry__").child("in_stock").child(date).child(truck_date_uid).get().val()
            wholeseller_name = db.child("WholeSellers").child(truck_details['Wholeseller_uid']).child("name").get().val()
            products = db.child("__Products__").get().val()
            return render_template("Truck_Details.html",WholeSellers = WholeSellers,truck_date_uid = truck_date_uid,date =date,truck_details = truck_details,wholeseller_name = wholeseller_name,products=products,handle_catch = handle_catch)
        else:
            db.child("__NewTruckEntry__").child("out_of_stock").child(date).child(truck_date_uid).child("main_data").update(json_data)
            truck_details = db.child("__NewTruckEntry__").child("out_of_stock").child(date).child(truck_date_uid).get().val()
            wholeseller_name = db.child("WholeSellers").child(truck_details['Wholeseller_uid']).child("name").get().val()
            products = db.child("__Products__").get().val()
            return render_template("Truck_Details.html",WholeSellers = WholeSellers,truck_date_uid = truck_date_uid,date =date,truck_details = truck_details,wholeseller_name = wholeseller_name,products=products,handle_catch = handle_catch)


    WholeSellers = db.child("WholeSellers").get()
    truck_details = db.child("__NewTruckEntry__").child("in_stock").child(date).child(truck_date_uid).get().val()
    if truck_details is None:
        truck_details = db.child("__NewTruckEntry__").child("out_of_stock").child(date).child(truck_date_uid).get().val()
    if truck_details['is_wholeseller'] == 0:
        products = db.child("__Products__").get().val()
        return render_template("Truck_Details.html",WholeSellers = WholeSellers,truck_date_uid = truck_date_uid,date =date,truck_details = truck_details,products=products,handle_catch = handle_catch)
    else:
        wholeseller_name = db.child("WholeSellers").child(truck_details['Wholeseller_uid']).child("name").get().val()
        products = db.child("__Products__").get().val()
        return render_template("Truck_Details.html",WholeSellers = WholeSellers,truck_date_uid = truck_date_uid,date =date,truck_details = truck_details,wholeseller_name = wholeseller_name,products=products,handle_catch = handle_catch)


@app.route("/addwholsellertoTruck",methods=['GET','POST'])
def addwholsellertoTruck():
    if request.method == 'POST':
        Wholeseller_uid = request.form.get("Wholeseller_uid")
        date = request.form.get("date")
        truck_date_uid = request.form.get("truck_date_uid")
        truck_no = request.form.get("truck_no")
        #Creating new bijak after wholseller is added to the truck
        bijak_no = random.randint(1000000, 9999999)
        # today = date.today()
        data = {
        'is_ledger':0,
        'visible_name':f"{remove_lower(truck_no)}-({date})-({bijak_no})",
        'bijak_no':bijak_no,
        'ledger_key':"",
        'transaction_key':"",
        'main_data':{
            'date_of_issue':date,
            'item':' ',
            'no_of_items': 0,
            'truck_no':remove_lower(truck_no),
            'where_from':' ',
            'where_to':' ',
            'detail_items':{
                'trial':1
            },
            'other_details':{
            'truck_loading':0,
            'labour':0,
            'khali_bardan':0,
            'loading':0,
            'chhatai':0,
            'kanta':0,
            'tel_postage':0,
            'phone':0,
            'commission':0,
            'hard_cash':0,
            'draft_cash':0,
            'exp':0
            }
        }
}

        new_bijak = db.child("WholeSellers").child(Wholeseller_uid).child("__Bijaks__").push(data)
        trucknodeData = {
            "uid":Wholeseller_uid,
            "bijak_key":new_bijak['name']
        }
        today = datetime.date.today()
        datenodeData = {
            "uid":Wholeseller_uid,
            "bijak_key":new_bijak['name']
        }
        db.child("__TruckNumbers__").child(remove_lower(truck_no)).push(trucknodeData)
        db.child("__Dates__").child(str(today.year)).push(datenodeData)
        db.child("__NewTruckEntry__").child("in_stock").child(date).child(truck_date_uid).update({
            'Wholeseller_uid':str(Wholeseller_uid),
            'is_wholeseller':1,
            'bijak_uid':new_bijak['name']
        })
        return redirect(url_for('truck_date_uid',truck_date_uid = truck_date_uid,date = date))

@app.route('/new_wholeseller',methods = ['POST'])
def add_wholeseller():
    if request.method == 'POST':
        name_wholeseller = request.form.get('wholeseller_name')
        db.child("WholeSellers").push({
            'name':name_wholeseller
        })
        result = db.child("WholeSellers").get()
        return render_template('WholeSellers.html',result = result,handle_catch = handle_catch)
        # return redirect(url_for('start'))
@app.route('/<string:wholseller_uid>')
def detail(wholseller_uid):
    name = db.child("WholeSellers").child(wholseller_uid).get().val()['name']
    bijaks_list = db.child("WholeSellers").child(wholseller_uid).child('__Bijaks__').get()
    ledgers_list = db.child("WholeSellers").child(wholseller_uid).child('__Ledgers__').get()
    return render_template('WholeSellerDetail.html',name = name,uid = wholseller_uid,list_bijaks = bijaks_list,ledgers_list=ledgers_list,  handle_catch = handle_catch)

@app.route('/<string:uid>/new-ledger',methods = ['POST'])
def new_ledger(uid):
    if request.method == 'POST':
        today = date.today()
        ledger_no = random.randint(1000, 9999)
        cur_year = str(today).split('-')[0]
        data = {
            'visible_name':f"ledger : {cur_year}-({today})-({ledger_no})"
        }
        db.child("WholeSellers").child(uid).child("__Ledgers__").push(data)
        return redirect(url_for('detail',wholseller_uid = uid))

@app.route('/<string:uid>/new-bijak',methods = ['POST'])
def new_bijak(uid):
    if request.method == 'POST':
        bijak_no = random.randint(1000000, 9999999)
        # today = date.today()
        truck_no = request.form.get('bijak_truck_no')
        date = request.form.get('bijak_date_of_issue')
        data = {
        'is_ledger':0,
        'is_paid':0,
        'is_paid'
        'visible_name':f"{remove_lower(truck_no)}-({date})-({bijak_no})",
        'bijak_no':bijak_no,
        'ledger_key':"",
        'transaction_key':"",
        'main_data':{
            'date_of_issue':date,
            'item':' ',
            'no_of_items': 0,
            'truck_no':remove_lower(truck_no),
            'where_from':' ',
            'where_to':' ',
            'detail_items':{
                'trial':1
            },
            'other_details':{
            'truck_loading':0,
            'labour':0,
            'khali_bardan':0,
            'loading':0,
            'chhatai':0,
            'kanta':0,
            'tel_postage':0,
            'phone':0,
            'commission':0,
            'hard_cash':0,
            'draft_cash':0,
            'exp':0
            }
        }
}

    new_bijak = db.child("WholeSellers").child(uid).child("__Bijaks__").push(data)
    trucknodeData = {
         "uid":uid,
         "bijak_key":new_bijak['name']
    }
    today = datetime.date.today()
    datenodeData = {
         "uid":uid,
         "bijak_key":new_bijak['name']
    }
    db.child("__TruckNumbers__").child(remove_lower(truck_no)).push(trucknodeData)
    db.child("__Dates__").child(str(today.year)).push(datenodeData)
    return redirect(url_for('detail',wholseller_uid = uid))

@app.route("/deleteBijak",methods=['POST'])
def deleteBijak():
    if request.method == 'POST':
        bijak_key = request.form.get("bijak_key")
        uid = request.form.get("uid")
        ledger_key = db.child("WholeSellers").child(uid).child('__Bijaks__').child(bijak_key).child('ledger_key').get().val()
        transaction_key = db.child("WholeSellers").child(uid).child('__Bijaks__').child(bijak_key).child('transaction_key').get().val()
        db.child("WholeSellers").child(uid).child('__Ledgers__').child(ledger_key).child("debit_transactions").child(transaction_key).remove()
        db.child("WholeSellers").child(uid).child('__Bijaks__').child(bijak_key).remove()
        return redirect(url_for('detail',wholseller_uid = uid))


@app.route("/deleteMemo",methods = ['POST'])
def deleteMemo():
    if request.method == 'POST':
        customer_uid = request.form.get("customer_uid")
        memo_key = request.form.get("memo_key")
        all_memo_items = db.child("Customers").child("__credit__").child(customer_uid).child("__Memos__").child(memo_key).child("main_data").child("detail_items").get().val()
        for key,value in all_memo_items.items():
            if (type(value) is dict):
                truck_specifics = value['truck_specifics'].split("-->")
                date = truck_specifics[0]
                truck_key = truck_specifics[1]
                db.child("__NewTruckEntry__").child("in_stock").child(date).child(truck_key).child("sold_data").child("__credit__").child(key).remove()
            else:
                pass
        db.child("Customers").child("__credit__").child(customer_uid).child("__Memos__").child(memo_key).remove()
        return redirect(url_for('cutsomerCredit',customer_uid = customer_uid))




@app.route('/<string:uid>/bijak/<string:bijak_key>',methods = ['GET','POST'])
def load_bijak(uid,bijak_key):
    if request.method == 'POST':
        data = request.form.get('All_JSON_DATA')
        json_data = json.loads(data)
        bijak_no =  db.child("WholeSellers").child(uid).child("__Bijaks__").child(bijak_key).child('bijak_no').get().val()
        visible_name = f"{json_data['truck_no']}-({json_data['date_of_issue']})-({bijak_no})"
        db.child("WholeSellers").child(uid).child("__Bijaks__").child(bijak_key).update({
            'visible_name':visible_name
        })
        db.child("WholeSellers").child(uid).child("__Bijaks__").child(bijak_key).child("main_data").update(json_data)
        bijak_details = db.child("WholeSellers").child(uid).child("__Bijaks__").child(bijak_key).get().val()
        if(bijak_details['transaction_key']==""):
            transaction_key = db.child("WholeSellers").child(uid).child("__Ledgers__").child(bijak_details['ledger_key']).child('debit_transactions').push({
                'bijak_no':bijak_details['bijak_no'],
                'bijak_key':bijak_key,
                'amount':bijak_details['main_data']['total_amount']
            })
            db.child("WholeSellers").child(uid).child("__Bijaks__").child(bijak_key).update({
                'transaction_key':transaction_key['name']
            })
        else:
            db.child("WholeSellers").child(uid).child("__Ledgers__").child(bijak_details['ledger_key']).child('debit_transactions').child(bijak_details['transaction_key']).update({
                'amount':bijak_details['main_data']['total_amount']
            })
        name_of_bijak_holder = db.child("WholeSellers").child(uid).get().val()['name']
        ledgers_list = db.child("WholeSellers").child(uid).child("__Ledgers__").get()
        settings_data = db.child("Settings_Wholeseller").get().val()
        products = db.child("__Products__").get().val()
        return render_template('WholeSellerBijak.html',bijak_details = bijak_details,name = name_of_bijak_holder,bijak_key=bijak_key,uid = uid,settings_data =settings_data,ledgers_list=ledgers_list,products=products,handle_catch = handle_catch)
    bijak_details = db.child("WholeSellers").child(uid).child("__Bijaks__").child(bijak_key).get().val()
    name_of_bijak_holder = db.child("WholeSellers").child(uid).get().val()['name']
    settings_data = db.child("Settings_Wholeseller").get().val()
    ledgers_list = db.child("WholeSellers").child(uid).child("__Ledgers__").get()
    products = db.child("__Products__").get().val()
    return render_template('WholeSellerBijak.html',bijak_details = bijak_details,name = name_of_bijak_holder,bijak_key=bijak_key,uid = uid,settings_data=settings_data,ledgers_list=ledgers_list,products=products,handle_catch = handle_catch)

@app.route('/<string:customer_uid>/memo/<string:memo_key>',methods = ['GET','POST'])
def load_memo(customer_uid,memo_key):
    if request.method == 'POST':
        data = request.form.get('All_JSON_DATA')
        json_data = json.loads(data)
        memo_no =  db.child("Customers").child('__credit__').child(customer_uid).child("__Memos__").child(memo_key).child('memo_no').get().val()
        ###Code for adding the truck sold items from memeo to wholeseller stock
        for k,v in json_data['detail_items'].items():
            if (type(v) is dict):
                specifics = v['truck_specifics'].split("-->")
                key = specifics[0]
                truck_key = specifics[1]
                v['customer_uid'] = str(customer_uid)
                v['memo_key'] = str(memo_key)
                v['customer_name'] = db.child("Customers").child('__credit__').child(customer_uid).child("name").get().val()
                db.child("__NewTruckEntry__").child("in_stock").child(key).child(truck_key).child("sold_data").child("__credit__").child(k).set(v)

                #check for out of stock
                total = 0
                total_data = db.child("__NewTruckEntry__").child("in_stock").child(key).child(truck_key).get().val()
                total_no_of_items = int(total_data['main_data']['no_of_items'])
                sold_data = total_data['sold_data']
                if('__credit__' in sold_data.keys()):
                    for k,v in sold_data['__credit__'].items():
                        total+=int(v['quantity'])
                if('__cash__' in sold_data.keys()):
                    for k,v in sold_data['__cash__'].items():
                        total+=int(v['quantity'])
                if total >= total_no_of_items:
                    db.child("__NewTruckEntry__").child("out_of_stock").child(key).child(truck_key).set(total_data)
                    db.child("__NewTruckEntry__").child("in_stock").child(key).child(truck_key).remove()
                else:
                    pass

            else:
                pass
        db.child("Customers").child('__credit__').child(customer_uid).child("__Memos__").child(memo_key).child("main_data").update(json_data)
        memo_details = db.child("Customers").child('__credit__').child(customer_uid).child("__Memos__").child(memo_key).get().val()
        if(memo_details['transaction_key']==""):
            transaction_key = db.child("Customers").child('__credit__').child(customer_uid).child("__Ledgers__").child(memo_details['ledger_key']).child('debit_transactions').push({
                'memo_no':memo_details['memo_no'],
                'memo_key':memo_key,
                'amount':memo_details['main_data']['total_amount']
            })
            db.child("Customers").child('__credit__').child(customer_uid).child("__Memos__").child(memo_key).update({
                'transaction_key':transaction_key['name']
            })
        else:
            db.child("Customers").child('__credit__').child(customer_uid).child("__Ledgers__").child(memo_details['ledger_key']).child('debit_transactions').child(memo_details['transaction_key']).update({
                'amount':memo_details['main_data']['total_amount']
            })
        name_of_memo_holder = db.child("Customers").child('__credit__').child(customer_uid).get().val()['name']
        ledgers_list = db.child("Customers").child('__credit__').child(customer_uid).child("__Ledgers__").get()
        new_truck_lists = db.child("__NewTruckEntry__").child("in_stock").get()
        products = db.child("__Products__").get().val()
        return render_template('CreditCustomerMemo.html',memo_details = memo_details,name = name_of_memo_holder,memo_key=memo_key,customer_uid = customer_uid,ledgers_list=ledgers_list,new_truck_lists = new_truck_lists,products=products,handle_catch = handle_catch)
    memo_details = db.child("Customers").child('__credit__').child(customer_uid).child("__Memos__").child(memo_key).get().val()
    name_of_memo_holder = db.child("Customers").child('__credit__').child(customer_uid).get().val()['name']
    ledgers_list = db.child("Customers").child('__credit__').child(customer_uid).child("__Ledgers__").get()
    new_truck_lists = db.child("__NewTruckEntry__").child("in_stock").get()
    products = db.child("__Products__").get().val()
    return render_template('CreditCustomerMemo.html',memo_details = memo_details,name = name_of_memo_holder,memo_key=memo_key,customer_uid = customer_uid,ledgers_list=ledgers_list,new_truck_lists = new_truck_lists,products=products,handle_catch = handle_catch)

@app.route('/<string:uid>/ledger/<string:ledger_key>',methods = ['GET','POST'])
def load_ledger(uid,ledger_key):
    name_of_ledger_holder = db.child("WholeSellers").child(uid).get().val()['name']
    ledger_details = db.child("WholeSellers").child(uid).child("__Ledgers__").child(ledger_key).get().val()
    return render_template('WholeSellerLedger.html',ledger_key=ledger_key,uid = uid,name = name_of_ledger_holder,ledger_details=ledger_details,handle_catch=handle_catch)

@app.route('/<string:customer_uid>/credit_ledger/<string:ledger_key>',methods = ['GET','POST'])
def load_credit_ledger(customer_uid,ledger_key):
    name_of_ledger_holder = db.child("Customers").child('__credit__').child(customer_uid).get().val()['name']
    ledger_details = db.child("Customers").child('__credit__').child(customer_uid).child("__Ledgers__").child(ledger_key).get().val()
    return render_template('CreditCustomerLedger.html',ledger_key=ledger_key,customer_uid = customer_uid,name = name_of_ledger_holder,ledger_details=ledger_details,handle_catch=handle_catch)

@app.route('/<string:uid>/add-credit/<string:ledger_key>',methods = ['POST'])
def add_credit_ledger(uid,ledger_key):
    amount_paid = request.form.get('amount_paid')
    account_no = request.form.get('account_no')
    data = {
        'amount_paid':amount_paid,
        'account_no':account_no

    }
    db.child("WholeSellers").child(uid).child("__Ledgers__").child(ledger_key).child("credit_transactions").push(data)
    return redirect(url_for('load_ledger',uid = uid,ledger_key = ledger_key))

@app.route('/<string:customer_uid>/add-credit-customer/<string:ledger_key>',methods = ['POST'])
def add_credit_ledger_customer(customer_uid,ledger_key):
    amount_paid = request.form.get('amount_paid')
    account_no = request.form.get('account_no')
    date_of_credit = request.form.get('date_of_credit')
    data = {
        'amount_paid':amount_paid,
        'account_no':account_no,
        "date_of_credit":date_of_credit

    }
    db.child("Customers").child('__credit__').child(customer_uid).child("__Ledgers__").child(ledger_key).child("credit_transactions").push(data)
    return redirect(url_for('load_credit_ledger',customer_uid = customer_uid,ledger_key = ledger_key))

@app.route("/delete_credit",methods=['POST'])
def delete_credit():
    if request.method == 'POST':
        credit_push_key = request.form.get("credit_push_key")
        uid = request.form.get("uid")
        ledger_key = request.form.get("ledger_key")
        db.child("WholeSellers").child(uid).child("__Ledgers__").child(ledger_key).child("credit_transactions").child(credit_push_key).remove()
        db.child("WholeSellers").child(uid).child("__Ledgers__").child(ledger_key).child("credit_transactions").child(credit_push_key).remove()
        return redirect(url_for('load_ledger',uid = uid,ledger_key = ledger_key))


@app.route('/<string:uid>/ledger-change/<string:bijak_key>',methods = ['POST'])
def ledger_connection_change(uid,bijak_key):
    if request.method == 'POST':
        ledger_id = request.form.get("ledger_ID")
        db.child("WholeSellers").child(uid).child("__Bijaks__").child(bijak_key).update({
            'ledger_key':str(ledger_id),
            'is_ledger':1
        })
        return redirect(url_for('load_bijak',uid = uid,bijak_key = bijak_key))

@app.route('/<string:customer_uid>/ledger-change-customer/<string:memo_key>',methods = ['POST'])
def ledger_connection_change_customer(customer_uid,memo_key):
    if request.method == 'POST':
        ledger_id = request.form.get("ledger_ID")
        db.child("Customers").child('__credit__').child(customer_uid).child('__Memos__').child(memo_key).update({
            'ledger_key':str(ledger_id),
            'is_ledger':1
        })
        return redirect(url_for('load_memo',customer_uid = customer_uid,memo_key = memo_key))
    
@app.route("/customercreditAccount",methods=['GET','POST'])
def customercreditAccount():
    customercreditdetails =  db.child("Customers").child('__credit__').get()
    return render_template("customercreditAccount.html",customercreditdetails = customercreditdetails,handle_catch = handle_catch)

@app.route("/cutsomerCredit/<string:customer_uid>",methods=['GET','POST'])
def cutsomerCredit(customer_uid):
    name = db.child("Customers").child('__credit__').child(customer_uid).get().val()['name']
    memos_list = db.child("Customers").child('__credit__').child(customer_uid).child('__Memos__').get()
    ledgers_list = db.child("Customers").child('__credit__').child(customer_uid).child('__Ledgers__').get()
    return render_template("customercreditDetails.html",name = name,ledgers_list = ledgers_list,memos_list = memos_list,customer_uid = customer_uid,handle_catch = handle_catch)

@app.route("/<string:customer_uid>/newCustomerCreditLedger",methods=['POST'])
def newCustomerCreditLedger(customer_uid):
    if request.method == 'POST':
        today = date.today()
        ledger_no = random.randint(1000, 9999)
        cur_year = str(today).split('-')[0]
        data = {
            'visible_name':f"ledger : {cur_year}-({today})-({ledger_no})"
        }
        db.child("Customers").child('__credit__').child(customer_uid).child("__Ledgers__").push(data)
        return redirect(url_for('cutsomerCredit',customer_uid = customer_uid))

@app.route("/<string:customer_uid>/newCustomerCreditMemo",methods=['POST'])
def newCustomerCreditMemo(customer_uid):
    if request.method == 'POST':
        memo_no = random.randint(1000000, 9999999)
        date = request.form.get('memo_date_of_issue')
        data = {
        'is_ledger':0,
        'visible_name':f"({date})-({memo_no})",
        'memo_no':memo_no,
        'ledger_key':"",
        'transaction_key':"",
        'main_data':{
            'address':"",
            'date_of_issue':date,
            'item':' ',
            'no_of_items': 0,
            'detail_items':{
                'trial':1
            },
        'other_details':{
            'hamaali':0
            }
        }
}

    new_memo = db.child("Customers").child('__credit__').child(customer_uid).child("__Memos__").push(data)
    return redirect(url_for('cutsomerCredit',customer_uid = customer_uid))

@app.route("/customercashAccount",methods=['GET','POST'])
def customercashAccount():
    cashMemoLists = db.child("Customers").child("__cash__").get()
    return render_template("customercashAccount.html",cashMemoLists=cashMemoLists,handle_catch = handle_catch)

@app.route("/cashMemo/<string:cash_memo_key>",methods=['GET','POST'])
def loadcashMemo(cash_memo_key):
    if request.method == 'POST':
        data = request.form.get('All_JSON_DATA')
        json_data = json.loads(data)
        memo_no =   db.child("Customers").child('__cash__').child(cash_memo_key).child('memo_no').get().val()
        ###Code for adding the truck sold items from memeo to wholeseller stock
        for k,v in json_data['detail_items'].items():
            if (type(v) is dict):
                specifics = v['truck_specifics'].split("-->")
                key = specifics[0]
                truck_key = specifics[1]
                v['customer_name'] = db.child("Customers").child("__cash__").child(cash_memo_key).child("name").get().val()
                v['cash_memo_key'] = cash_memo_key
                db.child("__NewTruckEntry__").child("in_stock").child(key).child(truck_key).child("sold_data").child("__cash__").child(k).set(v)
                #check for out of stock
                total = 0
                total_data = db.child("__NewTruckEntry__").child("in_stock").child(key).child(truck_key).get().val()
                total_no_of_items = int(total_data['main_data']['no_of_items'])
                sold_data = total_data['sold_data']
                if('__credit__' in sold_data.keys()):
                    for k,v in sold_data['__credit__'].items():
                        total+=int(v['quantity'])
                if('__cash__' in sold_data.keys()):
                    for k,v in sold_data['__cash__'].items():
                        total+=int(v['quantity'])
                if total >= total_no_of_items:
                    db.child("__NewTruckEntry__").child("out_of_stock").child(key).child(truck_key).set(total_data)
                    db.child("__NewTruckEntry__").child("in_stock").child(key).child(truck_key).remove()
                else:
                    pass


            else:
                pass
        db.child("Customers").child('__cash__').child(cash_memo_key).update({
            'is_filled':1
        })
        db.child("Customers").child('__cash__').child(cash_memo_key).child("main_data").update(json_data)


        memo_details = db.child("Customers").child('__cash__').child(cash_memo_key).get().val()
        name_of_memo_holder = db.child("Customers").child('__cash__').child(cash_memo_key).get().val()['name']
        # ledgers_list = db.child("Customers").child('__credit__').child(customer_uid).child("__Ledgers__").get()
        new_truck_lists = db.child("__NewTruckEntry__").child("in_stock").get()
        products = db.child("__Products__").get().val()
        return render_template('cashMemo.html',memo_details = memo_details,name = name_of_memo_holder,memo_key=cash_memo_key,customer_uid = "customer_uid",ledgers_list='ledgers_list',new_truck_lists = new_truck_lists,products=products,handle_catch = handle_catch)

    memo_details = db.child("Customers").child('__cash__').child(cash_memo_key).get().val()
    name_of_memo_holder = db.child("Customers").child('__cash__').child(cash_memo_key).get().val()['name']
    # ledgers_list = db.child("Customers").child('__credit__').child(customer_uid).child("__Ledgers__").get()
    new_truck_lists = db.child("__NewTruckEntry__").child("in_stock").get()
    products = db.child("__Products__").get().val()
    return render_template('cashMemo.html',memo_details = memo_details,name = name_of_memo_holder,memo_key=cash_memo_key,customer_uid = "customer_uid",ledgers_list='ledgers_list',new_truck_lists = new_truck_lists,products=products,handle_catch = handle_catch)


@app.route("/new_credit_customer",methods=['GET','POST'])
def new_credit_customer():
    customer_name = request.form.get("customer_name")
    data = {
        'name':customer_name
    }
    db.child("Customers").child('__credit__').push(data)
    return redirect(url_for('customercreditAccount'))

@app.route("/new_cash_customer",methods=['GET','POST'])
def new_cash_customer():
    customer_name = request.form.get("customer_name")
    date = request.form.get('memo_date_of_issue')
    memo_no = random.randint(1000000, 9999999)
    data = {
    'name':customer_name,
    'is_filled':0,
    'visible_name':f"({date})-({memo_no})",
    'memo_no':memo_no,
    'ledger_key':"",
    'transaction_key':"",
    'main_data':{
        'address':"",
        'date_of_issue':date,
        'item':' ',
        'no_of_items': 0,
        'detail_items':{
            'trial':1
        },
    'other_details':{
        'hamaali':0
        }
    }
}

    db.child("Customers").child('__cash__').push(data)
    return redirect(url_for('customercashAccount'))

@app.route('/settings',methods = ['GET','POST'])
def settings():
    if request.method == 'POST':
        percen_comm_Load = request.form.get('percen_comm_Load')
        percen_comm_Comm = request.form.get('percen_comm_Comm')
        data = {
            'percen_comm_Load':percen_comm_Load,
            'percen_comm_Comm':percen_comm_Comm
        }
        db.child("Settings_Wholeseller").set(data)
        products = db.child("__Products__").get().val()
        return render_template('WholeSellerSettings.html',data = data,products = products,handle_catch = handle_catch)
    products = db.child("__Products__").get().val()
    data = db.child("Settings_Wholeseller").get().val()
    return render_template('WholeSellerSettings.html',data = data,products = products,handle_catch = handle_catch)

@app.route("/addProducts",methods=['POST'])
def addProducts():
    if request.method == 'POST':
        all_data = dict(request.form)
        db.child("__Products__").set(all_data)
        # return all_data
        return redirect(url_for('settings'))

@app.route("/mbsa",methods = ['GET','POST'])
def mbsa():
    data = db.child("__NewTruckEntry__").child("in_stock").child("2022-12-19").child("-NJfGVctm-wGP-x_ka7i").get().val()
    return str(data)
# @app.route("/givepdf/<string:name>/<string:occ>",methods = ['GET','POST'])
# def pdf(name,occ):
#     rendered = render_template("bill.html",name = name,occ = occ)
#     pdf = pdfkit.from_string(rendered,False)
#     response = make_response(pdf)
#     response.headers['Content-type'] = 'application/pdf'
#     response.headers['Content-disposition'] = 'inline; filename=output.pdf'
#     return response
if __name__ == '__main__':
    # webbrowser.open('http://localhost:5500')
    app.run(debug=True,port=5500)