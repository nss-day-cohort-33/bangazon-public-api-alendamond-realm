###python-bangazon-api-template###

**There are a couple steps to run this server. After you clone the repo, cd into it and perform the following steps:**

1. Run this command: `python -m venv bangazon-api-env`
2. Next, in cmd cd into the bangazon-api-env directory within the project directory
3. Then cd into the Scripts directory and run the command: Start activate.bat
4. In the rood directory run the command: `pip install django autopep8 pylint djangorestframework django-cors-headers pylint-django`
5. Run: `pip freeze -r requirements.txt`

**The next steps are for setting up the database:**

1. In the root project directory run the command: `python manage.py makemigrations`
2. Next run: `python manage.py migrate`
3. Then run: `python manage.py loaddata <fixture file name minus .json>` load order should be: `customer payment product_types product order order_product`

**Now that your database is set up all you have to do is run the command:**

`python manage.py runserver`

*You can test your new server out in postman if you so desire.*