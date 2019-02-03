# Quizer
Host an online quiz with just python and some dependencies installed!

### Installation and Setup
1. Download Latest Release
2. Make a python virtualenv
```console
foo@bar:~$ cd CTF-Client
foo@bar:~$ apt install pip
foo@bar:~$ pip install virtualenv
foo@bar:~$ virtualenv env
foo@bar:~$ source env/bin/activate
```
3. Install Dependencies
```console
foo@bar:~$ pip3 -r install requirments.txt
```
4. Add Challenges
For this step, you will have to access `databases/users.db` with an sqlite3 client and add the questions in their respective columns
5. Run the app!!
```console
foo@bar:~$ python3 run.py
```
