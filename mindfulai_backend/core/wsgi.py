import os
from django.core.wsgi import get_wsgi_application

# This points to your settings file, using the 'core' folder we created
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mindfulai_backend.core.settings')

application = get_wsgi_application()
