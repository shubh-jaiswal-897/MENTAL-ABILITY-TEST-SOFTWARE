import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testmybrain.settings")
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def test_all_routes():
    print("Testing all application and admin routes...")
    client = Client()

    # Get or create superuser
    user, _ = User.objects.get_or_create(username="admin", is_staff=True, is_superuser=True)
    client.force_login(user)

    routes = [
        '/',
        '/revision/',
        '/test-session/',
        '/contests/',
        '/goodies/',
        '/dashboard/',
        '/about/',
        '/contact/',
        '/admin/',
        '/admin/quiz/question/',
        '/admin/quiz/question/ai-generate/',
        '/admin/quiz/subject/',
        '/admin/quiz/contest/',
        '/admin/quiz/goodieitem/',
        '/admin/quiz/userprofile/',
    ]

    errors = 0
    for route in routes:
        try:
            res = client.get(route)
            status = res.status_code
            if status in [200, 302]:
                print(f"[OK {status}] {route}")
            else:
                print(f"[FAIL {status}] {route}")
                errors += 1
        except Exception as e:
            print(f"[ERROR] {route} -> {e}")
            errors += 1

    if errors == 0:
        print("\nAll routes tested successfully with 0 errors!")
    else:
        print(f"\nFound {errors} route errors!")

if __name__ == "__main__":
    test_all_routes()
