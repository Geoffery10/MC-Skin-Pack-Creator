# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 10:10:13 2020

@author: powel
"""

import os
import shutil
from os.path import basename
from zipfile import ZipFile
import requests
import PySimpleGUI as sg

#================================METHODS=======================================

def checkForDir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    
def getUUID(id_value):
    #Scrape UUID from Online UUID Generator's Developer API
    UUID_API = "https://www.uuidgenerator.net/api/version4"
    response = requests.get(UUID_API)
    soup = BeautifulSoup(response.text, 'html.parser') 
    results = soup.prettify()
    print("Genereated: UUID", id_value, ": ", results, end = '')
    return str(results)

#==============================DRIVER CODE=====================================

#Create Directories If Missing
checkForDir(".\Skins")
checkForDir(".\Temp")
checkForDir(".\Temp/texts")

#Count Skins (This should only look for PNGs)
numberOfSkins = sum([len(files) for r, d, files in os.walk(".\Skins")])

if (numberOfSkins <= 0):
    #No skins!
    skinStrings = "No skins found in Skins folder..."
else:
    #Display Found Skins
    skinFiles = os.listdir(".\Skins")
    skinStrings = "Skins in the \"Skins\" folder will be used. Number of Skins:" + str(numberOfSkins)


sg.theme('DarkGreen')   # Add a touch of color

# All the stuff inside your window.
layout = [  [sg.Text(skinStrings)],
            [sg.Text(skinFiles)],
            [sg.Text("Please your name: "), sg.InputText()],
            [sg.Text("Please your pack's name: "), sg.InputText()],
            [sg.Text("Please your pack's description: "), sg.InputText()],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Minecraft Skin Pack Creator', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0], values[1], values[2])

    print("Trying to get UUID from the internet...")
    try:
        #Internet UUID
        from bs4 import BeautifulSoup
        uuidA = getUUID(1)
        uuidA = uuidA[:-1]
        uuidB = getUUID(2)
        uuidB = uuidB[:-1]
        print("Success!")
        layoutUUID = [  [sg.Text(uuidA)],
                      [sg.Text(uuidB)],
                      [sg.Button('Continue'), sg.Button('Cancel')] ]
        windowUUID = sg.Window('Minecraft Skin Pack Creator', layoutUUID)
        while True:
            event, values = windowUUID.read()
            window.close()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
    except:
            #Manual UUID
            print("Failed to get UUID from the internet... ")
            print("You might be missing beautifulsoup4: https://pypi.org/project/beautifulsoup4/")
            print("Recommended UUID Generator: https://www.uuidgenerator.net/version4")
            uuidA = input("Please your first UUID: ")
            uuidB = input("Please your second UUID: ")