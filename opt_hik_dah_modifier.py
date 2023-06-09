from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
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
import configparser
import random
options = webdriver.ChromeOptions()
#options.add_argument("--no-sandbox")
#options.add_argument("--headless")
#driver = webdriver.Chrome(service=Service(executable_path="chromedriver"), options=options)
driver = webdriver.Chrome(ChromeDriverManager().install())

config = configparser.ConfigParser()
config.read("cam_config.ini") 
pass_to_cam = config["pass"]["pass_to_cam"]
new_pass_to_cam = config["pass"]["new_pass_to_cam"]
file_path_suc = config["path_to_file"]["file_path_suc"]
file_path_fail = config["path_to_file"]["file_path_fail"]
optimus_path_fail = config["path_to_file"]["optimus_path_fail"]
dahua_path_fail = config["path_to_file"]["dahua_path_fail"]
hikvision_path_file = config["path_to_file"]["hikvision_path_file"]
ntp_address = config["ntp"]["ntp_address"]


chars = '_abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
def password_gen(length = 8):
    password =''
    for i in range(length):
        password += random.choice(chars)
    return password

# with open('cameras.txt', 'r') as f:
with open('test.txt', 'r') as f:
    cameras_ip = f.read().splitlines()

def dahua_ntp_snmp(cam):
    try:
        dahua_login = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_user"]')))
        dahua_login.send_keys('admin')
        el2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_psw"]')))
        el2.send_keys(pass_to_cam)
        el2.send_keys(Keys.RETURN)
        try: 
            settings = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/ul/li[6]/span')))
            settings.click()
        except:
            settings = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/ul/li[8]/span')))
            ActionChains(driver).move_to_element(settings).click(settings).perform()        
        time.sleep(3)
        try:
            system_menu = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="set-menu"]/li[5]/a/span'))) 
            driver.execute_script("arguments[0].click();", system_menu)
            time.sleep(3)
            system_basic = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="set-menu"]/li[5]/ul/li[1]/span')))
            system_basic.click()
            system_date = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, ' //*[@id="page_generalConfig"]/ul/li[2]')))
            system_date.click()   
            dahua_time_zone = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="gen_timeZone"]')))
            dahua_time_zone.click()
            dahua_time_zone_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[8]/div[1]/div[2]/div/div[2]/div/div[2]/div[3]/select/option[118]'))) 
            time.sleep(2)
            driver.execute_script("arguments[0].click();", dahua_time_zone_select)
            time.sleep(2)
            ntp_checkbox_form = driver.find_element("xpath", '//*[@id="gen_NTPEnable"]')
            if ntp_checkbox_form.is_selected():
                pass
            else:
                ntp_checkbox_form.click()
            ntp = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="gen_NTPServer"]')))
            ntp.send_keys(Keys.CONTROL + "a")
            ntp.send_keys(Keys.DELETE)        
            ntp.send_keys(ntp_address)
            try:
                accept_save = driver.find_element("xpath",'//*[@id="page_generalConfig"]/div/div[2]/div[15]/a[3]') 
            except:
                accept_save = driver.find_element("xpath", '/html/body/div[2]/div[2]/div[8]/div[1]/div[2]/div/div[2]/div/div[2]/div[17]/a[3]')
            accept_save.click()
            time.sleep(3)  
            ntp_yes = driver.find_element("xpath",'/html/body/div[16]/div[3]/a[1]') 
            ntp_yes.click()
            with open(file_path_suc, 'a') as file:
                print(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), cam, "dahua ntp enabled", file = file)
        except:
            pass
        # PArt for changing pass
        time.sleep(1)
        dahua_acc_manager = driver.find_element("xpath", '/html/body/div[2]/div[2]/div[6]/div[1]/div[1]/ul/li[5]/ul/li[2]/span')
        dahua_acc_manager.click()
        time.sleep(1)
        dahua_redact_user = driver.find_element("xpath", '/html/body/div[2]/div[2]/div[6]/div[1]/div[2]/div/div[3]/div/div[1]/div[2]/div[1]/div[1]/div/div[2]/table/tbody/tr/td[5]/i')
        dahua_redact_user.click()
        time.sleep(1)
        dahua_change_pass = driver.find_element("xpath", '//*[@id="use_EUserChkPwd"]')
        dahua_change_pass.click()        
        dahua_old_login = driver.find_element("xpath", '//*[@id="use_EUserOPwd"]')
        dahua_old_login.send_keys(pass_to_cam)
        dahua_new_pass = driver.find_element("xpath", '//*[@id="use_EUserNPwd"]')
        dahua_new_pass.send_keys(new_pass_to_cam)
        dahua_acc_pass = driver.find_element("xpath", '//*[@id="use_EUserPwdCfm"]')
        dahua_acc_pass.send_keys(new_pass_to_cam)        
        dahua_accept_save = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[20]/div[3]/a[1]')))
        dahua_accept_save.click()
        with open(file_path_suc, 'a') as file:
            print(cam, new_pass_to_cam, file = file)        

        try:
            net = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="set-menu"]/li[2]/a/span')))
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
            try:
                accept_save = driver.find_element("xpath", '//*[@id="snmp_tip_dialog"]/div[3]/div/a[1]')
            except:
                accept_save = driver.find_element("xpath", '/html/body/div[18]/div[3]/div/a[1]')            
            accept_save.click()
            time.sleep(1)
            try:
                dialog = driver.find_element("xpath", '//*[@id="ui-id-1"]/div[16]/div[3]/a[1]')
            except:
                try:
                    dialog = driver.find_element("xpath", '//*[@id="ui-id-1"]/div[18]/div[3]/a[1]')
                except:
                    dialog = driver.find_element("xpath", '//*[@id="ui-id-1"]/div[19]/div[3]/a[1]')
            dialog.click()
            with open(file_path_suc, 'a') as file:
                print(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), cam, "dahua snmp v2 enabled", file = file)
        except:
            pass

    except Exception as exc:
        with open(dahua_path_fail, 'a') as file:
            print(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), cam, "FAILED because", exc, file = file)

def hikvision(link_to_cam):
    try:
        hik_login = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH,'//*[@id="username"]')))
        hik_login.send_keys('admin')
        hik_passw = driver.find_element("xpath", '//*[@id="password"]')
        hik_passw.send_keys(pass_to_cam)
        hik_passw.send_keys(Keys.RETURN)
        hik_settings = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="nav"]/li[5]/a')))
        hik_settings.click()
        time.sleep(3)
        try:
            hik_time_setup = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ui-id-2"]')))
            driver.execute_script("arguments[0].click();", hik_time_setup)
            hik_time_zone = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="settingTime"]/div/div[1]/span[2]/select')))
            hik_time_zone.click()
            hik_time_zone_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="settingTime"]/div/div[1]/span[2]/select/option[31]')))
            hik_time_zone_select.click()
            hik_ntp_check = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="radioNTP"]'))) 
            driver.execute_script("arguments[0].click();", hik_ntp_check)
            hik_ntp = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="settingTime"]/div/div[2]/div[3]/span[2]/input')))
            hik_ntp.send_keys(Keys.CONTROL + "a")
            hik_ntp.send_keys(Keys.DELETE)        
            hik_ntp.send_keys(ntp_address)
            hik_ntp.send_keys(Keys.RETURN)
            try:
                hik_accept_save = driver.find_element("xpath", '/html/body/div[4]/div[1]/div/div/div[2]/div/button')
            except:
                hik_accept_save = driver.find_element("xpath", '/html/body/div[4]/div[1]/div/div/div[2]/div/button/span[2]')
            driver.execute_script("arguments[0].click();", hik_accept_save)
            time.sleep(2)        
            with open(file_path_suc, 'a') as file:
                print(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), link_to_cam, "hikvision ntp enabled", file = file)
        except Exception as exc:
            with open(hikvision_path_file, 'a') as file:
                print(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), link_to_cam, "FAILED because", exc, file = file)
       # place for change pass
        time.sleep(3)
        hik_acc_manager = driver.find_element("xpath", '//*[@id="menu"]/div/div[2]/div[6]/span')
        hik_acc_manager.click()
        time.sleep(1)
        try:                
            hik_admin = driver.find_element("xpath", '//*[@id="tableUser"]/div/div[2]/div/span[2]/pre')
            hik_admin.click()
            time.sleep(1)
        except:
            hik_admin = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tableUser"]/div/div[2]/div/span[2]')))
            hik_admin.click()
            time.sleep(1)
        hik_redact_user = driver.find_element("xpath", '//*[@id="userManage"]/div[1]/div[1]/span[2]/button[2]')
        hik_redact_user.click()
        time.sleep(1)
        hik_old_login = driver.find_element("xpath", '//*[@id="userDlg"]/div[4]/div[1]/span[2]/input')
        hik_old_login.send_keys(pass_to_cam)
        hik_new_pass = driver.find_element("xpath", '//*[@id="userDlg"]/div[4]/div[2]/span[2]/input')
        hik_new_pass.send_keys(new_pass_to_cam)
        hik_acc_pass = driver.find_element("xpath", '//*[@id="userDlg"]/div[4]/div[4]/span[2]/input')
        hik_acc_pass.send_keys(new_pass_to_cam)        
        hik_accept_save = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="config"]/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]')))
        hik_accept_save.click()
        time.sleep(1)
        try:
            hik_exit = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header"]/div/div[2]/div[5]')))
            hik_exit.click()
        except:
            hik_exit = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="header"]/div/div[2]/div[4]')))
            hik_exit.click()
        try:
            hik_exit_ok = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="config"]/div[2]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]')))
            hik_exit_ok.click()
        except:
            hik_exit_ok = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/table/tbody/tr[2]/td[2]/div/table/tbody/tr[3]/td/div/button[1]')))
            hik_exit_ok.click()    
        with open(file_path_suc, 'a') as file:
            print(link_to_cam, new_pass_to_cam, file = file)        
    except Exception as exc:
        with open(hikvision_path_file, 'a') as file:
            print(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), link_to_cam, "FAILED because", exc, file = file)
def optimus_snmp_ntp(cam):
    try:
        driver.get("http://" + cam)
        opt_login = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[1]/div/div/input')))
        opt_login.send_keys('admin')
        time.sleep(1)
        opt_passw = driver.find_element("xpath", '/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/input')
        opt_passw.send_keys(pass_to_cam)
        time.sleep(1)
        opt_passw.send_keys(Keys.RETURN) 
        opt_settings = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mainContainer"]/section/header/div[2]/div/div[1]/div/ul/li[1]/div')))
        driver.execute_script("arguments[0].click();", opt_settings)
        try:
            # Place to change ntp and snmp
            time.sleep(1)
            opt_basic = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="remoteSetting"]/section/aside/div/div[6]/div[2]/div/ul/li[1]')))
            driver.execute_script("arguments[0].click();", opt_basic)
            time.sleep(1)
            opt_time = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div[3]/div/div/section/main/div[6]/div/div[1]/ul/li[1]')))
            driver.execute_script("arguments[0].click();", opt_time)
            time.sleep(1)
            opt_timezone = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div[3]/div/div/section/main/div[7]/div[1]/div/div/div[3]/div/div/div/input')))
            driver.execute_script("arguments[0].click();", opt_timezone)        
            opt_timezone_select = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div[1]/ul/li[31]')))
            driver.execute_script("arguments[0].click();", opt_timezone_select)        
            try:
                opt_select = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div[3]/div/div/section/main/div[7]/div[1]/div/div/div[6]/div/div[1]/div[1]/input')))
                opt_select.click()
                opt_select_user = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[5]/div[1]/div[1]/ul/li[4]/span')))
                opt_select_user.click()
                opt_ntp = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="subPage"]/div[1]/div/div/div[6]/div/div[2]/input')))        
            except:
                opt_ntp = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="subPage"]/div[1]/div/div/div[6]/div/div[2]/input')))
            opt_ntp.send_keys(Keys.CONTROL + "a")
            opt_ntp.send_keys(Keys.DELETE)
            opt_ntp.send_keys(ntp_address)
            opt_accept_save = driver.find_element("xpath", '//*[@id="subPage"]/div[2]/div/button[1]')
            driver.execute_script("arguments[0].click();", opt_accept_save)
            time.sleep(7)
            try:
                opt_net_basic = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="remoteSetting"]/section/aside/div/div[4]/div[2]/div/ul/li[1]')))
            except:
                opt_net_basic = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="remoteSetting"]/section/aside/div/div[6]/div[2]/div/ul/li[1]'))) 
            driver.execute_script("arguments[0].click();", opt_net_basic)
            time.sleep(5)
            opt_snmp_menu = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.XPATH, '//*[@id="remoteSetting"]/section/main/div[4]/div/div[1]/ul/li[3]')))
            driver.execute_script("arguments[0].click();", opt_snmp_menu)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", opt_snmp_menu)   
            time.sleep(1)
            opt_snmp_menu.click()             
            try: 
                snmp_checkbox_form = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="subPage"]/div[1]/div/div/div/div[1]/div/div/span'))) 
            except:
                snmp_checkbox_form = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/section/div[3]/div/div/section/main/div[7]/div[1]/div/div/div/div[1]/div/div/span')))
            if snmp_checkbox_form.is_selected():
                pass
            else:
                driver.execute_script("arguments[0].click();", snmp_checkbox_form)
            time.sleep(3)
            driver.find_element("xpath", "//div[@class='el-input el-input--suffix']//input[@placeholder='пожалуйста, выбери']").click()
            time.sleep(3)
            driver.find_element("xpath", '//div[@class="el-select-dropdown el-popper"]//ul[@class="el-scrollbar__view el-select-dropdown__list"]/li/span[contains(text(),"V2")]').click()
            trap_address = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="subPage"]/div[1]/div/div/div/div[6]/div/div/input')))
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
        # Place to change pass
        opt_acc_manager = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,'//*[@id="remoteSetting"]/section/aside/div/div[6]/div[2]/div/ul/li[2]')))
        driver.execute_script("arguments[0].click();", opt_acc_manager)
        opt_acc_manager_2 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,'//*[@id="remoteSetting"]/section/main/div[6]/div/div[2]/ul/li')))
        driver.execute_script("arguments[0].click();", opt_acc_manager_2)
        opt_admin = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,'//*[@id="subPage"]/div[1]/div/div/div[1]/div[3]/table/tbody/tr[1]/td[5]/div/i')))
        driver.execute_script("arguments[0].click();", opt_admin)
        time.sleep(1)
        opt_new_pass = driver.find_element("xpath", '/html/body/div[1]/section/div[3]/div/div/section/main/div[7]/div[2]/div/div[2]/div/div/div[2]/div[1]/div/div/input')
        opt_new_pass.send_keys(new_pass_to_cam)
        opt_acc_pass = driver.find_element("xpath", '/html/body/div[1]/section/div[3]/div/div/section/main/div[7]/div[2]/div/div[2]/div/div/div[2]/div[3]/div/div/input')
        opt_acc_pass.send_keys(new_pass_to_cam)        
        opt_accept_save = driver.find_element("xpath", '/html/body/div[1]/section/div[3]/div/div/section/main/div[7]/div[2]/div/div[3]/div/button[1]')
        opt_accept_save.click()
        opt_old_pass = driver.find_element("xpath", '/html/body/div[1]/section/div[3]/div/div/section/main/div[7]/div[2]/div/div[2]/div/div/div/div[1]/input')
        opt_old_pass.send_keys(pass_to_cam)
        opt_old_pass.send_keys(Keys.RETURN)
        with open(file_path_suc, 'a') as file:
            print(cam, new_pass_to_cam, file = file)   
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
                optimus_snmp_ntp(link_to_cam)
            else:
                driver.get("http://" + link_to_cam)
                try:
                    naming = driver.find_element(By.CLASS_NAME, "footer")
                    if re.findall(r'Hikvision', naming.text):
                        hikvision(link_to_cam)
                except:
                    dahua_ntp_snmp(link_to_cam)
        except Exception as exc:
            with open(file_path_fail, 'a') as file:
                print(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), link_to_cam, "FAILED because", exc, file = file)        
    else: 
        with open(file_path_fail, 'a') as file:
            print(datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'), link_to_cam, "unreachable", file = file) 

if __name__ == "__main__":
    for link_to_cam in tqdm(cameras_ip):
        first_look(link_to_cam)
    driver.quit()            
