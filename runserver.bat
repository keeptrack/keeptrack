@echo off

Rem We need this variables to run our dev environment
set SECRET_KEY="5TiuyV%f0K*8c!NIyjP$GfPfZ4+#bLdPyg7_ldx1u9N+@&pUD8"
set APP_DEBUG="1"

Rem start server
python manage.py runserver