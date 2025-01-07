# Yelp Application

## Abstract

This is a Yelp Application that allows users to retrieve information such as reviews of businesses or modify the database by, for example, adding new reviews.

## Technologies used

- Python (pymssql)
- SQL Database (MSSQL)

## How to set up

1. Download Yelp Dataset  
This application is designed to work with the Yelp dataset provided on their website. Visit the [Yelp Dataset page](https://www.yelp.com/dataset) and download the dataset if you wish to test the app.  
Ensure your dataset file names are as follows: business, checkin, friendship, review, tip, user_yelp.

3. Installation
Install python-dotenv by running `pip install python-dotenv` in the terminal  
Install pymssql by running `pip install pymssql` in the terminal

4. Set up Environment Variable  
Create a '.env' file in the project root and add the following details:  
DB_HOST=your-database-host  
DB_USER=your-database-username  
DB_PASSWORD=your-database-password  
DB_NAME=your-database-name  

5. Run the project
