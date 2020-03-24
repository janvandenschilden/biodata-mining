#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import os
from time import sleep

def download(url, fileName):
    for i in range(10):
        try:
            # Delete existing files with filename
            try:
                os.remove(fileName) 
            except:
                pass
            
            """ Use requests to download file. 
            Works with streams to be able large files without having the need of a 
            large memory.
            """
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(fileName, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192): 
                        if chunk:
                            f.write(chunk)
            return fileName
        except:
            print("Download", url,"failed:",i)
            sleep(5)