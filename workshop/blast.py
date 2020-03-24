#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
#   Import all the libraries
#------------------------------------------------------------------------------
from selenium import webdriver
import os
from time import sleep
import argparse
from download import download


#------------------------------------------------------------------------------
#   Functions
#------------------------------------------------------------------------------
def openWebDriver():
    return webdriver.Firefox()

def openBlastURL(webDriver):
    webDriver.get("https://www.uniprot.org/blast/")
 
def removeBanner(webDriver):
    try: 
        webDriver.find_element_by_id("privacy-panel-accept").click()
    except:
        pass 

def uploadSequence(webDriver, sequence):
    uploadSequenceField = webDriver.find_element_by_id("blastQuery")
    uploadSequenceField.send_keys(sequence)
    
def changeDatabase(webDriver, database="UniRef90"):
    try:
        fields = webDriver.find_elements_by_id(database)
        field = fields[0]
        field.click()
    except:
        fields = webDriver.find_elements_by_id("UniRef90")
        field = fields[0]
        field.click()

def changeEvalue(webDriver, eValue=0.001):
    try:
        eVAlueFields = webDriver.find_elements_by_name("threshold")
        eVAlueField = eVAlueFields[1]
        for option in eVAlueField.find_elements_by_tag_name('option'):
            if option.text.strip() == str(eValue):
                option.click()
                return
        raise
    except:
        eVAlueFields = webDriver.find_elements_by_name("threshold")
        eVAlueField = eVAlueFields[1]
        for option in eVAlueField.find_elements_by_tag_name('option'):
            if option.text.strip() == "0.001":
                option.click()
                return

def changeHits(webDriver, hits=1000):
    if hits in [100,1000]:
        ToClick=False
    else:
        ToClick=True
    for option in webDriver.find_elements_by_tag_name('option'):
        if option.text.strip() == str(hits):
            if ToClick:
                option.click()
                return
            else:
                ToClick=True  
    ToClick=False
    for option in webDriver.find_elements_by_tag_name('option'):
        if option.text.strip() == "1000":
            if ToClick:
                option.click()
                return
            else:
                ToClick=True
        
def submit(webDriver):
    submitButtons = webDriver.find_elements_by_id("blast-submit")   
    submitButton = submitButtons[0]                             
    submitButton.click()

def waitForJob(webDriver):
    sleep(15)
    while len(webDriver.find_elements_by_id("resulttable"))<1:
        sleep(1)
    sleep(10)
    
def downloadBlast(webDriver, output,format="list"):
    currentURL=webDriver.current_url
    newURL = currentURL+"&format="+format
    return download(newURL,output)

def closeDriver(webDriver):
    webDriver.quit()

def blast(sequence, output="temp.list" ,database="UniRef90", eValue=0.001, hits=1000, format="list"):
    def iter():
        driver= openWebDriver()
        openBlastURL(driver)
        removeBanner(driver)
        changeDatabase(driver, database=database)
        changeEvalue(driver,eValue=eValue)
        changeHits(driver,hits=hits)
        uploadSequence(driver, sequence)
        submit(driver)
        waitForJob(driver)
        file=downloadBlast(driver,output,format=format)
        closeDriver(driver)
        return file
    
    for i in range(10):
        try:
            blastFile = iter()
            if os.path.getsize(blastFile)==0:
                raise
            else:
                return blastFile
        except:
            print("Try",i,"failed")
            