# Quizer
Host an online quiz or Capture The Flag Competition with just python and some dependencies installed!

![Imgur](https://i.imgur.com/QTvaWDE.png) 

## Installation and Setup
1. Download Latest Release
2. Install Dependencies
```console
foo@bar:~$ pip3 -r install requirments.txt
```
DO NOT run this scirpt ONCE users have signed up as it will clear them all, however run initially.
```console
foo@bar:~$ python3 install.py
```

3. Run the app!!
There are many ways to deploy this. `gunicorn` is recomended, make sure to run `run.py` and not `app.py`.

4. Setup Challenges and Admin
Once you have the website running, signup a new user named `admin`, and click on the Admin link on the top of the page, then go to create a challenge and enter info

## Features
1. Uses SQLite3 database 
2. Admin Page Included
	1. Create your own Challenges
	2. Dynamic Scoring Challenges
	3. Support for file uploads
	4. Stats
3. Protection against SQLi, Cross-Site Request Forgery and Cross-Site scripting 

## More Images!!

![Imgur](https://i.imgur.com/JJMAUHg.png) 
![Imgur](https://i.imgur.com/VdzWnQy.png)
