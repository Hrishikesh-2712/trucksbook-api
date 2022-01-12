from flask import Flask
from flask import request
import json
import trucksbook

app=Flask(__name__)

@app.route('/')
def home_view():
    d={'/logbook?input=(player_id)':'get player monthly data','/company-employee?input=(compamy_id)':'get company data like members,position,player_id','author':'Ben X 🎄#8003'}
    json_dump= json.dumps(d)
    return json_dump

@app.route('/logbook', methods=['GET','POST'])
def logbook():
    text=str(request.args.get('input')) #requires ?input=a
    print(text)
    d=trucksbook.logb(text)
    json_dump= json.dumps(d)
    return json_dump

@app.route('/company, methods=['GET','POST'])
def company():
    text=str(request.args.get('input')) #requires ?input=a
    print(text)
    d=trucksbook.company(text)
    json_dump= json.dumps(d)
    return json_dump
if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(e)
