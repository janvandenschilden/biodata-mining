#!/usr/bin/env python
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
#   Import all the libraries
#------------------------------------------------------------------------------
import argparse
from selenium import webdriver
import os
from time import sleep


#------------------------------------------------------------------------------
#   Functions
#------------------------------------------------------------------------------
def openWebDriver():
    """Opens a webdriever
    
    Returns
    -------
    selenium.webdriver object
        Variable with webdriver object
    """
    return webdriver.Firefox()

def openUniprotMappingURL(webDriver):
    """Given webdriver opens given URL
    
    Parameters
    ----------
    webDriver : selenium.webdriver object
        Given webdriver for specific browser (e.g. Firefox)
    """
    webDriver.get("https://www.uniprot.org/uploadlists/")
    
def closePanel(webDriver):
    for i in range(10):    
        try:
            field = webDriver.find_element_by_id("privacy-panel-accept")
            field.click()
            break
        except:
            sleep(1)

def uploadList(webDriver, proteinList):
    """Uploads proteinList to https://www.uniprot.org/uploadlists/
    
    Parameters
    ----------
    webDriver : selenium.webdriver object
        Given webdriver for specific browser (e.g. Firefox)
    proteinList : str
        Path of the protein list
    """
    uploadFileField = webDriver.find_element_by_id("uploadfile")
    proteinListPath=os.path.realpath(proteinList)
    uploadFileField.send_keys(proteinListPath)
    

def setDatabaseFrom(webDriver, databaseFrom="UniProtKB AC/ID"):
    for i in range(10):
        try:
            if databaseFrom=="UniProtKB AC/ID":
                pass #This is the defaukt
            elif databaseFrom=="UniRef100":
                fields = webDriver.find_elements_by_id("NF100")
                field=fields[0]
                field.click()
            elif databaseFrom=="UniRef90":
                fields = webDriver.find_elements_by_id("NF90")
                field=fields[0]
                field.click()
            elif databaseFrom=="UniRef50":
                fields = webDriver.find_elements_by_id("NF50")
                field=fields[0]
                field.click() 
            else:
                pass
            break
        except:
            sleep(1)

def submit(webDriver):
    """Push submit button
    
    Parameters
    ----------
    webDriver : selenium.webdriver object
        Given webdriver for specific browser (e.g. Firefox)
    """
    try: # Tries to close the banner first (if there is one) 
        webDriver.find_element_by_id("privacy-panel-accept").click()
    except:
        pass
    submitButton = webDriver.find_element_by_id("upload-submit")
    submitButton.click()
        
def waitForPageRefresh(webDriver, oldURL):
    """ Checks whether the page has been refreshed
    
    Parameters
    ----------
    webDriver : selenium.webdriver object
        Given webdriver for specific browser (e.g. Firefox)
    oldURL : str
        the URL that was being used before the refresh
    """
    while webDriver.current_url == oldURL:
        sleep(0.1)

def extractYoulistID(webDriver):
    """Extract yourlist ID from query
    
    Parameters
    ----------
    webDriver : selenium.webdriver object
        Given webdriver for specific browser (e.g. Firefox)
    
    Returns
    -------
    yourlist : str
        yourlist:ID, this value can furhter on be used in queries
    """
    if len(webDriver.find_elements_by_id("noResultsMessage"))==0:
        currentURL=webDriver.current_url
        yourlist = currentURL.split("query=")[1].split(r"&sort")[0]
        return yourlist
    else:
        print("No results found.")
        print("Are you sure you mapped from the right database?")
        print("UniProtKB AC/ID | UniRef100 | UniRef90 | UniRef50")
        closeDriver(webDriver)
        raise

def closeDriver(webDriver):
    """Closes the webbrowser and driver
    
    Parameters
    ----------
    webDriver : selenium.webdriver object
        Given webdriver for specific browser (e.g. Firefox)
    """
    webDriver.quit()
    
def uniprotGroupId(proteinList, databaseFrom="UniProtKB AC/ID"):
    """ Gets yourlist:ID for provided protein list
    
    Parameters
    ----------
    proteinList : str
        Path to the protein list
        
    Returns
    -------
    yourlist : str
        yourlist:ID, this value can furhter on be used in queries
    """
    #--------------------------------------------------------------------------
    #   Main Code
    #--------------------------------------------------------------------------
    for i in range(10):
         try:
           driver= openWebDriver()
           openUniprotMappingURL(driver)
           closePanel(driver)
           uploadList(driver,proteinList)
           setDatabaseFrom(driver, databaseFrom=databaseFrom)
           submit(driver)
           waitForPageRefresh(driver,"https://www.uniprot.org/uploadlists/")
           yourlist = extractYoulistID(driver)
           closeDriver(driver)
           try:
               os.remove("geckodriver.log")
           except:
               pass
           return yourlist
         except:
             print("try",i,"failed")
             sleep(1)