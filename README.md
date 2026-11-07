# CS Club Website
A work-in-progress website for LHSS's CS Club  
Visit [https://csclub-886421535915.us-east1.run.app/](https://csclub-886421535915.us-east1.run.app/)

## Features
- [X] User registration/login/logout
- [X] Viewing and creating announcements
- [ ] Attendance system
- [ ] Links to lessons

## Getting Started
Just look at requirements.txt if you want to see all the prerequisite packages to install.  
Steps to install:  
```bash
git clone https://github.com/Filtrate8-Afterlife-Ocean/csclub.git
cd csclub
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate for windows
pip install -r requirements.txt
echo "SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" > .env
flask --app csclub db upgrade
flask --app csclub run --debug
```  
Then visit http://127.0.0.1:5000.  
For executive functionality, first create an account and then run:
```bash  
flask --app csclub auth declare-exec <username>
``` 
