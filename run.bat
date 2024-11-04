@echo off

REM Compliando as migrações
python manage.py makemigrations

REM Efetuando as migrações
python manage.py migrate

REM Iniciando o servidor de desenvolvimento em uma nova janela do shell
start cmd /c "python manage.py runserver"


pause
