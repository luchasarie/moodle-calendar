import time
start_time = time.time()
print("Initiating activation sequence.")
from configparser import RawConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import os
driver = webdriver.Chrome(ChromeDriverManager().install())

print("Reading configuration file.")
filename = "config.cfg"
if os.path.isfile(filename):
    parser = RawConfigParser()
    parser.read(filename)
else:
    print("Config file not found")

print("-----------")
print("Welcome to moodle for lazy people version 0.12, developed by Luchas.") 
print("Edit the config.cfg file to add or remove any specific subjects. Does not support lessons not properly set by teachers.")
print("Please Input your username")
username = input()
print("Please Input your password")
password = input()
print("-----------")

print("Setting up links.")
mainlink = parser.get('links', 'mainlink')
subjects = parser.get('links', 'subjects')
links = subjects.split("\n")
links.pop(0)
print(links)

print("Logging in...")
driver.get(mainlink)
loginform = driver.find_element_by_id("login_username")
loginform.send_keys(username)
passwordform = driver.find_element_by_id("login_password")
passwordform.send_keys(password)
passwordform.send_keys(Keys.RETURN)

assigned = list()
quizzed = list()

def both_check(subject):
    driver.get(subject)
    assign = driver.find_elements_by_css_selector("[href*='/assign']")
    for x in range(len(assign)):
        var1 = assign[x].get_attribute('href')
        assigned.append(var1)
    quiz = driver.find_elements_by_css_selector("[href*='/quiz']")
    for x in range(len(quiz)):
        var5 = quiz[x].get_attribute('href')

def assignment_date_check():
    for x in range(len(assigned)):
        href = assigned[x]
        driver.get(href)
        subject = driver.find_element_by_xpath("/html/body/div[3]/header/div/div[1]/nav/nav/ul/li[3]/span[1]/a/span").text
        title = driver.find_element_by_tag_name("h2").text
        col = driver.find_elements_by_tag_name("td")
        for x in range(len(col)):
            time_remaining = col[x].text
            if "horas" in time_remaining:
                if "atrasada" in time_remaining:
                    pass
                elif "enviada" in time_remaining:
                    pass
                else:
                    print("-----------")
                    print("Type: Quiz")
                    print("Link: " + href)
                    print("Subject: " + subject)
                    print("Title: " + title)
                    print("Date: " + time_remaining)

def quiz_date_check():
    for x in range(len(quizzed)):
        href = quizzed[x]
        driver.get(href)
        subject = driver.find_element_by_xpath("/html/body/div[3]/header/div/div[1]/nav/nav/ul/li[3]/span[1]/a/span").text
        titlebox = driver.find_element_by_xpath("//*[@id='region-main']/div/div[1]").text
        if "fechado" in titlebox:
            print("-----------")
            print("Type: Quiz")
            print("Link: " + href)
            print("Subject: " + subject)
            print("Information: " + titlebox)

for x in range(len(links)):
    both_check(links[x])
print("Following assignments found:")
assignment_date_check()
quiz_date_check()
print("Moodle Calendar finalized..")
print("Total Runtime:")
print("--- %s seconds ---" % (time.time() - start_time))