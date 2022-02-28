from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from random import randint
from time import sleep
import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

modal = input('(1)Manual | (2)bin2: ')
path = './bins.txt'

if modal == '2':
    path = '../bin2/bins.txt'
cantidad = '10'

open('./ccs.txt', 'w')

def gen(bin, mm, yy, cvv, cantidad, path):    
    meses = ("", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
             "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")

    # bin = '475869'
    # mm = meses[12]
    # yy = '2024'
    # cvv = '335'
    #sleep(3)

    i_bin = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//input[@id="bin"]'))
    )
    i_bin.clear()

    i_bin.send_keys(bin)
    # print('bin send')

    i_mm = Select(driver.find_element_by_xpath('//select[@id="mes"]')).select_by_visible_text('Aleatorio')
    if mm != 'rnd':
        i_mm = Select(driver.find_element_by_xpath('//select[@id="mes"]')).select_by_visible_text(meses[int(mm.replace('0', ''))])

    i_yy = Select(driver.find_element_by_xpath('//select[@id="anio"]')).select_by_visible_text('Aleatorio')
    if yy != 'rnd':
        i_yy = Select(driver.find_element_by_xpath('//select[@id="anio"]')).select_by_visible_text('20'+yy)

    i_cvv = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//input[@id="ncvv"]'))
    ).clear()
    if cvv != 'rnd':
       i_cvv.send_keys(cvv)
    # print('cvv send')

    i_cantidad = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
             (By.XPATH, '//*[@id="cantidad"]'))
    ).clear()
    
    i_cantidad = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
             (By.XPATH, '//*[@id="cantidad"]'))
    ).send_keys(cantidad)

    btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//button[@id="generar"]'))
    )
    btn.click()
    # print('generated')

    ccs = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//textarea[@id="mostrar"]'))
    )

    gen_ccs = (ccs.get_attribute("value").replace('/', '|'))
    open('./ccs.txt', 'a').write(gen_ccs)
    # print(gen_ccs)

comb = open(path, 'r').read().split('\n')

options = webdriver.FirefoxOptions()
options.headless = True
driver = webdriver.Firefox(executable_path='./drivers/geckodriver', options=options)
driver.get('https://namso.worldofbin.com/')

x = 1
for i in comb:
    if len(i) < 2:
        continue
    c = i.split('|')
    # print(c)
    try:
        cc = c[0]
    except:
        print('invalid bin')
    try:
        mm = c[1]
    except:
        mm = 'rnd'
    try:
        yy = c[2].replace('20', '')
    except:
        yy = 'rnd'
    try:
        cvv = c[3]
    except:
        cvv = 'rnd'

    if len(cc) != 16:
        cc = f'{cc}{"x"*(16-len(cc))}'

    print(f'bin {cc}|{mm}|{yy}|{cvv} => {x} of {len(comb)} generated')
    gen(cc, mm, yy, cvv, cantidad, path)
    x += 1
else:
    pass
    driver.close()

