from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from datetime import date
import pandas as pd

#This is the username and password for the login page
USERNAME = "username@gmail.com"
PASSWORD = "password123"

date = date.today() #this was so my URL opened on the current date
LOGIN_URL = "https://somethinghere.com/login" #this is the URL of your LogIn page
URL = f"https://somethinghere.com/schedule#/week?dt={date}&lt=staff" #this is the URL you're scraping (post-login)

#Selenium webdriver will physically open your webpage in (this case) firefox
driver = webdriver.Firefox()
driver.get(LOGIN_URL)

#actually logs the user in with the given USERNAME and PASSWORD from above
def site_open():
    driver.get(LOGIN_URL)
    #"account_email" was found by inspecting HTML on the login page. This may vary by site
    driver.find_element_by_id("account_email").send_keys(USERNAME)
    driver.find_element_by_id("account_password").send_keys(PASSWORD) #Just like account_email, found in HTML
    driver.find_element_by_name("button").click() #login button was called "button" in HTML
    driver.get(URL)
site_open() #run the function definted

#websites need to load, so good idea to sleep your code for around 5 seconds.
sleep(5)
#Every site will return its information formatted differently. This code simply returns the info I wanted.
#BeautifulSoup is very helpful in parsing HTML
html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
soup = BeautifulSoup(html, "lxml")
info = soup.find_all("span", class_="ng-binding")
#in order to not keep your firefox page open, use driver.quit()
driver.quit()


data = [x.string[1:-1] for x in info]

list1 = []
list2 = []

#
for i, x in enumerate(data):
    if i % 2 == 0:
        list1.append(x)
    else:
        list2.append(x)


data = {'tutors': list2, 'session': list1}
df = pd.DataFrame(data)


value_dict = {} #made a dictionary with my data and assigned values..
data2 = {'session': list(value_dict.keys()), 'price': list(value_dict.values())}
df2 = pd.DataFrame.from_dict(data2)

#left table join
week_df = pd.merge(df, df2, on='session', how='left')

total_income = week_df['price'].sum()
print(total_income)

string_income = str(total_income)

