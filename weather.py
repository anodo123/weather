import sqlite3
import requests
from geopy.geocoders import Nominatim
import sys
import json
import typer
import urllib.parse
import datetime
conn = sqlite3.connect("database.db")
conn.execute("""
CREATE TABLE IF NOT EXISTS ADMIN(
USERNAME TEXT NOT NULL, 
PASSWORD TEXT NOT NULL)
""")
conn.close()
app = typer.Typer()
def api_key():
    return str(input("please enter api key: "))
#api_key  = lambda x= str(input("please enter api key: ")):x
def display(x):
    r = {'-':"-----------------------------------",
         '*':"******************************",
         'again':'wrong input given please try again',
         'break': "Press 'CTRL+C' to exit application at any time",
         'exit':"Enter 1 to try again else enter any key to exit",
         'press1':'Enter 1 to try again',
         'else': 'else enter any key to exit',
         'terminated':'Program terminated'
         }
    return r[x]
def wronginput():
    print("{}\n     Program Terminated\n{}".format(display('-'),display('-')))
    return sys.exit()
def latlong():
        print("Enter Latitude and Longitude respectively seperated by spaces\n ")
        coordinates = list(map(str,input().split()))
        return ("https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,minutely&appid={}".format(coordinates[0],coordinates[1],api_key()))
def cityname():
        print("{}\n{}\nPlease enter City Name: ".format(display('*'),display('*')))
        address = str(input()).capitalize()
        try:
            url_construct = ('https://nominatim.openstreetmap.org/search/' + str(urllib.parse.quote(address)) +'?format=json')
            response = requests.get(url_construct).json()
        except:
            print("City name must be wrong")
            print("\n{} {}".format(display('press1'),display('else')))
            try:
                if(int(input()) == 1):
                    getforecast()
            except:
                print(display('terminated'))
                sys.exit()
        return ("https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=hourly,minutely&appid={}".format(response[0]["lat"],response[0]["lon"],api_key()))
def urladdress():
        choose_option = {'1':latlong, '2': cityname}
        try:
            base = choose_option[str(input("Press 1 to get forecast by latitude and longitude \nPress 2 to get forecast by cityname\nInput: "))]()
            return base
        except KeyError:
            print(display("again"))
            return urladdress()
def getdata(url):
        '''The function uses try and except to check to check whether data is recieved or not
           if error code is recieved try is executed else except block returns the data'''
        load = json.loads(requests.get(url).text) 
        try:
            load['cod']
            print("Wrong api key given\n")
            return wronginput()
        except KeyError:
            print("\nData Retrived Sucessfully")
            return load
def convert(timestamp):
        return  str(datetime.datetime.fromtimestamp(timestamp))          
def getforecast():
        data = getdata(urladdress())
        print("\nForecast is available for 7 days from current date")
        print("\nPlease choose date Carefully in 'YYYY-MM-DD' format\n")
        date = str(input())
        count=0
        for i in data['daily']:
            qw  = list(map(str,convert(timestamp = i['dt']).split()))
            if(str(qw[0]) == date):
                count+=1
                print("{}\n             Date: ".format(display('-')),qw[0])
                print("             Humidity: ", i['humidity'])
                print("             Pressure: ", i['pressure'])
                print('             temp average: ',i['temp']['day'])
                print("             Wind Speed: ", i['wind_speed'])
                print("             wind Degree ",i['wind_deg'])
                print("             UV index {}\n{}".format(i['uvi'],display('-')))
        if(count==0):
            print("\nWrong Date Entered\n")
        print("\nEnter 1 to get another forecast 2 to login {} ".format(display('else')))
        temp = str(input())
        if(temp == '1'):
            getforecast()
        if(temp == '2'):
            login()
        else:       
            return None    
@app.command()         
def login():
    print(display('break'))
    print('\n-----------LOGIN PAGE---------\n')
    name = str(input('Please enter the username: '))
    password = str(input('please enter the password: '))
    #applying empty validation
    if name=='' or password=='':
        print("fill the empty field!!!")
    else:
      #open database
      conn = sqlite3.connect('database.db')
      #select query
      cursor = conn.execute('SELECT USERNAME,PASSWORD FROM ADMIN WHERE USERNAME="%s" and PASSWORD="%s"'%(name,password))
      temp = cursor.fetchone()
      if(temp!=None):
         print("{}\n     Login success\n{}".format(display('-'),display('-')))
         conn.close()
         getforecast()
         
      else:
          print("Wrong username or password!!!\n")
          print("{} {}\n".format(display('press1'),display('else')))
          if(str(input("please give input: ")) == '1'):
              login()
          else:
              sys.exit()
@app.command()
def createuser():
    conn = sqlite3.connect('database.db')
    name = str(input('Please enter the username '))
    cursor = conn.execute('SELECT * from ADMIN where USERNAME="%s"'%(name))
    if(cursor.fetchone()):
        print('username already exists')
        print("{} enter 2 for login page {}".format(display('press1'),display('else')))
        given = str(input("please give input ")) 
        if(given == '1'):
            createuser()
        if(given == '2'):
            login()
        else:
            print("Thank You")
            return None    
    password =  str(input('please enter the password '))
    cpassword = str(input('please confirm the password '))
    if(password != cpassword):
        print("passwords do not match.....\n{}".format(display("terminated")))
        return None
    if(name=='' or password==''):
        print("field left empty!!!")
        createuser()
    else:
        conn.execute('insert into ADMIN (USERNAME, PASSWORD) VALUES ("%s","%s")'%(name,password))
        conn.commit()
        conn.close()
        print("{}\nAccount registered successfully".format(display('-')))
        print("Redirecting to login page\n{}".format(display('-')))
        login()
@app.command()
def deleteuser():
    name = str(input('Please enter the username: '))
    password = str(input('please enter the password: '))
    #applying empty validation
    if name=='' or password=='':
        print("fill the empty field!!!")
        deleteuser()
    else:
      #open database
      conn = sqlite3.connect('database.db')
      #select query
      cursor = conn.execute('SELECT USERNAME,PASSWORD FROM ADMIN WHERE USERNAME="%s" and PASSWORD="%s"'%(name,password))
      temp = cursor.fetchone()
      if(temp!=None):
         conn.execute('DELETE FROM ADMIN WHERE USERNAME="%s" and PASSWORD="%s"'%(name,password))
         conn.commit()
         conn.close()
         print("{}\nSUCCESSFULLY DELETED\n{}".format(display('-'),display('-')))
         return None
@app.command()
def start():
    print("\nPress 1 to Create User")
    print("Press 2 to Login")
    print("Press 3 to Delete user\n{}\n{}".format(display('-'),display('-')))        
    choose_start = {'1':createuser, '2':login,'3':deleteuser}
    try:
        choose_start[str(input('Enter your choice: '))]()              
    except KeyError:
        print(display("terminated"))
        wronginput()

if __name__ == "__main__":
    app()       
              