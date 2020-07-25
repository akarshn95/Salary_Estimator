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
df['company_name'] = df['company_name'].apply(lambda x: x.replace('\n',''))
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

#%%
# simplify and make job titles uniform

def title_simplify(title):
    if 'director' in title.lower():
        return 'director'
    if 'manager' in title.lower():
        return 'manager'
    if 'machine learning' in title.lower():
        return 'mle'
    if 'scientist' in title.lower() or 'data science' in title.lower():
        return 'data scientist'
    if 'analyst' in title.lower() or 'analytic' in title.lower():
        return 'data analyst'
    if 'data engineer' in title.lower():
        return 'data engineer'
    if 'architect' in title.lower() or 'model' in title.lower():
         return 'data architect'
    else:
        return 'na'

df['title_simple'] = df['Job Title'].apply(title_simplify)

# senior position check
def seniority(title):
    if 'senior' in title.lower() or 'sr' in title.lower() or 'lead' in title.lower() or 'manager' in title.lower() or 'director' in title.lower():
        return 1
    else:
        return 0

df['seniority'] = df['Job Title'].apply(seniority)

#%%
# Job Description length and competitor count
df['desc_len'] = df['Job Description'].apply(lambda x: len(x))
df['num_comp'] = df['Competitors'].apply(lambda x: 0 if x=='-1' else len(x.split(',')))

#%%
# export to csv and store the cleaned data
df.to_csv('glassdoor_jobs_cleaned.csv', index=False)
