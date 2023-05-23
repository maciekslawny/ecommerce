# Project Ecommerce
> Made for recruitment purposes

## Table of Contents
* [Technologies Used](#technologies-used)
* [Setup - Docker](#setup-docker)
* [Setup](#setup)


## Technologies Used
- Python - version 3.10
- Django - version 4.2.1
- Django Rest Framework - version 3.14.0
- Celery - version 5.2.7
- Pillow - version 9.5.0


## Setup Docker
1. Go to the main project directory
2. Execute the following code in the console:
`sudo docker-compose up`


## Setup
1. Clone the repository executing the following command:
`git clone https://github.com/maciekslawny/ecommerce.git`
2. Go to the main project directory
3. Create a virtual environment and run it with the appropriate command
4. Install all dependencies from the file executing the following command:
`pip install -r requirements.txt`
5. Make migrations in the project:
`python manage.py migrate`
6. Create superuser in the project:
`python manage.py createsuperuser`
7. Run the project with the following command:
`python manage.py runserver`
8. After starting the virtual environment in new consoles run celery & celery beat: 
`celery -A config worker -l info --pool=solo` and
`celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler`