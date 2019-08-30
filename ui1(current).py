from PyQt5 import QtGui,QtWidgets,QtCore
from PyQt5.QtWidgets import QApplication,QRadioButton,QPushButton,QListWidget,QDial,QSpinBox,QLCDNumber,QMessageBox,QLabel
from PyQt5.QtGui import QPixmap
import sys
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import time
import threading
from digi.xbee.devices import *
import serial
import platform







class window(QtWidgets.QMainWindow):   
   def __init__(self):
      super(window,self).__init__()
      self.currentlocal=0
      self.data=None
      self.checker=0
      self.lastcolored=0
      self.photo = QLabel(self)
      self.port=0
      self.pixmap = QPixmap('photo.png')
      self.pixmap = self.pixmap.scaled(600, 300, QtCore.Qt.KeepAspectRatio)
      self.photo.setPixmap(self.pixmap)

      self.labelgif=QLabel(self)      
      self.labelgif.setStyleSheet("QLabel { background-color : white;}");
      self.labelgif.setGeometry(100,50,500,430)
      self.movie = QtGui.QMovie('data.gif', QtCore.QByteArray(),self.labelgif)
      self.movie.setSpeed(100)
      self.labelgif.setMovie(self.movie) 
      self.movie.start()
      self.labelgif.setVisible(False)

      self.labelyazi=QLabel(self)
      self.labelgif1=QLabel(self)      
      self.labelgif1.setStyleSheet("QLabel { background-color : white;}")
      self.labelyazi.setText('G'+"\u00F6"+"zl"+"\u0259"+"yin..")
      font1=QtGui.QFont('Times',17)
      self.labelyazi.setFont(font1)
      self.labelyazi.setVisible(False)
      self.labelyazi.setGeometry(350,150,150,60)
      self.labelgif1.setGeometry(150,100,489,289)
      self.movie1 = QtGui.QMovie('wait.gif', QtCore.QByteArray(),self.labelgif1)
      self.movie1.setSpeed(100)
      self.labelgif1.setMovie(self.movie1) 
      self.movie1.start()
      self.labelgif1.setVisible(False)

      
      self.setWindowTitle("Diplom i\u015Fi v1")      
      self.setWindowIcon(QtGui.QIcon('pyicon.png'))
      self.button = QPushButton('PyQt5 button', self)#button yaradildi
      self.listw=QListWidget(self)#listWidget yaradildi
      self.button1=QPushButton(self)
      self.buttonlocal=QPushButton(self)
      self.buttonlocal.setText('Qo\u015F')
      self.button1.setText("Temperaturu"+" " +"\u00F6"+"l"+"\u00E7")
      self.dial=QDial(self)
      self.lcd=QLCDNumber(self)
      self.label=QLabel(self)
      self.labelrefresh=QLabel(self)
      self.obj=[]
   
      
      self.listCOM=QListWidget(self)
      self.spin=QSpinBox(self)
      self.radiosan=QRadioButton(self)
      self.radiosan.setText("Saniy"+"\u0259")
      self.radiodeq=QRadioButton(self)
      self.radiodeq.setText("D"+"\u0259"+"qiq"+"\u0259")
      self.starting()
      self.initUI()

      
   def initUI(self):                  
        self.setFixedSize(700,500)
        self.dial.setNotchesVisible(True)
        self.labelrefresh.setText('Yenil\u0259m\u0259k \u00FC\u00E7\u00FCn F5 d\u00FCym\u0259sini s\u0131x\u0131n ')
        self.labelrefresh.setStyleSheet("QLabel{background-color: yellow; }")
        font=QtGui.QFont('Times',10,QtGui.QFont.Bold)
        self.labelrefresh.setFont(font)
        self.lcd.setVisible(False)
        self.photo.setVisible(False)
        self.photo.raise_()            
        self.labelgif.raise_()
        self.labelgif1.raise_()
        self.labelyazi.raise_()
        self.spin.setRange(1,60)
        self.dial.setRange(1,60)
        self.button.setText("\u015E"+"\u0259"+"b\u0259k\u0259ni yoxla")
        self.button1.setEnabled(False)
        self.button.setEnabled(False)
        self.spin.setEnabled(False)
        self.dial.setEnabled(False)
        self.radiosan.setEnabled(False)
        self.radiodeq.setEnabled(False)
        self.label.setText('Qo\u015Fulmu'+'\u015F cihaz yoxdur')
        self.label.setStyleSheet("QLabel { background-color : #e20000; color : black; }");
        newfont = QtGui.QFont('Times',11) 
        self.label.setFont(newfont)        
        

        
        #geometries
        self.setGeometry(40,50,700,500)
        self.button.setGeometry(20,40,120,50)
        self.listw.setGeometry(380,160,300,200)
        self.button1.setGeometry(575,40,120,50)
        self.dial.setGeometry(40,400,75,70)
        self.spin.setGeometry(150,425,50,25)
        self.radiosan.setGeometry(150,400,75,25)
        self.radiodeq.setGeometry(150,380,75,25)
        self.lcd.setGeometry(300,40,100,50)
        self.buttonlocal.setGeometry(150,40,125,50)
        self.label.setGeometry(520,440,155,30)
        self.listCOM.setGeometry(20,160,300,200)
        self.labelrefresh.setGeometry(20,100,220,30)
        self.photo.setGeometry(50,100,600,300)
        
    
        #events
        self.buttonlocal.clicked.connect(self.checklocal)
        self.button.clicked.connect(self.thread1)
        self.button.clicked.connect(self.threadnetwork)
        self.dial.valueChanged.connect(self.spin.setValue)
        self.spin.valueChanged.connect(self.dial.setValue)
        self.listCOM.doubleClicked.connect(self.showdialog)
        self.listw.doubleClicked.connect(self.showdialogremote)
        self.button1.clicked.connect(self.thread) # communication
        self.radiodeq.clicked.connect(self.spinvalue)
        self.radiosan.clicked.connect(self.dialvalue)
        self.button1.clicked.connect(self.threadback)


    
   def threadback(self):
      if  self.radiodeq.isChecked() or self.radiosan.isChecked():
         self.thread1=threading.Thread(target=self.send)
         self.thread1.start()
      else:
         pass
   def loading(self):
      m=loading()
      

      
   def send(self):
      try:    
         self.currentlocal.open()
         remotestr=self.listw.currentItem().text()
         li=remotestr.split("-")
         xbee_network=self.currentlocal.get_network()         
         remote=xbee_network.get_device_by_64(XBee64BitAddress.from_hex_string(li[0]))
         arr_64=self.currentlocal.get_64bit_addr()
         NEW_TIMEOUT_FOR_SYNC_OPERATIONS = 1
         self.currentlocal.set_sync_ops_timeout(NEW_TIMEOUT_FOR_SYNC_OPERATIONS)
         if self.radiosan.isChecked():
            self.currentlocal.send_data(remote,str(arr_64)+"-"+str(self.spin.value()))
         else:
            self.currentlocal.send_data(remote,str(arr_64)+"-"+str(self.spin.value()*60))
         self.labelgif1.setVisible(False)     
         
                   
         self.labelgif1.setVisible(True)
         self.labelyazi.setVisible(True)
         while(True):
            self.data=self.currentlocal.read_data()
            if(self.data!=None):
               self.data=self.data.data.decode()
               self.labelgif1.setVisible(False)
               self.labelyazi.setVisible(False)
               break 
             
         self.currentlocal.close()
         
         data_list=self.data.split(',')
         self.labelgif.setVisible(True)
         
         objects = []
         performance=[]
         for i in range(1,len(data_list)):
            objects.append(i)
         for i in range(len(data_list)-1):
            li=data_list[i]
            li=li.split('-')
            performance.append(li[1])
         
         y_pos = np.arange(len(objects))
         objects=tuple(objects)
         plt.figure("Qrafik")
         plt.xticks(y_pos, objects)
         plt.ylabel('Temperatur')
         plt.xlabel('Zaman')
         plt.plot(y_pos,performance)
         self.labelgif.setVisible(False)
         plt.show()
         self.data=None
         
      except:
         print('salam')
         self.currentlocal.close()
      
         

         
   def showdialog(self): 
      try:
         li=self.listCOM.currentItem().text().split('-')
         local=XBeeDevice(li[2],9600)
         local.open()
         arr_64=local.get_64bit_addr()
         arr_16=local.get_16bit_addr()
         arr_node=local.get_node_id()
         arr_pro=local.get_protocol()
         arr_hard=local.get_hardware_version()
         local.close()
         dlg=dialog(arr_64,arr_16,arr_node,arr_pro,arr_hard)
      except:
         pass    #exception

      
   def showdialogremote(self): 
      li=self.listw.currentItem().text().split('-')
      if self.checker !=0:
         self.lastcolored.setBackground(QtGui.QColor(255,255,255))
         
      self.lastcolored=self.listw.currentItem()
      self.listw.currentItem().setBackground(QtGui.QColor(239, 255, 25))
      try:
         self.currentlocal.open()
         
         xbee_network=self.currentlocal.get_network()
         
         remote=xbee_network.get_device_by_64(XBee64BitAddress.from_hex_string(li[0]))
         
         arr_64=remote.get_64bit_addr()
         
         arr_16=remote.get_16bit_addr()
         arr_node=remote.get_node_id()
         arr_pro=remote.get_protocol()
         arr_hard=remote.get_hardware_version()
         self.currentlocal.close()
         dlg=dialog(arr_64,arr_16,arr_node,arr_pro,arr_hard)
         self.checker=1
      except:
         pass # exception
      

   def spinvalue(self):
      self.dial.setRange(1,60)
      self.spin.setRange(1,60)
      self.dial.setValue(1)
   def dialvalue(self):
      self.dial.setRange(4,60)
      self.spin.setRange(4,60)
      self.dial.setValue(4)
      
        
   def keyPressEvent(self, event):
      key = event.key()
      if key == QtCore.Qt.Key_F5:
         self.threadrefresh()


      

   def checklocal(self):                                               
      try:         
         if (self.currentlocal !=0):
            for i in range(0,self.listCOM.count()):
                 self.listCOM.item(i).setBackground(QtGui.QColor(255, 255, 255))
         self.listCOM.currentItem().setBackground(QtGui.QColor(97, 255, 66))
         li=self.listCOM.currentItem().text().split('-')
         self.currentlocal = XBeeDevice(li[2], 9600)
         self.port=li[2]        
         self.currentCOM=self.listCOM.currentItem().text()
         self.currentlocal.open()
         self.currentlocal.close()
         self.listw.clear()
         self.button1.setEnabled(True)
         self.button.setEnabled(True)
         self.spin.setEnabled(True)
         self.dial.setEnabled(True)     
         self.radiosan.setEnabled(True)
         self.radiodeq.setEnabled(True)
         if platform.system()=='Linux':
            self.label.setGeometry(500,440,180,30)
         self.label.setText('Qo\u015Fulmu'+'\u015F port: '+str(li[2]))
         self.checker=0  
         self.label.setStyleSheet("QLabel { background-color : #22ce00; color : white; }")
         
         
         
         
      except:
         QMessageBox.about(self, 'Yanl\u0131\u015F', 'Lokal cihaz\u0131n portu do\u011Fru deyil')

   def refresh(self):                                                                  
      self.listCOM.clear()
      index=0
      if platform.system()=='Windows':
         for i in range(0,257):
               try:               
                  local_xbee = XBeeDevice('COM'+str(i), 9600)
                  local_xbee.open()
                  addr64=local_xbee.get_64bit_addr()
                  noid=local_xbee.get_node_id()
                  local_xbee.close()
                  self.listCOM.addItem(str(addr64)+"-"+str(noid)+"-"+'COM'+str(i))
                  if(self.port=='COM'+str(i)):               
                     self.listCOM.item(index).setBackground(QtGui.QColor(97, 255, 66))
                  index+=1
               except:
                  pass
      elif platform.system()=='Linux':
         for i in range(257):
            try:               
               local_xbee = XBeeDevice('/dev/ttyUSB'+str(i), 9600)
               local_xbee.open()
               addr64=local_xbee.get_64bit_addr()
               noid=local_xbee.get_node_id()
               local_xbee.close()
               self.listCOM.addItem(str(addr64)+"-"+str(noid)+"-"+'/dev/ttyUSB'+str(i))
               if(self.port=='/dev/ttyUSB'+str(i)):               
                  self.listCOM.item(index).setBackground(QtGui.QColor(97, 255, 66))
               index+=1
            except:
               pass
      self.checker=0
         
      
      

         
        
   def thread(self):                                               
      if  self.radiodeq.isChecked() or self.radiosan.isChecked():
         self.thread=threading.Thread(target=self.timing)
         self.thread.start()
      else:
         QMessageBox.about(self, 'Yanl\u0131\u015F', 'Zaman vahidini se\u00E7in')

         
            
            
   def thread1(self):                                                          
      if  self.radiodeq.isChecked() or self.radiosan.isChecked():
         self.thread1=threading.Thread(target=self.scan)
         self.thread1.start()
      else:
         QMessageBox.about(self, 'Yanl\u0131\u015F', 'Zaman vahidini se\u00E7in')

   def threadnetwork(self):
      if  self.radiodeq.isChecked() or self.radiosan.isChecked():
         self.thread1=threading.Thread(target=self.network)
         self.thread1.start()
      else:
         pass


   def network(self):
      try:
         self.button1.setEnabled(False)
         self.buttonlocal.setEnabled(False)
         self.button.setEnabled(False)
         self.button1.setEnabled(False)
         self.spin.setEnabled(False)
         self.dial.setEnabled(False)    
         self.radiosan.setEnabled(False)
         self.radiodeq.setEnabled(False)
         self.listw.clear()
         self.currentlocal.open()
         xbee_network=self.currentlocal.get_network()
         xbee_network.clear()
         listdev=[]
         def callback_device_discovered(remote):
            listdev.append(str(remote))
         if self.radiosan.isChecked():
            if(self.spin.value()>25):
               defe=int((self.spin.value())/25)
               qaliqsan=(self.spin.value())%25
               for i in range(0,defe):
                  xbee_network.set_discovery_timeout(22)  
                  xbee_network.add_device_discovered_callback(callback_device_discovered)
                  xbee_network.start_discovery_process()
                  while xbee_network.is_discovery_running():
                     QtCore.QThread.msleep(100)
               if(qaliqsan<4):
                  add=q=4-qaliqsan
                  xbee_network.set_discovery_timeout(qaliqsan+add)  
                  xbee_network.add_device_discovered_callback(callback_device_discovered)
                  xbee_network.start_discovery_process()
                  while xbee_network.is_discovery_running():
                     QtCore.QThread.msleep(100)
               else:
                  xbee_network.set_discovery_timeout(qaliqsan) 
                  xbee_network.add_device_discovered_callback(callback_device_discovered)
                  xbee_network.start_discovery_process()
                  while xbee_network.is_discovery_running():
                     QtCore.QThread.msleep(100)
                     
               
               self.currentlocal.close()
            else:
               
               xbee_network.set_discovery_timeout(self.spin.value())   
               xbee_network.add_device_discovered_callback(callback_device_discovered)
               xbee_network.start_discovery_process()
               while xbee_network.is_discovery_running():
                  QtCore.QThread.msleep(100)
               self.currentlocal.close()
               
           
            self.photo.setVisible(True)
            listdev=list(set(listdev))
            for i in range(0,len(listdev)):
               self.listw.addItem(listdev[i])
            QtCore.QThread.msleep(1000)
            self.photo.setEnabled(True)
            self.buttonlocal.setEnabled(True)
            self.button1.setEnabled(True)
            self.button.setEnabled(True)
            self.spin.setEnabled(True)
            self.dial.setEnabled(True)     
            self.radiosan.setEnabled(True)
            self.radiodeq.setEnabled(True)
            self.photo.setVisible(False)
            
            

         if self.radiodeq.isChecked():
         
            defe=int((self.spin.value()*60)/25)
            qaliqsan=(self.spin.value()*60)%25
            for i in range(0,defe):
               xbee_network.set_discovery_timeout(22)  # 24 seconds + saniye elave.
               xbee_network.add_device_discovered_callback(callback_device_discovered)
               xbee_network.start_discovery_process()
               while xbee_network.is_discovery_running():
                  QtCore.QThread.msleep(100)
            xbee_network.set_discovery_timeout(qaliqsan)  # qaliq saniye.
            xbee_network.add_device_discovered_callback(callback_device_discovered)
            xbee_network.start_discovery_process()
            while xbee_network.is_discovery_running():
               QtCore.QThread.msleep(100)
            self.currentlocal.close()
         else:
            xbee_network.set_discovery_timeout(self.spin.value())  # qaliq saniye 
            xbee_network.add_device_discovered_callback(callback_device_discovered)
            xbee_network.start_discovery_process()
            while xbee_network.is_discovery_running():
               QtCore.QThread.msleep(100)
            self.currentlocal.close()
            
         self.photo.setVisible(True)  
         listdev=list(set(listdev))
         for i in range(0,len(listdev)):
            self.listw.addItem(listdev[i])
         QtCore.QThread.msleep(2000)
         self.buttonlocal.setEnabled(True)
         self.button1.setEnabled(True)
         self.button.setEnabled(True)
         self.spin.setEnabled(True)
         self.dial.setEnabled(True)
         self.radiosan.setEnabled(True)
         self.radiodeq.setEnabled(True)
         self.photo.setVisible(False)
         
      except:
         self.currentlocal.close()





   def threadrefresh(self):
      t=threading.Thread(target=self.refresh)
      t.start()
      


   #UI has been finished
      
   def timing(self):
      QtCore.QThread.msleep(1000)
      self.button1.setEnabled(False)
      if(self.radiodeq.isChecked()):
         self.lcd.setVisible(True)
         j=self.spin.value()*60
         k=self.spin.value()
         if(k<10):
            self.lcd.display("0{}:00".format(k))
            QtCore.QThread.msleep(1000)
         else:
            self.lcd.display("{}:00".format(k))
            QtCore.QThread.msleep(1000)
            
         j-=1
         k-=1
         while(j>-1):
            if(k<10):
               if(j%60<10):
                  if(j%60 is 0):                     
                     self.lcd.display("0{}:0{}".format(k,j%60))
                     k-=1
                     j-=1
                     QtCore.QThread.msleep(1000)
                     continue
                  self.lcd.display("0{}:0{}".format(k,j%60))
                  app.processEvents()
                  QtCore.QThread.msleep(1000)                     
                  j-=1
               else:
                  self.lcd.display("0{}:{}".format(k,j%60))
                  QtCore.QThread.msleep(1000)                     
                  j-=1
            else:
               if(j%60 is 0):
                  self.lcd.display("0{}:0{}".format(k,j%60))
                  k-=1
                  j-=1
                  QtCore.QThread.msleep(1000)
                  continue
               if(j%60<10):
                  self.lcd.display("{}:0{}".format(k,j%60))
                  QtCore.QThread.msleep(1000)
                  j-=1
               else:
                  self.lcd.display("{}:{}".format(k,j%60))
                  QtCore.QThread.msleep(1000)                     
                  j-=1
         self.lcd.setVisible(False)
         self.button1.setEnabled(True)

      elif (self.radiosan.isChecked()):
         self.lcd.setVisible(True)
         timing=self.spin.value()
         for i in range(timing,-1,-1):                     
            if(i<10):
               self.lcd.display("00:0{}".format(i))
               QtCore.QThread.msleep(1000)
               
            else:
               self.lcd.display("00:{}".format(i))
               QtCore.QThread.msleep(1000)
         self.lcd.setVisible(False)
         self.button1.setEnabled(True)

   def starting(self):
      splash=QtWidgets.QSplashScreen(QtGui.QPixmap('splash.jpg'),QtCore.Qt.WindowStaysOnTopHint)
      splash.show()
      for i in range(0,257):
         app.processEvents()
         if (i is 50):
               splash.showMessage("<h1><font color=#608fdb>Proqram başladılır!</font></h1>", QtCore.Qt.AlignTop)
               QtCore.QThread.msleep(1000)
         try:
            if (platform.system() == 'Windows'):
               local_xbee = XBeeDevice('COM'+str(i), 9600)
               local_xbee.open()
               addr64=local_xbee.get_64bit_addr()
               noid=local_xbee.get_node_id()
               local_xbee.close()
               self.listCOM.addItem(str(addr64)+"-"+str(noid)+"-"+'COM'+str(i))
            elif (platform.system() == 'Linux'):
               local_xbee = XBeeDevice('/dev/ttyUSB'+str(i), 9600)
               local_xbee.open()
               addr64=local_xbee.get_64bit_addr()
               noid=local_xbee.get_node_id()
               local_xbee.close()
               self.listCOM.addItem(str(addr64)+"-"+str(noid)+"-"+'/dev/ttyUSB'+str(i))         
         except:
            pass
      splash.close()

         
         
         



   def createlistw(self):
       self.listw.clear()
       for i in range(0,9):
          self.obj.append(i)
          self.obj[i]=elements()
          self.obj[i].t=[10,20,30,40,2,3,4,5,6]
          self.obj[i].s=[5,6,7,8,9,1,2,3,4,5,88]
          self.listw.addItem(str(self.obj[i].t[i]))

            
           

   def scan(self):
      self.button.setEnabled(False)

      if(self.radiodeq.isChecked()):
         self.lcd.setVisible(True)
         j=self.spin.value()*60
         k=self.spin.value()
         if(k<10):
            self.lcd.display("0{}:00".format(k))
            QtCore.QThread.msleep(1000)
         else:
            self.lcd.display("{}:00".format(k))
            QtCore.QThread.msleep(1000)
            
         j-=1
         k-=1
         while(j>-1):
            if(k<10):
               if(j%60<10):
                  if(j%60 is 0):
                     self.lcd.display("0{}:0{}".format(k,j%60))
                     k-=1
                     j-=1
                     QtCore.QThread.msleep(1000)
                     continue
                  self.lcd.display("0{}:0{}".format(k,j%60))
                  app.processEvents()
                  QtCore.QThread.msleep(1000)                     
                  j-=1
               else:
                  self.lcd.display("0{}:{}".format(k,j%60))
                  QtCore.QThread.msleep(1000)                     
                  j-=1
            else:
               if(j%60 is 0):
                  self.lcd.display("0{}:0{}".format(k,j%60))
                  k-=1
                  j-=1
                  QtCore.QThread.msleep(1000)
                  continue
               if(j%60<10):
                  self.lcd.display("{}:0{}".format(k,j%60))
                  QtCore.QThread.msleep(1000)
                  j-=1
               else:
                  self.lcd.display("{}:{}".format(k,j%60))
                  QtCore.QThread.msleep(1000)                     
                  j-=1
         self.lcd.setVisible(False)
         self.button.setEnabled(True)
      elif (self.radiosan.isChecked()):
         self.lcd.setVisible(True)
         timing=self.spin.value()
         for i in range(timing,-1,-1):
            if(i<10):
               self.lcd.display("00:0{}".format(i))
               QtCore.QThread.msleep(1000)                     
            else:
               self.lcd.display("00:{}".format(i))
               QtCore.QThread.msleep(1000)
         self.lcd.setVisible(False)
         self.button.setEnabled(True)

class dialog(QtWidgets.QDialog):
   def __init__(self,edit64,edit16,editnode,editpro,edithard):
      super(dialog,self).__init__()
      self.setWindowIcon(QtGui.QIcon('pyicon.png'))
      
      self.text_64=str(edit64)
      self.text_16=str(edit16)
      self.text_node=str(editnode)
      protocol=str(editpro).split('.')
      self.text_pro=str(protocol[1])
      self.text_hard=str(edithard)
      
      self.setFixedSize(470,325)
      self.setWindowTitle("Haqq\u0131nda")
      
      self.uiinit()
      
      self.show()
      self.exec_()


   def uiinit(self):
      
      newfont = QtGui.QFont('Times',11,QtGui.QFont.Bold)
      self.photo = QLabel(self)
      self.pixmap = QPixmap('xbee-wire.jpg')
      self.pixmap=self.pixmap.scaled(225,300,QtCore.Qt.KeepAspectRatio) 
      self.photo.setPixmap(self.pixmap)
      self.photo.move(0,20)
      
      self.label_64=QLabel("64-bitlik "+"\u00DC"+"nvan",self)
      self.label_64.setGeometry(250,0,150,30)
      self.label_64.setFont(newfont)
      self.line_64=QtWidgets.QLineEdit(self)
      self.line_64.setGeometry(250,30,210,30)
      self.line_64.setText(self.text_64)
      self.line_64.setReadOnly(True)
      
      self.label_16=QLabel("16-bitlik "+"\u00DC"+"nvan",self)
      self.label_16.setGeometry(250,60,150,30)
      self.label_16.setFont(newfont)
      self.line_16=QtWidgets.QLineEdit(self)
      self.line_16.setGeometry(250,90,210,30)
      self.line_16.setText(self.text_16)
      self.line_16.setReadOnly(True)
      
      self.label_nodeid=QLabel("Ad\u0131",self)
      self.label_nodeid.setGeometry(250,120,150,30)
      self.label_nodeid.setFont(newfont)
      self.line_nodeid=QtWidgets.QLineEdit(self)
      self.line_nodeid.setGeometry(250,150,210,30)
      self.line_nodeid.setText(self.text_node)
      self.line_nodeid.setReadOnly(True)
      
      self.label_firm=QLabel('Protokol',self)
      self.label_firm.setGeometry(250,180,210,30)
      self.label_firm.setFont(newfont)
      self.line_firm=QtWidgets.QLineEdit(self)
      self.line_firm.setGeometry(250,210,210,30)
      self.line_firm.setText(self.text_pro)
      self.line_firm.setReadOnly(True)
     
      self.label_hard=QLabel("Aparat versiyas"+"\u0131",self)
      self.label_hard.setGeometry(250,240,210,30)
      self.label_hard.setFont(newfont)
      self.line_hard=QtWidgets.QLineEdit(self)
      self.line_hard.setGeometry(250,270,210,30)
      self.line_hard.setText(self.text_hard)
      self.line_hard.setReadOnly(True)


      
            
if __name__=='__main__':       
    app=QApplication(sys.argv)
    win=window()
    win.show()
    sys.exit(app.exec_())
