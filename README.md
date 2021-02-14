# Solved Chinese

*Solve Chinese characters like riddles.*

## File Structure
- `jiezi/` django main app
- `accounts/` app manages the `User` model and its basic information.
- `content/` app manages the data created by our content team
- `learning` app implements our learning algorithm
- `static/` & `templates/` for django front end
- `frontend/` for React

## Installation
We have conda environments for both Mac and Ubuntu, Windows should also work 
but you would have to install the environment by yourself

1. clone this repo
```shell script
git clone git@github.com:solved-chinese/app.git
```
2. Create a conda environment using the `env.yaml/env-mac.yaml` file in project root and activate it:
```shell script
conda env create -f env.yaml # use env-mac.yaml if on mac
conda activate jiezi
```
3. Setup PostgresSQL:
install PostgresSQL <https://www.postgresql.org/download/linux/ubuntu/>
setup the database to match `jiezi.settings.DATABASES`:
``` shell script
sudo -u postgres psql
postgre# \password postgres (use this to change the password of postgres to 'jiezi')
```

4. Make the required migrations
```shell script
python manage.py migrate
```

5. Locally run the development server
```shell script
python manage.py runserver
```
