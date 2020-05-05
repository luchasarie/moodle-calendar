from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import codecs
import difflib

driver = webdriver.Chrome(ChromeDriverManager().install())
# TO-DO
# ADD SPECIAL CASE FOR PROD TEXTO
# ADD QUIZZES
# MAKE LISTS BETTER
# Sets up links
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
# texto = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4148" - REMOVED FROM LIST
ingles = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4278"
literatura = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4149"
quimica = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4150"
sociologia = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=4151"
tecnico1 = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=3703"
tecnico2 = "https://ead.fecap.br/moodleFECAPCol/course/view.php?id=3704"

links = [algebra, biologia, edfisica, empreend, filosofia, fisica, geografia, geometria, gramatica, historia, ingles,
         literatura, quimica, sociologia, tecnico1, tecnico2]
print(links)

print("Logging in...")
driver.get(mainlogin)
loginform = driver.find_element_by_id("login_username")
loginform.send_keys("18010153")
passwordform = driver.find_element_by_id("login_password")
passwordform.send_keys("16092002")
passwordform.send_keys(Keys.RETURN)

print("Setting up variables...")
assigned = list()
quizzed = list()

def assignment_check(subject):
    driver.get(subject)
    assign = driver.find_elements_by_css_selector("[href*='/assign']")
    for x in range(len(assign)):
        var1 = assign[x].get_attribute('href')
        assigned.append(var1)

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
                    print("Assignment Found!")
                    print("Link: " + href)
                    print("Subject: " + subject)
                    print("Title: " + title)
                    print("Date: " + time_remaining)



def quiz_check(subject):
    driver.get(subject)  # Enters the subject's Link
    quiz = driver.find_elements_by_css_selector("[href*='/quiz']")  # Gets all assignments in a page
    for x in range(len(quiz)):  # Appends all links to a list.
        var1 = quiz[x].get_attribute('href')
        quizzed.append(var1)


def quizz_date_check():
    for x in range(len(quizzed)):
        href = assigned[x]
        driver.get(href)


for x in range(len(links)):
    assignment_check(links[x])
    quiz_check(links[x])


print(quizzed)
assignment_date_check()