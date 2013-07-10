import os
import sys

project_dir = os.path.abspath(os.path.dirname(__file__))

enviroment_root = os.path.abspath(os.path.join(project_dir, '..'))
activate_this = os.path.join(enviroment_root, "bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

sys.path.append(project_dir)
sys.path.append(os.path.abspath(os.path.join(enviroment_root, 'lib/python2.7/site-packages')))
os.environ['DJANGO_SETTINGS_MODULE'] = 'tradenplay.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

