# Solved Chinese

*Learn Chinese characters like riddles.*

## File Structure
- `docs/`: <https://solved-chinese.github.io/app/> automatically generated API files
- `static/` & `templates/` for front end use
-  `learning/` & `accounts/` & `jiezi_admin/` our custom apps for backend use
- `jiezi` django main app

## API generation
our API's are currently currently served at <https://solved-chinese.github.io/app/>.  
 They are generated from python source code by apidoc (<https://apidocjs.com>).  
 
 To install apidoc:   `npm install apidoc -g`  
 To update API's from current code, run from project root folder, and ignore the warning about missing configuration file: `apidoc -i ./ -o docs/` 

## Installation
this is supposed to be done on a Ubuntu machine
1. clone this repo
```shell script
git clone git@github.com:solved-chinese/app.git
```
2. Create a conda environment using the `env.yaml` file in project root and activate it:
```shell script
conda env create -f env.yaml
conda activate jiezi
```
3. Setup PostgresSQL:
install PostgresSQL <https://www.postgresql.org/download/linux/ubuntu/>  
setup the database to match our setting file:
```
'NAME': 'postgres',
'USER': 'postgres',
'PASSWORD': 'jiezi',
'HOST': 'localhost',
'PORT': '5432',
```

4. Create your own secret files:
    1. Generate your own django secret_key, in python:  
    
   ``` python
   from django.core.management.utils import get_random_secret_key  
   get_random_secret_key() # the returned value is your secret key
   ```  
   
    2. Create `jiezi_secret/secret.py` using your secret key:  
    
    ```python
   """This file is suppose to keep secret variables """
    
    SECRET_KEY = 'YOUR_SECRET_KEY'
    
    # This should store jiezi_secret or local database, and it will update setting
    # DATABASES (you may override default database if necessary)
    DATABASES = {
    }
   ```
   
   3. get `jiezi_secret/datafile_service_account.json` from us, this is used to access our google drive data 

5. Make the required migrations
```shell script
python manage.py migrate
```

6. Locally run the development server
```shell script
python manage.py runserver
```
