from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time
import os
import datetime
from tqdm import tqdm
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
options = webdriver.ChromeOptions()
#options.add_argument("--no-sandbox")
#options.add_argument("--headless")
#driver = webdriver.Chrome(service=Service(executable_path="/home/milov/python/opt_snmp/chromedriver"), options=options)
driver = webdriver.Chrome(ChromeDriverManager().install())

pass_to_cam = "Lbr650bf"
file_path_suc = "/home/milov/python/opt_snmp/log_snmp_cam_suc.txt"
file_path_fail = "/home/milov/python/opt_snmp/log_snmp_cam_fail.txt"
optimus_path_fail = "/home/milov/python/opt_snmp/log_optimus_snmp_cam_fail.txt"
dahua_path_fail = "/home/milov/python/opt_snmp/log_dahua_snmp_cam_fail.txt"
hikvision_file = "/home/milov/python/opt_snmp/hikvision.txt"

with open('/home/milov/python/opt_snmp/cameras.txt', 'r') as f:
# with open('/home/milov/python/opt_snmp/test.txt', 'r') as f:
    cameras_ip = f.read().splitlines()

def dahua_snmp(cam):
    try:
        # driver.get("http://" + cam)
        el = driver.find_element(By.ID, 'login_user')
        el.send_keys('admin')
        # driver.implicitly_wait(5)
        el2 = driver.find_element(By.ID, 'login_psw')
        el2.send_keys(pass_to_cam)
        el2.send_keys(Keys.RETURN)
        settings = WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/ul/li[6]/span')))
        settings.click()
        net = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="set-menu"]/li[2]/a/span')))
        net.click()
        time.sleep(3)
        try:
            snmp = driver.find_element("xpath", '//*[@title="SNMP"]')
        except:
            snmp = driver.find_element("xpath", '//*[@id="set-menu"]/li[2]/ul/li[7]/span')
        snmp.click()
        time.sleep(3)
        snmp_checkbox_form = driver.find_element("xpath", '//*[@id="snmp_v2_enable"]')
        if snmp_checkbox_form.is_selected():
            pass
        else:
            snmp_checkbox_form.click()
        time.sleep(3)
        snmp_port = driver.find_element("xpath", '//*[@id="page_SNMPConfig"]/div/div/div[3]/input')
        snmp_port.send_keys(Keys.CONTROL + "a")
        snmp_port.send_keys(Keys.DELETE)
        snmp_port.send_keys('161')
        snmp_read = driver.find_element("xpath", '//*[@id="page_SNMPConfig"]/div/div/div[4]/input')
        snmp_read.send_keys(Keys.CONTROL + "a")
        snmp_read.send_keys(Keys.DELETE)
        snmp_read.send_keys('public')
        snmp_write = driver.find_element("xpath", '//*[@id="page_SNMPConfig"]/div/div/div[5]/input')
        snmp_write.send_keys(Keys.CONTROL + "a")
        snmp_write.send_keys(Keys.DELETE)
        snmp_write.send_keys('private')
        trap_address = driver.find_element("xpath", '//*[@id="page_SNMPConfig"]/div/div/div[6]/input')
        trap_address.send_keys(Keys.CONTROL + "a")
        trap_address.send_keys(Keys.DELETE)
        trap_address.send_keys('192.168.168.2')
        trap_port = driver.find_element("xpath", '//*[@id="page_SNMPConfig"]/div/div/div[7]/input')
        trap_port.send_keys(Keys.CONTROL + "a")
        trap_port.send_keys(Keys.DELETE)
        trap_port.send_keys('162')
        time.sleep(1)
        save_button = driver.find_element("xpath", '//*[@id="page_SNMPConfig"]/div/div/div[10]/a[3]')
        save_button.click()
        time.sleep(1)
        accept_save = driver.find_element("xpath", '//*[@id="snmp_tip_dialog"]/div[3]/div/a[1]')
        accept_save.click()
        time.sleep(1)
        try:
            dialog = driver.find_element("xpath", '//*[@id="ui-id-1"]/div[16]/div[3]/a[1]')
        except:
            dialog = driver.find_element("xpath", '//*[@id="ui-id-1"]/div[18]/div[3]/a[1]')
        dialog.click()
        with open(file_path_suc, 'a') as file:
            print(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), cam, "dahua snmp v2 enabled", file = file)
    except Exception as exc:
        with open(dahua_path_fail, 'a') as file:
            print(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), cam, "FAILED because", exc, file = file)


def optimus_snmp(cam):
    try:
        driver.get("http://" + cam)
        opt_login = WebDriverWait(driver, 25).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div/input')))
        opt_login.send_keys('admin')
        time.sleep(1)
        opt_passw = driver.find_element("xpath", '/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/input')
        opt_passw.send_keys(pass_to_cam)
        time.sleep(1)
        opt_passw.send_keys(Keys.RETURN) 
        opt_settings = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="mainContainer"]/section/header/div[2]/div/div[1]/div/ul/li[1]/div')))
        opt_settings.click()
        try:
            opt_net_basic = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="remoteSetting"]/section/aside/div/div[4]/div[2]/div/ul/li[1]')))
            opt_net_basic.click()
            time.sleep(1)
        except:
            opt_net_basic = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="remoteSetting"]/section/aside/div/div[6]/div[2]/div/ul/li[1]'))) 
            opt_net_basic.click()
            time.sleep(1)
        opt_snmp_menu = driver.find_element("xpath", '//*[@id="remoteSetting"]/section/main/div[4]/div/div[1]/ul/li[3]') 
        opt_snmp_menu.click()
        snmp_checkbox_form = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="subPage"]/div[1]/div/div/div/div[1]/div/div/span')))
        if snmp_checkbox_form.is_selected():
            pass
        else:
            snmp_checkbox_form.click()
        time.sleep(3)
        driver.find_element("xpath", "//div[@class='el-input el-input--suffix']//input[@placeholder='пожалуйста, выбери']").click()
        time.sleep(3)
        driver.find_element("xpath", '//div[@class="el-select-dropdown el-popper"]//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li/span[contains(text(),"V2")]').click()
        trap_address = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="subPage"]/div[1]/div/div/div/div[6]/div/div/input')))
        trap_address.send_keys(Keys.CONTROL + "a")
        trap_address.send_keys(Keys.DELETE)
        trap_address.send_keys('192.168.168.2')
        opt_accept_save = driver.find_element("xpath", '//*[@id="subPage"]/div[2]/div/button[1]')
        opt_accept_save.click()
        with open(file_path_suc, 'a') as file:
            print(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), cam, "optimus snmp v2 enabled", file = file)
        
    except Exception as exc:
        with open(optimus_path_fail, 'a') as file:
            print(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), cam, "FAILED because", exc, file = file)

def first_look(link_to_cam):
    response = os.system("fping " + link_to_cam + " >/dev/null")
    if response == 0:
        try: 
            page = urlopen("http://" + link_to_cam)
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            if soup.title.string == "webpackSPA":
                optimus_snmp(link_to_cam)
            else:
                driver.get("http://" + link_to_cam)
                try:
                    naming = driver.find_element(By.CLASS_NAME, "footer")
                    if re.findall(r'Hikvision', naming.text):
                        with open(hikvision_file, 'a') as file:
                            print(link_to_cam, file = file)
                except:
                    dahua_snmp(link_to_cam)
        except Exception as exc:
            with open(file_path_fail, 'a') as file:
                print(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), link_to_cam, "FAILED because", exc, file = file)        
    else: 
        with open(file_path_fail, 'a') as file:
            print(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), link_to_cam, "unreachable", file = file) 
for link_to_cam in tqdm(cameras_ip):
    first_look(link_to_cam)

driver.quit()            
