# Hackerank Contest Plagiarism Checker 

### Based on Python Selenium WebScrapping + SQL
 
#### This project is to webscrape the hackerrank dashboard of the students and get the attempts of each student and store it int the SQL database
#


## To run this code:
You have to install all the dependencies, and also you have to setup MySQL localhost server in your pc.

Inputs for this Code will be:
    
    1. Hackerank:
       - Admin Username
       - Admin Password
       - Student Username to fetch the data
       - Contest Name

    2. MySQL:
       - username
       - password
       - database
       - host 

# Code Explaination:

main.py:

This is a FAST API backend file which have the endpoints.
To run this use the command:
   Uvicorn main:app --reload
After running this we can access api endpoint at http://localhost:8000
Then run the frontend which can access the crud operations on this endpoint.


selenium_webscrapping.py :  This python script uses selenium web scrapping module of
python library to scrape contest details from hackerrank website. It takes input as admin credentials (username & password). After that it scrapes each page containing problem statement and stores them into mysql db using sqlalchemy ORM.

hackerank_SQL.
The sql queries are stored here. These query helps us to perform CRUD operation like fetching problems adding new users etc..


# Setting Up Database:

We will be using MySQL Database to store the results,
Download and Install MySQL Database. 
When mysql is running at localhost 3360 then create a database with name test.
then makesure there are no errors in chromedriver, Rest it will create the tables and You are ready to go

Install the requirements then run the command it will fetch all the latest attempts.



# Screenshots
![Screenshot](https://github.com/)
