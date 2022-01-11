from flask import Flask
from flask import request
import json
import trucksbook

app=Flask(__name__)

@app.route('/', methods=['GET','POST'])
def handle_request():
    text=str(request.args.get('input')) #requires ?input=a
    print(text)
    d={'/logbook?input=(player_id)':'get player monthly data','/company-employee?input=(compamy_id)':'get company data like members,position,player_id'}
    json_dump= json.dumps(d)
    return json_dump

@app.route('/logbook', methods=['GET','POST'])
def logbook():
    text=str(request.args.get('input')) #requires ?input=a
    print(text)
    d=trucksbook.logb(text)
    json_dump= json.dumps(d)
    return json_dump

@app.route('/company-employee', methods=['GET','POST'])
def company_employee():
    text=str(request.args.get('input')) #requires ?input=a
    print(text)
    d=trucksbook.company_employees(text)
    json_dump= json.dumps(d)
    return json_dump
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
