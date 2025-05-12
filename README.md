# Agile-Web-Dev-Group-58

## Instructions: How to launch the application 

### Set up the virtual environment

```bash
python3 -m venv venv
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
```

### Initialise database 

To initialise the database, run the following commands: 

```bash
# Delete old migrations folder if present with `rm -r migrations`
flask db init        # Initialize the migrations folder
flask db migrate     # Create the migration file 
flask db upgrade     # Apply migrations to the database
```

### Launching the application 

Once all of the above steps have been completed, then you can launch the application. 

```bash
flask run
```
