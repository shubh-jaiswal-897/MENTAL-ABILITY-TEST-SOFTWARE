import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testmybrain.settings")
django.setup()

from django.contrib.auth.models import User

def create_admin():
    username = "admin"
    email = "admin@example.com"
    password = "admin"

    if not User.objects.filter(username=username).exists():
        user = User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser '{username}' created successfully with password '{password}'!")
    else:
        user = User.objects.get(username=username)
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        print(f"Superuser '{username}' updated successfully with password '{password}'!")

if __name__ == "__main__":
    create_admin()
