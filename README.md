# FilmGraph 
CITS3403 Agile Web Development: Group 58

## Features
FilmGraph is designed to be a movie archiving website that collects user information relating to a film
and attaches the input to information about the film. The user can browse their growing collection of films,
search for a particular film in the collection to view more details, favourite it or remove it.
Graphs and statistics can be viewed, associated with the data from a user's collection. They are also able to connect with other users through the friends system and share their graphs with others.

## Contributors
| Student ID | Student Name | GitHub Account |
|------------|--------------|----------------|
|Nico Buchanan|22924258|nicostellar|
|Michael Sosulski|23385553|MichaelSosulski|
|Tyson Haines|23779585|TysonHaines|
|Thyler Cung|23743032|thylercung|

## Instructions: How to launch the application 

### Set up the virtual environment

```bash
python3 -m venv venv
# if using Windows, you may need to use python -m venv venv
source venv/bin/activate
# if using Windows command prompt, use venv\Scripts\activate
# if using Windows PowerShell, use venv\Scripts\Activate.ps1
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set secret key

Set a secret key for Flask CSRF by exporting an environment variable. 

If you need to generate a secret key, you can use the secrets module (available from Python 3.6 and later). For example, to generate a 16 byte token, you can use the following command: 

```python 
import secrets
secrets.token_hex(16)
```

Then you can set the secret key:

```bash
export SECRET_KEY='secret_key' 
# replace 'secret_key' with your generated key
# on Windows use $env:SECRET_KEY='secret_key'
```

### Initialise database 

To initialise the database, run the following commands: 

```bash
flask db init        # Initialize the migrations folder
flask db migrate     # Create the migration file 
flask db upgrade     # Apply migrations to the database
```

### Launching the application 

Once all of the above steps have been completed, then you can launch the application. 

```bash
flask run
```
