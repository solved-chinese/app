# Solved Chinese

*Solve Chinese characters like riddles.*

## File Structure
- `jiezi/` django main app
- `accounts/` app manages the `User` model and its basic information.
- `content/` app manages the data created by our content team, i.e. the `Character`, `Radical`, and `CharacterSet` models. The data can be updated and synchronized from content team's Google Drive by staff when needed.  
- `learning` app implements our learning algorithm, see the wiki page for detail
- `classroon` app manages the `Student`, `Class`, and `Teacher` models and their interactions within a classroom setting. 
- `static/` & `templates/` for front end use

## API generation
We are now using Django REST Framework's self-browsable API served at <https://solvedchinese.org/api_root>. You can also test it locally in your development server.

## Installation
this is supposed to be done on a Ubuntu machine
1. clone this repo
```shell script
git clone git@github.com:solved-chinese/app.git
```
2. Create a conda environment using the `env.yaml` file in project root and activate it:
```shell script
conda env create -f env.yaml # if you use ubuntu
conda env create -f env_mac.yaml # if you use mac
conda activate jiezi
```
3. Setup PostgresSQL:
install PostgresSQL <https://www.postgresql.org/download/>
setup the database to match `jiezi.settings.DATABASES`:
``` shell script
sudo -u postgres psql
postgre# \password postgres (use this to change the password of postgres to 'jiezi')
```

4. Create your own secret files `jiezi_secret/secret.py`:
     
    ```python
   """This file is suppose to keep secret variables locally"""
     
    SECRET_KEY = '^&@nc_x_23(fmd9ye&v%d)x+(jo8ssqs!7+c@g(q&+4hgm8n(m'
    
    # This should store jiezi_secret or local database, and it will update setting
    # DATABASES (you may override default database if necessary)
    DATABASES = {
    }
   ```
 
5. Make the required migrations
```shell script
python manage.py migrate
``` 

6. Load content data
```shell script
python manage.py loaddata content/fixtures/content.json
```

7. Locally run the development server
```shell script
python manage.py runserver
```

8. [optional]Reference our wiki page for more details.
