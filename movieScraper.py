#Made by Jehlyen Fuller


import requests
import pandas as pd 
from bs4 import BeautifulSoup as soup
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter






url = "https://en.wikipedia.org/wiki/List_of_highest-paid_film_actors" #URL to extract information from
data = []

try:
	#Send a request to wikipedia
	response = requests.get(url)

	# See if the requests library gets us a response. 200 means there's a good connection.
	if response.status_code == 200:
		site_data = soup(response.content, 'html.parser')

		# Find the table

		table = site_data.find("table", class_= "wikitable sortable plainrowheaders")

		# Check if the table exists, if it does let's extract its components

		if table:
			print("Found the table, let's extract data.")
			#Find all the columns in the table

			rows = table.find_all("tr")
			

			for row in rows[1:]:
				# Get all columns with the Data information
				columns = row.find_all("td")
				
				if len(columns) > 4: #Check and see if columns have more than 4 rows of data
					
					actor = columns[0].get_text("", strip=True)
					film = columns[1].get_text(" ",strip=True)
					year_filmed = columns[2].get_text(" ",strip=True)
					salary = columns[3].get_text(" ",strip=True)
					total_income = columns[4].get_text(" ",strip=True)

					data.append([actor,film,year_filmed,salary,total_income]) # Add these to our data table for our dataframe

			actor_dataframe = pd.DataFrame(data, columns=['Actor', 'Film', 'Year', 'Salary', 'Total Income'])
			actor_dataframe.drop_duplicates(inplace=True)
			actor_dataframe.dropna(inplace=True)

			# Fix the console's output so that all columns are shown properly
			pd.set_option("display.max_columns", None)
			pd.set_option("display.width", 0)

			print(actor_dataframe) # This is the uncleaned dataframe, so you can see actors' salaries and income better.

			#Format Salary and Total Income sections

			# Convert empty strings to NaN (Nothing)
			actor_dataframe['Salary'] = actor_dataframe['Salary'].replace('', np.nan)
			actor_dataframe['Total Income'] = actor_dataframe['Total Income'].replace('', np.nan)

			# Drop rows with missing values
			actor_dataframe = actor_dataframe.dropna(subset=['Salary', 'Total Income'])

			# Clean and convert Salary
			actor_dataframe['Salary'] = (
				actor_dataframe['Salary']
				.astype(str) # Change valuetype to string
				.str.replace(r'[\$,+]', '', regex=True)   # remove $ and ,
				.astype(int) # Change valuetype to int
			)

			# Clean up Total Income
			actor_dataframe['Total Income'] = (
				actor_dataframe['Total Income']
				.astype(str) # Change valuetype to string
				.str.replace(r'[\$,+]', '', regex=True) # remove $ and ,
				.astype(int) # Change valuetype to int
				) 

			# Data Visualization
			# Who's the top 10 actors paid over 5 million dollars for a single movie?

			highest_paid_salary = actor_dataframe[actor_dataframe['Salary'] > 5000000].sort_values(by="Salary", ascending=False)
			print("Highest Paid Salaries:\n", highest_paid_salary.head(10))

			# Set up the bar chart

			x_values = highest_paid_salary["Actor"]
			y_values = highest_paid_salary["Salary"]

			plt.bar(x_values, y_values, color='#F28E2B')

			ax = plt.gca() #Set Axis as a Variable for easy manipulation
			ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v/1_000_000:.0f}M")) #Format the Y Axis values to show in Millions
			
			
			plt.xlabel("Actors")
			plt.xticks(fontsize=8,rotation=45, ha="right") # Align the values so that it fit properly on the chart
			plt.ylabel("Salaries in Millions (USD)")
			plt.margins(x=0.1)
			plt.title("Highest Paid Actors")
			plt.tight_layout()
			

			# What years paid the most for actors?

			highest_paid_salary["Year"] = highest_paid_salary["Year"].astype(int)

			year_twentyten = highest_paid_salary[highest_paid_salary["Year"] > 2010] 
			year_twothousand = highest_paid_salary[(highest_paid_salary["Year"] > 2000) & (highest_paid_salary["Year"] < 2010)]
			year_nineteenhundred = highest_paid_salary[(highest_paid_salary["Year"] > 1900) & (highest_paid_salary["Year"] < 2000)]

			twentyTenValue = year_twentyten["Salary"].sum()
			twothousandValue = year_twothousand["Salary"].sum()
			nineteenHundredValue = year_nineteenhundred["Salary"].sum()

			salary_data=[twentyTenValue, twothousandValue, nineteenHundredValue]
			salary_years=['2010s', '2000s', '1900s']

			plt.figure()
			plt.title("Actor Salaries Over Time")
			ax = plt.gca() #Set Axis as a Variable for easy manipulation
			ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v/1_000_000:.0f}M")) #Format the Y Axis values to show in Millions
			plt.plot(salary_years, salary_data, color="gray", linewidth=3, alpha=0.5)
			plt.grid(True, linestyle="--", alpha=0.7)
			plt.show()

			



	else:
		print("Error getting response, error code ", response.status_code)

except ConnectionError:
	print("Cannot pull information, experienced an error.")