from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time

from classes import Class, Email

import config

# Configuring the browser
options = webdriver.ChromeOptions()
options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"

service = Service(executable_path="D:/Coding/Sick-Day-Notice/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service)

# Your email information
myEmail = config.EMAIL
myPassword = config.PASSWORD

# Setup classes
CAS100 = Class('Testa', 'CAS 100A, Section 003: Effective Speech (22411--AB---P-CAS-----100A------003-)', ['monday', 'wednesday', 'friday'])
CMPSC132 = Class('Ganther', 'CMPSC 132, Section 003: PROG & COMP II (22411--AB---P-CMPSC---132-------003-)', ['monday', 'wednesday', 'friday'])
MATH141 = Class('Shwe', 'MATH 141, Section 009: CALC ANLY GEOM II (22411--AB---P-MATH----141-------009-)', ['monday', 'wednesday', 'friday'])
PHYS211 = Class('Pearson', 'PHYS 211, Section 006: Mechanics (22411--AB---P-PHYS----211-------006-)', ['tuesday', 'thursday'])
GAME251 = Class('KHALIQ', 'GAME 251, Section 001: 2D Web Game Dev (22411--AB---P-GAME----251-------001-)', ['tuesday', 'thursday'])

classes = [ CAS100, CMPSC132, MATH141, PHYS211, GAME251]
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']

myName = 'Bashir Hilaly'

# Note templates
medical = Email(subject="Absence from [Course Name] on [Date]", 
                body="Dear Professor [Name],\n\nI hope this email finds you well. Unfortunately, due to unforeseen circumstances, I won't be able to attend [Course Name] on [Date]. I have a doctor's appointment that I cannot reschedule.\n\nI apologize for any inconvenience this may cause and kindly request any materials or assignments I'll miss during my absence. I'll make sure to catch up promptly.\n\nThank you for your understanding.\n\nSincerely,\n[Your Full Name]")
personal = Email("Absence Notification for [Course Name]", "Dear Professor [Last Name],\n\nI regret to inform you that I won't be able to attend [Course Name] on [Date]. A family emergency has arisen, and I need to be away from campus.\n\nI kindly request any information or assignments I'll miss during my absence. I'll do my best to catch up as soon as possible.\n\nThank you for your consideration.\n\nBest regards,\n[Your Full Name]")

if __name__ == '__main__':

    daysAbsentInput = input("What days will you be absent?")
    daysAbsent = []

    for day in days:
        if not daysAbsentInput.find(day):
            daysAbsent.append(day)

    Note = None
    inputValid = False

    while inputValid == False:
        customOrNot = input('\nEnter 1 for medical, 2 for personal emergency, 3 for custom: ')
        if customOrNot == '1':
            Note = medical
            inputValid = True
        elif customOrNot == '2':
            Note = personal
            inputValid = True
        elif customOrNot == '3':
            # Create Note
            subject = input("Type your Subject: ")
            body = input(r'Type your body (use "\n" for new lines): ')
            Note = Email(subject, body)
            inputValid = True
        else:
            print('\nInvalid Input')
            inputValid = False
    
    # Now loop through classes for the day
    # Check what days you are absent
    classesYouWillMiss = []
    for _class in classes:
        for day in daysAbsent:
            if day in _class.getDays():
                classesYouWillMiss.append(_class)

    print("\n\nClasses: ")
    for i in classesYouWillMiss:
        print(i.getCourse())



    print("LOGGING YOU IN!\nBE READY TO SHARE YOUR VERIFICATION CODE")

    # Login to your university email (may require two step authentication so have phone nearby)
    driver.get("""https://psu.instructure.com/""")

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "loginfmt"))
    )

    # Input your email to login
    emailForm = driver.find_element(By.NAME, "loginfmt")
    emailForm.clear()
    emailForm.send_keys(myEmail + Keys.ENTER)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "passwd"))
    )
    time.sleep(3)
    # Input password
    passwordForm = driver.find_element(By.NAME, "passwd")
    passwordForm.clear()
    passwordForm.send_keys(myPassword + Keys.ENTER)

    # Verify identity with using text msg
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div"))
    )

    # Input password
    text = driver.find_element(By.XPATH, "/html/body/div/form[1]/div/div/div[2]/div[1]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div/div[1]/div/div/div[2]/div")
    text.click()

    time.sleep(5)

    verificationCode = input("Input Verification Code: ")

    # Verify identity with using text msg
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "otc"))
    )

    # Input password
    code = driver.find_element(By.NAME, "otc")
    code.clear()
    code.send_keys(verificationCode + Keys.ENTER)

    time.sleep(2)

    
    # TESTING IN PRODUCTION WE WILL LOOP THROUGH CLASSES AND RUN THIS
    for _class in classesYouWillMiss:
        driver.get("""https://psu.instructure.com/""")
        # Go to inbox
        driver.get("""https://psu.instructure.com/conversations#filter=type=inbox""")
        # Click compose
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div/span[1]/div/div/span/span[4]/span/span[1]/span/span/button"))
        )
        compose = driver.find_element(By.XPATH, "/html/body/div[3]/div[2]/div/div[2]/div[1]/div/div[2]/div/span[1]/div/div/span/span[4]/span/span[1]/span/span/button")
        compose.click()
        # Select course
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "Select_2"))
        )
        course = driver.find_element(By.ID, "Select_2")
        course.clear()
        course.send_keys(_class.getCourseName() + Keys.ENTER)
        # Select teacher
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "TextInput_4"))
        )
        teacher = driver.find_element(By.ID, "TextInput_4")
        teacher.click()
        time.sleep(1)
        teacher.send_keys(Keys.ENTER)
        time.sleep(2)
        teacher.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        teacher.send_keys(Keys.ENTER)

        # Editing the template

        # Days absent string
        date = ''
        if len(daysAbsent) > 1:
            for day in daysAbsent:
                date += day
        else:
            date = daysAbsent[0]

        # Write the subject
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "TextInput_5"))
        )
        subject = driver.find_element(By.ID, "TextInput_5")
        subject.clear()
        subject.send_keys(Note.subject.replace('[Course Name]', _class.getCourse()).replace('[Date]', date))

        # Write the body    
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "TextArea_0"))
        )
        body = driver.find_element(By.ID, "TextArea_0")
        body.clear()
        print("Writing: " + Note.body)
        body.send_keys(Note.body.replace('[Name]', myName).replace('[Course Name]', _class.getCourse()).replace('[Date]', date).replace('[Your Full Name]', myName))



    time.sleep(10)

    driver.quit()