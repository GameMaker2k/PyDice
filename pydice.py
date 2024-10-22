#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

'''
    This program is free software; you can redistribute it and/or modify
    it under the terms of the Revised BSD License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    Revised BSD License for more details.

    Copyright 2016-2021 Game Maker 2k - https://github.com/GameMaker2k
    Copyright 2016-2021 Joshua Przyborowski - https://github.com/JoshuaPrzyborowski

    $FileInfo: pydice.py - Last Update: 1/4/2021 Ver. 0.3.2 RC 1 - Author: joshuatp $
'''

from __future__ import absolute_import, division, print_function, unicode_literals, generators, with_statement, nested_scopes
from collections import OrderedDict
import re
import random
try:
    import xml.etree.cElementTree as cElementTree
except ImportError:
    import xml.etree.ElementTree as cElementTree

__program_name__ = "PyDice-Roll"
__project__ = __program_name__
__project_url__ = "https://github.com/JoshuaPrzyborowski/PyDice"
__version_info__ = (0, 3, 2, "RC 1", 1)
__version_date_info__ = (2024, 10, 22, "RC 1", 1)
__version_date__ = str(__version_date_info__[0])+"."+str(__version_date_info__[
    1]).zfill(2)+"."+str(__version_date_info__[2]).zfill(2)
if(__version_info__[4] != None):
    __version_date_plusrc__ = __version_date__ + \
        "-"+str(__version_date_info__[4])
if(__version_info__[4] == None):
    __version_date_plusrc__ = __version_date__
if(__version_info__[3] != None):
    __version__ = str(__version_info__[0])+"."+str(__version_info__[1])+"."+str(
        __version_info__[2])+" "+str(__version_info__[3])
if(__version_info__[3] == None):
    __version__ = str(
        __version_info__[0])+"."+str(__version_info__[1])+"."+str(__version_info__[2])


def GetItemFromList(listvar, listval, defval):
    retval = None
    try:
        retval = listvar.get(listval, defval)
    except AttributeError:
        try:
            retval = listvar[listval]
        except IndexError:
            retval = defval
    return retval


def GetMinValues(DiceList, DiceNum=5):
    if type(DiceList) is not list:
        return False
    if type(DiceNum) is not int:
        DiceNum = 5
    MinValList = []
    UsedVals = []
    MinValDict = OrderedDict()
    ilist = 1
    ixlist = DiceNum
    while(ilist <= ixlist):
        subilist = 0
        subixlist = len(DiceList)
        curminval = float('inf')
        curvalpos = 0
        while(subilist < subixlist):
            if(DiceList[subilist] < curminval and subilist not in UsedVals):
                curminval = DiceList[subilist]
                curvalpos = subilist + 1
            subilist = subilist + 1
        UsedVals.append(curvalpos - 1)
        MinValDict.update({curvalpos: curminval})
        ilist = ilist + 1
    MinValDict = OrderedDict(sorted(MinValDict.items()))
    for key, value in MinValDict.items():
        MinValList.append(value)
    return MinValList


def GetMaxValues(DiceList, DiceNum=5):
    if type(DiceList) is not list:
        return False
    if type(DiceNum) is not int:
        DiceNum = 5
    MaxValList = []
    UsedVals = []
    MaxValDict = OrderedDict()
    ilist = 1
    ixlist = DiceNum
    while(ilist <= ixlist):
        subilist = 0
        subixlist = len(DiceList)
        curmaxval = 0
        curvalpos = 0
        while(subilist < subixlist):
            if(DiceList[subilist] > curmaxval and subilist not in UsedVals):
                curmaxval = DiceList[subilist]
                curvalpos = subilist + 1
            subilist = subilist + 1
        UsedVals.append(curvalpos - 1)
        MaxValDict.update({curvalpos: curmaxval})
        ilist = ilist + 1
    MaxValDict = OrderedDict(sorted(MaxValDict.items()))
    for key, value in MaxValDict.items():
        MaxValList.append(value)
    return MaxValList


def GetDictValueFromDiceNumber(DiceValue, DiceArray={}):
    DiceRolls = []
    DiceRollValue = GetItemFromList(DiceArray, DiceValue, DiceValue)
    DiceRolls.append(DiceRollValue)
    return DiceRolls


def GetDictValueFromDiceList(DiceList, DiceArrayList={}):
    DiceRolls = []
    NumOfDice = len(DiceList)
    CountNumOfDice = 0
    while(CountNumOfDice < NumOfDice):
        DiceRolls.append(GetDictValueFromDiceNumber(
            DiceList[CountNumOfDice], DiceArrayList)[0])
        CountNumOfDice = CountNumOfDice + 1
    return DiceRolls


def GetDictValueFromDiceListAlt(DiceList, DiceArrayList=[{}]):
    DiceRolls = []
    NumOfDice = len(DiceList)
    CountNumOfDice = 0
    while(CountNumOfDice < NumOfDice):
        DiceRolls.append(GetDictValueFromDiceNumber(
            DiceList[CountNumOfDice], DiceArrayList[CountNumOfDice])[0])
        CountNumOfDice = CountNumOfDice + 1
    return DiceRolls


def RandomDiceRoll(MinNum=1, MaxNum=6, RandType=1, RandSeed=random.seed(), DiceArray=None):
    if(len(re.findall("^([\-]?[0-9]+)$", str(MinNum))) < 1):
        MinNum = 1
    try:
        MinNum = int(MinNum)
    except ValueError:
        return [False]
    if(len(re.findall("^([\-]?[0-9]+)$", str(MaxNum))) < 1):
        MaxNum = 6
    try:
        MaxNum = int(MaxNum)
    except ValueError:
        return [False]
    if(len(re.findall("^([\-]?[1-5]+)$", str(RandType))) < 1):
        RandType = 1
    try:
        RandType = int(RandType)
    except ValueError:
        RandType = 1
    if(MinNum > MaxNum):
        TmpMinNum = MaxNum
        TmpMaxNum = MinNum
        MaxNum = TmpMaxNum
        MinNum = TmpMinNum
    RandType = int(RandType)
    if(RandType < 1):
        RandType = 1
    if(RandType > 5):
        RandType = 5
    if(RandType == 1):
        DiceRollValue = random.randint(MinNum, MaxNum)
    if(RandType == 2):
        randtype = random.WichmannHill(RandSeed)
        DiceRollValue = randtype.randint(MinNum, MaxNum)
    if(RandType == 3):
        randtype = random.SystemRandom(RandSeed)
        DiceRollValue = randtype.randint(MinNum, MaxNum)
    if(RandType == 4):
        DiceRollValue = random.randrange(MinNum, MaxNum + 1)
    if(RandType == 5):
        icount = 1
        ilist = []
        while(icount <= MaxNum):
            ilist.append(icount)
            icount += 1
        DiceRollValue = random.choice(ilist)
    if(DiceArray is not None and type(DiceArray) is dict):
        DiceRollValue = GetDictValueFromDiceNumber(DiceRollValue, DiceArray)[0]
    return [DiceRollValue]


def RandomDieRoll(MinNum=1, MaxNum=6, RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomDiceRoll(MinNum, MaxNum, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomDiceRollAlt(MaxNum=6, RandType=1, RandSeed=random.seed(), DiceArray=None):
    if(MaxNum > 0):
        DiceRollValue = RandomDiceRoll(
            1, MaxNum, RandType, RandSeed, DiceArray)[0]
    if(MaxNum < 0):
        DiceRollValue = RandomDiceRoll(
            MaxNum, -1, RandType, RandSeed, DiceArray)[0]
    if(MaxNum == 0):
        DiceRollValue = RandomDiceRoll(
            MaxNum, 1, RandType, RandSeed, DiceArray)[0]
    return [DiceRollValue]


def RandomDieRollAlt(MaxNum=6, RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomDiceRollAlt(MaxNum, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDiceRoll(MinNum=[1], MaxNum=[6], RandType=1, RandSeed=random.seed(), DiceArray=None):
    if not isinstance(MinNum, list):
        MinNum = [MinNum]
    if not isinstance(MaxNum, list):
        MaxNum = [MaxNum]
    CountMinNum = len(MinNum)
    CountMaxNum = len(MaxNum)
    if(CountMinNum >= CountMaxNum):
        NumOfDice = CountMinNum
    if(CountMinNum < CountMaxNum):
        NumOfDice = CountMaxNum
    CountNumOfDice = 0
    DiceRolls = []
    while(CountNumOfDice < NumOfDice):
        DiceRolls.append(RandomDiceRoll(
            MinNum[CountNumOfDice], MaxNum[CountNumOfDice], RandType, RandSeed, DiceArray)[0])
        CountNumOfDice = CountNumOfDice + 1
    return DiceRolls


def RandomMultiDieRoll(MinNum=[1], MaxNum=[6], RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiDiceRoll(
        MinNum, MaxNum, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDiceRollByXML(DiceStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    dieminv = []
    diemaxv = []
    tree = cElementTree.ElementTree(file=DiceStrFile)
    root = tree.getroot()
    for child in root:
        if(child.tag == "dice"):
            diemin = ""
            if('min' in child.attrib):
                diemin = str(child.attrib['min'])
            else:
                diemin = "1"
            if(len(re.findall("^([\-]?[0-9]+)$", diemin)) < 1):
                diemin = "1"
            diemax = ""
            if('max' in child.attrib):
                diemax = str(child.attrib['max'])
            else:
                diemax = "6"
            if(len(re.findall("^([\-]?[0-9]+)$", diemax)) < 1):
                diemax = "6"
            dieminv.append(diemin)
            diemaxv.append(diemax)
    DiceRolls = RandomMultiDiceRoll(
        dieminv, diemaxv, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDieRollByXML(DieStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiDiceRollByXML(
        DieStrFile, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDiceRollAlt(MaxNum=[6], RandType=1, RandSeed=random.seed(), DiceArray=None):
    if not isinstance(MaxNum, list):
        MaxNum = [MaxNum]
    NumOfDice = len(MaxNum)
    CountNumOfDice = 0
    DiceRollsMin = []
    DiceRollsMax = []
    while(CountNumOfDice < NumOfDice):
        if(MaxNum[CountNumOfDice] > 0):
            DiceRollsMin.append(1)
            DiceRollsMax.append(MaxNum[CountNumOfDice])
        if(MaxNum[CountNumOfDice] < 0):
            DiceRollsMin.append(MaxNum[CountNumOfDice])
            DiceRollsMax.append(-1)
        if(MaxNum[CountNumOfDice] == 0):
            DiceRollsMin.append(MaxNum[CountNumOfDice])
            DiceRollsMax.append(1)
        CountNumOfDice = CountNumOfDice + 1
    DiceRolls = RandomMultiDiceRoll(
        DiceRollsMin, DiceRollsMax, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDieRollAlt(MaxNum=[6], RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiDiceRollAlt(MaxNum, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDiceRollAltByXML(DiceStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    diemaxv = []
    tree = cElementTree.ElementTree(file=DiceStrFile)
    root = tree.getroot()
    for child in root:
        if(child.tag == "dice"):
            diemax = ""
            if('max' in child.attrib):
                diemax = str(child.attrib['max'])
            else:
                diemax = "6"
            if(len(re.findall("^([\-]?[0-9]+)$", diemax)) < 1):
                diemax = "6"
            diemaxv.append(diemax)
    DiceRolls = RandomMultiDiceRollAlt(diemaxv, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDieRollAltByXML(DieStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiDiceRollAltByXML(
        DieStrFile, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiSameDiceRoll(NumOfDice=1, MinNum=1, MaxNum=6, RandType=1, RandSeed=random.seed(), DiceArray=None):
    CountNumOfDice = 0
    DiceRollsMin = []
    DiceRollsMax = []
    while(CountNumOfDice < NumOfDice):
        DiceRollsMin.append(MinNum)
        DiceRollsMax.append(MaxNum)
        CountNumOfDice = CountNumOfDice + 1
    DiceRolls = RandomMultiDiceRoll(
        DiceRollsMin, DiceRollsMax, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiSameDieRoll(NumOfDie=1, MinNum=1, MaxNum=6, RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiSameDiceRoll(
        NumOfDie, MinNum, MaxNum, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiSameDiceRollAlt(NumOfDice=1, MaxNum=6, RandType=1, RandSeed=random.seed(), DiceArray=None):
    CountNumOfDice = 0
    DiceRollsMin = []
    DiceRollsMax = []
    while(CountNumOfDice < NumOfDice):
        if(MaxNum > 0):
            DiceRollsMin.append(1)
            DiceRollsMax.append(MaxNum)
        if(MaxNum < 0):
            DiceRollsMin.append(MaxNum)
            DiceRollsMax.append(-1)
        if(MaxNum == 0):
            DiceRollsMin.append(MaxNum)
            DiceRollsMax.append(1)
        CountNumOfDice = CountNumOfDice + 1
    DiceRolls = RandomMultiDiceRoll(
        DiceRollsMin, DiceRollsMax, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiSameDieRollAlt(NumOfDie=1, MaxNum=6, RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiSameDiceRollAlt(
        NumOfDie, MaxNum, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomDiceRollByPosition(DiceStr="0,0,0,0,0,1", RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceStr = DiceStr.strip()
    DiceStrList = DiceStr.split(",")
    NumOfDice = len(DiceStrList)
    CountNumOfDice = 0
    DiceRolls = []
    while(CountNumOfDice < NumOfDice):
        CurDiceNum = CountNumOfDice + 1
        if(int(DiceStrList[CountNumOfDice]) > 0):
            DiceRollsTmp = RandomMultiSameDiceRollAlt(
                int(DiceStrList[CountNumOfDice]), CurDiceNum, RandType, RandSeed, DiceArray)
            DiceRolls = DiceRolls + DiceRollsTmp
        CountNumOfDice = CountNumOfDice + 1
    return DiceRolls


def RandomDieRollByPosition(DieStr="0,0,0,0,0,1", RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomDiceRollByPosition(DieStr, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomDiceRollByString(DiceStr="d6", RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceStr = DiceStr.strip()
    DiceStr = DiceStr.lower()
    DiceStr = re.sub("c", "d2", DiceStr)
    DiceStrList = DiceStr.split(",")
    NumOfDice = len(DiceStrList)
    CountNumOfDice = 0
    DiceRolls = []
    while(CountNumOfDice < NumOfDice):
        GetDiceRoll = int(re.findall(
            "d([0-9]+)", DiceStrList[CountNumOfDice])[0])
        DiceRolls = DiceRolls + \
            RandomDiceRollAlt(GetDiceRoll, RandType, RandSeed, DiceArray)
        CountNumOfDice = CountNumOfDice + 1
    return DiceRolls


def RandomDieRollByString(DieStr="d6", RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomDiceRollByString(DieStr, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomDiceRollByXML(DiceStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    diestr = ""
    tree = cElementTree.ElementTree(file=DiceStrFile)
    root = tree.getroot()
    for child in root:
        if(child.tag == "dice"):
            if(diestr != ""):
                diestr = diestr+","
            diemax = ""
            if('max' in child.attrib):
                diemax = str(child.attrib['max'])
            else:
                diemax = "6"
            if(len(re.findall("^([\-]?[0-9]+)$", diemax)) < 1):
                diemax = "6"
            diestr = "d"+diemax
    DiceRolls = RandomDiceRollByString(diestr, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomDieRollByXML(DieStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomDiceRollByXML(DieStrFile, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDiceRollByString(DiceStr="1d6", RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceStr = DiceStr.strip()
    DiceStr = DiceStr.lower()
    DiceStr = re.sub("([0-9]*)c", "\\1d2", DiceStr)
    DiceStrList = DiceStr.split(",")
    NumOfDice = len(DiceStrList)
    CountNumOfDice = 0
    DiceRolls = []
    while(CountNumOfDice < NumOfDice):
        GetPreDiceRoll = re.findall(
            "([0-9]*)d([0-9]+)([l|h]?[0-9]*)", DiceStrList[CountNumOfDice])[0]
        if(GetPreDiceRoll[1] == ""):
            GetDiceRoll = 1
        else:
            GetDiceRoll = int(GetPreDiceRoll[1])
        GetNumDice = int(GetPreDiceRoll[0])
        GetDiceAVGList = ""
        if(not GetPreDiceRoll[2] == ""):
            if(len(re.findall("^([l|h]{1})([0-9]+)$",  GetPreDiceRoll[2])) > 0):
                GetDiceAVGList = re.findall(
                    "^([l|h]{1})([0-9]+)$", GetPreDiceRoll[2])[0]
            else:
                GetPreDiceRoll[2] = ""
        GetPreDiceRollList = []
        if(GetNumDice > 0):
            GetPreDiceRollList = GetPreDiceRollList + \
                RandomMultiSameDiceRollAlt(
                    GetNumDice, GetDiceRoll, RandType, RandSeed, DiceArray)
        if(GetPreDiceRoll[2] == ""):
            GetDiceRollList = GetPreDiceRollList
        else:
            if(int(GetDiceAVGList[1]) > int(GetPreDiceRoll[0])):
                GetDiceAVGList[1] = GetPreDiceRoll[0]
            if(GetDiceAVGList[0] == "l"):
                GetDiceRollList = GetMinValues(
                    GetPreDiceRollList, int(GetDiceAVGList[1]))
            if(GetDiceAVGList[0] == "h"):
                GetDiceRollList = GetMaxValues(
                    GetPreDiceRollList, int(GetDiceAVGList[1]))
        DiceRolls = DiceRolls + GetDiceRollList
        CountNumOfDice = CountNumOfDice + 1
    return DiceRolls


def RandomMultiDieRollByString(DieStr="1d6", RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiDiceRollByString(
        DieStr, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDiceRollByXML(DiceStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    diestr = ""
    tree = cElementTree.ElementTree(file=DiceStrFile)
    root = tree.getroot()
    for child in root:
        if(child.tag == "dice"):
            if(diestr != ""):
                diestr = diestr+","
            diemax = ""
            if('max' in child.attrib):
                diemax = str(child.attrib['max'])
            else:
                diemax = "6"
            if(len(re.findall("^([\-]?[0-9]+)$", diemax)) < 1):
                diemax = "6"
            dienum = ""
            if('num' in child.attrib):
                dienum = str(child.attrib['num'])
            else:
                dienum = "1"
            if(len(re.findall("^([0-9]+)$", dienum)) < 1):
                dienum = "1"
            diestr = diestr+dienum+"d"+diemax
        if(child.tag == "coin"):
            if(diestr != ""):
                diestr = diestr+","
            dienum = ""
            if('num' in child.attrib):
                dienum = str(child.attrib['num'])
            else:
                dienum = "1"
            if(len(re.findall("^([0-9]+)$", dienum)) < 1):
                dienum = "1"
            diestr = diestr+dienum+"c"
    DiceRolls = RandomMultiDiceRollByString(
        diestr, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDieRollByXML(DieStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiDiceRollByXML(
        DieStrFile, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDiceRollByStringAlt(DiceStr="d6:1", RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceStr = DiceStr.strip()
    DiceStr = DiceStr.lower()
    DiceStr = re.sub("c([\:]?[0-9])", "d2\\1", DiceStr)
    DiceStrList = DiceStr.split(",")
    NumOfDice = len(DiceStrList)
    CountNumOfDice = 0
    DiceRolls = []
    while(CountNumOfDice < NumOfDice):
        GetPreDiceRoll = re.findall(
            "d([0-9]+)([\:]?[0-9]*)([l|h]?[0-9]*)", DiceStrList[CountNumOfDice])[0]
        GetDiceRoll = int(GetPreDiceRoll[0])
        GetPreNumDice = GetPreDiceRoll[1].replace(":", "")
        if(GetPreNumDice == ""):
            GetNumDice = 1
        else:
            GetNumDice = int(GetPreNumDice)
        GetDiceAVGList = ""
        if(not GetPreDiceRoll[2] == ""):
            if(len(re.findall("^([l|h]{1})([0-9]+)$",  GetPreDiceRoll[2])) > 0):
                GetDiceAVGList = re.findall(
                    "^([l|h]{1})([0-9]+)$", GetPreDiceRoll[2])[0]
            else:
                GetPreDiceRoll[2] = ""
        GetPreDiceRollList = []
        if(GetNumDice > 0):
            GetPreDiceRollList = GetPreDiceRollList + \
                RandomMultiSameDiceRollAlt(
                    GetNumDice, GetDiceRoll, RandType, RandSeed, None)
        if(GetPreDiceRoll[2] == ""):
            GetDiceRollList = GetPreDiceRollList
        else:
            if(int(GetDiceAVGList[1]) > int(GetPreDiceRoll[0])):
                GetDiceAVGList[1] = GetPreDiceRoll[0]
            if(GetDiceAVGList[0] == "l"):
                GetDiceRollList = GetMinValues(
                    GetPreDiceRollList, int(GetDiceAVGList[1]))
            if(GetDiceAVGList[0] == "h"):
                GetDiceRollList = GetMaxValues(
                    GetPreDiceRollList, int(GetDiceAVGList[1]))
        if(DiceArray is not None and type(DiceArray) is dict):
            GetDiceRollList = GetDictValueFromDiceList(
                GetDiceRollList, DiceArray)
        if(DiceArray is not None and (type(DiceArray) is list or type(DiceArray) is tuple)):
            if(DiceArray[0] is not None and type(DiceArray[0]) is dict):
                GetDiceRollList = GetDictValueFromDiceListAlt(
                    GetDiceRollList, DiceArray)
        DiceRolls = DiceRolls + GetDiceRollList
        CountNumOfDice = CountNumOfDice + 1
    return DiceRolls


def RandomMultiDieRollByStringAlt(DieStr="d6:1", RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiDiceRollByStringAlt(
        DieStr, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDiceRollByXMLAlt(DiceStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    diestr = ""
    tree = cElementTree.ElementTree(file=DiceStrFile)
    root = tree.getroot()
    for child in root:
        if(child.tag == "dice"):
            if(diestr != ""):
                diestr = diestr+","
            diemax = ""
            if('max' in child.attrib):
                diemax = str(child.attrib['max'])
            else:
                diemax = "6"
            if(len(re.findall("^([\-]?[0-9]+)$", diemax)) < 1):
                diemax = "6"
            dienum = ""
            if('num' in child.attrib):
                dienum = str(child.attrib['num'])
            else:
                dienum = "1"
            if(len(re.findall("^([0-9]+)$", dienum)) < 1):
                dienum = "1"
            diestr = diestr+"d"+diemax+":"+dienum
    DiceRolls = RandomMultiDiceRollByStringAlt(
        diestr, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDieRollByXMLAlt(DieStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiDiceRollByXMLAlt(
        DieStrFile, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDiceRollMinMaxByString(DiceStr="1d1:6", RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceStr = DiceStr.strip()
    DiceStr = DiceStr.lower()
    DiceStr = re.sub("([0-9]*)c", "\\1d1:2", DiceStr)
    DiceStr = re.sub("([0-9]*)u([0-9]+)([l|h]?[0-9]*)",
                     "\\1d-\\2:\\2\\3", DiceStr)
    DiceStrList = DiceStr.split(",")
    NumOfDice = len(DiceStrList)
    CountNumOfDice = 0
    DiceRolls = []
    while(CountNumOfDice < NumOfDice):
        GetPreDiceRoll = re.findall(
            "([0-9]*)d([\-]?[0-9]+)([\:]?[\-]?[0-9]*)([l|h]?[0-9]*)", DiceStrList[CountNumOfDice])[0]
        if(GetPreDiceRoll[1] == ""):
            GetMinDiceRoll = 1
        else:
            GetMinDiceRoll = int(GetPreDiceRoll[1])
        GetPreMaxDiceRoll = GetPreDiceRoll[2].replace(":", "")
        if(GetPreMaxDiceRoll == ""):
            GetMaxDiceRoll = ""
        else:
            GetMaxDiceRoll = int(GetPreMaxDiceRoll)
        GetNumDice = int(GetPreDiceRoll[0])
        GetDiceAVGList = ""
        if(not GetPreDiceRoll[3] == ""):
            if(len(re.findall("^([l|h]{1})([0-9]+)$",  GetPreDiceRoll[3])) > 0):
                GetDiceAVGList = re.findall(
                    "^([l|h]{1})([0-9]+)$", GetPreDiceRoll[3])[0]
            else:
                GetPreDiceRoll[3] = ""
        GetPreDiceRollList = []
        if(GetNumDice > 0):
            if(GetMaxDiceRoll == ""):
                GetPreDiceRollList = GetPreDiceRollList + \
                    RandomMultiSameDiceRollAlt(
                        GetNumDice, GetMinDiceRoll, RandType, RandSeed, None)
            else:
                GetPreDiceRollList = GetPreDiceRollList + RandomMultiSameDiceRoll(
                    GetNumDice, GetMinDiceRoll, GetMaxDiceRoll, RandType, RandSeed, None)
        if(GetPreDiceRoll[3] == ""):
            GetDiceRollList = GetPreDiceRollList
        else:
            if(int(GetDiceAVGList[1]) > int(GetPreDiceRoll[0])):
                GetDiceAVGList[1] = GetPreDiceRoll[0]
            if(GetDiceAVGList[0] == "l"):
                GetDiceRollList = GetMinValues(
                    GetPreDiceRollList, int(GetDiceAVGList[1]))
            if(GetDiceAVGList[0] == "h"):
                GetDiceRollList = GetMaxValues(
                    GetPreDiceRollList, int(GetDiceAVGList[1]))
        if(DiceArray is not None and type(DiceArray) is dict):
            GetDiceRollList = GetDictValueFromDiceList(
                GetDiceRollList, DiceArray)
        if(DiceArray is not None and (type(DiceArray) is list or type(DiceArray) is tuple)):
            if(DiceArray[0] is not None and type(DiceArray[0]) is dict):
                GetDiceRollList = GetDictValueFromDiceListAlt(
                    GetDiceRollList, DiceArray)
        DiceRolls = DiceRolls + GetDiceRollList
        CountNumOfDice = CountNumOfDice + 1
    return DiceRolls


def RandomMultiDieRollMinMaxByString(DieStr="1d1:6", RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiDiceRollMinMaxByString(
        DieStr, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDiceRollMinMaxByXML(DiceStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    diestr = ""
    tree = cElementTree.ElementTree(file=DiceStrFile)
    root = tree.getroot()
    for child in root:
        if(child.tag == "dice"):
            if(diestr != ""):
                diestr = diestr+","
            diemin = ""
            if('min' in child.attrib):
                diemin = str(child.attrib['min'])
            else:
                diemin = "1"
            if(len(re.findall("^([\-]?[0-9]+)$", diemin)) < 1):
                diemin = "1"
            diemax = ""
            if('max' in child.attrib):
                diemax = str(child.attrib['max'])
            else:
                diemax = "6"
            if(len(re.findall("^([\-]?[0-9]+)$", diemax)) < 1):
                diemax = "6"
            dienum = ""
            if('num' in child.attrib):
                dienum = str(child.attrib['num'])
            else:
                dienum = "1"
            if(len(re.findall("^([0-9]+)$", dienum)) < 1):
                dienum = "1"
            diestr = diestr+dienum+"d"+diemin+":"+diemax
        if(child.tag == "fudge"):
            if(diestr != ""):
                diestr = diestr+","
            diemin = ""
            diemax = ""
            if('max' in child.attrib):
                diemax = str(child.attrib['max'])
                diemin = "-"+str(child.attrib['max'])
            else:
                diemax = "1"
                diemin = "-1"
            if(len(re.findall("^([\-]?[0-9]+)$", diemax)) < 1):
                diemax = "1"
            if(len(re.findall("^([\-]?[0-9]+)$", diemin)) < 1):
                diemin = "-1"
            dienum = ""
            if('num' in child.attrib):
                dienum = str(child.attrib['num'])
            else:
                dienum = "1"
            if(len(re.findall("^([0-9]+)$", dienum)) < 1):
                dienum = "1"
            diestr = diestr+dienum+"u"+diemin+":"+diemax
        if(child.tag == "coin"):
            if(diestr != ""):
                diestr = diestr+","
            dienum = ""
            if('num' in child.attrib):
                dienum = str(child.attrib['num'])
            else:
                dienum = "1"
            if(len(re.findall("^([0-9]+)$", dienum)) < 1):
                dienum = "1"
            diestr = diestr+dienum+"c"
    DiceRolls = RandomMultiDiceRollNotationMinMaxByString(
        diestr, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDieRollMinMaxByXML(DieStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiDiceRollMinMaxByXML(
        DieStrFile, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDiceRollNotationByString(DiceStr="1d6", RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceStr = DiceStr.strip()
    DiceStr = DiceStr.lower()
    DiceStr = re.sub("([0-9]*)c([\+\-\*\/]?[0-9\+\-\*\/]*)",
                     "\\1d2\\2", DiceStr)
    DiceStr = DiceStr.replace("x", "*")
    DiceStr = DiceStr.replace("×", "*")
    DiceStr = DiceStr.replace("÷", "/")
    DiceStrList = DiceStr.split(",")
    NumOfDice = len(DiceStrList)
    CountNumOfDice = 0
    DiceRolls = []
    while(CountNumOfDice < NumOfDice):
        GetPreDiceRoll = re.findall(
            "([0-9]*)d([\-]?[0-9]+)([l|h]?[0-9]*)([\+\-\*\/]?[0-9\+\-\*\/]*)([l|h]?[0-9]*)", DiceStrList[CountNumOfDice])[0]
        if(GetPreDiceRoll[0] == ""):
            GetNumDice = 1
        else:
            GetNumDice = int(GetPreDiceRoll[0])
        GetNewDiceRoll = int(GetPreDiceRoll[1])
        DiceRollSum = str(GetPreDiceRoll[3])
        GetDiceAVGList = ""
        if(not GetPreDiceRoll[2] == ""):
            if(len(re.findall("^([l|h]{1})([0-9]+)$",  GetPreDiceRoll[2])) > 0):
                GetDiceAVGList = re.findall(
                    "^([l|h]{1})([0-9]+)$", GetPreDiceRoll[2])[0]
            else:
                GetPreDiceRoll[2] = ""
        GetPreDiceRollList = []
        GetSubDiceRollList = []
        if(GetNumDice > 0):
            GetPreDiceRollList = GetPreDiceRollList + \
                RandomMultiSameDiceRollAlt(
                    GetNumDice, GetNewDiceRoll, RandType, RandSeed, None)
        if(GetPreDiceRoll[2] == ""):
            GetSubDiceRollList = GetPreDiceRollList
        else:
            if(int(GetDiceAVGList[1]) > int(GetPreDiceRoll[0])):
                GetDiceAVGList[1] = GetPreDiceRoll[0]
            if(GetDiceAVGList[0] == "l"):
                GetSubDiceRollList = GetMinValues(
                    GetPreDiceRollList, int(GetDiceAVGList[1]))
            if(GetDiceAVGList[0] == "h"):
                GetSubDiceRollList = GetMaxValues(
                    GetPreDiceRollList, int(GetDiceAVGList[1]))
        SubNumOfDice = len(GetSubDiceRollList)
        GetDiceRollList = []
        SubCountNumOfDice = 0
        while(SubCountNumOfDice < SubNumOfDice):
            NeoPreDiceRoll = str(GetSubDiceRollList[SubCountNumOfDice])
            GetDiceRollList.append(int(eval(NeoPreDiceRoll+DiceRollSum)))
            SubCountNumOfDice = SubCountNumOfDice + 1
        GetLastDiceRollList = []
        GetPostDiceAVGList = ""
        if(not GetPreDiceRoll[4] == ""):
            if(len(re.findall("^([l|h]{1})([0-9]+)$",  GetPreDiceRoll[4])) > 0):
                GetPostDiceAVGList = re.findall(
                    "^([l|h]{1})([0-9]+)$", GetPreDiceRoll[4])[0]
            else:
                GetPreDiceRoll[4] = ""
        if(GetPreDiceRoll[4] == ""):
            GetLastDiceRollList = GetDiceRollList
        else:
            if(int(GetPostDiceAVGList[1]) > int(GetPreDiceRoll[0])):
                GetPostDiceAVGList[1] = GetPreDiceRoll[0]
            if(GetPostDiceAVGList[0] == "l"):
                GetLastDiceRollList = GetMinValues(
                    GetDiceRollList, int(GetPostDiceAVGList[1]))
            if(GetPostDiceAVGList[0] == "h"):
                GetLastDiceRollList = GetMaxValues(
                    GetDiceRollList, int(GetPostDiceAVGList[1]))
        if(DiceArray is not None and type(DiceArray) is dict):
            GetLastDiceRollList = GetDictValueFromDiceList(
                GetLastDiceRollList, DiceArray)
        if(DiceArray is not None and (type(DiceArray) is list or type(DiceArray) is tuple)):
            if(DiceArray[0] is not None and type(DiceArray[0]) is dict):
                GetLastDiceRollList = GetDictValueFromDiceListAlt(
                    GetLastDiceRollList, DiceArray)
        DiceRolls = DiceRolls + GetLastDiceRollList
        CountNumOfDice = CountNumOfDice + 1
    return DiceRolls


def RandomMultiDieRollNotationByString(DieStr="1d6", RandType=1, RandSeed=random.seed()):
    DiceRolls = RandomMultiDiceRollNotationByString(DieStr, RandType, RandSeed)
    return DiceRolls


def RandomMultiDiceRollNotationByXML(DiceStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    diestr = ""
    tree = cElementTree.ElementTree(file=DiceStrFile)
    root = tree.getroot()
    for child in root:
        if(child.tag == "dice"):
            if(diestr != ""):
                diestr = diestr+","
            diemax = ""
            if('max' in child.attrib):
                diemax = str(child.attrib['max'])
            else:
                diemax = "6"
            if(len(re.findall("^([\-]?[0-9]+)$", diemax)) < 1):
                diemax = "6"
            dienum = ""
            if('num' in child.attrib):
                dienum = str(child.attrib['num'])
            else:
                dienum = "1"
            if(len(re.findall("^([0-9]+)$", dienum)) < 1):
                dienum = "1"
            dieexp = ""
            if('exp' in child.attrib):
                dieexp = str(child.attrib['exp'])
            else:
                dieexp = ""
            if(len(re.findall("^([\+\-\*\/]?[0-9\+\-\*\/]*)$", dieexp)) < 1):
                dieexp = ""
            diestr = diestr+dienum+"d"+diemax+dieexp
    DiceRolls = RandomMultiDiceRollNotationMinMaxByString(
        diestr, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDieRollNotationByXML(DieStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiDiceRollNotationByXML(
        DieStrFile, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDiceRollNotationMinMaxByString(DiceStr="1d1:6", RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceStr = DiceStr.strip()
    DiceStr = DiceStr.lower()
    DiceStr = re.sub("([0-9]*)c([\+\-\*\/]?[0-9\+\-\*\/]*)",
                     "\\1d1:2\\2", DiceStr)
    DiceStr = re.sub("([0-9]*)u([0-9]+)([l|h]?[0-9]*)([\+\-\*\/]?[0-9\+\-\*\/]*)([l|h]?[0-9]*)",
                     "\\1d-\\2:\\2\\3\\4\\5", DiceStr)
    DiceStr = DiceStr.replace("x", "*")
    DiceStr = DiceStr.replace("×", "*")
    DiceStr = DiceStr.replace("÷", "/")
    DiceStrList = DiceStr.split(",")
    NumOfDice = len(DiceStrList)
    CountNumOfDice = 0
    DiceRolls = []
    while(CountNumOfDice < NumOfDice):
        GetPreDiceRoll = re.findall(
            "([0-9]*)d([\-]?[0-9]+)([\:]?[\-]?[0-9]*)([l|h]?[0-9]*)([\+\-\*\/]?[0-9\+\-\*\/]*)([l|h]?[0-9]*)", DiceStrList[CountNumOfDice])[0]
        if(GetPreDiceRoll[0] == ""):
            GetNumDice = 1
        else:
            GetNumDice = int(GetPreDiceRoll[0])
        GetMinDiceRoll = int(GetPreDiceRoll[1])
        GetPreMaxDiceRoll = GetPreDiceRoll[2].replace(":", "")
        if(GetPreMaxDiceRoll == ""):
            GetMaxDiceRoll = ""
        else:
            GetMaxDiceRoll = int(GetPreMaxDiceRoll)
        DiceRollSum = str(GetPreDiceRoll[4])
        GetDiceAVGList = ""
        if(not GetPreDiceRoll[3] == ""):
            if(len(re.findall("^([l|h]{1})([0-9]+)$",  GetPreDiceRoll[3])) > 0):
                GetDiceAVGList = re.findall(
                    "^([l|h]{1})([0-9]+)$", GetPreDiceRoll[3])[0]
            else:
                GetPreDiceRoll[3] = ""
        GetPreDiceRollList = []
        GetSubDiceRollList = []
        if(GetNumDice > 0):
            if(GetMaxDiceRoll == ""):
                GetPreDiceRollList = GetPreDiceRollList + \
                    RandomMultiSameDiceRollAlt(
                        GetNumDice, GetMinDiceRoll, RandType, RandSeed, None)
            else:
                GetPreDiceRollList = GetPreDiceRollList + RandomMultiSameDiceRoll(
                    GetNumDice, GetMinDiceRoll, GetMaxDiceRoll, RandType, RandSeed, None)
        if(GetPreDiceRoll[3] == ""):
            GetSubDiceRollList = GetPreDiceRollList
        else:
            if(int(GetDiceAVGList[1]) > int(GetPreDiceRoll[0])):
                GetDiceAVGList[1] = GetPreDiceRoll[0]
            if(GetDiceAVGList[0] == "l"):
                GetSubDiceRollList = GetMinValues(
                    GetPreDiceRollList, int(GetDiceAVGList[1]))
            if(GetDiceAVGList[0] == "h"):
                GetSubDiceRollList = GetMaxValues(
                    GetPreDiceRollList, int(GetDiceAVGList[1]))
        SubNumOfDice = len(GetSubDiceRollList)
        GetDiceRollList = []
        SubCountNumOfDice = 0
        while(SubCountNumOfDice < SubNumOfDice):
            NeoPreDiceRoll = str(GetSubDiceRollList[SubCountNumOfDice])
            GetDiceRollList.append(int(eval(NeoPreDiceRoll+DiceRollSum)))
            SubCountNumOfDice = SubCountNumOfDice + 1
        GetLastDiceRollList = []
        GetPostDiceAVGList = ""
        if(not GetPreDiceRoll[5] == ""):
            if(len(re.findall("^([l|h]{1})([0-9]+)$",  GetPreDiceRoll[5])) > 0):
                GetPostDiceAVGList = re.findall(
                    "^([l|h]{1})([0-9]+)$", GetPreDiceRoll[5])[0]
            else:
                GetPreDiceRoll[5] = ""
        if(GetPreDiceRoll[5] == ""):
            GetLastDiceRollList = GetDiceRollList
        else:
            if(int(GetPostDiceAVGList[1]) > int(GetPreDiceRoll[0])):
                GetPostDiceAVGList[1] = GetPreDiceRoll[0]
            if(GetPostDiceAVGList[0] == "l"):
                GetLastDiceRollList = GetMinValues(
                    GetDiceRollList, int(GetPostDiceAVGList[1]))
            if(GetPostDiceAVGList[0] == "h"):
                GetLastDiceRollList = GetMaxValues(
                    GetDiceRollList, int(GetPostDiceAVGList[1]))
        if(DiceArray is not None and type(DiceArray) is dict):
            GetLastDiceRollList = GetDictValueFromDiceList(
                GetLastDiceRollList, DiceArray)
        if(DiceArray is not None and (type(DiceArray) is list or type(DiceArray) is tuple)):
            if(DiceArray[0] is not None and type(DiceArray[0]) is dict):
                GetLastDiceRollList = GetDictValueFromDiceListAlt(
                    GetLastDiceRollList, DiceArray)
        DiceRolls = DiceRolls + GetLastDiceRollList
        CountNumOfDice = CountNumOfDice + 1
    return DiceRolls


def RandomMultiDieRollNotationMinMaxByString(DieStr="1d1:6", RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiDiceRollNotationMinMaxByString(
        DieStr, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDiceRollNotationMinMaxByXML(DiceStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    diestr = ""
    tree = cElementTree.ElementTree(file=DiceStrFile)
    root = tree.getroot()
    for child in root:
        if(child.tag == "dice"):
            if(diestr != ""):
                diestr = diestr+","
            if('min' in child.attrib):
                diemin = str(child.attrib['min'])
            else:
                diemin = "1"
            if(len(re.findall("^([\-]?[0-9]+)$", diemin)) < 1):
                diemin = "1"
            diemax = ""
            if('max' in child.attrib):
                diemax = str(child.attrib['max'])
            else:
                diemax = "6"
            if(len(re.findall("^([\-]?[0-9]+)$", diemax)) < 1):
                diemax = "6"
            dienum = ""
            if('num' in child.attrib):
                dienum = str(child.attrib['num'])
            else:
                dienum = "1"
            if(len(re.findall("^([0-9]+)$", dienum)) < 1):
                dienum = "1"
            dieexp = ""
            if('exp' in child.attrib):
                dieexp = str(child.attrib['exp'])
            else:
                dieexp = ""
            if(len(re.findall("^([\+\-\*\/]?[0-9\+\-\*\/]*)$", dieexp)) < 1):
                dieexp = ""
        if(child.tag == "fudge"):
            if(diestr != ""):
                diestr = diestr+","
            diemin = ""
            diemax = ""
            if('max' in child.attrib):
                diemax = str(child.attrib['max'])
                diemin = "-"+str(child.attrib['max'])
            else:
                diemax = "1"
                diemin = "-1"
            if(len(re.findall("^([\-]?[0-9]+)$", diemax)) < 1):
                diemax = "1"
            if(len(re.findall("^([\-]?[0-9]+)$", diemin)) < 1):
                diemin = "-1"
            dienum = ""
            if('num' in child.attrib):
                dienum = str(child.attrib['num'])
            else:
                dienum = "1"
            if(len(re.findall("^([0-9]+)$", dienum)) < 1):
                dienum = "1"
            dieexp = ""
            if('exp' in child.attrib):
                dieexp = str(child.attrib['exp'])
            else:
                dieexp = ""
            if(len(re.findall("^([\+\-\*\/]?[0-9\+\-\*\/]*)$", dieexp)) < 1):
                dieexp = ""
            diestr = diestr+dienum+"u"+diemin+":"+diemax+dieexp
        if(child.tag == "coin"):
            if(diestr != ""):
                diestr = diestr+","
            dienum = ""
            if('num' in child.attrib):
                dienum = str(child.attrib['num'])
            else:
                dienum = "1"
            if(len(re.findall("^([0-9]+)$", dienum)) < 1):
                dienum = "1"
            diestr = diestr+dienum+"c"
            dieexp = ""
            if('exp' in child.attrib):
                dieexp = str(child.attrib['exp'])
            else:
                dieexp = ""
            if(len(re.findall("^([\+\-\*\/]?[0-9\+\-\*\/]*)$", dieexp)) < 1):
                dieexp = ""
            diestr = diestr+dienum+"d"+diemin+":"+diemax+dieexp
    DiceRolls = RandomMultiDiceRollNotationMinMaxByString(
        diestr, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomMultiDieRollNotationMinMaxByXML(DieStrFile, RandType=1, RandSeed=random.seed(), DiceArray=None):
    DiceRolls = RandomMultiDiceRollNotationMinMaxByXML(
        DieStrFile, RandType, RandSeed, DiceArray)
    return DiceRolls


def RandomCoinFlip(ReturnValType="int", RandType=1, RandSeed=random.seed()):
    ReturnValType = ReturnValType.lower()
    CoinFlip = RandomDiceRollAlt(2, RandType, RandSeed)
    if(ReturnValType == "int" or ReturnValType == "integer"):
        CoinFlipValue = CoinFlip[0]
    if(ReturnValType == "bool" or ReturnValType == "boolean"):
        if(CoinFlipValue == 1):
            CoinFlipValue = True
        if(CoinFlipValue == 2):
            CoinFlipValue = False
    if(ReturnValType == "str" or ReturnValType == "string"):
        if(CoinFlipValue == 1):
            CoinFlipValue = "Heads"
        if(CoinFlipValue == 2):
            CoinFlipValue = "Tails"
    return [CoinFlipValue]


def RandomCoinFlipAlt(ReturnValType="int", RandType=1, RandSeed=random.seed()):
    ReturnValType = ReturnValType.lower()
    CoinFlipDict = None
    if(ReturnValType == "bool" or ReturnValType == "boolean"):
        CoinFlipDict = {1: True, 2: False}
    if(ReturnValType == "str" or ReturnValType == "string"):
        CoinFlipDict = {1: "Heads", 2: "Tails"}
    CoinFlipValue = RandomDiceRollAlt(2, RandType, RandSeed, CoinFlipDict)
    return CoinFlipValue


def RandomMultiCoinFlip(NumOfCoins=1, ReturnValType="int", RandType=1, RandSeed=random.seed()):
    CountNumOfCoins = 0
    CoinFlipValue = []
    while(CountNumOfCoins < NumOfCoins):
        CoinFlipValue = CoinFlipValue + \
            RandomCoinFlip(ReturnValType, RandType, RandSeed)
        CountNumOfCoins = CountNumOfCoins + 1
    return CoinFlipValue


def RandomMultiCoinFlipAlt(NumOfCoins=1, ReturnValType="int", RandType=1, RandSeed=random.seed()):
    CountNumOfCoins = 0
    CoinFlipValue = []
    while(CountNumOfCoins < NumOfCoins):
        CoinFlipValue = CoinFlipValue + \
            RandomCoinFlipAlt(ReturnValType, RandType, RandSeed)
        CountNumOfCoins = CountNumOfCoins + 1
    return CoinFlipValue
