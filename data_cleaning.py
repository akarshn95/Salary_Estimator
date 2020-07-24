#%%
import selenium.common.exceptions
import pandas as pd
import datetime

df = pd.read_csv('glassdoor_jobs.csv')
# drop duplicates
df.drop_duplicates(inplace=True)
# %%
# Cleaning the salary field

# remove $ and K; calc avg salary
salary = df['Salary Estimate'].apply(lambda x: x.split(' ')[0]).apply(lambda x:x.replace('K','')).apply(lambda x:x.replace('$',''))
df['min_salary'] = salary.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = salary.apply(lambda x: int(x.split('-')[1]))
df['avg_salary'] = (df.min_salary+df.max_salary)/2

# %%
# parse company name; remove the rating in company name
df['Rating']=df['Rating'].apply(int)
df['company_name'] = df.apply(lambda x: x['Company Name'] if x['Rating']<0 else x['Company Name'][:-3], axis=1)

#%%

# get state from location

#temp = df['Location'].apply(lambda x: x[-2:]).unique()
# cleaning rows which do not have state codes in their location
df.iloc[807,5]='CA'
df.iloc[377,5]='CO'
df.iloc[817,5]='FL'
df.iloc[[39,414],5]='UT'
df.iloc[[79,702],5]='NJ'
df.iloc[[40,296,303,343,383,461,487,592,678,681,722,816,858,876,879,950], 5] = 'rm'

# dropping rows which do not have location
df=df[df['Location']!='United States']

#df.apply(lambda x: x['Location'] if x['Location'][-2:] in ('ia','es','te','ah','ey','do','da') else 'Good', axis=1)
df['state'] = df['Location'].apply(lambda x: x[-2:])
# flag to determine if the job location is same as HQ location
df['hq_same_loc'] = df.apply(lambda x: 1 if x.Location==x.Headquarters else 0, axis=1)

# Age of company
df['age'] = df.Founded.apply(lambda x: x if x<0 else datetime.datetime.now().year-x)

# %%

# obtaining features from job description

df['python'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
df['tableau'] = df['Job Description'].apply(lambda x: 1 if 'tableau' in x.lower() else 0)
df['sql'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)
# %%

# export to csv and store the cleaned data
df.to_csv('glassdoor_jobs_cleaned.csv', index=False)