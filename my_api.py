from flask import Flask
from flask import request
import json
import trucksbook
from datetime import datetime
app=Flask(__name__)

@app.route('/', methods=['GET','POST'])
def handle_request():
    text=str(request.args.get('input')) #requires ?input=a
    print(text)
    d={'sitemap':{'/logbook?id=(player_id)&year=(year)&month=(month)':'get player monthly data','/company?id=(company_id)':'get company data like founder,members,position,player_id'},'author':'Ben X','emoji':':D'}
    json_dump= json.dumps(d)
    return json_dump

@app.route('/logbook', methods=['GET','POST'])
def logbook():
    args=[]
    id_  = request.args.get('id', None)
    year  = request.args.get('year', datetime.now().strftime('%Y'))
    month = request.args.get('month', datetime.now().strftime('%m'))
    #text=str(request.args.get('input')) #requires ?input=a
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

@app.route('/company', methods=['GET','POST'])
def company_members():
    text=str(request.args.get('input')) #requires ?input=a
    print(text)
    d=trucksbook.company(text)
    json_dump= json.dumps(d)
    return json_dump
if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0')
    except Exception as e:
        print(e)
