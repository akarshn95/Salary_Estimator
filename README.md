# Data Scientist Salary Predictor

### Project Overview
Built a data science salary predictor capable of making salary predictions based on job location, title, skills required, seniority among other parameters. The data is scraped off Glassdoor job postings using Selenium Web Scraper for data scraping. The data is cleaned and suitable feature engineering is peformed to prepare the parameters that can help us make accurate predictions. Exploratory Data Analysis is performed to understand the relationship between different parameters and on the salary. Finally, linear regression, lasso regression and random forest regression are implemented. Random Forest regressor provided the best Mean Absolute Error, followed by Lasso regression. 

### Resources
Glassdoor scraper : https://github.com/arapfaik/scraping-glassdoor-selenium

### Model
The Machine Learning model predicts the average salary based on the following parameters:
- Rating
- Company Size
- Type of Ownership, Indusrty, Sector
- Number of competitors
- Location
- Skills required in job description

## Model Performance 
I initially used Linear Regression model to provide a baseline for comparison. Lasso regression is tuned and used with the best alpha value. Random Forest Regressor is tuned with GridSearchCV and the best parameters are used for fitting it.
- Linear Regression - $19.77k 
- Lasso Regression - $19.28k
- Random Forest Regression - $14.98k

The final model is a combination of Linear Regression and Random Forest Regression with an overall MAE of $14.33k. 
