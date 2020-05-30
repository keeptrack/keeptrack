#!/bin/bash

export SECRET_KEY='5TiuyV%f0K*8c!NIyjP$GfPfZ4+#bLdPyg7_ldx1u9N+@&pUD8'
export APP_DEBUG=1

if [ $# -eq 0 ]; then
	python manage.py runserver
else
	python manage.py $@
fi
