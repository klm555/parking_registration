# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 18:22:31 2022
@author: hwlee

Install Dependencies
------------
conda install spyder
conda install pyqt5? (pip install PyQt5)
pip install -c conda-forge selenium
pip install webdriver_manager
pip install cx_Freeze --upgrade

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import CREATE_NO_WINDOW
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSettings, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5 import uic # ui 파일을 사용하기 위한 모듈

#%% UI CONNECTION

# .ui 파일을 class 형태로 load
UI_class = uic.loadUiType('parking_registration.ui')[0]

class WindowClass(QMainWindow, UI_class): # 화면 띄우는데 사용되는 class 선언
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.setWindowIcon(QIcon('./images/parking_icon.png')) # icon 설정
        
        self.setting = QSettings('App', "Car Number") # 차 번호 기억하기
        self.car_num_input_box.setText(self.setting.value('text box'))
        
        self.reg_btn.clicked.connect(self.crawling_fn) # 버튼 누르면 실행
        self.cancel_btn.clicked.connect(self.close) # 취소 누르면 꺼짐
        self.pw_input_box.setEchoMode(QLineEdit.Password) # password 안보이게 설정
        
        self.setting.setValue('text box', self.car_num_input_box.text()) # 차량 번호 저장
        
#%% AUTOMATIC EXECUTION

    def crawling_fn(self):
              
        # 경고창 처리
        try:
            
            # 현재 크롬 버전에 맞게 ChromeDriver 자동 설치
            service = Service(ChromeDriverManager().install())
            # service.creationflags = CREATE_NO_WINDOW # ChromeDriver 설치할 때 콘솔창 뜨지 않게 해줌
            driver = webdriver.Chrome(service=service)
            
            # 로그인 페이지
            driver.get('http://ajhkic.asuscomm.com/discount/carSearch.cs')
            driver.implicitly_wait(15) # 페이지 다 뜰 때 까지 기다림
            
            driver.find_element(By.ID, 'name').send_keys(self.id_input_box.text()) # ID
            driver.find_element(By.ID, 'pwd').send_keys(self.pw_input_box.text()) # PW
            driver.find_element(By.XPATH, '/html/body/form/table[1]\
                                /tbody/tr[3]/td[2]/input').click() # 로그인 버튼
            
            # 차량 조회 페이지
            # 차량번호
            driver.find_element(By.ID, 'carNumber').send_keys(self.car_num_input_box.text())
            driver.find_element(By.XPATH, '/html/body/table[2]/tbody\
                                /tr[5]/td/input').click() # 조회버튼
            driver.implicitly_wait(10)            
            
            # 무료 등록 페이지
            # 2시간 무료 버튼
            try: 
                driver.find_element(By.ID, 'BTN_2시간무료 (방문차량)').click()
                
                # WebDriverWait(driver, 3).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept() # 경고창 확인버튼            
                time.sleep(2) # 이거 안 설정해주면, 등록이 안됨...
                
                self.reg_status_label.setText('등록 성공!')
                
            except: self.reg_status_label.setText('이미 등록됨')
            
        except: self.reg_status_label.setText('등록 실패!')

#%% UI CONNECTION

if __name__ == '__main__':
    
    app = QApplication(sys.argv) # QApplication : 프로그램을 실행시켜주는 class
    mywindow = WindowClass() # WindowClass의 인스턴스 생성   
    mywindow.show() # 프로그램 보여주기
    app.exec_() # 프로그램을 작동시키는 코드