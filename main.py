from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import requests
from selenium import webdriver

from config import LOGIN, PASSWORD, MAIL_LOGIN, MAIL_PASSWORD

stavka = 0.9

while True:
    params = {
        'query': 'генератор инверторный'
    }
    response = requests.get(
        'https://www.farpost.ru/khabarovsk/dir', params=params)

    if response.text.find('ТРУДЯГА') != -1:

        driver = webdriver.Firefox(executable_path='./geckodriver')
        driver.get('https://www.farpost.ru/sign')
        driver.find_element_by_name('sign').send_keys(LOGIN)
        driver.find_element_by_name('password').send_keys(PASSWORD)
        driver.find_element_by_class_name('signbutton').click()

        driver.find_element_by_class_name('login').click()
        sleep(1)
        driver.find_element_by_link_text('Прайс-лист').click()
        driver.implicitly_wait(5)
        driver.find_element_by_link_text('Управление ставкой').click()
        sleep(1)
        competitor = driver.find_element_by_link_text('trudyagadv')
        opponent_row = competitor.find_element_by_xpath('../../../..')
        print(opponent_row.get_attribute('outerHTML'))
        rate = opponent_row.find_element_by_class_name('rate')
        print(rate)

        sleep(2)
        driver.close()
        exit()
        driver.find_element_by_xpath("//button[@data-value='+']").click()
        driver.find_element_by_class_name('save').click()
        driver.close()
        stavka += 0.1  # прибавляем к счётчику ставки для отображения в письме
        print('Установлена ставка: ', stavka)

        # Настройки e-mail
        mail_sender = 'stroykinkhv2@gmail.com'
        mail_receiver = ['adm223@yandex.ru', 'tva@dvtools.ru']
        username = MAIL_LOGIN
        server = smtplib.SMTP('smtp.gmail.com:587')

        # Формируем тело письма
        subject = u'Ставка на Farpost ' + str(stavka)
        body = u'Отправка письма by Python '
        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')

        # Отпавляем письмо
        server.starttls()
        server.ehlo()
        server.login(MAIL_LOGIN, MAIL_PASSWORD)
        # server.sendmail(mail_sender, mail_receiver, msg.as_string())
        server.quit()
        sleep(240)
    else:
        sleep(140)
