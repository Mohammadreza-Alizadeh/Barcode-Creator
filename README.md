# Barcode-Creator
A simple Flask App Designed to Register for a Conference and create a Barcode for user

### Project summary
This was an audience registration project that was supposed to be used for the nearest conference of the Computer Science Association, but due to the cancellation of the conference by the university, the development of this app was also stopped.
But we can look at this project from the perspective of familiarity and how to connect a Flask app to Zarin Pal and store information with SQL Alchemy.  

this app is capable of creating beautifull barcodes  
you can see an example in this url when you run it in your localhost
```
localhost:5000/test/
```

## Getting Started
To get this project up and running, you should start by having Python installed on your computer. It’s advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with pip install virtualenv.

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

``` 
python -m venv env
```

That will create a new folder naemd env in your project directory. Next activate it with this command on mac/linux:

```
source env/bin/active
```

or if you use windows activate it with this command :
```
.\env\scripts\activate
```

Then install the project dependencies with:
```
pip install -r requirements.txt
```

because i used SQLAlchemy in this project you have to create database tables manually.    
you can do this by following steps bellow  
  
in project root (where app.py is located) enter the following command
```
flask shell
```

after that you will enter to interactive command-line tool for flask   
now you have to import some objects with commands bellow
```
from database import db
from models import Students
```

now you have to create tables  
you can do that with this command
```
db.create_all()
```
now you can exit from flask-shell  
like this: 
```
quit()
```

now there must be a new file in `/instance` directory named `students.db`

now you are good to go  
just simply enter this command to start the app :
```
flask run
```
