from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import requests
import threading
import pygame
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal,QObject



def downloadImage(url,counter,keyword="None"):
    import urllib
    format=url[url.rindex("."):]
    try:
        urllib.request.urlretrieve(url, "/home/nimish/Documents/images/"+keyword + str(counter) + format)
    except Exception as E:
        print("Error in downloadImage function")

class myListWithSignal(QObject):
    downloadSignal = pyqtSignal()

    def __init__(self):
        super(myListWithSignal, self).__init__()
        self.myInternalList = []

    def append(self, object):
        self.myInternalList.append(object)
        self.downloadSignal.emit()

    def getLastElement(self):
        return self.myInternalList[-1]




class Process():
    def __init__(self,keyword,count=10,parent=None):
        self.driver=None
        self.keyword=keyword
        self.myUrls=[]
        self.parent=parent
        self.myElements1=None

    def startProcess(self):
        self.driver = webdriver.Chrome("/home/nimish/PycharmProjects/so/internship/macroproject/chromedriver")
        self.driver.get("http://google.co.in/images")
        self.driver.find_element_by_css_selector(".gLFyf.gsfi").send_keys(self.keyword + Keys.RETURN)
        time.sleep(3)
        self.myElements = self.driver.find_elements_by_tag_name("img")
        self.myElements1 = list(filter(lambda i: i.get_attribute('class') == 'rg_ic rg_i', self.myElements))
        mainUrl = self.driver.current_url
        try:

            for j in range(10):
                self.myElements = self.driver.find_elements_by_tag_name("img")
                self.myElements1 = list(filter(lambda i: i.get_attribute('class') == 'rg_ic rg_i', self.myElements))
                self.myElements1[j].click()
                try:
                    viewImageButton=self.driver.find_elements_by_css_selector(".irc_fsl.i3596")
                except:
                    print("viewImageButton not found")
                # time.sleep(1)
                for i in range(len(viewImageButton)):
                    if (viewImageButton[i].text=='View image'):
                        self.myUrls.append(viewImageButton[i].get_attribute('href'))
                        self.lastThread=threading.Thread(target=downloadImage,args=(self.myUrls.getLastElement(),j,self.keyword))
                        self.lastThread.start()
                        break
            self.lastThread.join()
            self.driver.quit()
            self.onFinish()

        except Exception as E:
            print(E)



    def onFinish(self):
        pygame.init()
        pygame.mixer.music.load("sound.mp3")
        pygame.mixer.music.play()


if __name__=="__main__":
    classobject=Process("company_logo",10,None)
    classobject.startProcess()
