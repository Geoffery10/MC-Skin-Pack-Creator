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
from os.path import basename
from zipfile import ZipFile

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
        shutil.copy("./Skins/" + obj.file, "./Temp/" + obj.file, follow_symlinks=True)

def spaceAndTooLower(name):
    name = name.replace(" ", "")
    name = name.lower()
    return name

#THESE 3 METHODS GENERATE THE FILES

def generateManifest(packName, uuidA, version, uuidB):
    manifest_file = open("./Temp/manifest.json", 'w+')
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
    
def generatePackManifest(uuidA, packName, version, description, uuidB):
    pack_manifest_file = open("./Temp/pack_manifest.json", 'w+')
    temp = "{\n\t\"header\": {\n\t\t\"pack_id\": \"" + uuidA + "\",\n\t\t\"name\": \"" + packName + "\",\n\t\t\"packs_version\": \"" + str(version[0]) + \
    "." + str(version[1]) + "." + str(version[2]) + "\",\n\t\t\"description\": \"" + description + "\",\n\t\t\"modules\": [\n\t\t\t{\n\t\t\t  \"description\": \""
    temp = temp + description + "\",\n\t\t\t  \"version\": \"6.0.0\",\n\t\t\t  \"uuid\": \"" + uuidB + "\",\n\t\t\t  \"type\": \"skin_pack\"\n\t\t\t}\n\t\t]\n\t}\n}"
    pack_manifest_file.write(temp)
    pack_manifest_file.close
    
def generateSkins(skinsArr, packName, creatorID):
    skins_file = open("./Temp/skins.json", 'w+')
    temp = "{\n\t\"geometry\": \"skinpacks/skins.json\",\n\t\"skins\": ["
    for obj in skinsArr:
        name = spaceAndTooLower(obj.name)
        bodyType = obj.bodyType
        file = obj.file
        temp = temp + "\n\t\t{\n\t\t\t\"localization_name\": \"" + name + "\",\n\t\t\t\"geometry\": \"" + str(bodyType) + \
        "\",\n\t\t\t\"texture\": \"" + str(file) + "\",\n\t\t\t\"type\": \"free\"\n\t\t},"
    temp = temp[:-1]
    temp = temp + "\n\n\t],\n\t\"serialize_name\": \"" + packName + "\",\n\t\"localization_name\": \"" + creatorID + "\"\n}"
    skins_file.write(temp)
    
    skins_file.close
    
def generateLangs(creatorID, skinsArr, lang_id, packName): 
    langs_file = open("./Temp/texts/" + lang_id + ".lang", 'w+')
    temp = ""
    for obj in skinsArr:
        name = spaceAndTooLower(obj.name)
        temp = temp + "skin." + creatorID + "." + name + "=" + obj.name + "\n"
    temp = temp + "skinpack." + creatorID + "=" + packName
    langs_file.write(temp)
    langs_file.close
    
def makeMCPACK(packName, skinsArr, lang_id):
    # create a ZipFile object
    with ZipFile(packName + ".mcpack", 'w') as zipObj:
        for obj in skinsArr:
            #Save Skins
            filePath = "./Temp/" + obj.file
            zipObj.write(filePath, basename(filePath))
        #Save text files
        zipObj.write("./Temp/manifest.json", basename("./Temp/manifest.json"))
        zipObj.write("./Temp/pack_manifest.json", basename("./Temp/pack_manifest.json"))
        zipObj.write("./Temp/skins.json", basename("./Temp/skins.json"))
        zipObj.write("./Temp/texts", basename("./Temp/texts"))
        zipObj.write("./Temp/texts/" + lang_id + ".lang", "texts/" + lang_id + ".lang")
    zipObj.close()

    
    
  
#==============================DRIVER CODE=====================================

#Variables
lang_id = "en_US" #This should be set by the user in final version
version = [2, 0, 0] #I believe this is the pack version
uuidA = ""
uuidB = ""
creator = ""
creatorID = ""
packName = ""
description = ""
numberOfSkins = 0 #The number of skins in the skins folder


#Print Header
print("\nMinecraft Skin Pack Creator\n    by Geoffery Powell\n")

#Create Directories If Missing
checkForDir(".\Skins")
checkForDir(".\Temp")
checkForDir(".\Temp/texts")

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
    description = input("Please your pack's description: ")
    print("\nRecommended UUIDD Generator: https://www.uuidgenerator.net/version4")
    uuidA = input("Please your first UUID: ")
    uuidB = input("Please your second UUID: ")
    
    #Get skin info
    skinsArr = createSkins(skinFiles)
    
    #Print Skin Values
    print("\n\tSkin Data")
    for obj in skinsArr: 
        print( "Name:", obj.name,"- File:", obj.file, "- Body Type:", obj.bodyType, sep =' ' )
        
    creatorID = (creator + uuidA[len(uuidA)-4:])
    #Time to make the files
    #Copy Skins
    copySkins(skinsArr)
    print("\n\nCopied skins to pack.")
    #Write to Files
    generateManifest(packName, uuidA, version, uuidB)
    print("Created manifest.json.")
    generatePackManifest(uuidA, packName, version, description, uuidB)
    print("Created pack_manifest.json.")
    generateSkins(skinsArr, packName, creatorID)
    print("Created skins.json.")
    generateLangs(creatorID, skinsArr, lang_id, packName)
    print("Created " + lang_id + ".lang")
    #Pack Zip
    #CODE HERE
    makeMCPACK(packName, skinsArr, lang_id)
    print("Packed into .mcpack file")
    shutil.rmtree("./Temp")
    print("\n\tDONE!")
    
    