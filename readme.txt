#Libraries to be installed for successful app run
json, requests, geopy, sys, sqlite3, typer.

#Introduction
This application gives weather forecast of a specific city 
which can be chosen with latitude and longitude or by city name.
The available forecast is for next days which can be accessed with
by typing the date.

#How to make application run
after ensuring that dependencies are correctly installed,
one can type
1) python weather.py --help
it will access the set the arguments that can be entered.
The app can be accessed by following commands also,

:- python weather.py start
This command will start the application.

:- python weather.py createuser
This command will help you creater a user.

:- python weather.py login
This command will take you directly to the login page.

:- python weather.py deleteuser
This command will help you to delete a user.

#What makes it work
The apps works mainly with the help of openweathermap.org which helps you get
the weather data with api, which is received by python with the help 
of requests library.
Another api  was used that helps to get latitude and longitude when
city name is entered.  
The User creation, deletion and login is made with the help of sqlite 
database that comes with python
