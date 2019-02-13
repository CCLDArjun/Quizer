# Quizer
Host an online quiz or Capture The Flag Competition with just python and some dependencies installed!

![Imgur](https://i.imgur.com/QTvaWDE.png) 

## Installation and Setup
1. Download Latest Release
2. Make a python virtualenv
```console
foo@bar:~$ cd CTF-Client
foo@bar:~$ apt install pip
foo@bar:~$ pip install virtualenv
foo@bar:~$ virtualenv env
foo@bar:~$ source env/bin/activate
```
3. Install
```console
foo@bar:~$ pip3 -r install requirments.txt
```
DO NOT run this scirpt ONCE users have signed up as it will clear them all, however run it while trying to install.
```console
foo@bar:~$ python3 install.py
```

4. Run the app!!
There are many ways to deploy this. `gunicorn` is recomended, make sure to run `run.py` and not `app.py`.

5. Setup Challenges and Admin
Once you have the website running, signup a new user named `admin`, and click on the Admin link on the top of the page, then go to create a challenge and enter info

## Features
1. Uses SQLite3 database instead of storing in memory
	1. User Management with hashed passwords
	2. Many To Many Relationship to keep track of solved challenges
2. Easily expandable as it uses blueprints
3. Admin Page Included
	1. Create your own Challenges
	2. Dynamic Scoring Challenges
	3. Support for file uploads
	4. Lots of Statistics 
4. Simple 
5. Protection against SQLi, Cross-Site Request Forgery and Cross-Site scripting 
