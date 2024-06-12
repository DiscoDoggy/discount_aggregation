# Multi Sourced Discount Viewing 
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Insomnia](https://img.shields.io/badge/Insomnia-black?style=for-the-badge&logo=insomnia&logoColor=5849BE) ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)

## What?
This application serves as a way to aggregate data from multiple different clothing line stores and bring them into one place/website so it is easier to browser discount/onsale items and filter based on several different criteria. 

## Why?
As someone who, from time to time, explores online shopping for clothing and as someone who loves nothing more than discounts, I have often found myself wanting to figure out
what is on discount/sale from multiple stores. Currently, to figure out what sales exist, I would have to go to every stores' website and see what is on sale manually which takes a lot of time.

Most importantly though, I am using this application to learn more about data engineering and how, under the hood, data engineering tools may be implemented such as workflow orchestration tools like Mage and Airflow work.
Additionally, I hope this project increases my system design and software engineering abilities. This project takes an object oriented approach for the data pipeline in hopes that new sites are easy to build for and the wheel does not have to be remade.

## How?
On a high level, this application can be split into 3 parts:
* Data pipelines which extract, transform, and load data into a final database
* A backend that serves to retrieve information for the frontend
* A front end that presents different discounted items to users

### Data Pipelines
The data pipelines follow a traditional ETL architecture. First, data is extracted from a source using one of or a mix of three methods: Reverse engineering the site's API, Beautiful Soup based scraping, and Selenium.
Once the data is extracted, they are minimally processed and ingested into a MongoDB that serves as a staging data base where most of the data is raw still. The data is then pulled from the MongoDB, transformed, before being ingested into a final 
PostgreSQL database. 

Not all extracted data should be pushed to the Postgres Database. For example, if there are required fields missing from a clothing  item, an import error should be thrown and that item should not end up in the database. Another case
is if the item already exists in the database as a result of a past extraction. There should not be duplicates in the database. There are more cases of what should and should not make it into the final database but the recently listed is sufficient here. 
