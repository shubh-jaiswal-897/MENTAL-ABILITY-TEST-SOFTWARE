#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testmybrain.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# Expose WSGI application for Vercel
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testmybrain.settings')
    from django.core.wsgi import get_wsgi_application
    app = get_wsgi_application()
except Exception:
    pass
