"""
WSGI config for Healthcare project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

from contract.deploy import ContractInteractions as Deploy

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Healthcare.settings')
makemigrations: str = "python manage.py makemigrations"
migrate: str = "python manage.py migrate"

# Smart contract creation and deployment, ran once on startup
deploy_instance = Deploy()
deploy_instance.deploy()

# inizializza il db
os.system(makemigrations)
os.system(migrate)


application = get_wsgi_application()
