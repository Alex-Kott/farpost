from time import sleep
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import requests
from selenium import webdriver

from config import LOGIN, PASSWORD, MAIL_LOGIN, MAIL_PASSWORD


def send_mail_notification(rate):
    addressees = ['adm223@yandex.ru', 'tva@dvtools.ru']
    server = smtplib.SMTP('smtp.gmail.com:587')

    # Формируем тело письма
    subject = u'Ставка на Farpost ' + str(rate)
    body = u'Уведомление об изменении ставки'
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    # Отпавляем письмо
    server.starttls()
    server.ehlo()
    server.login(MAIL_LOGIN, MAIL_PASSWORD)
    server.sendmail(MAIL_LOGIN, addressees, msg.as_string())
    server.quit()


if __name__ == "__main__":
    default_rate = 0.9

    while True:
        params = {
            'query': 'генератор инверторный'
        }
        response = requests.get(
            'https://www.farpost.ru/khabarovsk/dir', params=params)

        if response.text.find('ТРУДЯГА') != -1:

            driver = webdriver.Firefox()  # executable_path='./geckodriver'
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
            competitor_rate = float(opponent_row.find_element_by_class_name('rate').text.strip('₽'))

            user_rate = float(driver.find_element_by_class_name('rate-field').get_attribute('value'))

            if competitor_rate > user_rate:
                rate = str(round(competitor_rate + 0.1, 1))
                driver.find_element_by_class_name('rate-field').clear()
                driver.find_element_by_class_name('rate-field').send_keys(rate)
                sleep(1)
                driver.find_element_by_class_name('save-button').click()

                print('Установлена ставка: ', rate)
                send_mail_notification(rate)
                sleep(2)

            sleep(100)
            driver.close()

            sleep(240)
        else:
            sleep(140)
