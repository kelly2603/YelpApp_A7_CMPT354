# Yelp Application

## Abstract

This is a Yelp Application that allows users to retrieve information such as reviews of businesses or modify the database by, for example, adding new reviews.

## Technologies used

- Python (with `pymssql` for database connection)
- SQL Database (MSSQL)

## How to set up

1. Download Yelp Dataset  
This application is designed to work with the Yelp dataset provided on their website. Visit the [Yelp Dataset page](https://www.yelp.com/dataset) and download the dataset.  
Ensure your dataset file names are as follows: business, checkin, friendship, review, tip, user_yelp.  

3. Install Dependencies  
Run the following commands in the terminal to set up required dependencies:  
`pip install python-dotenv`  
`pip install pymssql`  

5. Set up Environment Variable  
Create a '.env' file in the project root and add the following details:  
DB_HOST=your-database-host  
DB_USER=your-database-username  
DB_PASSWORD=your-database-password  
DB_NAME=your-database-name  

6. Run the project  
Once setup is complete run `python YelpApp.py`  
