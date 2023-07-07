#!/usr/bin/env python
# coding: utf-8

'''
Author:Parul Baderia
Filename: CommodityData_FinalProject_parul_17.py
Purpose: To generate grouped bar graphs using Plotly
Revisions:
    00:Importing the relevant modules
    01:Reading the data from the csv file and iterating through locations and values
    02:Veryfiying that conversions are correct
    03:Create a sorted list of Products
    04:Visualize the Products and indices
    05:Prompting the user to give the product indices
    06:Visualizing the sorted list of dates
    07:Prompting the user to give the start and end dates
    08:Visualizing the sorted list of locations
    09:Visualizing the sorted list of locations with their indices
    10:Prompting the user to give the indices of the locations
    11:Select the data records that meet the criteria given: date range, selected products and selected cities.  
    12:Organize the selected data records in a dictionary with two keys: product and location
    13:Printing the Price for each Product
    14:Taking the average price of each product in each location
    15:Converting the dictionary into list
    16:Plotting the Grouped Bar graph
    17:plot the figure to the html file 
    
'''

#1:Importing the relevant modules

import csv
from datetime import datetime
from itertools import product
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go


#2:Reading the data from the csv file and iterating through locations and values

##: Announce the program
print(f"{'='*26}\nAnalysis of Commodity Data\n{'='*26}")

 
data = []
csvfile = open('C:\\Users\\rakes\\OneDrive\\Desktop\\PYTHON\\final\\produce_extra.csv','r')
reader = csv.reader(csvfile)
for row in reader:  ###! main loop reads one row at a time
    if reader.line_num == 1: ###! get the location names from row 1
        locations = row[2:]  ###! slice to remove commodity and date
    else:
        for location,value in zip(locations,row[2:]):  ###! iterate through locations and values
            row_num = len(data)     ###! index for the data row 
            data.append(row[:2])    ###! new data row: commodity and date
            data[row_num].append(location)  ###! append location
            data[row_num].append(float(value.replace('$','')))
            data[row_num][1]=datetime.strptime(data[row_num][1],'%m/%d/%Y').date()
csvfile.close()


#3:Veryfiying that conversions are correct
print("Veryfiying that conversions are correct\n")
for item in data[5]:
    print(f'{item}, {type(item)}')
print('\n')

#4:Create a sorted list of Products
products = sorted(list(set([elements[0] for elements in data])))

#5:Visualize the Products and indices
print('SELECT PRODUCTS BY NUMBER ...\n')
for count_prod, value_prod in enumerate(products):
    print(f'{count_prod}:{value_prod}')


#6:Prompting the user to give the product indices
print(f'Enter product numbers from 0 to {(len(products)-1)} separated by spaces: ')
# print("For example: 0 2 3 4")
n = input("> ")

# Convert the user's input string into a list of integers
prod_idx = [int(i) for i in n.split()]

# Use the index numbers to create a list of desired location strings
prod_list = [products[i] for i in prod_idx]

print("\nSelected Products: ")
for prod in prod_list:
    print(prod,end=" ")


#7:Visualizing the sorted list of dates
dates = sorted(list(set([elements[1] for elements in data])))

print('\nSELECT DATE RANGE BY NUMBER ...\n')
for count_dates, value_dates in enumerate(dates):
    print(f'<{count_dates}> {value_dates}')

print()  # To add a newline after the dates

print(f'Earliest available date is: {min(dates)}')
print(f'Latest available date is: {max(dates)}')  


#8:Prompting the user to give the start and end dates
dates = sorted(list(set([elements[1] for elements in data])))
print(f'Enter start/end date numbers separated by a space 0 {(len(dates)-1)}: ')
start_idx, end_idx = input("> ").split()
start_idx = int(start_idx)
end_idx = int(end_idx)

if start_idx >= 0 and end_idx <= len(dates) - 1 and start_idx <= end_idx:
    start_date = dates[start_idx]
    end_date = dates[end_idx]
    print(f"Dates from {start_date} to {end_date}")
else:
    print(f"Invalid input. Please enter start/end date numbers separated by a space between 0 and {len(dates) - 1}.")

#9:Visualizing the sorted list of locations
locations_sorted = sorted(list(set(locations)))
print(locations_sorted)


#10:Visualizing the sorted list of locations with their indices
print('SELECT LOCATIONS BY NUMBER ...\n')
for count_loc, value_loc in enumerate(locations_sorted):
    print(f'<{count_loc}>:{value_loc}')


#11:Prompting the user to give the indices of the locations
print(f'Enter location numbers separated by spaces: 0 to {len(locations_sorted)-1}')
user_choice = input("> ")

# Convert the user's input string into a list of integers
index_list = [int(i) for i in user_choice.split()]

# Use the index numbers to create a list of desired location strings
chosen_locations = [locations_sorted[i] for i in index_list]

print("Selected locations:", " ".join(chosen_locations))



#12:Select the data records that meet the criteria given: date range, selected products and selected cities.  
new_data = list(filter(lambda x: x[2] in chosen_locations and x[0] in prod_list and start_date <= x[1] <= end_date, data))
print(f'\n{len(new_data)} records have been selected.\n')

for count_loc, value_loc in enumerate(new_data):
    print(f'<{count_loc}>:{value_loc}')


#13:Organize the selected data records in a dictionary with two keys: product and location
prod_loc=list(product(prod_list, chosen_locations))
my_dict={}
for i in prod_loc:
    my_dict[i] = []
    
for row in new_data:
    my_dict[(row[0],row[2])].append(row[3])


#14:Printing the Price for each Product
for key in my_dict:
    count = len(my_dict[key])
    print(f'{count} prices for {key[0]} in {key[1]}' )


#15:Taking the average price of each product in each location
for key in my_dict:
    
    my_dict[key]=np.average(my_dict[key])
my_dict
    


#16:Converting the dictionary into list
my_list = [[key[1], key[0], value] for key, value in my_dict.items()]
my_list


#17:Plotting the Grouped Bar graph
print("\n\nPlotting the Grouped Bar graph")
# Create an empty dictionary to store the data by category
category_data = {}

# Traverse the list and group the data by category
for item in my_list:
    category = item[0]
    city = item[1]
    value = item[2]
    if category not in category_data:
        category_data[category] = {'Products': [], 'values': []}
    category_data[category]['Products'].append(city)
    category_data[category]['values'].append(value)

# Create a list of traces for the plot
traces = []
for category in category_data:
    traces.append(go.Bar(
        name=category,
        x=category_data[category]['Products'],
        y=category_data[category]['values']
    ))



# Add axis titles and formatting
#fig.layout(
layout = go.Layout(
    xaxis_title="Product",
    yaxis_title=" Average Price (USD)",
    yaxis_tickprefix="$",
    title={
        'text': f"Product Prices from {start_date} through {end_date}",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    }
)

# Create the figure and plot the data
fig = go.Figure(data=traces, layout=layout)
fig.show()


#18:plot the figure to the html file 
fig.write_html("ProductPricesByLocation.html")
py.plot(fig, filename="ProductPricesByLocation.html")




