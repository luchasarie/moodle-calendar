from PyQt5 import QtWidgets
from configparser import RawConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import sys
import os
import qtmodern.styles
import qtmodern.windows
import time

assigned = list()
quizzed = list()
driver = webdriver.Chrome(ChromeDriverManager().install())

def check(subject):
    driver.get(subject)
    assign = driver.find_elements_by_css_selector("[href*='/assign']")
    for x in range(len(assign)):
        var1 = assign[x].get_attribute('href')
        assigned.append(var1)
    quiz = driver.find_elements_by_css_selector("[href*='/quiz']")
    for x in range(len(quiz)):
        var2 = quiz[x].get_attribute('href')
        quizzed.append(var2)

class window(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Moodle Calendar')
        tabWidget = QtWidgets.QTabWidget()
        tabWidget.addTab(mainTab(), "Application")
        tabWidget.addTab(configTab(), "Configuration")
        vBox = QtWidgets.QVBoxLayout()
        vBox.addWidget(tabWidget)
        self.setLayout(vBox)

class mainTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        username = QtWidgets.QLabel("Username:")
        self.usernameEdit = QtWidgets.QLineEdit()

        password = QtWidgets.QLabel("Password:")
        self.passwordEdit = QtWidgets.QLineEdit()
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.activateButton = QtWidgets.QPushButton("Start")
        self.activateButton.clicked.connect(self.activate)

        self.terminalBox = QtWidgets.QTextEdit()
        self.terminalBox.setReadOnly(True)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(username)
        layout.addWidget(self.usernameEdit)
        layout.addWidget(password)
        layout.addWidget(self.passwordEdit)
        layout.addWidget(self.activateButton)
        layout.addWidget(self.terminalBox)
        self.setLayout(layout)
    
    def assignment_date_check(self):
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
                        self.terminalBox.append("-----------")
                        self.terminalBox.append("Title: " + title)
                        self.terminalBox.append("Type: Quiz")
                        self.terminalBox.append("Link: " + href)
                        self.terminalBox.append("Subject: " + subject)
                        self.terminalBox.append("Date: " + time_remaining)
                        QtWidgets.qApp.processEvents()

    def quiz_date_check(self):
        for x in range(len(quizzed)):
            href = quizzed[x]
            driver.get(href)
            title = driver.find_element_by_tag_name("h2").text
            subject = driver.find_element_by_xpath("/html/body/div[3]/header/div/div[1]/nav/nav/ul/li[3]/span[1]/a/span").text
            titlebox = driver.find_element_by_xpath("//*[@id='region-main']/div/div[1]").text
            if "fechado" in titlebox:
                self.terminalBox.append("-----------")
                self.terminalBox.append("Title: " + title)
                self.terminalBox.append("Type: Quiz")
                self.terminalBox.append("Link: " + href)
                self.terminalBox.append("Subject: " + subject)
                self.terminalBox.append("Information: " + titlebox)
                QtWidgets.qApp.processEvents()

    def activate(self):
        start_time = time.time()
        self.activateButton.setText('Started. Please Wait.')
        self.terminalBox.append("-----------")
        self.terminalBox.append("Welcome to moodle for lazy people version 0.12, developed by Luchas.") 
        self.terminalBox.append("Edit the config.cfg file to add or remove any specific subjects. Does not support lessons not properly set by teachers.")
        self.terminalBox.append("-----------")
        self.terminalBox.append("Setting up username and password.")
        QtWidgets.qApp.processEvents()
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        self.terminalBox.append("Reading Configuration File")
        QtWidgets.qApp.processEvents()
        filename = "config.cfg"
        if os.path.isfile(filename):
            parser = RawConfigParser()
            parser.read(filename)
        else:
            self.terminalBox.append("Config file not found")
            return
        self.terminalBox.append("Setting up Links")
        QtWidgets.qApp.processEvents()
        mainlink = parser.get('links', 'mainlink')
        subjects = parser.get('links', 'subjects')
        links = subjects.split("\n")
        links.pop(0)
        driver.get(mainlink)
        self.terminalBox.append("Logging In.")
        QtWidgets.qApp.processEvents()
        loginform = driver.find_element_by_id("login_username")
        loginform.send_keys(username)
        passwordform = driver.find_element_by_id("login_password")
        passwordform.send_keys(password)
        passwordform.send_keys(Keys.RETURN)
        for x in range(len(links)):
            check(links[x])
        self.terminalBox.append("Following assignments found:")
        self.assignment_date_check()
        self.quiz_date_check()
        self.activateButton.setText('Finished')
        self.terminalBox.append("Total Runtime:")
        self.terminalBox.append("--- %s seconds ---" % (time.time() - start_time))
        driver.close()

class configTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()

        self.textEdit = QtWidgets.QTextEdit()
        text=open('config.cfg').read()
        self.textEdit.setPlainText(text)

        self.saveButton = QtWidgets.QPushButton('Save')
        self.saveButton.clicked.connect(self.saveFile)

        layout.addWidget(self.saveButton)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)

    def saveFile(self):
        text2 = self.textEdit.toPlainText()
        with open('config.cfg', 'w') as f:
            f.write(text2)
        self.saveButton.setText('Saved!')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = window()
    qtmodern.styles.dark(app)
    mw = qtmodern.windows.ModernWindow(win)
    mw.show()
    sys.exit(app.exec_())