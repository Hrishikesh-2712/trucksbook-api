from flask import Flask
from flask import request
import json
import trucksbook
from datetime import datetime
app=Flask(__name__)

with open('api_key.json') as f:
    api_keys=json.load(f)

@app.route('/', methods=['GET','POST'])
def handle_request():
    appid=request.args.get('appid', None) #requires ?input=appid
    print('base',appid,type(appid))
    if appid in api_keys:
        print('requested by',api_keys[appid])
        d={'sitemap':{'/logbook?id=(player_id)&year=(year)&month=(month)&appid=(api_key)':'get player monthly data','/company?id=(company_id)&appid=(api_key)':'get company data like founder,members,position,player_id'},'author':'Ben X','emoji':':D'}
        json_dump= json.dumps(d)
        return json_dump
    else: return {"error":True, "message": "Invalid API key. Please contact author for details."}

@app.route('/logbook', methods=['GET','POST'])
def logbook():
    args=[]
    id_  = request.args.get('id', None)
    year  = request.args.get('year', datetime.now().strftime('%Y'))
    month = request.args.get('month', datetime.now().strftime('%m'))
    appid=request.args.get('appid', None) #requires ?input=appid
    print('logbook',appid)
    if appid in api_keys:
        print('requested by',api_keys[appid])
        if id_!=None and id_.isdigit(): 
            id_=str(abs(int(id_)))
            try:
                arg=''
                if id_:
                    arg+='/'+id_
                if year:
                    arg+='/'+year
                if month:
                    arg+='/'+month
                print(id_,year,month)
                print(arg)
                d=trucksbook.logb(arg)
                json_dump= json.dumps(d)
                return json_dump
            except Exception as e:
                print('----error----\n',e)
                return {"error":True, "message": "Invalid request"}
        else: return {"error":True, "message": "Invalid player id"}
    else: return {"error":True, "message": "Invalid API key. Please contact author for details."}

@app.route('/company', methods=['GET','POST'])
def company_members():
    id_=request.args.get('id', None) #requires ?id=a
    appid=request.args.get('appid', None) #requires ?input=appid
    print('company',appid)
    if appid in api_keys:
        print('requested by',api_keys[appid])
        if id_!=None and id_.isdigit(): 
            id_=abs(int(id_))
            d=trucksbook.company(id_)
            json_dump= json.dumps(d)
            return json_dump
        else: return {"error":True, "message": "Invalid company id"}
    else: return {"error":True, "message": "Invalid API key. Please contact author for details."}
if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0')
    except Exception as e:
        print('----error----\n',e)
