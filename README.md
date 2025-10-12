id  == "shubh111"
pas == "shubh111"
MENTAL ABILITY TEST SOFTWARE - minimal Django quiz app

Quick start (Windows PowerShell):

1. Create and activate a virtualenv

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install requirements

```powershell
pip install -r requirements.txt
```

3. Run migrations and start server

```powershell
python manage.py migrate
python manage.py runserver
```

4. Create an admin user to add questions:

```powershell
python manage.py createsuperuser
```

Run tests:

```powershell
python manage.py test
```

