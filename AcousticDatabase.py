import string
import pandas as pd
import numpy as np
import importlib
import json
import io
import os
import glob
import sys
import csv
import sqlite3
import hashlib
import json,re
import psycopg2
import re
import logging
import logging.config
from datetime import datetime, timedelta
from dotmap import DotMap
from PyQt5.QtWebEngineWidgets import QWebEngineView
from psycopg2.extensions import register_adapter, AsIs
import time
import plotly.express as px
import plotly
import webbrowser
import tempfile
import math
import statistics
import random
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import faulthandler
import time
import scipy.stats
import fnmatch
import plotly.graph_objects as go
import connectorx as cx
import plotly.offline as offline
from scipy.stats import f_oneway
from scipy.fft import fft
from scipy.fft import rfft,rfftfreq
from scipy import signal
import matplotlib.pyplot as plt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, QUrl, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

   
class Login_Screen(QDialog):
    def __init__(self):
        super(Login_Screen, self).__init__()
        loadUi(GUI_path+"/frontend/login.ui",self)#"frontend/login.ui"
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.register_2.clicked.connect(self.registerfun)
        self.submit.clicked.connect(self.submitfun)
        directory = os.getcwd()
        print(directory,GUI_path)
        self.label.setStyleSheet(f"background-image : url({GUI_path}/frontend/radar.jpg)")
        #self.label.setStyleSheet(f"background-image : url({directory}/frontend/radar.jpg)")
        self.setTabOrder(self.userid,self.password)
        self.setTabOrder(self.password,self.submit)
        self.setTabOrder(self.submit,self.register_2)
        
        date = datetime. now(). strftime("%Y%m%d_%I%M%S")

    def registerfun(self):
        create = Create_Screen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def submitfun(self):
        us  = self.userid.text()
        ps  = self.password.text()
        if len(us)==0 or len(ps)==0:
            self.login_info.setText("Please input all fields.")
            self.login_info.setStyleSheet("color:red")
        else:
            print("0Successfully logged in.")
            us  = hashlib.sha256(us.encode()).hexdigest()
            ps  = hashlib.sha256(ps.encode()).hexdigest()
            
            db = MyDatabase()
            print("0.5Successfully logged in.")
            pswd = db.userverfy(us)
            print("0.5Successfully logged in.")
            db.close()
            if len(pswd)==0:
                self.login_info.setText("Invalid username or password")
                self.login_info.setStyleSheet("color:red")
            else:
                print("0.5Successfully logged in.")
                if pswd[0][0] == ps:
                    print("1Successfully logged in.")
                    pro = Welcome_Screen()
                    print("2Successfully logged in.")
                    widget.addWidget(pro)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                    #logging.info("Successfully logged in\n")
                    print("Successfully logged in.")
                    self.login_info.setText("")
                else:
                    self.login_info.setText("Invalid username or password")
                    self.login_info.setStyleSheet("color:red")     

                    
                    
class Create_Screen(QDialog):
    def __init__(self):
        super(Create_Screen, self).__init__()
        loadUi(GUI_path+"/frontend/create.ui",self) #"frontend/create.ui"
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.submit.clicked.connect(self.submitfun)
        self.back.clicked.connect(self.backfun)
        self.setTabOrder(self.userid,self.password)
        self.setTabOrder(self.password,self.cf_pass)
        self.setTabOrder(self.cf_pass,self.submit)
        self.setTabOrder(self.submit,self.back)
    
    def backfun(self):
        widget.removeWidget(self)

    def submitfun(self):
        us  = self.userid.text()
        ps  = self.password.text()
        cps = self.cf_pass.text()

        if len(us)==0 or len(ps)==0 or len(cps)==0:
            self.login_info.setText("Please fill in all inputs.")
            self.login_info.setStyleSheet("color:red")
        else:
            us  = hashlib.sha256(us.encode()).hexdigest()
            ps  = hashlib.sha256(ps.encode()).hexdigest()
            cps  = hashlib.sha256(cps.encode()).hexdigest()            
            
            db = MyDatabase()
            pswd = db.userverfy(us)         
            
            if len(pswd)!=0:
                self.login_info.setText("username already exists.")
                self.login_info.setStyleSheet("color:red")
            elif ps!=cps:
                self.login_info.setText("Passwords do not match.")
                self.login_info.setStyleSheet("color:red")
            else:                
                db.adduser(us, ps)                
                self.login_info.setText("Account created.")
                self.login_info.setStyleSheet("color: rgb(29,255,26)")
                
            db.close()

                
                
class Welcome_Screen(QDialog):
    def __init__(self):
        super(Welcome_Screen, self).__init__()
        loadUi(GUI_path+"/frontend/welcome.ui",self)
        #self.setTabOrder(self.label,self.logout)
        self.setTabOrder(self.logout,self.add)
        self.setTabOrder(self.add,self.input)        
        self.setTabOrder(self.input,self.dashboard)
        self.setTabOrder(self.dashboard,self.visualize)
        
        self.add.clicked.connect(self.addfun)        
        self.input.clicked.connect(lambda : self.button_press(2))
        self.dashboard.clicked.connect(self.dashboardfun)
        self.visualize.clicked.connect(self.visualizefun)
        self.logout.clicked.connect(self.Logoutfun)
        self.pop_up.hide()

    def button_press(self, n):
        project_list = []
        with open(GUI_path+'projects.json','r') as input:
            data = json.load(input)
            for project in data.keys():
                project_list.append(project)
                
        if len(project_list)==0:
            self.label_2.setText("No Projects added. Click Continue to add Project Configuration")
            self.pop_up.show()
            self.label_2.setStyleSheet("font-size : 12pt;color: red") 
            self.cont.clicked.connect(self.addfun)
            self.back.clicked.connect(lambda : self.pop_up.hide())
        else:
            self.comboBox.show()
            self.comboBox.clear()
            self.comboBox.addItems(project_list)
            self.pop_up.show()
            self.cont.clicked.connect(lambda : self.cont_press(n))
            self.back.clicked.connect(lambda : self.pop_up.hide())
    
    def cont_press(self, n):
        project_name = self.comboBox.currentText()
        self.pop_up.hide()
        if n == 2:            
            self.inputfun(project_name)

    def addfun(self):
        create = Port_details_Screen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def inputfun(self, name):
        inp = Parser_screen(name)
        widget.addWidget(inp)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def dashboardfun(self):
        dsh = Dashboard_Screen()
        widget.addWidget(dsh)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def visualizefun(self):
        vis = Visualize_Screen()
        widget.addWidget(vis)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def Logoutfun(self):
        widget.removeWidget(self)
        size = widget.count()
        for i in range(size+1):
            widg = widget.widget(size-i)
            widget.removeWidget(widg)
        login = Login_Screen()
        widget.addWidget(login)
        #logging.info("Successfully logged Out\n")
        print("Successfully logged Out.")
        
class PopUp2buttons(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)        
        loadUi(GUI_path+"/frontend/pop_up2.ui",self)
        
        #self.setWindowTitle("Extracting Data")        
        self.ok_button.clicked.connect(self.accept)
        self.not_ok.clicked.connect(self.accept)
        #self.label = QLabel("Extracted: 0%")
        self.setModal(True)  

class PopUpAddtoDB(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)        
        loadUi(GUI_path+"/frontend/pop_upDB.ui",self)
        #self.setWindowTitle("Extracting Data")        
        self.ok_button.clicked.connect(self.accept)
        self.not_ok.clicked.connect(self.accept)
        #self.label = QLabel("Extracted: 0%")
        self.setModal(True) 


class Port_details_Screen(QDialog) :
    def __init__(self):
        super(Port_details_Screen, self).__init__()
        loadUi(GUI_path+"frontend/port_details.ui",self)
        self.submit.clicked.connect(self.submitfun)
        self.addacoustic.clicked.connect(self.addacousticfun)
        self.addmetadata.clicked.connect(self.addmetadatafun)
        self.delacoustic.clicked.connect(self.delacousticfun)
        self.delmetadata.clicked.connect(self.delmetadatafun)        
        self.home.clicked.connect(lambda: exit_popup.exec_())        
                        
        exit_popup= PopUp2buttons(self)
        exit_popup.setWindowTitle("Exit Adding Project")
        exit_popup.not_ok.setText("Cancel") 
        exit_popup.ok_button.setText("Exit")      
        exit_popup.label.setText("Do you really want to exit?\nProject details may not be saved.")
        exit_popup.ok_button.clicked.connect(self.backfun) 
        
        self.packettype_popup= PopUpAddtoDB(self)
        self.packettype_popup.setWindowTitle("Add New Packet Type")             
        self.packettype_popup.label.setText("Add new packet type only if none of current values are matching.")
        self.packettype_popup.ok_button.clicked.connect(self.addpackettype)
        
        self.packetsource_popup= PopUpAddtoDB(self)
        self.packetsource_popup.setWindowTitle("Add New Packet Source")             
        self.packetsource_popup.label.setText("Add new packet source only if none of current values are matching.")
        self.packetsource_popup.ok_button.clicked.connect(self.addpacketsource)
        
        
        self.project = ""
        self.edit0=[]
        self.edit1=[]
        self.edit2=[]
        self.edit3=[]
        self.edit4=[]
        self.edit5=[]
        self.edit6=[]
        self.edit7=[]
        self.edit8=[]
        
        self.edit10=[]
        self.edit11=[]
        self.edit12=[]
        self.edit13=[]
        self.edit14=[]
        self.edit15=[]
        
        self.edit0.append(self.label_10)
        self.edit1.append(self.lineEdit11)
        self.edit2.append(self.lineEdit12)
        self.edit3.append(self.lineEdit13)               
        self.edit4.append(self.comboBox)
        self.edit5.append(self.lineEdit15)        
        self.edit6.append(self.lineEdit16)
        self.edit7.append(self.lineEdit17)
        self.edit8.append(self.lineEdit18)      
        
        self.edit10.append(self.label_12)        
        self.edit11.append(self.lineEdit21)
        self.edit12.append(self.lineEdit22)
        self.edit13.append(self.lineEdit23)
        self.edit14.append(self.comboBox_2)
        self.edit15.append(self.comboBox_3)
        self.delacoustic.hide()
        self.delmetadata.hide()


        self.db = MyDatabase()
        self.packettypes =self.db.getvalues('packettype')        
        self.packetsources =self.db.getvalues('packetsource')  
        self.packettype_popup.comboBox.addItems(self.packettypes)
        self.packetsource_popup.comboBox.addItems(self.packetsources)
        
        self.comboBox_2.currentIndexChanged.connect(lambda:self.other_packettype(self.comboBox_2))       
        self.comboBox_2.addItem("-Select-")
        self.comboBox_2.addItems(self.packettypes)
        self.comboBox_2.addItem("Other")

        self.comboBox.currentIndexChanged.connect(lambda:self.other_packetsource(self.comboBox))       
        self.comboBox.addItem("-Select-")
        self.comboBox.addItems(self.packetsources) 
        self.comboBox.addItem("Other")
        
        self.comboBox_3.currentIndexChanged.connect(lambda:self.other_packetsource(self.comboBox_3))     
        self.comboBox_3.addItem("-Select-")
        self.comboBox_3.addItems(self.packetsources) 
        self.comboBox_3.addItem("Other")
        
        for i in range(2):
            self.addacousticfun()
            self.addmetadatafun()
        
        
        
        
    def other_packetsource(self,combobox):
        if combobox.currentText()=="Other":
            self.packetsource_popup.label.clear()
            self.packetsource_popup.exec_()
        
    def other_packettype(self,combobox):
        if combobox.currentText()=="Other":
            self.packettype_popup.label.clear()
            self.packettype_popup.exec_()
        
    def addpackettype(self):
        
        try:
            new=self.packettype_popup.lineEdit.text()
            self.db.addpackettype(new)
        except:
            self.packettype_popup.label.setText("Packet type already exists.")
            self.packettype_popup.label.setStyleSheet("color:red")    
            
        self.packettypes =self.db.getvalues('packettype') 
        for comboBox in self.edit15:
            print(self.packettypes)
            comboBox.addItem("-Select-")
            comboBox.addItems(self.packettypes) 
            comboBox.addItem("Other")
            
            #self.packettype_popup.label.setText("Adding new packet type Failed.")
            #self.packettype_popup.label.setStyleSheet("color:red")
            
    def addpacketsource(self):
        try:
            new=self.packettype_popup.lineEdit.text()
            self.db.addpacketsource(self.packetsource_popup.lineEdit.text())
            for combobox in self.edit4:
                combobox.addItem(new)
            for combobox in self.edit14:
                combobox.addItem(new)
                
                
        except:
            self.packetsource_popup.label.setText("Add new packet type Failed.")
            self.packetsource_popup.label.setStyleSheet("color:red")
            
    def addacousticfun(self):        
        count=len(self.edit0)
        self.edit0.append(QLabel())
        self.edit0[count].setText("{}.".format(count+1))
        self.edit0[count].setStyleSheet("color:rgb(255,255,255); font-size : 12pt; text-align : center;")
        self.edit0[count].setAlignment(QtCore.Qt.AlignCenter)
        
        self.edit1.append(QLineEdit())
        self.edit2.append(QLineEdit())
        self.edit3.append(QLineEdit())
        
        col4=QComboBox()
        col4.currentIndexChanged.connect(lambda:self.other_packetsource(col4))
        col4.addItem("-Select-")
        col4.addItems(self.packetsources)
        col4.addItem("Other")
        self.edit4.append(col4)        
        
        self.edit5.append(QLineEdit())
        self.edit6.append(QLineEdit())
        self.edit7.append(QLineEdit())
        self.edit8.append(QLineEdit())        
                       
        self.edit1[count].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
        self.edit2[count].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
        self.edit3[count].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
        self.edit4[count].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
        self.edit5[count].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
        self.edit6[count].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
        self.edit7[count].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
        self.edit8[count].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")        
        
        self.details.addWidget(self.edit0[count],count+1,0)
        self.details.addWidget(self.edit1[count],count+1,1)
        self.details.addWidget(self.edit2[count],count+1,2)
        self.details.addWidget(self.edit3[count],count+1,3)
        self.details.addWidget(self.edit4[count],count+1,4)
        self.details.addWidget(self.edit5[count],count+1,5)
        self.details.addWidget(self.edit6[count],count+1,6)
        self.details.addWidget(self.edit7[count],count+1,7)
        self.details.addWidget(self.edit8[count],count+1,8)
                
        self.delacoustic.show()
        self.details.addWidget(self.addacoustic,count+1,9)
        self.details.addWidget(self.delacoustic,count+1,10)
            

    def addmetadatafun(self): 
        count=len(self.edit10)
        self.edit10.append(QLabel())
        self.edit10[count].setText("{}.".format(count+1))
        self.edit10[count].setStyleSheet("color:rgb(255,255,255); font-size : 12pt; text-align : center;")
        self.edit10[count].setAlignment(QtCore.Qt.AlignCenter)
        
        self.edit11.append(QLineEdit())
        self.edit12.append(QLineEdit())
        self.edit13.append(QLineEdit())
        
        col4=QComboBox()
        col4.currentIndexChanged.connect(lambda:self.other_packettype(col4))
        col4.addItem("-Select-")
        col4.addItems(self.packettypes)
        col4.addItem("Other")
        self.edit14.append(col4) 
        
        col5=QComboBox()
        col5.currentIndexChanged.connect(lambda:self.other_packettype(col4))
        col5.addItem("-Select-")
        col5.addItems(self.packetsources)
        col5.addItem("Other")
        self.edit15.append(col5)        
        
        self.edit11[count].setStyleSheet("background-color: rgba(60,60,94,255);color: rgb(255, 255, 255);")
        self.edit12[count].setStyleSheet("background-color: rgba(60,60,94,255);color: rgb(255, 255, 255);")
        self.edit13[count].setStyleSheet("background-color: rgba(60,60,94,255);color: rgb(255, 255, 255);")
        self.edit14[count].setStyleSheet("background-color: rgba(60,60,94,255);color: rgb(255, 255, 255);")
        self.edit15[count].setStyleSheet("background-color: rgba(60,60,94,255);color: rgb(255, 255, 255);")     
        
        self.details_2.addWidget(self.edit10[count],count+1,0)
        self.details_2.addWidget(self.edit11[count],count+1,1)
        self.details_2.addWidget(self.edit12[count],count+1,2)
        self.details_2.addWidget(self.edit13[count],count+1,3)
        self.details_2.addWidget(self.edit14[count],count+1,4)
        self.details_2.addWidget(self.edit15[count],count+1,5)
        
        self.delmetadata.show()
        self.details_2.addWidget(self.addmetadata,count+1,6)
        self.details_2.addWidget(self.delmetadata,count+1,7)
            
            
    def delacousticfun(self):
        count=len(self.edit0)-1
        self.details.removeWidget(self.edit0[count])
        self.details.removeWidget(self.edit1[count])
        self.details.removeWidget(self.edit2[count])
        self.details.removeWidget(self.edit3[count])
        self.details.removeWidget(self.edit4[count])
        self.details.removeWidget(self.edit5[count])
        self.details.removeWidget(self.edit6[count])
        self.details.removeWidget(self.edit7[count])
        self.details.removeWidget(self.edit8[count])
        self.details.removeWidget(self.addacoustic)
        self.details.removeWidget(self.delacoustic)
        
        
        self.edit0[count].deleteLater()
        self.edit1[count].deleteLater()
        self.edit2[count].deleteLater()
        self.edit3[count].deleteLater()
        self.edit4[count].deleteLater()
        self.edit5[count].deleteLater()
        self.edit6[count].deleteLater()
        self.edit7[count].deleteLater()
        self.edit8[count].deleteLater()
        
        del self.edit0[count]
        del self.edit1[count]
        del self.edit2[count]
        del self.edit3[count]
        del self.edit4[count]
        del self.edit5[count]
        del self.edit6[count]
        del self.edit7[count]
        del self.edit8[count]
        
        if count==1:
            self.details.addWidget(self.addacoustic,count,9)
            self.delacoustic.hide()
        else:            
            self.details.addWidget(self.addacoustic,count,9)
            self.details.addWidget(self.delacoustic,count,10)
           
        
    def delmetadatafun(self):        
        count=len(self.edit10)-1
        self.details_2.removeWidget(self.edit10[count])
        self.details_2.removeWidget(self.edit11[count])
        self.details_2.removeWidget(self.edit12[count])
        self.details_2.removeWidget(self.edit13[count])
        self.details_2.removeWidget(self.edit14[count])
        self.details_2.removeWidget(self.edit15[count])
        self.details_2.removeWidget(self.addmetadata)
        self.details_2.removeWidget(self.delmetadata)
        
        self.edit10[count].deleteLater()
        self.edit11[count].deleteLater()
        self.edit12[count].deleteLater()
        self.edit13[count].deleteLater()
        self.edit14[count].deleteLater()
        self.edit15[count].deleteLater()

        del self.edit10[count]
        del self.edit11[count]
        del self.edit12[count]
        del self.edit13[count]
        del self.edit14[count]
        del self.edit15[count]
        
        if count==1:
            self.details_2.addWidget(self.addmetadata,count,6)
            self.delmetadata.hide()
        else:
            self.delmetadata.show()
            self.details_2.addWidget(self.addmetadata,count,6)
            self.details_2.addWidget(self.delmetadata,count,7)         
        
   
        
    def submitfun(self):
        self.msg.clear()
        self.metamsg.clear()
        self.acousmsg.clear()
        metaports = {}
        acousticports = {}
            
        if self.name.text() != "":
            self.project = self.name.text()
             
            with open(GUI_path+'projects.json','r') as output:
                data = json.load(output)
                projects = [] 
                for project in data.keys():
                    projects.append(project.lower())
            
            if self.project.lower() in projects:
                self.msg.setText("Project Name already exists")
                self.msg.setStyleSheet("color:red")
                return
            
            
            
            
            for i in range(len(self.edit0)) : 
                if (not self.edit1[i].text() and i>0):                	
                    self.acousmsg.setText(f"Port No. {i+1}: Please remove extra rows")
                    self.acousmsg.setStyleSheet("color:red")
                    return
                    
                if (not self.edit1[i].text() or not self.edit2[i].text() or self.edit4[i].currentText()== "-Select-" or not self.edit5[i].text() or not self.edit6[i].text() or not self.edit7[i].text() or not self.edit8[i].text()):
                    self.acousmsg.setText(f"Port No. {i+1}: Please fill all mandatory fields")
                    self.acousmsg.setStyleSheet("color:red")
                    return
                
                if(not self.edit1[i].text().isnumeric()):
                    self.acousmsg.setText(f"Port No. {i+1}: Dest UDP Port must be numeric")
                    self.acousmsg.setStyleSheet("color:red")
                    return
                    
                if(not self.edit2[i].text().isnumeric()):
                    self.acousmsg.setText(f"Port No. {i+1}: Packet Size must be numeric")
                    self.acousmsg.setStyleSheet("color:red")
                    return
                    
                if(self.edit3[i].text()):
                    if(not self.edit3[i].text().isnumeric()):
                        self.acousmsg.setText(f"Port No. {i+1}: Source IP must be numeric")
                        self.acousmsg.setStyleSheet("color:red")
                        return
                    
                if(self.edit4[i].currentText()== "-Select-"):
                    self.acousmsg.setText(f"Port No. {i+1}: Select Packet Source from drop down")
                    self.acousmsg.setStyleSheet("color:red")
                    return                    
                    
                if(not self.edit5[i].text().isnumeric()):
                    self.acousmsg.setText(f"Port No. {i+1}: No. of nodes must be numeric")
                    self.acousmsg.setStyleSheet("color:red")
                    return
                    
                if(not self.edit6[i].text().isnumeric()):
                    self.acousmsg.setText(f"Port No. {i+1}: No. of channels must be numeric")
                    self.acousmsg.setStyleSheet("color:red")
                    return
                    
                if(not self.edit7[i].text().isnumeric()):
                    self.acousmsg.setText(f"Port No. {i+1}: No. of samples must be numeric")
                    self.acousmsg.setStyleSheet("color:red")
                    return
                    
                if(not self.edit8[i].text().isnumeric()):
                    self.acousmsg.setText(f"Port No. {i+1}: No. of packets must be numeric")
                    self.acousmsg.setStyleSheet("color:red")
                    return
                    
                if self.edit1[i].text() not in acousticports.keys():
                    acousticports[self.edit1[i].text()]=[{"packetsize": int(self.edit2[i].text()), 
                                                                  "packetsource": self.edit4[i].currentText() ,
                                                                  "packettype" : 'Acoustic', 
                                                                  "nPckt" : int(self.edit5[i].text()),
                                                                  "nNode": int(self.edit6[i].text()),
                                                                  "nSamp": int(self.edit7[i].text()),
                                                                  "nChann": int(self.edit8[i].text())}]
                  
            self.acousmsg.setText(f"Acoustic Ports Added")
            self.acousmsg.setStyleSheet("color:green")
                    
                
            for i in range(len(self.edit10)) :
                if (not self.edit11[i].text()):
                    if i>0:
                        self.metamsg.setText(f"Port No. {i+1}: Please remove extra rows")
                        self.metamsg.setStyleSheet("color:red")
                        return
                    else:
                        self.metamsg.setText(f"Add metadata ports")
                        self.metamsg.setStyleSheet("color:red")
                        return
                    
                if (not self.edit11[i].text() or not self.edit12[i].text() or self.edit14[i].currentText()== "-Select-" or  self.edit15[i].currentText()== "-Select-"):
                    self.metamsg.setText(f"Port No. {i+1}: Please fill all mandatory fields")
                    self.metamsg.setStyleSheet("color:red")
                    return
                    
                else:
                    if (self.edit11[i].text().isnumeric() and self.edit12[i].text().isnumeric()):
                        if(self.edit13[i].text()):
                            ip= self.edit13[i].text().split(",")
                            for x in ip:
                                if not x.isnumeric():
                                    self.metamsg.setText("Port No. {i+1}: Source IP should be integer")
                                    self.metamsg.setStyleSheet("color:red")
                                    return
                                
                            if self.edit11[i].text() not in metaports.keys():
                                metaports[self.edit11[i].text()]=[{"packetsize": int(self.edit12[i].text()), 
                                                              "ip": ip ,
                                                              "packetsource" : self.edit15[i].currentText(), 
                                                              "packettype" : self.edit14[i].currentText()}]
                            else:
                                metaports[self.edit11[i].text()].append( {"packetsize":int(self.edit12[i].text()),
                                                                     "ip":ip,
                                                                     "packetsource":self.edit15[i].currentText(),
                                                                     "packettype": self.edit14[i].currentText()})
                        
                        else:                               
                            if self.edit11[i].text() not in metaports.keys():
                                metaports[self.edit11[i].text()]=[{"packetsizesize": int(self.edit12[i].text()),
                                                              "packetsource":self.edit15[i].currentText(), 
                                                              "packettype" : self.edit14[i].currentText()}]
                            else:
                                [self.edit11[i].text()].append({"packetsize": int(self.edit12[i].text()),
                                                               "packetsource" : self.edit15[i].currentText(), 
                                                               "packettype" : self.edit14[i].currentText()})
                             
                    else:
                        flag = False
                        self.metamsg.setText(f"Port No. {i+1}: Dest UDP Port and Packet size should be integer")
                        self.metamsg.setStyleSheet("color:red")
                        return
                    
                            
                        
            
            
            if len(acousticports)==0:
                self.acousmsg.setText("Add acoustic ports")
                self.acousmsg.setStyleSheet("color:red")
                return 
            if len(metaports)==0:
                self.metamsg.setText("Add metadata ports")
                self.metamsg.setStyleSheet("color:red")
                return 
                
                         

        else:
            self.msg.setText("Enter the Project Name")
            self.msg.setStyleSheet("color:red")
            return False
        
        self.msg.clear()
        self.metamsg.clear()
        self.acousmsg.clear()

        m = len(metaports)
        n = len(acousticports)

        submit_popup= PopUp2buttons(self)

        submit_popup.setWindowTitle("Submit Port Details") 
        submit_popup.not_ok.setText("Back") 
        submit_popup.ok_button.setText("Continue")      

        submit_popup.label.setText(f"{n} acoustic ports and {m} metadata ports detected. Click continue to enter packet details")            
        submit_popup.ok_button.clicked.connect(lambda:self.nextfun(metaports,acousticports))
        submit_popup.exec_() 
       
    def backfun(self):
        self.db.close()
        widget.removeWidget(self)
        size = widget.count()
        for i in range(size+1):
            widg = widget.widget(size-i)
            widget.removeWidget(widg)
        welcome = Welcome_Screen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def nextfun(self,metaports,acousticports):
        self.db.close()
        
        packet_type=["metaheader"]            
        for value in metaports.values():
            for item in value:
                if item["packettype"] not in packet_type:
                    packet_type.append(item["packettype"])                        
        
        ports = acousticports.copy()
        ports.update(metaports)

        with open(GUI_path+'projects.json','r+') as output:
            data = json.load(output)
            data[self.project.upper()] = {"ports":ports, "packets":{}, "parameters":{}}
            output.seek(0)
            json.dump(data,output,indent=2)

        create = Packet_field_Screen(self.project, packet_type)       
        
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex()+1)
         
class Packets(QWidget):
    def __init__(self):
        super().__init__()             
        loadUi(GUI_path+"/frontend/Packet.ui",self)       
        self.add.clicked.connect(self.addfun)
        self.delt.clicked.connect(self.delfun)
        self.delt.hide()
        
        self.edit0=[]
        self.edit1=[]
        self.edit2=[]
        self.edit3=[]
        self.edit4=[]
        self.edit5=[]
        self.edit0.append(self.label_5)
        self.edit1.append(self.comboBox_1)
        self.edit2.append(self.comboBox_2)
        self.edit3.append(self.comboBox_3)
        self.edit4.append(self.lineEdit)
        self.edit5.append(self.checkBox)
        
        self.db = MyDatabase()
        self.datatypes =self.db.getvalues('datatype')        
        self.endianness =self.db.getvalues('endianness')
        self.fields =self.db.getfields()
                   
        self.comboBox_1.addItem("-Select-")
        self.comboBox_1.addItems(self.fields)
               
        self.comboBox_2.addItem("-Select-")
        self.comboBox_2.addItems(self.datatypes)        
    
        self.comboBox_3.addItem("-Select-")
        self.comboBox_3.addItems(self.endianness) 
            
        self.db.close()
        
        
    def addfun(self):
        count=len(self.edit0)
        self.edit0.append(QLabel())
        self.edit0[count].setText("{}.".format(count+1))
        self.edit0[count].setStyleSheet("color:rgb(255,255,255); font-size : 12pt; text-align : center;")
        self.edit0[count].setAlignment(QtCore.Qt.AlignCenter)
        
        col1=QComboBox()
        col2=QComboBox()
        col3=QComboBox()
        
        col1.addItem("-Select-")
        col1.addItems(self.fields)  
        #col1.addItem("Other")
        #col1.currentIndexChanged.connect(lambda:self.other_field(col1))
        
        col2.addItem("-Select-")
        col2.addItems(self.datatypes)
        col3.addItem("-Select-")
        col3.addItems(self.endianness)
        
        self.edit1.append(col1)
        self.edit2.append(col2)
        self.edit3.append(col3)
        self.edit4.append(QLineEdit())      
        self.edit5.append(QCheckBox())              
             
        self.edit1[count].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
        self.edit2[count].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
        self.edit3[count].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
        self.edit4[count].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
        self.edit5[count].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
              
        self.details.addWidget(self.edit0[count],count+1,0)
        self.details.addWidget(self.edit1[count],count+1,1)
        self.details.addWidget(self.edit2[count],count+1,2)
        self.details.addWidget(self.edit3[count],count+1,3)
        self.details.addWidget(self.edit4[count],count+1,4)
        self.details.addWidget(self.edit5[count],count+1,5)
                        
        self.delt.show()
        self.details.addWidget(self.add,count+1,6)
        self.details.addWidget(self.delt,count+1,7)
    
    def delfun(self):
        count=len(self.edit0)-1
        self.details.removeWidget(self.edit0[count])
        self.details.removeWidget(self.edit1[count])
        self.details.removeWidget(self.edit2[count])
        self.details.removeWidget(self.edit3[count])
        self.details.removeWidget(self.edit4[count])
        self.details.removeWidget(self.edit5[count])
        
        self.edit0[count].deleteLater()
        self.edit1[count].deleteLater()
        self.edit2[count].deleteLater()
        self.edit3[count].deleteLater()
        self.edit4[count].deleteLater()
        self.edit5[count].deleteLater()
        
        del self.edit0[count]
        del self.edit1[count]
        del self.edit2[count]
        del self.edit3[count]
        del self.edit4[count]
        del self.edit5[count]
                
        if count==1:
            self.details.addWidget(self.add,count,6)
            self.delt.hide()
        else:            
            self.details.addWidget(self.add,count,6)
            self.details.addWidget(self.delt,count,7)
    
    def validate(self):
        self.fields = {}
        self.parameters=[]
        spare=1

        for i in range(len(self.edit1)) :
            if(self.edit1[i].currentText()=="-Select-" and self.edit2[i].currentText()=="-Select-" and self.edit3[i].currentText()=="-Select-" and not self.edit4[i].text()): 
                if i>0:
                	self.msg.setText(f'Please remove unwanted rows')
                	self.msg.setStyleSheet("color:red")
                	return False
                else:
                	self.msg.setText(f'Please add fields')
                	self.msg.setStyleSheet("color:red")
                	return False
            else:                
                if(self.edit1[i].currentText()!="-Select-"  and self.edit2[i].currentText()!="-Select-" and self.edit3[i].currentText()!="-Select-"): 
                                            
                    if(self.edit4[i].text()):
                        if(self.edit4[i].text().isnumeric()):
                            if self.edit1[i].currentText()=="Spare":
                                self.fields["spare"+str(spare)] = {"datatype" : self.edit2[i].currentText(), "endianness" : 
                                                            self.edit3[i].currentText(), "size" : int(self.edit4[i].text())}
                                spare+=1
                            else:
                                self.fields[self.edit1[i].currentText()] = {"datatype" : self.edit2[i].currentText(), "endianness" :                                                         self.edit3[i].currentText(), "size" : int(self.edit4[i].text())}
                                if self.edit5[i].isChecked():
                                    self.parameters.append(self.edit1[i].currentText())
                                   
                        else:
                            self.msg.setText(f'Size of the {self.edit1[i].text()} should be integer')
                            self.msg.setStyleSheet("color:red")
                            return False
                    else :
                        if self.edit1[i].currentText()=="Others":
                            self.fields["spare"+str(spare)] = {"datatype" : self.edit2[i].currentText(), 
                                                        "endianness" : self.edit3[i].currentText()}  
                            spare+=1
                        else:
                            self.fields[self.edit1[i].currentText()] = {"datatype" : self.edit2[i].currentText(), "endianness" : self.edit3[i].currentText()}
                            if self.edit5[i].isChecked():
                                self.parameters.append(self.edit1[i].currentText())
                else:
                    self.msg.setText(f'Please fill all mandatory fields')
                    self.msg.setStyleSheet("color:red")
                    return False
                    
        return True
                    
                    
    def coverttojson(self,project,packet):
        if len(self.fields)==0:
            self.msg.setText("Add fields to proceed")
            self.msg.setStyleSheet("color:red")
            return False
        
        project= project.upper()    
        #try:
        with open(GUI_path+'projects.json','r') as output:
            data = json.load(output)
        data[project]["packets"][packet]= {"fields" : self.fields}
        data[project]["parameters"][packet]= self.parameters
        with open(GUI_path+'projects.json','w') as output:
            json.dump(data,output,indent=1)
        
        #except:
            #return False
        
        self.msg.setText(f'Packet Added')
        self.msg.setStyleSheet("color:green")
        return True
        
class Packet_field_Screen(QDialog):
    def __init__(self, name, packets):
        super(Packet_field_Screen, self).__init__()
        loadUi(GUI_path+"/frontend/packet_details.ui",self)
        self.project = name
        self.fList = packets
        self.submit.clicked.connect(self.submitfun)
        self.home.clicked.connect(lambda: exit_popup.exec_())        
                        
        exit_popup= PopUp2buttons(self)
        exit_popup.setWindowTitle("Exit Adding Project")
        exit_popup.not_ok.setText("Cancel") 
        exit_popup.ok_button.setText("Exit")      
        exit_popup.label.setText("Do you really want to exit?\nProject details may not be saved.")
        exit_popup.ok_button.clicked.connect(self.backfun)
        self.table=[]
        
        for pckt in self.fList:
            custom_widget = Packets()
            custom_widget.addfun()
            self.table.append(custom_widget)
            self.layout.addWidget(custom_widget)
            custom_widget.label.setText("Packet- "+pckt )
        
        
    def submitfun(self):
        try:
            j=0
            for pckt in self.fList:
                if(self.table[j].validate()):
                    if(self.table[j].coverttojson(self.project, pckt)):
                        pass
                    else:
                        return False
                else:
                    return False
                
                j+=1
            
            submit_popup= PopUp2buttons(self)
            submit_popup.setWindowTitle("Exit Adding Project")
            submit_popup.not_ok.hide()
            submit_popup.ok_button.setText("OK")      
            submit_popup.label.setText("Project details added successfully")
            submit_popup.ok_button.clicked.connect(self.homefun)
            submit_popup.exec_()
        except:
            with open(GUI_path+'projects.json','r') as file:
                data = json.load(file)
            data.pop(self.project.upper())
            with open(GUI_path+'projects.json','w') as file:
                json.dump(data,file,indent=1)
                
    def backfun(self):
        try:
            with open(GUI_path+'projects.json','r') as file:
                data = json.load(file)
            data.pop(self.project.upper())
            with open(GUI_path+'projects.json','w') as file:
                json.dump(data,file,indent=1)
        except:
            pass
        widget.removeWidget(self)
        size = widget.count()
        for i in range(size):
            widg = widget.widget(size-i)
            widget.removeWidget(widg)
        welcome = Welcome_Screen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def homefun(self):
        widget.removeWidget(self)
        size = widget.count()
        for i in range(size):
            widg = widget.widget(size-i)
            widget.removeWidget(widg)
        welcome = Welcome_Screen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
            
class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QtWidgets.QPlainTextEdit(parent)        
        self.widget.setStyleSheet("border-radius : 10px;background-color: rgba(40,40,74,255);color: rgb(255, 255, 255);")
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)    
    
class Parser_screen(QDialog):
    def __init__(self, project):
        super(Parser_screen, self).__init__()
        loadUi(GUI_path+"/frontend/parser.ui",self)         
        self.percent=0   
        self.count=1
        self.exitflag=True
        self.logger=logging.getLogger()
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        logTextBox = QTextEditLogger(self)
        logTextBox.widget.setGeometry(455, 150, 380, 540)
        logTextBox.setFormatter(formatter)
        self.logger.addHandler(logTextBox)       
        
        self.exit.hide()
        self.progress.hide()
        self.complete.hide()
        self.browse.clicked.connect(lambda : self.browsefun(project))
        self.back.clicked.connect(self.backfun)
        self.complete.clicked.connect(self.backfun)
        self.home.clicked.connect(self.backfun)
        self.logout.clicked.connect(self.logoutfun)
        self.exit.clicked.connect(self.exitfun)
        
    def browsefun(self,project):
        fname=QFileDialog.getOpenFileNames(self, "Select files to load",'/run/media/c4/FS1/Python/', 'GDR (*.gdr)')
        if(len(fname[0])==0):
            self.message.setText("No file Selected")
        else:            
            self.message.setText(f" {len(fname[0])} files selected")
            self.submit.clicked.connect(lambda : self.submitfun(project,fname[0]))  
            
    def submitfun(self,project,fname):          
        self.exit.show() 
        #self.home.hide()
        #self.logout.hide()
        self.home.setEnabled(False)
        self.logout.setEnabled(False)
        self.exit.setEnabled(True)
        self.progress.show()
        self.browse.hide()
        self.back.hide()
        self.submit.hide()  
        self.total=len(fname)
        self.thread = QThread()
        # Step 3: Create a worker object
        self.worker = WorkerParse()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Step 5: Connect signals and slots
        self.thread.started.connect(lambda: self.worker.loadfun(project,fname))
        self.exit.clicked.connect(self.exitfun)  
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.updateProgressBar   )
        self.worker.fcount.connect(self.updatelabel )
        # Step 6: Start the thread
        self.thread.start()
        # Final resets
        #self.longRunningBtn.setEnabled(False)
        self.worker.finished.connect(
            #lambda: self.longRunningBtn.setEnabled(True)
            self.reportstatus
        )
        #self.loadfun(project,fname)       
             
        
    def updateProgressBar(self, value):
        self.progress.setValue(value)
        
    def updatelabel(self, value):
        self.message.setText(f"Uploading {value}/{self.total} files")
        
    def reportstatus(self,fcount):   
        if(fcount==self.total+1):
            self.complete.show()
            self.message.setText("Uploaded!!")
            self.message.setStyleSheet("color: green")
            self.progress.hide()            
                       
        else:            
            self.message.setText("Upload Failed")
            self.message.setStyleSheet("color: red")            
            self.progress.hide() 
            self.back.show()
            
        self.home.setEnabled(True)
        self.logout.setEnabled(True)
        self.exit.hide()
        #self.home.show()
        #self.logout.show()
         
        
    def exitfun(self): 
        self.exitflag=False 
        
        self.message.setText("Upload Stopped")
        self.message.setStyleSheet("color: red")            
        self.progress.hide() 
        self.back.show()
        self.home.show()
        self.logout.show()
        print("Exiting parsing!!")
           
    def backfun(self):        
        widget.removeWidget(self)
        size = widget.count()
        for i in range(size):
            widg = widget.widget(size-i)
            widget.removeWidget(widg)
        welcome = Welcome_Screen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)   
        
    def logoutfun(self):
        widget.removeWidget(self)
        size = widget.count()
        for i in range(size+1):
            widg = widget.widget(size-i)
            widget.removeWidget(widg)
        login = Login_Screen()
        widget.addWidget(login)  
        #logging.info("Successfully logged Out\n")
        print("Successfully logged Out.")
     
            

class WorkerParse(QObject):
    finished = pyqtSignal(int)
    fcount= pyqtSignal(int)
    progress = pyqtSignal(int)

   #def run(self):
   #    """Long-running task."""
   #    for i in range(5):
   #        sleep(1)
   #        self.progress.emit(i + 1)
   #    self.finished.emit()        
       
    def loadfun(self,project,fnames):    
        percent=1
        count=1
        self.fcount.emit(count) 
        self.progress.emit(percent) 

        logging.info("Starting file parsing")
        
        start_time=datetime.now()         
        
        with open(GUI_path+'projects.json','r+') as config:
            data = json.load(config)            
        ports=data[project]["ports"]
        packets=data[project]["packets"]
        parameters=data[project]["parameters"]
        
        metaheader=self.parsefieldtype(packets["metaheader"]["fields"])        
        totalsize=0    
        for filename in fnames: 
            
            t1=datetime.now()
            record_count=0 
            indexed_count=0
            byteoffset=0
            
            file =open(filename,'rb') 
            fsize= os.path.getsize(filename)            
            
            fname= filename.split("/")[-1]
            floc= filename.replace(fname, "")
            db = MyDatabase()
            try:
                pattern = re.compile(r'\d{4}\w{3}\d{2}_\d{2}_\d{2}_\d{2}')
                datestring = pattern.search(filename)
                date = datetime.strptime(datestring.group(), "%Y%b%d_%H_%M_%S") 
            except:
                logging.info(f"Filename {fname} is not as expected. Timestamp is missing"+ "\n")
                file.close()
                db.close()
                self.finished.emit(count)
                return False
            
            try:
                db.file_detail(fname,floc,date,project,fsize/(1000*1000*1000))
            except:
                logging.info(f"File {fname} is already loaded"+ "\n")
                count+=1
                self.fcount.emit(count) 
                continue          
                  
            fid,floc,project= db.get_fid(fname)
            #db.close() 
            logging.info("Parsing file "+fname) 
            logging.info("Size in GB: "+str(round(fsize/(1000*1000*1000),2))) 
            #try:  
            records_list=[]
            while True: 
                buffer= file.read(metaheader.itemsize)
                if not buffer:                
                    file.close()
                    break    
                metahdr=np.frombuffer(buffer,metaheader)             
                header=int(metahdr['Header'])
                if header != 2779110894:                         
                    logging.error("File structure is not matching with configuration given, error in parsing header "+ "\n")
                    #db = MyDatabase()
                    db.remove_fid(fname)
                    file.close()
                    db.close()
                    self.finished.emit(count)
                    return False
        
                seq_num=int(metahdr['SequenceNumber'])
                timestamp=int(metahdr['Timestamp']) 
                dest_port=int(metahdr['DestUDPPort'])
                pkt_size=int(metahdr['Packetsize'])
                source_ip=int(metahdr['SourceIP'])
                #print(dest_port)
                if str(dest_port) in ports:    
                    found=0                
                    for port in ports[str(dest_port)]:                      
                        if port["packetsize"]==pkt_size:
                            if port["packettype"]=="acoustic":
                                break
                            if "ip" in port:
                                if str(source_ip) in port["ip"]:                        
                                    found=1
                                    break
                            else:
                                    found=1
                                    break
        
                    if found==1: 
                        buffer= file.read(pkt_size)
                        packettype=port["packettype"]
                        packetsource=port["packetsource"]
        
                        #if packetsource=="sonarconfig":
                        #    np_record = np.frombuffer(buffer[sonarheader.itemsize:], self.parsefieldtype(packets[packettype]["fields"]))
                        #else:
                        np_record = np.frombuffer(buffer, self.parsefieldtype(packets[packettype]["fields"]))

                        if packettype in parameters.keys():                            
                            prmlist=parameters[packettype]                            
                            try:
                                nodenum=np_record['NodeNum'][0]
                            except:
                                nodenum=None                               

                            for prm in prmlist:
                                if prm=="Azimuth" or prm=="Roll":
                                    record= [fid,prm, np_record[prm][0]/10, packetsource,nodenum,timestamp,byteoffset]
                                    records_list.append(record)
                                    indexed_count+=1 
                                    #if np_record[prm][0]/10>360:
                                        #print("ERROR in azimuth roll values",value,deg,mint,sec,dirn)
                                        #break
                                elif prm=="Latitude" or prm=="Longitude":
                                    deg= np_record[prm][0][0]
                                    mint= np_record[prm][0][1]
                                    sec= np_record[prm][0][2]
                                    dirn= np_record[prm][0][3]
                                    
                                    value= round(deg+(mint/60)+(sec/3600),4)
                                    if int(dirn)==1:
                                        value= -value
                                    else:
                                        value= value
                                        
                                    #if value>360:
                                        #print("ERROR in lat long values",value,deg,mint,sec,dirn)
                                        #break
                                        
                                    record= [fid,prm, value, packetsource,nodenum,timestamp,byteoffset]
                                    records_list.append(record)
                                    indexed_count+=1                                
                                
                                else:
                                    record= [fid,prm, np_record[prm][0], packetsource,nodenum,timestamp,byteoffset]
                                    records_list.append(record)
                                    indexed_count+=1   


                    elif found==0:
                        file.seek(pkt_size,1)
        
                else:               
                    file.seek(pkt_size,1)       
             
        
                record_count+=1                
                byteoffset+= metaheader.itemsize+ pkt_size
                if (record_count%1000==0):
                    percent = int((byteoffset/fsize)*100)                    
                    self.progress.emit(percent)

                #self.exit.clicked.connect(self.exitfun)

            file.close()              
            #db = MyDatabase()
            if len(records_list)==0:
            	logging.info(f"File does not have any metadata packets."+ "\n")
            	file.close()
            	db.close()
            	count+=1
            	self.fcount.emit(count)
            	continue
            db.load_metadata(records_list)
            db.addtimestamp(timestamp/1000000.0,fid)
            t2= datetime.now() 
        
            logging.info("Total packets in file- "+str(record_count))           
            logging.info("Metadata packets loaded to Database- "+str(indexed_count ))
            logging.info("Time taken- "+str(t2-t1)+"\n")
            totalsize+= fsize/(1000*1000*1000)
            
            #except KeyboardInterrupt:
            #    logging.info("Quitting file parsing. Removing file "+fname+" from database")
            #    #db = MyDatabase()
            #    db.remove_fid(fname)                
            #    logging.info("Exiting!!")
            #    print("Exiting!!")
            #    self.finished.emit(count)
            #    sys.exit()
            #except:
            #    logging.error("Quitting file parsing. Removing file "+fname+" from database due to exception ")
            #    #db = MyDatabase()
            #    db.remove_fid(fname)                
            #    logging.error("Exiting!!")
            #    print("Exiting!!")
            #    self.finished.emit(count)
            #    sys.exit()
            #finally:
            
            db.close()
            
 
            percent = int((byteoffset/fsize)*100)              
            if percent==100:
                count+=1
                self.fcount.emit(count) 
            else:
                break
                
        end_time=datetime.now()
        logging.info("Total data parsed- "+ str(round(totalsize,2))+ "GB") 
        logging.info("Total time taken- "+ str(end_time- start_time).split(".")[0])   
        
        self.finished.emit(count) 
    
    def parsefieldtype(self,field_dict):
        datatypedict= {'unsigned long':'u4','unsigned long long':'u8','unsigned char':'u1','unsigned short':'u2',
               'unsigned int':'u4','int':'i4','float':'f4'}
        endiandict={'little':'<','big':'>'}
        dtlist=[]
        for key,value in field_dict.items():
            value=DotMap(value)        
            if(value.size):            
                dtype= (key,endiandict[value.endianness]+datatypedict[value.datatype],value.size)
            else:
                dtype= (key, endiandict[value.endianness]+datatypedict[value.datatype])
            dtlist.append(dtype)
        fieldtype=np.dtype(dtlist)
        return fieldtype
    
    
    
class MyDatabase(QDialog):
    def __init__(self):
        super(MyDatabase, self).__init__()
        self.conn = psycopg2.connect(database="SONAR_ATLAS", user = "postgres", password = "password", host = "127.0.0.1", port = "5432")        
        #127.0.0.1
        self.cur = self.conn.cursor()
        register_adapter(np.uint32, self.adapt_numpy_uint32)
        register_adapter(np.int32, self.adapt_numpy_int32)
        register_adapter(np.uint8, self.adapt_numpy_uint16)
        register_adapter(np.uint16, self.adapt_numpy_uint8)
        register_adapter(np.ndarray, self.adapt_numpy_array)
        register_adapter(np.float32, self.adapt_numpy_float32)
        
    def adapt_numpy_uint32(self,numpy_uint32):
        return AsIs(numpy_uint32)

    def adapt_numpy_int32(self,numpy_int32):
        return AsIs(numpy_int32)
    
    def adapt_numpy_uint8(self,numpy_uint8):
        return AsIs(numpy_uint8)
    
    def adapt_numpy_uint16(self,numpy_uint16):
        return AsIs(numpy_uint16)
    
    def adapt_numpy_float32(self,numpy_float32):
        return AsIs(numpy_float32)
    
    def adapt_numpy_array(self,numpy_array): 
        if len(numpy_array) == 0: 
            return AsIs("null")
        elif len(numpy_array) > 1: 
            return AsIs(str(tuple(numpy_array))) 
        else: 
            return AsIs(str(tuple(numpy_array)).replace(",","")) 
        #return AsIs("ARRAY" + np.array2string(numpy_array, separator=","))     

    def userverfy(self,us):
        self.cur.execute("SELECT password FROM USER_DETAIL WHERE username = %s",(us,))
        result = self.cur.fetchall()          
        return result
    
    def adduser(self,us,ps):
        self.cur.execute("INSERT INTO USER_DETAIL VALUES (%s,%s)", (us,ps))
        self.conn.commit()
        
    def addpackettype(self,value):        
        self.cur.execute("INSERT INTO PROJECT_PARAMETERS(NAME,VALUE) VALUES ('packettype',%s)", (value,))
        self.conn.commit()
        
    def addpacketsource(self,value):        
        self.cur.execute("INSERT INTO PROJECT_PARAMETERS(NAME,VALUE) VALUES ('packetsource',%s)", (value,))
        self.conn.commit()
        
    def getvalues(self,text):
        self.cur.execute("SELECT value FROM project_parameters where name = %s",(text,))
        result = [item[0] for item in self.cur.fetchall()]
        return result    
        
    def getfields(self):
        self.cur.execute("SELECT name FROM metadata_parameters")
        result = [item[0] for item in self.cur.fetchall()]
        return result 
        
    def file_detail(self, filename,fileloc,date, project,size):               
        self.cur.execute("INSERT INTO FILE_DETAIL(FNAME, FLOC, DATE, PROJECT, SIZE) VALUES (%s,%s,%s,%s,%s)",(filename,fileloc, date,project,size))
        self.conn.commit()
            
    def get_fid(self,filename):
        self.cur.execute("SELECT FID,FLOC,PROJECT FROM FILE_DETAIL WHERE FNAME=%s",(filename,))
        result = self.cur.fetchall()[0]           
        self.conn.commit()
        return int(result[0]),result[1],result[2]
    
    def addtimestamp(self,timestamp,fid):
        self.cur.execute("UPDATE FILE_DETAIL SET TIME=%s WHERE FID=%s",(timestamp,fid))
        self.conn.commit()
    
    def getmaxtimestamp(self,fname):
        self.cur.execute("SELECT TIME FROM FILE_DETAIL WHERE FNAME=%s",(fname,))
        time=(self.cur.fetchone()[0])        
        self.conn.commit()
        return time
    
    def getstartbyteloc(self,timestamp,fid):
        self.cur.execute("SELECT MAX(BYTEOFFSET) FROM ACOUSTIC_METADATA WHERE TIMESTAMP< %s and FID=%s",(timestamp,fid,))
        startbyte = int(self.cur.fetchone()[0])        
        self.conn.commit()
        return startbyte
    
    def remove_fid(self,filename):
        self.cur.execute("DELETE FROM FILE_DETAIL WHERE FNAME=%s",(filename,))
        self.conn.commit()
        
    def getdescription(self,parameter):
        if parameter=='CalenderDate':
            self.cur.execute("SELECT DATE(min(date)), DATE(max(date)) FROM file_detail")
        else:
            self.cur.execute("SELECT min(value), max(value) FROM acoustic_metadata WHERE NAME=%s",(parameter,))
        result = self.cur.fetchall()[0] 
        desc=f"Range of {parameter} is {str(result[0])} - {str(result[1])}"
        return desc
        
    def get_parameters(self):
        self.cur.execute("SELECT DISTINCT NAME FROM metadata_parameters")        
        parameters=self.cur.fetchall()
        self.conn.commit()
        return parameters
    
    def get_projects(self):
        self.cur.execute("SELECT DISTINCT PROJECT FROM FILE_DETAIL")        
        projects=self.cur.fetchall()
        self.conn.commit()
        return projects
    
    def get_fileprm(self,filename):
        self.cur.execute("SELECT DISTINCT NAME FROM acoustic_metadata where fid = (select fid from file_detail where fname=%s)",(filename,))    
        parameters=[item[0] for item in self.cur.fetchall()]
        self.conn.commit()
        return parameters
    
    def get_packetsource(self,filename,prm):
        self.cur.execute("SELECT DISTINCT packetsource FROM acoustic_metadata where fid = (select fid from file_detail where fname=%s) and name=%s",(filename,prm)) 
        src= [item[0] for item in self.cur.fetchall()]
        self.conn.commit()
        return src
    
    def get_nodenum(self,filename,prm,src):
        self.cur.execute("SELECT DISTINCT nodenum FROM acoustic_metadata where fid = (select fid from file_detail where fname=%s) and name=%s and packetsource=%s",(filename,prm,src)) 
        nodenum= [str(item[0]) for item in self.cur.fetchall()]
        self.conn.commit()
        return nodenum
        
    def load_metadata(self,record):
        args_str = ','.join(self.cur.mogrify("(%s,%s,%s,%s,%s,%s,%s)", x).decode('utf-8') for x in record)      
        #print(args_str)
        self.cur.execute("INSERT INTO ACOUSTIC_METADATA(fid,name,value,packetsource,nodenum,timestamp,byteoffset) VALUES"+ args_str)                
        self.conn.commit()    
        
    def get_timeseries(self,fname,parameter,pcktsrc,node):
        if node=='None':
            self.cur.execute("SELECT TIMESTAMP/1000000.0 as TIMESTAMP,VALUE FROM ACOUSTIC_METADATA WHERE NAME= %s AND FID=(select fid from file_detail where fname=%s) AND NODENUM is null AND PACKETSOURCE=%s order by TIMESTAMP",(parameter,fname,pcktsrc))
        else:
            self.cur.execute("SELECT TIMESTAMP/1000000.0 as TIMESTAMP,VALUE FROM ACOUSTIC_METADATA WHERE NAME= %s AND FID=(select fid from file_detail where fname=%s) AND NODENUM=%s AND PACKETSOURCE=%s order by TIMESTAMP",(parameter,fname,int(node),pcktsrc))
        df = pd.DataFrame(self.cur.fetchall(), columns=['Time in Seconds','Value'])
        return df
    
    def getmapdetails(self):
        self.cur.execute("select latlong.fid,file_detail.fname,file_detail.project,date(file_detail.date),latval,longval from (select lat.fid, lat.value as latval, long.value as longval from (SELECT fid,timestamp,value FROM public.acoustic_metadata where name = 'Latitude') as lat join (SELECT fid,timestamp,value FROM public.acoustic_metadata where name = 'Longitude') as long on lat.fid=long.fid and lat.timestamp= long.timestamp)latlong join file_detail on latlong.fid=file_detail.fid")       
        
        
        #"select distinct lat.fid,fname,project,date(date),lat.latitude, long.longitude from (select latdeg.fid,latdeg.timestamp,deg+(min/60)+(sec/3600) as latitude from (SELECT fid,timestamp,value as deg  FROM public.acoustic_metadata where name = 'LatitudeDegree' ORDER BY id ASC)as latdeg, (SELECT fid,timestamp,value as min  FROM public.acoustic_metadata where name = 'LatitudeMinutes' ORDER BY id ASC)as latmin ,(SELECT fid,timestamp,value as sec  FROM public.acoustic_metadata where name = 'LatitudeSeconds' ORDER BY id ASC)as latsec where latdeg.fid= latmin.fid and latdeg.timestamp= latmin.timestamp and latdeg.fid= latsec.fid and latdeg.timestamp= latsec.timestamp) lat join (select longdeg.fid,longdeg.timestamp,deg+(min/60)+(sec/3600) as longitude from (SELECT fid,timestamp,value as deg  FROM public.acoustic_metadata where name = 'LongitudeDegree' ORDER BY id ASC)as longdeg ,(SELECT fid,timestamp,value as min  FROM public.acoustic_metadata where name = 'LongitudeMinutes' ORDER BY id ASC)as longmin ,(SELECT fid,timestamp,value as sec  FROM public.acoustic_metadata where name = 'LongitudeSeconds' ORDER BY id ASC)as longsec where longdeg.fid= longmin.fid and longdeg.timestamp= longmin.timestamp and longdeg.fid= longsec.fid and longdeg.timestamp= longsec.timestamp) long on lat.fid= long.fid and lat.timestamp= long.timestamp join file_detail on lat.fid= file_detail.fid "
        
        df = pd.DataFrame(self.cur.fetchall(), columns=['Fid','Filename','Project','Date','Latitude','Longitude'])        
        return df
    
    def getfilenames(self,fid):
        self.cur.execute("SELECT fname FROM file_detail where fid in %s",(fid,))
        result = pd.DataFrame(self.cur.fetchall(), columns=['fname'])
        return result 
        
    def execute_query(self,querystring):
        self.cur.execute(querystring)
        result = self.cur.fetchall()
        self.conn.commit()
        return result
        
    def close(self):
        self.cur.close()
        self.conn.close()
        
        
    
      
class Dashboard_Screen(QDialog):
    def __init__(self):
        super(Dashboard_Screen, self).__init__()
        loadUi(GUI_path+"/frontend/dashboard.ui",self)
        self.home.clicked.connect(self.backfun)        
        self.logout.clicked.connect(self.logoutfun)
               
        self.db = MyDatabase()          
        
        self.cordinate= self.db.getmapdetails()
        
        if len(self.cordinate)==0:             
            self.error_text.setText("Database is empty")
            self.error_text.setStyleSheet("color:red")
            self.error_text.show()
            return
        
        self.error_text.clear()        
               
        fig = px.scatter_mapbox(self.cordinate, lat=self.cordinate.Latitude, lon=self.cordinate.Longitude, color= 'Project',  hover_data=['Fid','Project','Date'], zoom=3, mapbox_style="white-bg",center={'lat':10, 'lon':75}) #color='Project',
        
        fig.update_layout(
            mapbox_layers=[{
            "below": 'traces',
            "sourcetype": "raster",            
            "source":[ "http://localhost:7000/mapbox_tiles/{z}/{x}-{y}.png"],
            #"https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            #"http://localhost:7000/mapbox_tiles/{z}/{x}-{y}.png"
            #"http://localhost:7000/offline_tiles/{z}/{x}/{y}.png"            
        }],
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        
        #fig.add_selection(x0=60, y0=70, x1=70, y1=80)    
               
        #html = fig.to_html(include_plotlyjs='cdn')
        #self.webView = QWebEngineView()
        #self.webView.setHtml(html)
                
        offline.plot(fig, filename='mapplot.html', auto_open=False)
        self.webView = QWebEngineView()
        self.webView.load(QtCore.QUrl.fromLocalFile(os.path.abspath('mapplot.html')))     
         
        self.layout.addWidget(self.webView) 
         
        #filenames=
        self.select.clicked.connect(lambda: self.selectfun(fig))
        self.gotovis.hide()
        #self.download.clicked.connect(self.testfun)
        #self.selectedData = []     
        #self.maximize()
        
    def maximize(self):
        maximizespacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        widget.setFixedSize(rect.width(), rect.height())
        widget.setGeometry(rect.center().x() - widget.width() // 2,
	    rect.center().y() - widget.height() // 2,
	    widget.width(),
	    widget.height())
	    
	    
    def fixedsize(self):         
        widget.setFixedSize(892,750)        
        widget.setGeometry(
	    rect.center().x() - widget.width() // 2,
	    rect.center().y() - widget.height() // 2,
	    widget.width(),
	    widget.height())
        
    def selectfun(self,fig):
        if self.lat1.text()!="" and self.lat2.text()!="" and self.long1.text()!="" and self.long2.text()!="":        
            if self.lat1.text().isnumeric()and self.lat2.text().isnumeric() and self.long1.text().isnumeric() and self.long2.text().isnumeric():
                if not 0<=int(self.lat1.text())<=90  or not 0<=int(self.lat1.text())<=90:
                    self.error_text.setText(f"Latitude Ranges must be between 0 and 90")
                    self.error_text.setStyleSheet("color: red")     
                    return False
                elif not 0<=int(self.long1.text())<=180  or not 0<=int(self.long1.text())<=180:
                    self.error_text.setText(f"Longitude Ranges must be between 0 and 180")
                    self.error_text.setStyleSheet("color: red")  
                    return False
                else:
                	
                    selected= self.cordinate[(self.cordinate['Latitude'] >= int(self.lat1.text()) ) & (self.cordinate['Latitude']<= int(self.lat2.text())) & (self.cordinate['Longitude']>= int(self.long1.text())) &                                             (self.cordinate['Longitude']<= int(self.long2.text()))]          
                    
                    if len(selected)==0:
                        self.error_text.setText(f"No matching Data")
                        self.error_text.setStyleSheet("color: red")
                        return False
                    self.filenames= self.db.getfilenames(selected["Fid"].unique())
                    self.db.close()
            else:
                self.error_text.setText(f"Latitude and Longitude Ranges must be numeric")
                self.error_text.setStyleSheet("color: red")
                return False
         
        else:            
            self.error_text.setText(f"Enter Latitude and Longitude Ranges")
            self.error_text.setStyleSheet("color: red") 
            return False
        
        '''
        fig.add_selection(x0=int(self.lat1.text()), y0=int(self.long1.text()), x1=int(self.lat2.text()), y1=int(self.long2.text()))
        
        html = fig.to_html(include_plotlyjs='cdn')
        self.webView = QWebEngineView()
        self.webView.setHtml(html)
        self.layout.itemAt(0).widget().setParent(None)
        self.layout.addWidget(self.webView)
        '''
        
        count=selected["Fid"].unique()
        self.error_text.setText(f"{len(count)} matching Files found")
        self.error_text.setStyleSheet("color: green")
        self.gotovis.show()
        self.gotovis.clicked.connect(self.visfun)

        #if len(filenames)==0:
        #    self.error_text.setText(f"No matching Data")
        #    self.error_text.setStyleSheet("color: red")
        #    return False
    def visfun(self):    
        vis = Visualize_Screen()
        #vis.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowType_Mask)
        vis.mapgoto(self.filenames["fname"].unique(),self.lat1.text(),self.lat2.text(),self.long1.text(),self.long2.text())    
                
        vis.showFullScreen()
        widget.addWidget(vis)   
        widget.setCurrentIndex(widget.currentIndex()+1)
        #widget.setFixedSize(rect.width()*3/4, rect.height()*3/4)

     
            
    def backfun(self): 
        try:
            self.db.close()
        except:
            pass
        widget.removeWidget(self)
        size = widget.count()
        for i in range(size):
            widg = widget.widget(size-i)
            widget.removeWidget(widg)
        welcome = Welcome_Screen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
        #self.fixedsize()
        #widget.setFixedSize(892,750)
    
    def logoutfun(self):    
        try:
            self.db.close()
        except:
            pass
        widget.removeWidget(self)
        size = widget.count()
        for i in range(size+1):
            widg = widget.widget(size-i)
            widget.removeWidget(widg)
        login = Login_Screen()
        widget.addWidget(login)
        #logging.info("Successfully logged Out\n")
        print("Successfully logged Out.")
        #widget.setFixedSize(892,750)
        
class Visualize_Screen(QDialog):
    def __init__(self):
        super(Visualize_Screen, self).__init__()
        loadUi(GUI_path+"/frontend/visualize.ui",self)     
        self.db = MyDatabase()
        self.home.clicked.connect(self.backfun)      
        self.logout.clicked.connect(self.logoutfun) 
        
        self.back.hide()
        self.clear_md.hide()
        self.clear_ac.hide()
        self.download_ac.hide()
        self.channelselect.hide()
        self.channelselect_2.hide()
        
        self.metawidget.hide()
        self.datawidget.hide()
        self.filewidget.hide()    
        self.heatwidget.hide()
        
        
        self.filename.currentIndexChanged.connect(self.fileselectionchange)  
        self.parameter.currentIndexChanged.connect(self.prmselectionchange)
        self.packetsource.currentIndexChanged.connect(self.srcselectionchange) 
        self.port.currentIndexChanged.connect(self.portselectionchange)         
        self.clear_md.clicked.connect(self.clearmdfun)
        self.clear_heatmap.clicked.connect(self.clearfftheatmapfun)
        
        self.plot.disconnect()
        self.plot.clicked.connect(self.plotfun)
        self.download_md.clicked.connect(self.download_metadata)        
        self.plot_ac.disconnect()
        try:
            self.sensor.currentIndexChanged.disconnect()
        except:
            pass
        self.plot_ac.clicked.connect(self.plotaccoustic)
        self.plot_all.clicked.connect(self.plot_all_clicked)
        self.clear_ac.clicked.connect(self.clearacfun)
        self.submit.disconnect()
        self.submit.clicked.connect(self.submitfun)       
        self.add.disconnect()
        self.add.clicked.connect(self.addpfun)
        
        self.dele.clicked.connect(lambda:self.delpfun(self.dele))
        self.clear.clicked.connect(self.clearpfun)
        
        self.edit0 = []
        self.edit1 = []
        self.edit2 = []
        self.edit3 = []            
        self.edit4 = []
        self.edit5 = []

        self.edit0.append(self.label)
        self.edit1.append(self.comboBox_1) 
        self.edit2.append(self.comboBox_2) 
        self.edit3.append(self.lineEdit_1) 
        self.edit4.append(self.info)
        self.edit5.append(self.dele)

        self.count=len(self.edit1)

        self.operators = ['<','<=','>','>=','=']      
        self.parameters= [x[0] for x in self.db.get_parameters()]
        if(len(self.parameters))==0:
            self.txt_2.setText(f"Database is empty")
            self.txt_2.setStyleSheet("color: red")

        self.info.clicked.connect(lambda:self.infofun(1))     
        

        self.comboBox_1.clear()
        self.comboBox_1.addItem("-Select-")            
        self.comboBox_1.addItems(sorted(self.parameters))
            
        self.comboBox_2.clear()
        self.comboBox_2.addItems(self.operators)
            
        self.projects= [x[0] for x in self.db.get_projects()]
        self.projectbox.clear()
        self.projectbox.addItem("-All-") 
        self.projectbox.addItems(self.projects) 
            
    def mapgoto(self,filenames,lat1,lat2,long1,long2):
        for i in range(3):
        	self.addpfun()        
                        
        self.edit1[0].setCurrentText("Latitude")
        self.edit1[1].setCurrentText("Latitude")
        self.edit1[2].setCurrentText("Longitude")
        self.edit1[3].setCurrentText("Longitude")
        
        self.edit2[0].setCurrentText(">=")
        self.edit2[1].setCurrentText("<=")
        self.edit2[2].setCurrentText(">=")
        self.edit2[3].setCurrentText("<=")
        
        self.edit3[0].setText(lat1)        
        self.edit3[1].setText(lat2)
        self.edit3[2].setText(long1)
        self.edit3[3].setText(long2)
        
        self.back.show()
        self.back.clicked.connect(self.dashboardfun)
        self.txt.setText(f"{len(filenames)} Matching Files Found.")
        self.txt.setStyleSheet("color: green")
                
        self.submitfun()    
        
    def maximize(self):
        maximizespacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.plotlayout.addItem(maximizespacer)
        widget.setFixedSize(rect.width(), rect.height())
        widget.setGeometry(rect.center().x() - widget.width() // 2,
	    rect.center().y() - widget.height() // 2,
	    widget.width(),
	    widget.height())
	    
	    
    def fixedsize(self):         
        widget.setFixedSize(892,750)        
        widget.setGeometry(
	    rect.center().x() - widget.width() // 2,
	    rect.center().y() - widget.height() // 2,
	    widget.width(),
	    widget.height())    
	    
	    
    def infofun(self,count):
        if self.edit1[count-1].currentText()=="-Select-":
            self.txt_3.setText("Please select parameter")
            self.txt_3.setStyleSheet("color: red")
        else:
            self.txt_3.setText(self.db.getdescription(self.edit1[count-1].currentText()))
            self.txt_3.setStyleSheet("color: green")     
        
    def addpfun(self):
        self.txt_3.clear()        
        infopush= QPushButton('i')
        label=QLabel()
        delete_button = QPushButton()
        
        #self.dele.show()
        self.edit0.append(label)
        self.edit1.append(QComboBox())
        self.edit2.append(QComboBox())        
        self.edit3.append(QLineEdit())
        self.edit4.append(infopush)
        self.edit5.append(delete_button)
        
        count=len(self.edit1)
        infopush.setStyleSheet('border-radius:0.1px;background-color: rgb(85, 112, 245);color:rgb(255,255,255);font: italic 11pt "C059";')       
        infopush.clicked.connect(lambda:self.infofun(count))
        label.setText("{}.".format(count))        
        label.setStyleSheet(" background-color: rgba(60,60,94,255); co lor:rgb(255,255,255); font-size : 12pt; text-align : center;")        
        label.setAlignment(QtCore.Qt.AlignCenter)       
        
        self.edit1[count-1].addItem("-Select-")
        self.edit1[count-1].addItems(sorted(self.parameters))
        self.edit2[count-1].addItems(self.operators)
        self.edit1[count-1].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
        self.edit2[count-1].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
        self.edit3[count-1].setStyleSheet("background-color: rgba(60,60,94,255);color:rgb(255,255,255)")
        
        delete_button.setIcon(QIcon.fromTheme('window-close'))  # Default icon for deleting
        delete_button.setIconSize(delete_button.sizeHint())
        delete_button.clicked.connect(lambda:self.delpfun(delete_button))
        icon_size = QSize(16, 16)
        delete_button.setIconSize(icon_size)
        
        self.details.addWidget(label, count+1, 0)
        self.details.addWidget(self.edit1[count-1], count+1, 1)
        self.details.addWidget(self.edit2[count-1], count+1, 2)
        self.details.addWidget(self.edit3[count-1], count+1, 3)              
        self.details.addWidget(self.edit4[count-1], count+1, 4)
        self.details.addWidget(self.edit5[count-1], count+1, 5)
                      
    def delpfun(self, button):
        count= self.edit5.index(button)
        #count= int(label.text().split('.')[0])
        #if count > 0 and count <= len(self.edit0):
        # Remove widgets from layout
        self.details.removeWidget(self.edit0[count])
        self.details.removeWidget(self.edit1[count])
        self.details.removeWidget(self.edit2[count])
        self.details.removeWidget(self.edit3[count])
        self.details.removeWidget(self.edit4[count])
        self.details.removeWidget(self.edit5[count])

        # Delete widgets from lists
        self.edit0[count].deleteLater()
        self.edit1[count].deleteLater()
        self.edit2[count].deleteLater()
        self.edit3[count].deleteLater()
        self.edit4[count].deleteLater()
        self.edit5[count].deleteLater()

        # Delete the references from the lists
        del self.edit0[count]
        del self.edit1[count]
        del self.edit2[count]
        del self.edit3[count]
        del self.edit4[count]
        del self.edit5[count]

        # Update the remaining row labels
        for i in range(count, len(self.edit0)):
            self.edit0[i].setText("{}.".format(i + 1))



    def clearpfun(self):        
        self.projectbox.setCurrentText("-Select-")
        self.datefrom.clear()
        self.dateto.clear()
        count=len(self.edit5)

        for i in range(count,0,-1):
            self.delpfun(self.edit5[i-1])
        
        self.txt.clear()
        self.txt_3.clear() 
        self.filename.clear()
        self.parameter.clear()
        self.packetsource.clear()
        self.nodenum.clear()  
        self.sensor.clear()
        self.port.clear()
        self.start.clear()
        self.end.clear()
        
    def submitfun(self):
        start=datetime.now()         
        self.txt.clear() 
        self.txt_3.clear()
        self.filename.clear()
        self.parameter.clear()
        self.packetsource.clear()
        self.nodenum.clear()  
        self.sensor.clear()
        self.port.clear()
        self.start.clear()
        self.end.clear()
        #self.metawidget.hide()
        #self.datawidget.hide()
        self.filewidget.hide()
        self.heatwidget.hide()
        
        try:
        	self.showhide.disconnect()
        	self.showhide1.disconnect()
        except:
        	pass
        
        
        for i in reversed(range(1,self.Metadata.count())): 
            self.Metadata.itemAt(i).widget().setParent(None)
        
        for i in reversed(range(1,self.Acoustic.count())): 
            self.Acoustic.itemAt(i).widget().setParent(None)
            
        
        count=0
        subquery1=""
        subquery2=""
        subquery3=""
        querystr="SELECT FNAME FROM FILE_DETAIL"
        
        if self.projectbox.currentText()!="-All-":
            querystr+=" WHERE PROJECT='"+self.projectbox.currentText()+"'"
          
        if self.datefrom.text()!="":
            try:                        
                datetime.strptime(self.datefrom.text(), "%Y-%m-%d")                
                if "WHERE" in querystr:
                    querystr+=" AND date(date)>'"+ self.datefrom.text()+"'"
                else:
                    querystr+=" WHERE date(date)>'"+ self.datefrom.text()+"'"
            except ValueError:
                self.txt_3.setText(f'Incorrect format, Date From should be YYYY-MM-DD')
                self.txt_3.setStyleSheet("color:red")                
                return False 
            
        if self.dateto.text()!="":     
            try:                        
                datetime.strptime(self.dateto.text(), "%Y-%m-%d")
                if "WHERE" in querystr:
                    querystr+=" AND date(date)<'"+ self.dateto.text()+"'"
                else:
                    querystr+=" WHERE date(date)<'"+ self.dateto.text()+"'"
            except ValueError:
                self.txt_3.setText(f'Incorrect format, Date To should be YYYY-MM-DD')
                self.txt_3.setStyleSheet("color:red")                
                return False 
        
        for i in range(len(self.edit1)):
            if(self.edit1[i].currentText() == "-Select-"): 
                continue
            #elif(not self.edit3[i].text().isnumeric()):
            #    self.txt_3.setText(f'Value is mandatory and must be numeric ')
            #    self.txt_3.setStyleSheet("color:red")  
            #    subquery=""
            #    return False
            else:
                try:
                    value=float(self.edit3[i].text())
                    print(value)
                except:
                    self.txt_3.setText(f'Value is mandatory and must be numeric ')
                    self.txt_3.setStyleSheet("color:red")  
                    subquery=""
                    return False
              
                count+=1
                subquery1+="SELECT DISTINCT FID FROM ACOUSTIC_METADATA WHERE NAME= '"+ self.edit1[i].currentText() +"' AND VALUE "+self.edit2[i].currentText() + self.edit3[i].text() +" INTERSECT "
               
            
        if count>0: 
            if "WHERE" in querystr:
                querystr+=' AND FID IN ('+subquery1[:-11]+' )'
            else:
                querystr+=' WHERE FID IN ('+subquery1[:-11]+' )'
                
        print(querystr)
        
        result= self.db.execute_query(querystr)          
        
            
        if len(result)<1:
            self.txt.setText(f"No Matching Files Found")
            self.txt.setStyleSheet("color: red")  
            return False
                            
        else:
            self.txt.setText(f"{len(result)} Matching Files Found.")
            self.txt.setStyleSheet("color: green")  
                       
            self.filename.addItem("-Select File-")  
        
            for item in result:                    
                self.filename.addItem(item[0])             
        
            self.filewidget.show()
            #self.metawidget.show()
            #self.datawidget.show()
            #self.showhide.setText("Show")
            #self.showhide1.setText("Show")
            self.showhide.clicked.connect(self.metashowhide)
            self.showhide1.clicked.connect(self.datashowhide)
             
        end=datetime.now()
        print("Query submission time", str(end-start),"\n")

    def metashowhide(self):
        if self.showhide.text()=="Show":
            self.metawidget.show()
            self.maximize()
            self.showhide.setText("Hide")
        else:
        	self.metawidget.hide()
        	#self.clearmdfun()
        	self.showhide.setText("Show")
        	
    def datashowhide(self):
        if self.showhide1.text()=="Show":
            self.datawidget.show()
            self.maximize()
            self.showhide1.setText("Hide")
        else:
        	self.datawidget.hide()        	
        	self.showhide1.setText("Show")
        	    	
    
    
    def dashboardfun(self):
        dsh = Dashboard_Screen()
        widget.addWidget(dsh)
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setFixedSize(892,750)
        
    def fileselectionchange(self):        
        self.parameter.clear()       
        self.sensor.clear()
        self.port.clear()
        self.start.clear()
        self.end.clear() 
        self.txt_2.clear()  
                
        
        if self.filename.currentText() == "-Select File-" or self.filename.currentText() =="":
            #self.metawidget.hide()
            #self.datawidget.hide()
            return        
        
        prm=self.db.get_fileprm(self.filename.currentText())   
        if len(prm)==0:
            self.txt_2.setText(f"No Medatadata packets found in selected file. Please choose a different file")
            self.txt_2.setStyleSheet("color: red")
            return
           
        self.parameter.addItems(sorted(prm))
        fid,floc,project= self.db.get_fid(self.filename.currentText())
        with open(GUI_path+'projects.json','r') as config_file:
            data = json.load(config_file)
        ports=data[project]["ports"]
        #packets=data[project]["packets"]  
        
        acoustic_ports=[]
        for port in ports.keys():
            for item in ports[port]:
                if item["packettype"]=="acoustic":
                    acoustic_ports.append(port)
                    break
        
        self.port.addItems(sorted(acoustic_ports)) 
        self.data=np.ndarray(shape=(0,0))
        self.channelselect.hide()
        self.channelselect_2.hide()
        self.download_ac.hide()
        self.plot_all.hide()

    def prmselectionchange(self):
        self.packetsource.clear()
        src=self.db.get_packetsource(self.filename.currentText(),self.parameter.currentText())        
        self.packetsource.addItems(sorted(src))
        
        
    def srcselectionchange(self):
        self.nodenum.clear()
        prm=self.db.get_nodenum(self.filename.currentText(), self.parameter.currentText(), self.packetsource.currentText())
        self.nodenum.addItems(sorted(prm))
    
    def portselectionchange(self):
               
        self.data=np.ndarray(shape=(0,0))
        self.channelselect.hide()
        self.channelselect_2.hide()
        self.download_ac.hide()
        self.plot_all.hide()
        self.clearfftheatmapfun()
        self.typebox.setCurrentIndex(0)
        
    def clearmdfun(self):
        self.txt_2.clear()
        for i in reversed(range(self.Metadata.count())):             
            self.Metadata.itemAt(i).widget().setParent(None)
        self.clear_md.hide()
        #self.metawidget.hide()
          
    def clearacfun(self):
        self.txt_2.clear()
        for i in reversed(range(self.Acoustic.count())):             
            self.Acoustic.itemAt(i).widget().setParent(None)
        self.clear_ac.hide()  
        #self.datawidget.hide()  
        
    def clearfftheatmapfun(self):
        self.txt_2.clear()        
        self.heatwidget.hide()

    def plotfun(self):
        start=datetime.now()
        self.txt_2.clear()        
        
        if self.filename.currentText()=="-Select File-":
            self.txt_2.setText(f'No File Selected. Select from FileSelect Window')
            self.txt_2.setStyleSheet("color:red")                
            return False
        
        
        self.metawidget.show()
            
        data= self.db.get_timeseries(self.filename.currentText(), self.parameter.currentText(),self.packetsource.currentText(),self.nodenum.currentText())   
        #print(data)
        
        fig1 = px.scatter(data,x='Time in Seconds', y='Value') 
        fig2 = px.line(data,x='Time in Seconds', y='Value',title = self.parameter.currentText()+"<br><sup>"+self.filename.currentText()+"-"+self.packetsource.currentText()+"-"+self.nodenum.currentText()+"</sup>") 
        fig2.update_layout(margin=dict(l=0, r=0, t=40, b=0),paper_bgcolor='rgba(0,0,0,0)',)#paper_bgcolor="LightSteelBlue"
        
        fig3 = go.Figure(data=fig1.data + fig2.data,layout = fig2.layout)
                
        offline.plot(fig3, filename='plot.html', auto_open=False)
        webView = QWebEngineView()
        webView.load(QtCore.QUrl.fromLocalFile(os.path.abspath('plot.html')))     
                
        inner_layout = QVBoxLayout()
        
        label=QLabel(self.filename.currentText()+"-"+self.packetsource.currentText()+"-"+self.nodenum.currentText())
        label.setStyleSheet("background-color: rgba(60,60,94,255)")
        close_button = QPushButton()
        close_button.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogCancelButton))
        close_button.setIconSize(QSize(16, 16))  # Set the desired icon size
        close_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Create a horizontal layout for the close button and spacer
        button_layout = QHBoxLayout()
        button_layout.addWidget(label)
        button_layout.addWidget(close_button)
        
        inner_layout.setSpacing(0)
        inner_layout.addLayout(button_layout)
        inner_layout.addWidget(webView)
        inner_widget = QWidget()
        inner_widget.setMinimumHeight(350)
        inner_widget.setMaximumHeight(500)
        inner_widget.setLayout(inner_layout)
        self.Metadata.insertWidget(0, inner_widget)  
        close_button.clicked.connect(lambda:self.close(inner_widget))
        self.clear_md.show()
        end=datetime.now()
        print(" Metadata Visualize time", str(end-start), "\n")
	
    def close(self,widget):
    	widget.setParent(None)
    	
    def download_metadata(self):    
        start=datetime.now()
        self.txt_2.clear()
        data= self.db.get_timeseries(self.filename.currentText(), self.parameter.currentText(),self.packetsource.currentText(),self.nodenum.currentText())
        
        
        path= "./Downloads/"+ self.filename.currentText().replace(".gdr","")
        try:
            os.mkdir(path)        
        except:
            pass
        
        try:        
            pattern = re.compile(r'\d{4}\w{3}\d{2}_\d{2}_\d{2}_\d{2}')
            datestring = pattern.search(self.filename.currentText())
            date = datetime.strptime(datestring.group(), "%Y%b%d_%H_%M_%S")
            
            def f(x):    
                return date + timedelta(microseconds=int(x['Time in Seconds']*1000000))
            
            data['TIMESTAMP']= data.apply(f,axis = 1)
            
            if self.nodenum.currentText()=="None":
                data.to_csv(path+ "/"+self.parameter.currentText()+"_"+self.packetsource.currentText(), index=False)
            else:
                data.to_csv(path+ "/"+self.parameter.currentText()+"_"+self.packetsource.currentText()+"_"+self.nodenum.currentText(), index=False)            
            self.txt_2.setText("Download successfull")
            self.txt_2.setStyleSheet("color:green")
            end=datetime.now()
            print(" Metadata Download time", str(end-start),"\n")
            return True
            
        except:  
            
            self.txt_2.setText("Download Failed")
            self.txt_2.setStyleSheet("color:red") 
            return False   
        
    def get_sensor_numbers(self):
        sensor_numbers_str = self.sensor.text()
        sensor_numbers = []
    
        for num_range in sensor_numbers_str.split(','):
            num_range = num_range.strip()
            if ":" in num_range:
                start, end = num_range.split(":")
                if start.strip().isdigit() and end.strip().isdigit():
                    start_num = int(start.strip())
                    end_num = int(end.strip())
                    sensor_numbers.extend(range(start_num, end_num + 1))
            elif num_range.isdigit():
                sensor_numbers.append(int(num_range))
    
        return sensor_numbers    
        
    def plotaccoustic(self): 
        
        self.txt_2.clear()
        typebox_value = self.typebox.currentText() 
        channelnum=self.sensor.text()
               
        
        try:
            self.sensor.currentIndexChanged.disconnect()
        except:
            pass
            
        if self.filename.currentText()=="-Select File-":
            self.txt_2.setText(f'No File Selected. Select from FileSelect Window')
            self.txt_2.setStyleSheet("color:red")                
            return False       
        
        if self.port.currentText()=="":
            self.txt_2.setText(f'No Port Selected')
            self.txt_2.setStyleSheet("color:red")                
            return False
        
        maxTim= self.db.getmaxtimestamp(self.filename.currentText())
        if self.start.text()=="" or self.end.text()=="":
            self.txt_2.setText(f"Enter start and end time in seconds")
            self.txt_2.setStyleSheet("color: red")
            return False
        if not self.start.text().replace(".", "").isnumeric() or not self.end.text().replace(".", "").isnumeric():
            self.txt_2.setText(f"Start and End time must be numeric")
            self.txt_2.setStyleSheet("color: red")
            return False
        if float(self.end.text()) > maxTim or float(self.end.text()) < 0:
            self.txt_2.setText(f"End time must be between 0 and {maxTim} seconds")
            self.txt_2.setStyleSheet("color: red")
            return False
        if float(self.start.text()) > maxTim or float(self.start.text()) < 0:
            self.txt_2.setText(f"Start time must be between 0 and {maxTim} seconds")
            self.txt_2.setStyleSheet("color: red")
            return False
        if float(self.start.text()) >= float(self.end.text()):
            self.txt_2.setText(f"Start time must be smaller than End Time")
            self.txt_2.setStyleSheet("color: red")
            return False
        
        sensor_numbers = self.get_sensor_numbers()
        fname= self.filename.currentText()
        port= self.port.currentText()
        start= self.start.text()
        end= self.end.text()
        fid,floc,project= self.db.get_fid(fname)
        try:
            file = open(floc+fname,'rb')
        except:
            print(f"Error in opening file- File Not Found in {floc}/{fname} ")
            #logging.error(f"Error in opening file- File Not Found in {floc}/{fname} ")
            self.txt_2.setText(f"Error in opening file")
            self.txt_2.setStyleSheet("color: red")
            return False       

               
        
        
        with open(GUI_path+'projects.json','r') as config_file:
            data = json.load(config_file)
        ports=data[project]["ports"]
        packets=data[project]["packets"] 
        self.nChann=ports[str(port)][0]["nChann"]
        self.nNode=ports[str(port)][0]["nNode"]
        self.nSamp=ports[str(port)][0]["nSamp"]
        self.nPckt=ports[str(port)][0]["nPckt"]
        
        self.sensor.clear()
               
        startbyte=0
        if float(start) !=0:
            startbyte= self.db.getstartbyteloc(float(start)*1000000,fid) 
            file.seek(startbyte,1)           
        
        starttimestamp= float(start)
        endtimestamp= float(end) 
        packetcount = math.ceil(float(end)- float(start))*self.nNode*self.nPckt
        self.flag=False 
        print("here")
        try:
            self.sensor.currentIndexChanged.disconnect()
        except:
            pass
        try:
            self.download_ac.clicked.disconnect()
        except:
            pass
        try:
            self.typebox.currentIndexChanged.disconnect()
        except:
            pass
        try:
            self.truncate.disconnect()
        except:
            pass      
        
        self.download_ac.clicked.connect(lambda:self.download_acoustic(self.nChann,self.nNode,self.nSamp,self.nPckt,start,end))
        self.typebox.currentIndexChanged.connect(lambda:self.currentindexchange(self.nChann,self.nNode,self.nSamp,self.nPckt,start,end))
        

        self.truncate.clicked.connect(lambda: self.fullfftheatmap_plot( self.nChann, self.nNode, self.nSamp, self.nPckt,start,end))
        self.truncate.clicked.connect(self.check_and_display_message)
        starttime=datetime.now()

        self.worker_thread = WorkerThread(port,file, ports, packets, starttimestamp,endtimestamp)
        self.worker_thread.processed_data.connect(self.handle_processed_data)
        self.worker_thread.update_progress.connect(self.update_popup_progress)
        
        self.open_popup()
        if self.flag==True and len(self.data)!=0:
            self.download_ac.show()
            self.plot_all.show()
            self.channelselect.show()
            endtime=datetime.now()
            print(" Acoustic Data Retrieval time", str(endtime-starttime),"\n")
             
            
    def update_plots(self, sensor_numbers, nChann, nNode, nSamp, nPckt, start, end):
        typebox_value = self.typebox.currentText()
        channelnum=self.sensor.text()
        try:
            self.sensor.textChanged.connect.disconnect()
        except:
            pass
        self.sensor.clear()
        if typebox_value == "Power Spectral Density(psd)":
           self.psd_plot(sensor_numbers, nChann, nNode, nSamp, nPckt, start, end)
        elif typebox_value == "Timeseries Plot":
            self.plotchannel(sensor_numbers, nChann, nNode, nSamp, nPckt, start, end)
        elif typebox_value == "Spectrogram":
             self.spectrogram_plot(channelnum, nChann, nNode, nSamp, nPckt, start, end)
        elif typebox_value == "Mean Plot":
            self.mean_plot(nChann,nNode,nSamp,nPckt,start,end)
            
        elif typebox_value == "Varience Plot":
            self.varience_plot(nChann,nNode,nSamp,nPckt,start,end)
            
        
    
    def plot_all_clicked(self):
        sensor_numbers = self.get_sensor_numbers()
        self.update_plots(sensor_numbers, self.nChann, self.nNode, self.nSamp, self.nPckt, self.start, self.end)        
        
    def check_and_display_message(self):
        if self.startsensor.text() == "" or self.endsensor.text() == "":
            self.txt_2.setText("Enter start sensor and end sensor values")
            self.txt_2.setStyleSheet("color: red")
            return False
        if float(self.startsensor.text()) >= float(self.endsensor.text()):
            self.txt_2.setText(f"Start sensor must be smaller than End sensor")
            self.txt_2.setStyleSheet("color: red")
            return False
        if self.startfreq.text() == ""  or self.endfreq.text()=="":
            self.txt_2.setText("Enter start frequency and end frequency values")
            self.txt_2.setStyleSheet("color: red")
            return False
        if float(self.startfreq.text()) >= float(self.endfreq.text()):
            self.txt_2.setText(f"Start frequency must be smaller than End frequency")
            self.txt_2.setStyleSheet("color: red")
            return False
        
    @pyqtSlot(np.ndarray)  # Or @pyqtSlot(np.ndarray)
    def handle_processed_data(self, data):
        self.data=data          
        if len(self.data)==0:
            self.txt_2.setText(f"No Matching data to plot")
            self.txt_2.setStyleSheet("color: red")
            #self.datawidget.hide()
                           
        else: 
            self.txt_2.clear()          
            #self.datawidget.show()            
            
        
    def open_popup(self):
        popup = PopUpWindow(self)
        self.worker_thread.start()  # Start the worker thread
        popup.exec_()

    def update_popup_progress(self, value):
        popup = self.findChild(PopUpWindow)
        if popup:
            popup.update_progress(value)
        if value==100:
            self.flag=True    
            

    def closeEvent(self, event):
        self.worker_thread.quit()
        self.worker_thread.wait()
        event.accept()
        if self.flag==False:
            self.txt_2.setText(f"Error: Data Mismatch")
            self.txt_2.setStyleSheet("color: red")
            self.datawidget.hide()
    
    def currentindexchange(self,nChann,nNode,nSamp,nPckt,start,end):
        #self.txt.clear()
        starttime=datetime.now()
        maxsensor=self.nChann * self.nNode
        typebox_value = self.typebox.currentText()
        channelnum=self.sensor.text()
        updateprogress=self.update_popup_progress
        #popup = PopUpWindow(self)
        if typebox_value == "Timeseries Plot":
            self.plotchannel(channelnum,nChann,nNode,nSamp,nPckt,start,end)
            self.channelselect_2.hide()
            if self.sensor.text()=="" :
                self.txt_2.setText(f"Enter the sensor value between 0 and {maxsensor}")
                self.txt_2.setStyleSheet("color: green")
                return False 
        elif typebox_value == "FFT Plot":
            self.fft_plot(channelnum,nChann,nNode,nSamp,nPckt,start,end)
        elif typebox_value == "PSD Heatmap":
            #popup = PopUpWindow(self)
            #popup.show() 
            #self.update_popup_progress(100)
            #popup.exec_()
            self.fullfftheatmap_plot(nChann, nNode, nSamp, nPckt,start,end)
            self.channelselect_2.hide()
        elif typebox_value == "Power Spectral Density(psd)":
            self.psd_plot(channelnum,nChann,nNode,nSamp,nPckt,start,end)
            self.channelselect_2.show()
            if self.sensor.text()=="":
                self.txt_2.setText(f"Enter the sensor value between 0 and {maxsensor}\nnoverlap =less than nperseg(eg:128)\nnperseg={maxsensor},NFFT=1024,Fs=12800")
                self.txt_2.setStyleSheet("color: green")
        elif typebox_value == "Spectrogram":
            self.spectrogram_plot(channelnum,nChann,nNode,nSamp,nPckt,start,end)
            self.channelselect_2.show()
            if self.sensor.text()=="":
                self.txt_2.setText(f"Enter the sensor value between 0 and {maxsensor}\nnoverlap =less than nperseg(eg:128)\nnperseg={maxsensor},NFFT=1024,Fs=12800")
                self.txt_2.setStyleSheet("color: green")

        elif typebox_value == "Mean Plot":
            self.mean_plot(nChann,nNode,nSamp,nPckt,start,end)
            self.channelselect_2.hide()
     
        elif typebox_value == "Varience Plot":
            self.varience_plot(nChann,nNode,nSamp,nPckt,start,end)
            self.channelselect_2.hide()
            
        else:
            pass
        
        endtime=datetime.now()
        print(" Acoustic Data Visualization time", str(endtime-starttime),"\n")  
          
    def plotchannel(self,sensor_numbers,nChann,nNode,nSamp,nPckt,start,end):
        self.txt_2.clear()
        if not sensor_numbers:
            self.txt_2.setText(f"Enter the sensor values")
            self.txt_2.setStyleSheet("color: red")
            return
        fig = go.Figure()
        for sensor_num in sensor_numbers:
           
            dataseries=self.data[:,int(sensor_num-1)]
            fig.add_trace(go.Scatter(x=list(range(len(dataseries))), y=dataseries.flatten(),
                                 mode='lines', name=f'Sensor {sensor_num}'))
       
           
        fig.update_layout(title_text="Amplitude-time", xaxis_title="Sample Number", yaxis_title="Amplitude",margin=dict(l=0, r=0, t=35, b=0),
                      paper_bgcolor='rgba(0,0,0,0)', showlegend=True, legend=dict(y=1, x=1))
       
        #html = fig.to_html(include_plotlyjs='cdn')
        #webView = QWebEngineView()
        #webView.setHtml(html)
       
         
        offline.plot(fig, filename='channelplot.html', auto_open=False)
        webView = QWebEngineView()
        webView.load(QtCore.QUrl.fromLocalFile(os.path.abspath('channelplot.html')))  
       
        inner_layout = QVBoxLayout()
       
        #spacer_item = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        label=QLabel("Timeseries Ports:" + self.port.currentText() + " Sensors: " + ','.join(map(str,sensor_numbers)) + " Start: " + self.start.text() + " End: " + self.end.text())
        label.setStyleSheet("background-color: rgba(60,60,94,255)")
        close_button = QPushButton()
        close_button.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogCancelButton))
        close_button.setIconSize(QSize(16, 16))  # Set the desired icon size
        close_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # Create a horizontal layout for the close button and spacer
        button_layout = QHBoxLayout()
        button_layout.addWidget(label)
        button_layout.addWidget(close_button)
       
        inner_layout.setSpacing(0)
        inner_layout.addLayout(button_layout)
        inner_layout.addWidget(webView)
        inner_widget = QWidget()
        inner_widget.setMinimumHeight(350)
        inner_widget.setMaximumHeight(500)
        inner_widget.setLayout(inner_layout)
        self.Acoustic.insertWidget(0, inner_widget)  
        close_button.clicked.connect(lambda:self.close(inner_widget))
        self.clear_ac.show()   
             
        
    
        
                
                    
    def download_acoustic(self,nChann,nNode,nSamp,nPckt,start,end):
        starttime=datetime.now()
       
        self.txt_2.clear()
        if self.flag!=True or len(self.data)==0:
            self.txt_2.setText(f"Extract data first to download")
            self.txt_2.setStyleSheet("color: red")
            return            
        popup = PopUpWindow(self)
        popup.exec_()

        data=pd.DataFrame(self.data)
        column_values = [f"sensor{i}" for i in range(1, data.shape[1] + 1)]
        data.columns = column_values        
       
        path= "./Downloads/"+ self.filename.currentText().replace(".gdr","")
        try:
            os.mkdir(path)        
        except:
            pass        
        popup.update_progress(50)      
        data.to_csv(path+ "/"+self.port.currentText()+"_Start"+self.start.text()+"_End"+self.end.text(), index=True)
        self.txt_2.setText("Download successfull")
        self.txt_2.setStyleSheet("color:green")        
   
        endtime=datetime.now()
        popup.update_progress(100)
        #popup.exec_()
        print(" Acoustic data Download time", str(endtime-starttime),"\n")
        return True
 
    def psd_plot(self, sensor_numbers, nChann, nNode, nSamp, nPckt, start, end):
        self.txt_2.clear()
       

        if not sensor_numbers:
            self.txt_2.setText(f"Enter the sensor values")
            self.txt_2.setStyleSheet("color: red")
            return

        try:
           # Try to get user-entered values for parameters
           window = self.typebox_window.currentText()
           noverlap = int(self.noverlap.text())
           nperseg = int(self.nperseg.text())
           nfft = int(self.nfft.text())
           fs = float(self.fs.text())
           # Check if noverlap is less than nperseg
           if noverlap >= nperseg:
              self.txt_2.setText("Overlap (noverlap) must be less than Segment Length (nperseg)")
              self.txt_2.setStyleSheet("color: red")
              return False
           if nperseg >=nfft:
              self.txt_2.setText("Segment Length (nperseg) must be less than nfft ")
              self.txt_2.setStyleSheet("color: red")
              return False

         
        except ValueError :
                          # Handle the case where user input is missing or invalid
                          self.txt_2.setText(f"Enter all the reruired parameters")
                          self.txt_2.setStyleSheet("color: red")
                          return False  
       
        # Prepare a list to store the variance values and corresponding sensor numbers
        variances = []

        for sensor_num in sensor_numbers:
           
            dataseries=self.data[:,sensor_num-1]
            # Calculate the variance of the sensor data and store it along with the sensor number
            variance = np.var(dataseries.flatten())
            variances.append((sensor_num, variance))
        print("started")
        # Sort the sensor numbers based on variance in descending order
        sorted_variances = sorted(variances, key=lambda x: x[1], reverse=True)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_title("Power Spectral Density (PSD)")
       
        for i, (sensor_num, _) in enumerate(sorted_variances):
           
            dataseries=self.data[:,sensor_num-1]
            # Calculate the PSD using Welch's method
            f, Pxx = signal.welch(dataseries.flatten(), fs=fs, window=window, noverlap=noverlap, nperseg=nperseg, nfft=nfft)

            # Creating the stem plot for each sensor's PSD
            markerline, stemlines, baseline = ax.stem(f, Pxx, linefmt='C{}'.format(i), markerfmt='C{}o'.format(i), basefmt=' ')
       
        ax.set_ylabel("PSD (dB/Hz)")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_xlim(0, fs / 2)  # Display up to Nyquist frequency
        ax.legend(['Sensor {}'.format(sensor_num) for sensor_num, _ in sorted_variances])
       
        plt.tight_layout()

        # Create a new FigureCanvas to display the matplotlib figure within the GUI
        canvas = FigureCanvas(fig)
       
        # Add navigation toolbar for zoom in and zoom out
        navigation_toolbar = NavigationToolbar(canvas, self)

        inner_layout = QVBoxLayout()
        label = QLabel("Power Spectral Density (PSD) Ports:" + self.port.currentText() + " Sensors: " + ','.join(map(str, sensor_numbers)) + " Start: " + self.start.text() + " End: " + self.end.text())
        label.setStyleSheet("background-color: rgba(60,60,94,255)")
        close_button = QPushButton()
        close_button.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogCancelButton))
        close_button.setIconSize(QSize(16, 16))  # Set the desired icon size
        close_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        button_layout = QHBoxLayout()
        button_layout.addWidget(label)
        button_layout.addWidget(close_button)

        inner_layout.setSpacing(0)
        inner_layout.addLayout(button_layout)
       
        # Add the navigation toolbar above the canvas
        inner_layout.addWidget(navigation_toolbar)
        # Add the matplotlib canvas to the layout
        inner_layout.addWidget(canvas)

        inner_widget = QWidget()
        inner_widget.setMinimumHeight(350)
        inner_widget.setMaximumHeight(500)
        inner_widget.setLayout(inner_layout)
        self.Acoustic.insertWidget(0, inner_widget)
        close_button.clicked.connect(lambda: self.close(inner_widget))
        self.clear_ac.show()
        
    def spectrogram_plot(self, channelnum, nChann, nNode, nSamp, nPckt, start, end):
        self.txt_2.clear()
   
        try:
            window = self.typebox_window.currentText()
            noverlap = int(self.noverlap.text())
            nperseg = int(self.nperseg.text())
            nfft = int(self.nfft.text())
            fs = float(self.fs.text())
            # Check if noverlap is less than nperseg
            if noverlap >= nperseg:
                self.txt_2.setText("Overlap (noverlap) must be less than Segment Length (nperseg)")
                self.txt_2.setStyleSheet("color: red")
                return False
            if nperseg >= nfft:
                self.txt_2.setText("nfft must be larger than Segment Length (nperseg)")
                self.txt_2.setStyleSheet("color: red")
                return False
        except ValueError:
            # Handle the case where user input is missing or invalid
            self.txt_2.setText(f"Enter all the required parameters")
            self.txt_2.setStyleSheet("color: red")
            return False

        # Split the channel numbers by comma and process them one by one
        channel_list = channelnum.split(',')
        for channel in channel_list:
            if not channel.strip().isnumeric():
                self.txt_2.setText(f"Enter single sensor value")
                self.txt_2.setStyleSheet("color: red")
                return False

        # Process each channel number
        for channel in channel_list:
            channel = channel.strip()  # Remove leading/trailing spaces
            dataseries = self.data[:, int(channel) - 1]
            f, t, Sxx = signal.spectrogram(dataseries.flatten(), fs=float(fs), window=window, noverlap=int(noverlap),
                                       nperseg=int(nperseg), nfft=int(nfft))

            plt.figure(figsize=(8, 6))
            plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
            plt.colorbar(label='dB')
            plt.title(f"Spectrogram - Channel {channel}")
            plt.xlabel("Time (sec)")
            plt.ylabel("Frequency (Hz)")
            #plt.grid(True)
            plt.tight_layout()

            inner_layout = QVBoxLayout()
            label = QLabel(f"Spectrogram Port: {self.port.currentText()} Channel: {channel} Start: {self.start.text()} End: {self.end.text()}")
            label.setStyleSheet("background-color: rgba(60,60,94,255)")
            close_button = QPushButton()
            close_button.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogCancelButton))
            close_button.setIconSize(QSize(16, 16))
            close_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            button_layout = QHBoxLayout()
            button_layout.addWidget(label)
            button_layout.addWidget(close_button)

            inner_layout.setSpacing(0)
            inner_layout.addLayout(button_layout)
            inner_widget = QWidget()
            inner_widget.setMinimumHeight(350)
            inner_widget.setMaximumHeight(500)
            inner_widget.setLayout(inner_layout)
            self.Acoustic.insertWidget(0, inner_widget)
            close_button.clicked.connect(lambda: self.close(inner_widget))
            self.clear_ac.show()

            # Display the Matplotlib plot in your application
            canvas = FigureCanvasQTAgg(plt.gcf())
            navigation_toolbar = NavigationToolbar(canvas, self)  # Create the navigation toolbar
            inner_layout.addWidget(navigation_toolbar)  # Add the toolbar to the layout
            inner_layout.addWidget(canvas)
            
    def fullfftheatmap_plot(self, nChann, nNode, nSamp, nPckt,start,end):
        channelnum= self.sensor.text()
        self.txt_2.clear()
        #popup = PopUpWindow(self)
        #popup.exec_()        
        #popup.update_progress(50)
        #popup.progress_bar.setValue(50)
        fs = 12800  
        f, self.fft = signal.welch(self.data, fs=fs,nperseg=261)  
        print(self.fft.shape,self.fft.size)
        #fig = go.Figure(data=go.Heatmap(z=self.psd.T, x=f, y=np.arange(1, nNode * nChann + 1), colorscale='Viridis'))
        # Create a range of sensor indices from 1 to nNode*nChann
        all_sensor_indices = np.arange(1, nNode * nChann + 1)
        # Check if any sensor indices are missing in the dataseries
        missing_indices = np.setdiff1d(all_sensor_indices, np.arange(1, nChann * nNode + 1))
        # Add missing columns to dataseries filled with zeros
        '''
        if len(missing_indices) > 0:
           missing_columns = np.zeros((self.fft.shape[0], len(missing_indices)))
           self.fft = np.hstack((self.fft, missing_columns))
        print(self.fft.shape, self.fft.size)
        '''
        # If there are missing sensors, add them with zeros
        if len(all_sensor_indices) > self.fft.shape[1]:
            missing_columns = np.zeros((self.fft.shape[0], len(all_sensor_indices) - self.fft.shape[1]))
            self.fft = np.hstack((self.fft, missing_columns))
        startsensor = self.startsensor.text()
        endsensor = self.endsensor.text()
        startfreq = self.startfreq.text()
        endfreq = self.endfreq.text()

        
        
        if(startsensor and endsensor  and startfreq  and endfreq):
            self.fft = self.fft[int(self.startfreq.text()):(int(self.endfreq.text()))+1, int(self.startsensor.text()):(int(self.endsensor.text()))+1]
            fig=go.Figure(data=go.Heatmap(z=self.fft.T,x=np.arange(int(self.startfreq.text()),(int(self.endfreq.text()))+1),y=np.arange(int(self.startsensor.text()),(int(self.endsensor.text()))+1),colorscale='Viridis'))
            print(self.fft)
            fig.update_layout(title='PSD Heatmap of Sensor Data',
                          xaxis=dict(title='Frequency(Hz)'),
                          yaxis=dict(title='Sensor Index'),
                          coloraxis=dict(colorscale='Viridis'),margin=dict(l=0, r=0, t=30,b=0),
                          paper_bgcolor='rgba(0,0,0,0)',
                          showlegend=False)#width=450,height=650)
            
        else:
            fig = go.Figure(data=go.Heatmap(z=self.fft.T, colorscale='Viridis'))  
            fig.update_layout(title='PSD Heatmap of Sensor Data',
                          xaxis=dict(title='Frequency(Hz)'),
                          yaxis=dict(title='Sensor Index'),
                          coloraxis=dict(colorscale='Viridis'),margin=dict(l=0, r=0, t=30,b=0),
                          paper_bgcolor='rgba(0,0,0,0)',
                          showlegend=False)#width=450,height=650)
        
        # Save the plot as an HTML file
        offline.plot(fig, filename='fullfftheatmap.html', auto_open=False)

        # Find and remove the previous plot widget from the layout
        previousWidget = None
        
        for i in reversed(range(self.Heatplot.count())):
            item = self.Heatplot.itemAt(i).widget()
            if isinstance(item, QWebEngineView):
               previousWidget = item
               self.Heatplot.removeWidget(item)
               item.deleteLater()
    	
        # Create a new WebView for the new heatmap plot
        self.webView = QWebEngineView()
        self.webView.load(QtCore.QUrl.fromLocalFile(os.path.abspath('fullfftheatmap.html')))
        self.Heatplot.addWidget(self.webView)
        self.webView.show()
        self.typebox.setCurrentIndex(0) 
        self.heatwidget.show()
        self.download_hmap.clicked.connect(lambda:self.download_heatmap(self.sensor.text(),nChann,nNode,nSamp,nPckt))
        #popup.update_progress(100)
        #popup.progress_bar.setValue(100)
        #popup.ok_button.show()
        #popup.exec_()
        

    def mean_plot(self, nChann, nNode, nSamp, nPckt, start, end):
        channelnum = self.sensor.text()
        self.txt_2.clear()
        

        # Create a list to store the data for each sensor
        sensor_data = []
        for sensor_num in range(1, nNode * nChann + 1):
            sensor_data.append(self.data[:, sensor_num - 1])  # Subtract 1 to account for 0-based indexing

        # Perform one-way ANOVA test
        f_statistic, p_value = f_oneway(*sensor_data)  # Perform ANOVA on all sensor data

        # Display ANOVA results in txt_2
        self.txt_2.clear()
        # Display ANOVA results in txt_2
        result_text = f"ANOVA F-statistic: {f_statistic}\nANOVA p-value: {p_value}"
        self.txt_2.setText(result_text)  # Set the text to display the ANOVA results
        self.txt_2.setStyleSheet("color: green")

        
        mean_values = np.mean(self.data, axis=0)  # Calculate mean along columns
        #print(mean_values)
        # Create a range of sensor indices from 1 to nNode * nChann
        #sensor_indices = np.arange(1, nNode * nChann + 1)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_title("Mean Amplitude vs. Sensor Index")

        # Creating the stem plot for mean values
        markerline, stemlines, baseline = ax.stem(mean_values, basefmt=' ')

        ax.set_xlabel("Sensor Index")
        ax.set_ylabel("Mean Amplitude")

        plt.tight_layout()

        # Create a new FigureCanvas to display the matplotlib figure within the GUI
        canvas = FigureCanvas(fig)
        # Add navigation toolbar for zoom in and zoom out
        navigation_toolbar = NavigationToolbar(canvas, self)


        inner_layout = QVBoxLayout()
        label = QLabel("Mean Amplitude Plot Ports:" + self.port.currentText()  + " Start: " + self.start.text() + " End: " + self.end.text())
        label.setStyleSheet("background-color: rgba(60,60,94,255)")
        close_button = QPushButton()
        close_button.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogCancelButton))
        close_button.setIconSize(QSize(16, 16))  # Set the desired icon size
        close_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        button_layout = QHBoxLayout()
        button_layout.addWidget(label)
        button_layout.addWidget(close_button)

        inner_layout.setSpacing(0)
        inner_layout.addLayout(button_layout)
        
        # Add the navigation toolbar above the canvas
        inner_layout.addWidget(navigation_toolbar)
        
        # Add the matplotlib canvas to the layout
        inner_layout.addWidget(canvas)

        inner_widget = QWidget()
        inner_widget.setMinimumHeight(350)
        inner_widget.setMaximumHeight(500)
        inner_widget.setLayout(inner_layout)
        self.Acoustic.insertWidget(0, inner_widget)
        close_button.clicked.connect(lambda: self.close(inner_widget))
        self.clear_ac.show()

    def varience_plot(self, nChann, nNode, nSamp, nPckt, start, end):
        channelnum = self.sensor.text()
        
        self.txt_2.clear()
        # Create a list to store the data for each sensor
        sensor_data = []
        for sensor_num in range(1, nNode * nChann + 1):
            sensor_data.append(self.data[:, sensor_num - 1])  # Subtract 1 to account for 0-based indexing

        # Perform one-way ANOVA test on each group of sensor data
        f_statistic, p_value = f_oneway(*sensor_data)

        # Display ANOVA results in txt_2
        self.txt_2.clear()
        result_text = f"ANOVA F-statistic for Variance: {f_statistic}\nANOVA p-value for Variance: {p_value}"
        self.txt_2.setText(result_text)
        self.txt_2.setStyleSheet("color: green")

        varience_values = np.var(self.data, axis=0)  # Calculate varience along columns
        #print(varience_values)
        # Create a range of sensor indices from 1 to nNode * nChann
        sensor_indices = np.arange(1, nNode * nChann + 1)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_title("Varience Amplitude vs. Sensor Index")

        # Creating the stem plot for varience values
        markerline, stemlines, baseline = ax.stem(sensor_indices, varience_values, basefmt=' ')

        ax.set_xlabel("Sensor Index")
        ax.set_ylabel("Varience Amplitude")

        plt.tight_layout()

        # Create a new FigureCanvas to display the matplotlib figure within the GUI
        canvas = FigureCanvas(fig)
        # Add navigation toolbar for zoom in and zoom out
        navigation_toolbar = NavigationToolbar(canvas, self)


        inner_layout = QVBoxLayout()
        label = QLabel("varience Amplitude Plot Ports:" + self.port.currentText() + " Start: " + self.start.text() + " End: " + self.end.text())
        label.setStyleSheet("background-color: rgba(60,60,94,255)")
        close_button = QPushButton()
        close_button.setIcon(QApplication.style().standardIcon(QStyle.SP_DialogCancelButton))
        close_button.setIconSize(QSize(16, 16))  # Set the desired icon size
        close_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        button_layout = QHBoxLayout()
        button_layout.addWidget(label)
        button_layout.addWidget(close_button)

        inner_layout.setSpacing(0)
        inner_layout.addLayout(button_layout)
        
        # Add the navigation toolbar above the canvas
        inner_layout.addWidget(navigation_toolbar)
        
        # Add the matplotlib canvas to the layout
        inner_layout.addWidget(canvas)

        inner_widget = QWidget()
        inner_widget.setMinimumHeight(350)
        inner_widget.setMaximumHeight(500)
        inner_widget.setLayout(inner_layout)
        self.Acoustic.insertWidget(0, inner_widget)
        close_button.clicked.connect(lambda: self.close(inner_widget))
        self.clear_ac.show()
    
    
    def download_heatmap(self,channelnum,nChann,nNode,nSamp,nPckt):
        self.txt_2.clear()
        popup = PopUpWindow(self)
        popup.show()

        data=pd.DataFrame(self.fft)
        # Set the column names as "sensor1", "sensor2", ..., "sensor261"
        column_values = [f"sensor{i}" for i in range(1, data.shape[1] + 1)]
        data.columns = column_values

        # Set the index names as "freq1", "freq2", ..., "freqN"
        index_values = [f"freq{i}" for i in range(1, data.shape[0] + 1)]
        data.index = index_values

        #print(data)
       
        path= "./Downloads/PSD_heatmap"+ self.filename.currentText().replace(".gdr","")
        try:
            os.mkdir(path)        
        except:
            pass
       
               
        data.to_csv(path+ "/PSD_Heatmap"+self.port.currentText()+"_"+channelnum+"_"+self.start.text()+"_"+self.end.text(), index=True)
       
        self.txt_2.setText("Download successfull")
        self.txt_2.setStyleSheet("color:green")
        self.update_popup_progress(100)
        popup.exec_()
        return True  
    
    
           
    def backfun(self):
        #logging.info("Exiting Query and Retrieve Window\n")
        self.db.close()
        widget.removeWidget(self)
        size = widget.count()
        for i in range(size):
            widg = widget.widget(size-i)
            widget.removeWidget(widg)
        welcome = Welcome_Screen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
        self.fixedsize()
	    
	    
    def logoutfun(self):
        widget.removeWidget(self)
        self.db.close()
        size = widget.count()
        for i in range(size+1):
            widg = widget.widget(size-i)
            widget.removeWidget(widg)
        login = Login_Screen()
        widget.addWidget(login)
        #logging.info("Successfully Logged Out")
        self.fixedsize()
	    
    

class WorkerThread(QThread):
    update_progress = pyqtSignal(int)
    processed_data = pyqtSignal(np.ndarray)
    
    def __init__(self, port, file, ports, packets, starttimestamp,endtimestamp, parent=None):
        super().__init__(parent)
        self.starttimestamp = starttimestamp
        self.endtimestamp=endtimestamp
        #self.packetcount = packetcount
        self.ports=ports
        self.packets=packets
        self.file=file
        self.port=port

    def run(self):   
        start_time = datetime.now()
        #mint=1     
        metaheader=self.parsefieldtype(self.packets["metaheader"]["fields"]) 
        acoustic=self.parsefieldtype(self.packets["acoustic"]["fields"]) 
        size_acous=self.packets["acoustic"]["fields"]["Value"]["size"]
        percent= 0 
        self.update_progress.emit(percent)
        count=0
        databuffer=bytearray() 
        
        duration = self.endtimestamp - self.starttimestamp 
        
        nPckt = self.ports[str(self.port)][0]["nPckt"]
        nNode = self.ports[str(self.port)][0]["nNode"]
        nSamp = self.ports[str(self.port)][0]["nSamp"]
        nChann = self.ports[str(self.port)][0]["nChann"]
        
        total= math.floor(int(duration)) * nNode * nPckt

        while True:             
            buffer= self.file.read(metaheader.itemsize)   
            if not buffer:
                print("eof reached..")                
                dataseries = np.frombuffer(databuffer, acoustic)
                dataseries = dataseries["Value"].astype(int)
                print(len(dataseries))
                reccount= len(dataseries)//(nNode)
                dataseries= dataseries[:(reccount*nNode)]
                print(len(dataseries))
                dataseries = dataseries.reshape(-1, nNode, nSamp, nChann)
                dataseries = np.transpose(dataseries, [0, 2, 1, 3])
                dataseries = dataseries.reshape(-1, nNode * nChann)
                dataseries = dataseries / (2 ** 13) * (2.5) - (2.5)
                print(dataseries.shape)
                print(f"Writing minute-{duration} data from port {dest_port}")            
                dataseries = np.array([], dtype=acoustic)
                databuffer=bytearray()
                end_time = datetime.now()
                print(f"Time taken for minute {duration}: {end_time - start_time}\n")                 
                self.file.close()
                break  
            metahdr=np.frombuffer(buffer,metaheader)        
            dest_port =int(metahdr['DestUDPPort'])                 
            pkt_size =int(metahdr['Packetsize'])    
            timestamp=int(metahdr['Timestamp'])            
                                    
            #print(dest_port,port)
            if dest_port==int(self.port):
                if count < total:
                    count += 1
                    databuffer += self.file.read(pkt_size)
                else:                    
                    dataseries = np.frombuffer(databuffer, acoustic)
                    dataseries = dataseries["Value"].astype(int)
                    dataseries = dataseries.reshape(-1, nNode, nSamp, nChann)
                    dataseries = np.transpose(dataseries, [0, 2, 1, 3])
                    dataseries = dataseries.reshape(-1, nNode * nChann)
                    dataseries = dataseries / (2 ** 13) * (2.5) - (2.5)
                    print(dataseries.shape)            
                    print(f"Writing minute-{duration} data from port {dest_port}")           
                    end_time = datetime.now()
                    print(f"Time taken for minute {duration}: {end_time - start_time}\n")
                    #output = os.path.join(output_dir, f'{dest_port}_{mint}min_timeseries')
                    #header_row = ",".join([f"sensor{i + 1}" for i in range(nNode * nChann)])
                    #output.write(header_row + "\n")                    
                    break          
            
                                        
            else:
                self.file.seek(pkt_size,1)   
                
            percent= count*100/total
            print(percent)
            self.update_progress.emit(percent)
        
       
        self.update_progress.emit(100)        
        self.processed_data.emit(dataseries)
            
            
    def parsefieldtype(self,field_dict):
        datatypedict= {'unsigned long':'u4','unsigned long long':'u8','unsigned char':'u1','unsigned short':'u2',
               'unsigned int':'u4','int':'i4','float':'f4'}
        endiandict={'little':'<','big':'>'}
        dtlist=[]
        for key,value in field_dict.items():
            value=DotMap(value)        
            if(value.size):            
                dtype= (key,endiandict[value.endianness]+datatypedict[value.datatype],value.size)
            else:
                dtype= (key, endiandict[value.endianness]+datatypedict[value.datatype])
            dtlist.append(dtype)
        fieldtype=np.dtype(dtlist)
        return fieldtype    
            
            
class PopUpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        #super(PopUpWindow, self).__init__()
        loadUi(GUI_path+"/frontend/pop_up.ui",self)
        
        self.setWindowTitle("Extracting Data")
        self.ok_button.hide()
        self.ok_button.clicked.connect(self.accept)
        self.label = QLabel("Extracted: 0%")
        self.progress_bar.setValue(0) 
        self.setModal(True) 
        
    def update_progress(self, value):
        self.label.setText(f"Extracted: {value}%")
        self.progress_bar.setValue(value)
        if value==100:
            self.ok_button.show()
            
            

            
        	




def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
       
GUI_path = resource_path("")  
download_path = resource_path("")
    
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print('running in a PyInstaller bundle')
else:
    print('running in a normal Python process')
    
    

app = QApplication(sys.argv)

screen = app.primaryScreen()
rect = screen.availableGeometry()

welcome = Login_Screen()
welcome.setWindowFlags(Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint | Qt.WindowType_Mask)

widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setMinimumSize(892, 750)
widget.setWindowTitle("ATHARVA")

# Calculate the center position of the screen
widget.setGeometry(
    rect.center().x() - widget.width() // 2,
    rect.center().y() - widget.height() // 2,
    widget.width(),
    widget.height()
)

widget.show()

if __name__ == '__main__':
    #try:
    sys.exit(app.exec_())
    #except:
    print("Exiting!!") 
    

    
    
    
    
    
    
    
    
    

