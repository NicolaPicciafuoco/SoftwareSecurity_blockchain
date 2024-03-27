"""
WSGI config for Healthcare project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from contract.deploy import ContractInteractions as Deploy

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Healthcare.settings')

# Smart contract creation and deployment, ran once on startup

deploy_instance = Deploy()
deploy_instance.deploy()


application = get_wsgi_application()
