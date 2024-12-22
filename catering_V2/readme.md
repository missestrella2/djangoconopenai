PARA DEPLOYAR EN PYTHONANYWHERE

- tener el repo en github
- git clone de nuestro repo de github
- crear entorno virtual
- instalar librerias necesarias

Agregar Web App, Python 3,9 y elegir CONFIGURACION MANUAL

# =====================================================
# 1 - Configurar WSGI: 

# +++++++++++ DJANGO +++++++++++
# To use your own Django app use code like this:
import os
import sys

# Ruta al directorio donde está settings.py
path = '/home/cynthiavillagra/catering_V2/catering_V2'
if path not in sys.path:
    sys.path.insert(0, path)

# Configuración del módulo de Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'catering_V2.settings'

# Importar y configurar la aplicación WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# =====================================================
# 2 - Configurar SETTINGS.PY: 

 cambiar DEBUG a FALSE
 agregar en ALLOWED HOSTS la direccion mia de pythonanywhere
#

# =====================================================
# 3 - Configurar statics:

en URL : /static/
en Directory: /home/cynthiavillagra/catering_V2/catering_V2/calculos/static


