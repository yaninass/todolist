pip install -r requirements.txt
cd todolist
python manage.py makemigrations 
python manage.py migrate    
python manage.py createsuperuser

python manage.py runserver  
