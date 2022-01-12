import requests
from bs4 import BeautifulSoup
import json
import re
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url='https://trucksbook.eu/components/notlogged/login.php'
with open('creds.json','r') as j:
    values=json.load(j)

#excell express company_id=144260

resp = requests.post(url, data=values)
if resp.status_code==200 and 'success' in str(resp.content):
    print(resp.content)
    with requests.Session() as sess:
        res=sess.post(url, data=values)
    def logb(playerid):
        #logbook
        res=sess.get(f'https://trucksbook.eu/logbook/{playerid}')
        if res.status_code==200:
            pass
        else:
            return 'error'
        soup=BeautifulSoup(res.text,'lxml')
        #player_monthly_data
        span=soup.find_all('div', class_='value')
        logbook=dict()
        def dd(f):
            digit=''
            f=''.join(f.split())
            for i in range(len(f)):
                if f[i].isdigit():
                    digit+=f[i]
            return digit

        def game(g):
            # euro or dollar
            if '€' in g:
                return 'Euro Truck Simulator 2'
            elif '$' in g:
                return 'American Truck Simulator'
            else:
                return 'Null'
        if len(span)==0:
            #game data
            logbook={'Euro Truck Simulator 2':{'Profit':'0',
                     'Driven Distance':'0',
                     'XP':'0',
                     'Fuel Cost':'0',
                     'Offences':'0',
                     'Cargo weight':'0'},
                     'American Truck Simulator':{'Profit':'0',
                     'Driven Distance':'0',
                     'XP':'0',
                     'Fuel Cost':'0',
                     'Offences':'0',
                     'Cargo weight':'0'}
                    }
            return {soup.find_all('div',class_='nick-card')[0].text:logbook}
        elif len(span)==6:
            #game data
            g=game(span[0].text)
            if 'Euro Truck Simulator 2' in g:
                g2='American Truck Simulator'
            elif 'American Truck Simulator' in g:
                g2='Euro Truck Simulator 2'
            else:
                g2='Null'
            
            logbook={game(span[0].text):{'Profit':dd(span[0].text),
                     'Driven Distance':dd(span[1].text),
                     'XP':dd(span[2].text),
                     'Fuel Cost':dd(span[3].text),
                     'Offences':dd(span[4].text),
                     'Cargo weight':dd(span[5].text)},
                     g2:{'Profit':'0',
                     'Driven Distance':'0',
                     'XP':'0',
                     'Fuel Cost':'0',
                     'Offences':'0',
                     'Cargo weight':'0'}}
            return {soup.find_all('div',class_='nick-card')[0].text:logbook}
            
        elif len(span)==12:
            logbook={game(span[0].text):{'Profit':dd(span[0].text),
                     'Driven Distance':dd(span[1].text),
                     'XP':dd(span[2].text),
                     'Fuel Cost':dd(span[3].text),
                     'Offences':dd(span[4].text),
                     'Cargo weight':dd(span[5].text)},
                     game(span[6].text):{'Profit':dd(span[6].text),
                     'Driven Distance':dd(span[7].text),
                     'XP':dd(span[8].text),
                     'Fuel Cost':dd(span[9].text),
                     'Offences':dd(span[10].text),
                     'Cargo weight':dd(span[11].text)}}
            return {soup.find_all('div',class_='nick-card')[0].text:logbook}
        else:
            pass
    def company(company_id):
        #returns name, position, trucksbook_player_id
        i=-1
        bd=''
        data={}
        members={}
        res=sess.get(f'https://trucksbook.eu/company/{company_id}')
        soup=BeautifulSoup(res.text,'lxml')
        company_name=soup.find_all('h4')[0].text.strip()
        founder=soup.find_all('div',class_='left')[0].text.strip()
        founder_id=soup.findAll('a', attrs={'href': re.compile("^https://trucksbook.eu/profile/")})[1].get('href').split('/')[-1]
        for s in soup.find_all('div',class_='profile-info-item'):
            b=''.join(s.text.strip().split('.'))
            if b.isdigit():
                bd=b
                break
        try:
            if 'The company was dissolved!' in soup.find_all('div',class_='alert alert-danger')[0].text:
                status='Closed'
                members['']=''
                i=-1
            else:
                pass
        except IndexError:
            status='Active'
            res=sess.get(f'https://trucksbook.eu/components/app/company/employee_list.php?id={company_id}')
            soup=BeautifulSoup(res.text,'lxml')
            players=soup.find_all('a', href=True, text=True)    
            positions=soup.find_all('td',class_="d-none d-sm-table-cell text-center")
            player_id=soup.findAll('a', attrs={'href': re.compile("^https://")})
            for i in range(len(players)):
                pl=''.join(players[i].text.split())
                pos=positions[i].text
                pid=player_id[i].get('href').split('/')[-1]
                members[pl]={'position':pos,'player_id':pid}
        data={'status':status,'company':{'name':company_name,'founder':founder,'founder_id':founder_id,'born':bd,'employee_count':i+1,'employees':members}}
        return data
