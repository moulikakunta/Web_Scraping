import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
def get_url(position, location):
    # Generate url from position and location
    position = position.replace(' ', '+')
    location = location.replace(' ', '+')
    template = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={position}&txtLocation={location}"
    url = template.format(position, location)
    print(f"URL : {url}")
    return url

def main(position, location):
    # Run the main program routine

    url = get_url(position, location)
    response = requests.get(url).text
    soup = BeautifulSoup(response, "lxml")
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    Total_no_of_jobs = soup.find('header', class_='srp-header clearfix').h1.text.split()[0]

    # jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    print(f"Total jobs: {Total_no_of_jobs}")
    jobs_data = []

    for job in jobs:
        data = {}

        data['Company'] = job.find('h3', class_='joblist-comp-name').get_text(strip=True)
        data['Skills'] = job.find('span', class_='srp-skills').get_text(strip=True)

        ul = job.find('ul', class_='top-jd-dtl clearfix').findChildren(recursive=False)
        data['Exp'] = ul[0].find(text=True, recursive=False)
        data['Location(s)'] = ul[1].span.text if ul[1].span else None

        data['link'] = job.header.h2.a['href']

        jobs_data.append(data)
        df = pd.DataFrame(jobs_data)
        # df.to_csv('jobs.xlsx')

    # creating pandas dataframe from dictionary of data
    # df_cars = pd.DataFrame({'Company': ['BMW', 'Mercedes', 'Range Rover', 'Audi'],
    #                         'Model': ['X7', 'GLS', 'Velar', 'Q7'],
    #                         'Power(BHP)': [394.26, 549.81, 201.15, 241.4],
    #                         'Engine': ['3.0 L 6-cylinder', '4.0 L V8', '2.0 L 4-cylinder', '4.0 L V-8']})

        writer = pd.ExcelWriter('converted-to-excel.xlsx')
        df.to_excel(writer)

        # save the excel
        writer.save()

# Exporting dataframe to Excel file
# df_cars.to_excel("converted-to-excel.xlsx")




if __name__ == "__main__":
    position = input("Enter your position : ")
    location = input("Enter your location : ")
    main(position, location)

    print("Task completed ...!")