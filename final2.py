# Group 14
# IST256 Fianl Project
# Alden Bohrmann, Maya Alston, Ayana Kerr


#TO-DO
# Import statments
# Create banner for program
# Check input from user to see if valid
# User input schedule year
# BeautifulSoup scrape web for table
# Name columns
# Assign columns for pandas
# Pandas
# Output scraped dataframe
# Search dataframe for specific sport
# Search dataframe for specific event
# Pass event to Wiki API
# Output wikipedia information

# Import staments
import requests #requests module
from bs4 import BeautifulSoup #beautifulsoup module
import pandas as pd #pandas module
import wikipedia #wikipedia API

# Banner
print("\n") #new line
print("Welcome to the Major Leauge Sports Calander Search \n") #banner
print("**Learn more about specific sporting events in a given year!**\n") #banner

# Check to see if the year is between 2011 and 2012
user_input_year = raw_input("Enter Sports Schedule Year (2011-2021): ")

def check_input_year(user_input_year):
    while True:
        try:
            val = int(user_input_year)
            break
        except ValueError:
            print("Sorry that year is not valid, Please Try Again!")

def check_input_range(user_input_year):
    while True:
       if 2011 <= user_input_year <= 2021:
          break
          print("Sorry that year is not valid, Please Try Again!")

check_input_year(user_input_year)
check_input_range(user_input_year)
# BeautifulSoup
year = user_input_year#if a nunmber assigns user_input_year to year variable
url = "http://www.topendsports.com/events/calendar-{y}.htm".format(y=year)#for whatever year the user inputs, {y}.fornmat will replace the year in the URL
r = requests.get(url) #scrape the HTML at the url
soup = BeautifulSoup(r.text, "html.parser") #turn the HTML into a Beautiful Soup object
table = soup.find('table') #find the table in the HTML code
rows = table.findAll('tr') #in the element table, find all 'tr' tags
data = [] #create new blank list name data
header = ['DATE', 'SPORT', 'EVENT', 'LOCATION'] #names of columns, also know as headers in HTML

data = [[td.findChildren(text=True) for td in tr.findAll("td")] for tr in rows] #find all 'tr'/'td' tags
data = data[1:] #first row is blank, so get rid of it

# Value
def get_value(x): #function to get the value, x, and handle the errors
    try:
        return x[0]
    except (TypeError, IndexError):
        return ''

# Column Function
# Apply function to each column to get the value out of the list
# Assigns df to create the panda dataframe
df = pd.DataFrame(data, columns=header)
df['DATE'] = df['DATE'].apply(get_value)
df['SPORT'] = df['SPORT'].apply(get_value)
df['EVENT'] = df['EVENT'].apply(get_value)
df['LOCATION'] = df['LOCATION'].apply(get_value)

# Dataframe Format
pd.set_option('display.expand_frame_repr', False) #prevents dataframe from outputting onto different lines depending on screensize

# Dataframe Print
print("\n")
print(df) # completed table print statement for panda dataframe, df
print("\n")

# Sport Search
while True:
    sport_search = raw_input("Enter sport from list to filter: ").title() #user input for sport search filter
    sport_df = df[df['SPORT'] == sport_search] #check to see if sport exists in dataframe
    if sport_df.empty:
        print("Not a Valid Sport, Please Try Again!")
    else:
        print(sport_df)
        break

# Event Search
while True:
    event_search = raw_input("Enter event title EXACTLY as it is looks find out more: ")  #user input for sport search filter
    event_df = sport_df[sport_df['EVENT'] == event_search] #check to see if sport exists in dataframe
    if event_df.empty:
        print("Not a Valid Event, Please Try Again (Hint: If the event starts with UPPERCASE letters use that! [ex: FIFA]")
        print("\n")
    else:
        break

# Event Search
print("\n") #print line
event_df = sport_df[sport_df['EVENT'] == event_search] #find event in dataframe, column 'event'

# Wikipedia API
wiki_find = wikipedia.page(event_search) #find event that was searched by user on wikipedia
wiki_find.content # extract the content


# Wikipedia Print
wiki_final_output = (wikipedia.summary(event_search)) # print wikipedia findings from user search
print(wiki_final_output)
print("\n")
print("Thanks for using the Major Leauge Sports Calander Search")
print("\n")
