# -*- coding: utf-8 -*-
"""
Created on Thu May 28 13:51:48 2020

This is a Minecraft Skin Pack Creator for Bedrock

manifest.json needs: 
    packName
    2 uuid
    version
    
skins.json needs:
    localization_name - file (all lower skin name no spaces)
    geometry - geometry.humanoid.customSlim or .custom
    texture - file (including .png)
    serialized_name - creator (no spaces)
    
en_US.lang nees:
    skin.serialized_name.localization_name=skin.name
"""

import os
import shutil

#================================CLASSES=======================================

class skin:
    def __init__(self, name, file, bodyType):
        self.name = name
        self.file = file
        self.bodyType = bodyType

#================================METHODS=======================================

def checkForDir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def createSkins(skinFiles):
    skins = []
    for i in skinFiles:
        print("\n\tCurrent Skin:", i)
        file = i
        name = input("\nPlease skin name: ")
        bodyValue = int(input("\nPlease body type (0 for Steve and 1 for Alex/Slim): "))
        bodyType = convertBodyValue(bodyValue)
        skins.append(skin(name, file, bodyType))
        
    return skins
        
def convertBodyValue(bodyValue):
    if (bodyValue == 1):
        bodyType = "geometry.humanoid.customSlim"
    else:
        bodyType = "geometry.humanoid.custom"
    return bodyType

def copySkins(skinsArr):
    for obj in skinsArr:
        shutil.copy("./Skins/" + obj.file, "./Output/" + obj.file, follow_symlinks=True)

def spaceAndTooLower(name):
    name = name.replace(" ", "").lower
    return name

def generateManifest(packName, uuidA, version, uuidB):
    manifest_file = open("./Output/manifest.json", 'w+')
    temp = "{\n\t\"format_version\": 1,\n\t\"header\": {\n\t\t\"name\": \"" + \
                                                                     packName + "\",\n\t\t\"uuid\": \"" + uuidA + \
                                                                     "\",\n\t\t\"version\": [\n\t\t\t" +  \
                                                                                              str(version[0]) + ",\n\t\t\t" + \
                                                                                              str(version[1]) + ",\n\t\t\t" + \
                                                                                              str(version[2]) + "\n\t\t]" + \
                                                                                             "\n\t},\n\t\"modules\": [\n\t\t{\n\t\t\t\"type\": \"skin_pack\"," \
                                                                                             "\n\t\t\t\"uuid\": \"" + uuidB + "\",\n\t\t\t\"version\": [" \
                                                                                             "\n\t\t\t\t6,\n\t\t\t\t" + \
                                                                                             "0,\n\t\t\t\t" + \
                                                                                              "0\n\t\t\t]\n\t\t}\n\t]\n}"
    manifest_file.write(temp)
    manifest_file.close
    
  
#==============================DRIVER CODE=====================================

#Variables
lang_id = "en_US"
version = [2, 0, 0]
uuidA = ""
creator = ""
packName = ""
description = ""
numberOfSkins = 0


#Print Header
print("\nMinecraft Skin Pack Creator\n    by Geoffery Powell\n")

#Create Directories If Missing
checkForDir(".\Skins")
checkForDir(".\Output")
checkForDir(".\Output/texts")

#Count Skins (This should only look for PNGs)
numberOfSkins = sum([len(files) for r, d, files in os.walk(".\Skins")])

if (numberOfSkins <= 0):
    #No skins!
    print("No skins found in Skins folder...")
else:
    #Display Found Skins
    print("Skins in the \"Skins\" folder will be used.\n")
    print("\tNumber of Skins:", numberOfSkins)
    skinFiles = os.listdir(".\Skins")
    print(skinFiles)

    #Get info
    creator = input("\nPlease your name: ")
    packName = input("Please your pack's name: ")
    print("\nRecommended UUIDD Generator: https://www.uuidgenerator.net/version4")
    uuidA = input("Please your first UUID: ")
    uuidB = input("Please your second UUID: ")
    
    #Get skin info
    skinsArr = createSkins(skinFiles)
    
    #Print Skin Values
    for obj in skinsArr: 
        print( "Name:", obj.name,"- File:", obj.file, "- Body Type:", obj.bodyType, sep =' ' )
        
    #Time to make the files
    #Copy Skins
    copySkins(skinsArr)
    #Write to Files
    generateManifest(packName, uuidA, version, uuidB)
    pack_manifest_file = open("./Output/pack_manifest.json", 'w+')
    pack_manifest_file.close
    skins_file = open("./Output/skins.json", 'w+')
    skins_file.close
    langs_file = open("./Output/texts/" + lang_id, 'w+')
    langs_file.close
    
    
    