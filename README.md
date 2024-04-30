# *Quest-quay*

### Project explained
>A description of the purpose of the application, explaining its design and use
 - Our application aims at improving the way **users interact with quests**, turning the simple act of **request and response** into an engaging experience.
 - With a clean and straightforward design, we prioritize a **user-friendly interface** that empowers users to navigate and utilize the platform with ease. By **enabling account creation** and **quest management** in an efficient manner, our platform excels in fostering a user-centric environment for **exchanging sideas**, **solving problems**, and building community connections. 
<br /> 
<br />
 >Team Members   

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
### Sept 1: Create a Python virtual environment and activate the Python interpreter from it.
#### Mac or Linux:
```bash
python3 -m venv venv
```
```bash
source venv/bin/activate
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
pip3 install -r requirements.txt
```


### Sept 3: Setup the local database and run the server
#### Start the database
```bash
flask db updrade
```
#### Start the flask app
```bash
flask run
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



