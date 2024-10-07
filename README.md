# CSB-project1

Clone the repository
```bash
git clone https://github.com/Sippee/CSB-project1
```

Move to the project folder
```bash
cd CSB-project1
```

Make python virtual environment
```bash
python3 -m venv venv
```

Activate the virtual environment<br>
```bash
source venv/bin/activate
```
If this one doesn't work try another one
```bash
. venv/scripts/activate
```

Install depencies
```bash
pip install -r requirements.txt
```

Initialize the database
```bash
python3 initialize_database.py
```

Run the app. The app will run on http://127.0.0.1:5000/
```bash
flask run
```
To close the flask app just press Control + C in the terminal

To exit from the virtual environment
```bash
deactivate
```
