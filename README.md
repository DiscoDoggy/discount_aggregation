# Multi Sourced Discount Viewing 
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Insomnia](https://img.shields.io/badge/Insomnia-black?style=for-the-badge&logo=insomnia&logoColor=5849BE) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) 

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

The ingestion also updates items in the DB whose data might have been updated since the last extraction. 

The database connection to MongoDB is done with PyMongo and the database connection to Postgres utilizes SQLAlchemy.

### Frontend
The frontend is written in raw HTML, some Bootstrap components, and raw javascript. Using this "lower" level approach to frontend web development as opposed to using established frameworks like React was done mostly for learning and developing stronger skills with javascript and the overall fundamentals of web development.  

![image](https://github.com/user-attachments/assets/ba223efb-968d-440d-832b-fe6507200eaa)
![image](https://github.com/user-attachments/assets/2f27e9e2-eb97-4ddd-8459-422a9598713e)



### Backend 
The backend is written in FastAPI and in order to connect to the database, we again use SQLAlchemy. 

Thus far, the backend is pretty simple. Most of the requests that need to be made are data reads (GET requests). The different GET operations support the basic needs of clothing websites. Users may want to filter by size, price, colors, and rating. Users may want to sort the selection of items or search for different types of items via a search bar. All these operations are supported. 

#### Filtering
To implement filtering, instead of passing the different pieces of filtering information through query parameters, I decided to use a JSON request payload. The JSON post request felt easier to pass in long lists of colors or sizes that a user may want to include within their filter query. All of the sizes and colors can be stored in a list each but if these were to be fed into a query parameter, it would be much more difficult to parse and process.

#### Sorting
Sorting is implemented through query parameter where some sort of "sort_key" is passed and then parsed in the backend to determine what SQL ORDERBY function should be performed.

#### Searching
In order to implement searching, we used PostgreSQL full text search support which involved crafting vectors and search query objects to pass to postgres to query in the database. 
