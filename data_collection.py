'''
Data collector which scrapes data from Glassdoor using the glassdoor_scraper and stores it in a DataFrame for analysis
'''
import glassdoor_scraper as gs 
import pandas as pd 

path = "/Users/AkarshNagaraj/Desktop/Projects/Data_Scientiest_Salaries/chromedriver"

df = gs.get_jobs('data scientist', 10, False, path, 15)

df.to_csv('/Users/AkarshNagaraj/Desktop/glassdoor_jobs2.csv', index = False)