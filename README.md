# Hostel-Allotment-Portal

## Setup instructions
```
sudo apt install python3
sudo apt install python3-pip
sudo apt install mysql-server
sudo apt install libmysqlclient-dev
pip3 install -r req.txt
- Run mysql: mysql
  - create database hostels
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
  - fill in admin login details
- To populate with default data: python3 setup_script.py
python3 manage.py runserver
- Default Login Dertails for Chief Warden:
  - Username : chief_warden
  - Password : warden@hostels

```
## ER Diagram

- ![ER Diagram](Diagrams/ER_Diagram.jpg)

## Relation Schema

- ![Relation Schema](Diagrams/Relation_Schema.png)
