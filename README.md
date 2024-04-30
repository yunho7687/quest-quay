# quest-quay
Step 0: install python 3.4+    
After clone the source code(make sure you are in the `quest-quay` directory):        
``` bash
cd quest-quay
```
### Sept 1: Create a Python virtual environment and activate the Python interpreter from it.
#### Mac or Linux:
```bash
(venv) $ python3 -m venv venv
```
```bash
(venv) $  source venv/bin/activate
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

### Sept 2: Install the requirements by `pip3`   
```bash
(venv) $ pip3 install -r requirements.txt
```


### Sept 3: Setup the local database and run the server
#### Start the database
```bash
(venv) $ flask db updrade
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
### Sept 4: Setup a local email server:
Start a new terminal and make sure in the `quest-quay` directory
```bash
(venv) $ aiosmtpd -n -c aiosmtpd.handlers.Debugging -l localhost:8025
```

Open a browser and go to URL:   
`http://<IP>:5505 `    
   
`http://127.0.0.1:5505 `

```
quest-quay
├── .flaskenv
├── app
│  ├── __init__.py
│  ├── errors.py
│  ├── forms.py
│  ├── images
│  ├── models.py
│  ├── routes.py
│  ├── static
│  │  ├── assets
│  │  │  ├── css
│  │  │  │  ├── bootstrap.min.css
│  │  │  │  └── style.css
│  │  │  ├── images
│  │  │  │  └── sample.png
│  │  │  └── js
│  │  │    ├── bootstrap.bundle.min.js
│  │  │    └── jquery-3.7.1.min.js
│  │  └── favicons
│  └── templates
│    ├── 404.html
│    ├── 500.html
│    ├── base.html
│    ├── components
│    │  ├── footer.html
│    │  └── post.html
│    ├── edit_profile.html
│    ├── index.html
│    ├── login.html
│    ├── register.html
│    └── user.html
├── app.db
├── config.py
├── logs
│  └── quest_quay.log
├── migrations
│  ├── alembic.ini
│  ├── env.py
│  ├── README
│  ├── script.py.mako
│  └── versions
│    ├── 1901c21c2e8a_posts_table.py
│    ├── 1e948b416ed8_users_table.py
│    ├── 6dda4d5aba19_d.py
│    ├── 8b2cb65c8247_add_followers_table.py
│    ├── af487df4c8ed_new_fields_in_user_model.py
│    └── ec3ab6d8be08_dd.py
├── new.tree
├── quest_quay.py
├── README.md
├── requirements.txt
└── tests.py
   ```
