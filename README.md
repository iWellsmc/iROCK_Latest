# IRock

IRock is Django Framework application.

## Installation

### Prerequisites:

* Python 3.8.10
* Django 3.2.10
* Mysql 8.0
* mysqlclient==2.0.3
* Phpmyadmin

### Procedure:

* Upload files to the Server and if python3.8 is not available need to install python3.8
follow these steps:

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.8
sudo apt install python3.8-venv python3.8-dev

* Create Python virtual environment and activate

```bash
python3.8 -m venv venv
source venv/bin/activate
```

* Before installing the requirements do these installation

```bash
sudo apt-get install pkg-config
sudo apt-get install libmysqlclient-dev
sudo apt-get install libpq-dev
sudo apt-get install build-essential
```

*And then run to install requirements

```bash
pip3 install -r requirements.txt
```

```
* Create **manage.py** file -> change file name  **sample.manage.py** into **manage.py** 

* Update Database configuration in - **irock/dev.py(development database config)** and **irock/pro.py(production database config)**

* Set Environment in **manage.py** (pro.py or dev.py )

Now run Python Migrations

```bash
python3 manage.py makemigartions
python3 manage.py migrate
```

* Create admin user, by
```
python manage.py createsuperuser
```

* Now Start Project by running,
```bash

python3 manage.py runserver 0.0.0.0:port

```
Now, It should be accessible via http://localhost:8000 (or) http://127.0.0.1:8000
Admin login via http://localhost:8000/adminlogin (or) http://127.0.0.1:8000/adminlogin
