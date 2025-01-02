import os
import sys

# Añade las rutas a tu proyecto
sys.path.append('/home/cynthiavillagra/catering_V2')  # Ruta base del proyecto
sys.path.append('/home/cynthiavillagra/catering_V2/catering_V2')  # Ruta a la carpeta donde está settings.py

# Activa el entorno virtual
activate_this = '/home/cynthiavillagra/.virtualenvs/myvirtualenv/bin/activate_this.py'
exec(open(activate_this).read(), {'__file__': activate_this})

# Configura DJANGO_SETTINGS_MODULE para que apunte al archivo settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'catering_V2.settings')

# Importa y configura la aplicación WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()