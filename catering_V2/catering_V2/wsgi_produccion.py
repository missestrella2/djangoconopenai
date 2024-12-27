
import os
import sys
# Ruta al directorio donde está el archivo manage.py
sys.path.append('/home/cynthiavillagra/catering_V2/catering_V2/catering_V2')
# Configuración del módulo de Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'catering_V2.settings'
# Importar y configurar la aplicación WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()