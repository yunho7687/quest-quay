# *Quest-quay*

### Project explained
>A description of the purpose of the application, explaining its design and use
 - Our application aims at improving the way **users interact with quests**, turning the simple act of **request and response** into an engaging experience.
 - With a clean and straightforward design, we prioritize a **user-friendly interface** that empowers users to navigate and utilize the platform with ease. By **enabling account creation** and **quest management** in an efficient manner, our platform excels in fostering a user-centric environment for **exchanging sideas**, **solving problems**, and building community connections. 
<br /> 
<br />
Team Members   

|  UWA Id   | Name  | GitHub |
|  :----:  | :----:  | :----:  |
| 24094053  | Chao Ding |[yunho7687](https://github.com/yunho7687) |
| 23895698  | Jiaxin Shi |[shijarrr](https://github.com/shijarrr) |
| 23936657  | Jeffrey Wan |[Jeffrey86Wan](https://github.com/Jeffrey86Wan)|
| 24122502  | Lanyizhe Deng |[woshixigou](https://github.com/woshixigou)|
<br />
 >A brief summary of the architecture of the application   

**Frontend**   
 - Our application leverages **HTML, CSS**, and **Bootstrap** for a responsive user interface, with **AJAX** and **JQuery** enriching the interactivity. This combination allows for a seamless and dynamic user experience tailored to desktop and mobile devices.

**Backend**   
 - Built on **Flask**, our backend architecture is designed for efficient request handling and data management. **SQLite** is used as the database solution, integrating directly with Flask to store user data and request interactions securely.

**Workflow**  
 - Users interact with the application through a streamlined process: **creating accounts, posting requests, searching and responding to others' requests**. The backend supports these activities with robust data processing.  
  
    
<br /> 

### Let's get started!
Step 0: install python 3.4+    
After clone the source code(make sure you are in the `quest-quay` directory):        
``` bash
cd quest-quay
```
### Step 1: Create a Python virtual environment and activate the Python interpreter from it.
#### Mac or Linux:
```bash
$ python3 -m venv venv
```
```bash
$ source venv/bin/activate
```
#### Win PowerShell:
```powershell
python3 -m venv venv
```
use Set-Execution Policy to allow the current user to execute scripts
```powershell
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
```
```powershell
venv/Scripts/Activate.ps1
```

### Step 2: Install the requirements by `pip3`   
```bash
(venv) $ pip3 install -r requirements.txt
```


### Step 3: Setup the local database and run the server
#### Start the database
```bash
(venv) $ flask db upgrade
```
#### Prepare for the email-related features(Mac or Linux):
``` bash
(venv) $ export MAIL_SERVER=localhost
(venv) $ export MAIL_PORT=8025
```
#### Prepare for the email-related features(Win):
```powershell
set MAIL_SERVER=localhost
set MAIL_PORT=8025
```
#### Start the flask app
```bash
(venv) $ flask run
```
### Step 4: Setup a local email server:
Start a new terminal and make sure in the `quest-quay` directory     
(make sure the virtural has been activated)
```bash
(venv) $ aiosmtpd -n -c aiosmtpd.handlers.Debugging -l localhost:8025
```
__Note__ after run the code above ⬆️ leave it alone. The email sending information will show in the terminal later once you send the reset password request     

### Step 5: Populate some mock user and post data:
Start a new terminal and make sure in the `quest-quay` directory    
 ``` bash
$ sqlite3 app.db
 ```
 ``` bash
sqlite> PRAGMA trusted_schema=1;      

sqlite> .read mock_data.sql
```


### Step 6: Go to the URL and login as a test user:  

`http://<IP>:5505 `      

   
`http://127.0.0.1:5505 `    

or    

`http://localhost:5505/`
 
you can use the `test user` directly:     
`Username`:  _agile_    
 
`Password`:  _admin_  
 
```
quest-quay
├── .flaskenv
├── .github
│  └── ISSUE_TEMPLATE
│    ├── bug_report.md
│    └── feature_request.md
├── .gitignore
├── app
│  ├── __init__.py
│  ├── auth
│  │  ├── __init__.py
│  │  ├── email.py
│  │  ├── forms.py
│  │  └── routes.py
│  ├── email.py
│  ├── errors
│  │  ├── __init__.py
│  │  └── handlers.py
│  ├── main
│  │  ├── __init__.py
│  │  ├── forms.py
│  │  └── routes.py
│  ├── models.py
│  ├── static
│  │  └── assets
│  │    ├── css
│  │    │  ├── bootstrap.min.css
│  │    │  └── style.css
│  │    ├── images
│  │    │  └── sample.png
│  │    └── js
│  │      ├── bootstrap.bundle.min.js
│  │      └── jquery-3.7.1.min.js
│  └── templates
│    ├── auth
│    │  ├── login.html
│    │  ├── register.html
│    │  ├── reset_password_request.html
│    │  └── reset_password.html
│    ├── base.html
│    ├── bootstrap_wtf.html
│    ├── components
│    │  ├── alerts.html
│    │  ├── footer.html
│    │  └── post.html
│    ├── edit_profile.html
│    ├── email
│    │  ├── reset_password.html
│    │  └── reset_password.txt
│    ├── errors
│    │  ├── 404.html
│    │  └── 500.html
│    ├── index.html
│    └── user.html
├── app.db
├── config.py
├── migrations
├── mock_data.sql
├── new.tree
├── quest_quay.py
├── README.md
├── requirements.txt
└── tests.py
   ```



