from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
start_time = time.time()

print("Initiating...")
print("Welcome to moodle for lazy people version 0.12, developed by Luchas. Edit the link of lists to add or remove any specific subjects. Does not support OCR, so it won't detected lessons not properly set by teachers.")

print("Please Input your username")
username = input()
print("Please Input your password")
password = input()

print("-----------")

driver = webdriver.Chrome(ChromeDriverManager().install())

print("Setting up links.")
mainlogin = "https://ead.fecap.br/moodleFECAPCol/" 
algebra = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4139"
biologia = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4140"
edfisica = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4141"
empreend = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4192"
filosofia = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4142"
fisica = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4143"
geografia = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4144"
geometria = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4145"
gramatica = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4146"
historia = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4147"
prodtexto = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4148"
literatura = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4149"
quimica = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4150"
sociologia = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4151"
#ingles = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4278"
#tecnico1 = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=3703"
#tecnico2 = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=3704"

links = [algebra, biologia, edfisica, empreend, filosofia, fisica, geografia, geometria, gramatica, historia, prodtexto, literatura, quimica, sociologia]

print("Logging in...")
driver.get(mainlogin)
loginform = driver.find_element_by_id("login_username")
loginform.send_keys(username)
passwordform = driver.find_element_by_id("login_password")
passwordform.send_keys(password)
passwordform.send_keys(Keys.RETURN)

print("Setting up variables...")
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
        quizzed.append(var5)

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
            print("Link: " + href)
            print("Subject: " + subject)
            print("Information: " + titlebox)

for x in range(len(links)):
    both_check(links[x])

assignment_date_check()
quiz_date_check()
print("Done.")
print("Total Runtime:")
print("--- %s seconds ---" % (time.time() - start_time))