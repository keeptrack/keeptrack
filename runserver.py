#!python3

import os
import sys

if os.getenv('VIRTUAL_ENV') == None:
    print("Start the venv first")
    exit()

port = sys.argv[1] if len(sys.argv) > 1 else ''

# Setup django environment variables
os.environ['SECRET_KEY'] = '5TiuyV%f0K*8c!NIyjP$GfPfZ4+#bLdPyg7_ldx1u9N+@&pUD8'
os.environ['APP_DEBUG']  = '1'
os.system('python manage.py runserver ' + port)
