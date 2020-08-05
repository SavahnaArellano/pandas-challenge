#!/usr/bin/env python
# coding: utf-8

# In[9]:


# Dependencies and setup
import pandas as pd

# File to Load (remember to change these)
purchase_data = "purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(purchase_data)

# Display
purchase_data


# In[7]:


# Number of unique players 
player_demo = purchase_data.loc[:, ["Gender", "SN", "Age"]]
player_demo = player_demo.drop_duplicates()
num_players = player_demo.count()[0]

# Display the total number of players
pd.DataFrame({"total players": [num_players]})


# In[17]:


# calcs
ave_item_price = purchase_data["Price"].mean()
total_purchase_value = purchase_data["Price"].sum()
purchase_count = purchase_data["Price"].count()
item_count = len(purchase_data["Item ID"].unique())

# data frame for results
summary_table = pd.DataFrame({"Number of Unique Items": item_count, "Total Revenue": [total_purchase_value],"Number of Purchases": [purchase_count], "Average Price": [ave_item_price]})

# Data Cleaning
summary_table ["Average Price"] = summary_table["Average Price"]
summary_table ["Number of Purchases"] = summary_table["Number of Purchases"]
summary_table ["Total Revenue"] = summary_table["Total Revenue"]
summary_table = summary_table.loc[:,["Number of Unique Items", "Average Price", "Number of Purchases", "Total Revenue"]]

#  Display data frame
summary_table


# In[18]:


# Number and Percentage by Gender
gender_demo_totals = player_demo["Gender"].value_counts()
gender_demo_percents = gender_demo_totals / num_players * 100
gender_demo = pd.DataFrame({"Total Count": gender_demo_totals, "Percentage of Players": gender_demo_percents})

#display data frame
gender_demo


# In[39]:


# Calcs
gender_purchase_total = purchase_data.groupby(["Gender"]).sum()["Price"].rename("Total Purchase Value")
gender_average = purchase_data.groupby(["Gender"]).mean()["Price"].rename("Average Purchase Price")
gender_counts = purchase_data.groupby(["Gender"]).count()["Price"].rename("Purchase Count")

# Calc avg
avg_pur_total = gender_purchase_total / gender_demo["Total Count"]

#Convert to data frame
gender_data = pd.DataFrame({"Purchase Count": gender_counts, "Average Purchase Price": gender_average, "Total Purchase Value": gender_purchase_total, "Average Purchase Total Per Person by Age Group": avg_pur_total})

# Display data frame
gender_data


# In[21]:


# Create bins
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

# Put data into bins
player_demo["Age Ranges"] = pd.cut(player_demo["Age"], age_bins, labels = group_names)

#Calc the numbers and Percentages by Age Group
age_demo_totals = player_demo["Age Ranges"].value_counts()
age_demo_percents = age_demo_totals / num_players * 100
age_demo =  pd.DataFrame({"Total Count": age_demo_totals, "Percentage of Players": age_demo_percents})

# Display Data Frame
age_demo.sort_index()


# In[33]:


# Bins 
purchase_data["Age Ranges"] = pd.cut(purchase_data["Age"], age_bins, labels = group_names)

# Run basic calculations 
age_purchase_total = purchase_data.groupby(["Age Ranges"]).sum()["Price"].rename("Total Purchase Value")
age_avg = purchase_data.groupby(["Age Ranges"]).mean()["Price"].rename("Average Purchase Price")
age_counts = purchase_data.groupby(["Age Ranges"]).count()["Price"].rename("Purchase Count")

# Calculate Normalized Purchasing
normalized_total = age_purchase_total / age_demo["Total Count"]

# Convert to DataFrame
age_data = pd.DataFrame({"Purchase Count":  age_counts, "Average Purchase Price": age_avg, "Total Purchase Value": age_purchase_total, "Normalized Totals": normalized_total})

# Minor Data Munging
age_data["Average Purchase Price"] = age_data["Average Purchase Price"].map("${:,.2f}".format)
age_data["Total Purchase Value"] = age_data["Total Purchase Value"].map("${:,.2f}".format)
age_data ["Purchase Count"] = age_data["Purchase Count"].map("{:,}".format)
age_data["Normalized Totals"] = age_data["Normalized Totals"].map("${:,.2f}".format)
age_data = age_data.loc[:, ["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Normalized Totals"]]

# Display Age Table
age_data


# In[35]:


spender = purchase_data.groupby("SN")

top_purchase_count = spender["SN"].count()
avg_spender_price = spender["Price"].mean()
total_spender_purchase = spender["Price"].sum()

# Top spender data frame
top_spender = pd.DataFrame({"Purchase Count": top_purchase_count, "Average Purchase Price": avg_spender_price, "Total Purchase Value": total_spender_purchase})

# display
top_spender


# In[42]:


# Data
item_data = purchase_data.loc[:,["Item ID", "Item Name", "Price"]]

#Basic calc
total_item_purchase = item_data.groupby(["Item ID", "Item Name"]).sum()["Price"].rename("Total Purchase Value")
avg_item_purchase = item_data.groupby(["Item ID", "Item Name"]).mean()["Price"]
item_count = item_data.groupby(["Item ID", "Item Name"]).count()["Price"].rename("Purchase Count")

# Create data frame
item_data_pd = pd.DataFrame({"Total Purchase Value": total_item_purchase, "Item Price": avg_item_purchase, "Purchase Count": item_count})

#Display data frame
item_data_pd.sort_values("Purchase Count", ascending=False).head(5)


# In[44]:


# Data
most_profit_item = item_data_pd.sort_values("Total Purchase Value" , ascending=False)
most_profit_item = item_data_pd.loc[:,["Purchase Count", "Item Price", "Total Purchase Value"]]

# Display data frame
most_profit_item.head(5)


# In[ ]:




