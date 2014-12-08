#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.tdrstyle as tdrstyle
#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.CommonLimitTools as limitTools
#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.aux as aux
#import HiggsAnalysis.HeavyChHiggsToTauNu.tools.ShellStyles as ShellStyles

import os
import math
import ROOT
ROOT.gROOT.SetBatch(True)

def Clone(obj, *args):
    cl = obj.Clone(*args)
    ROOT.SetOwnership(cl, True)
    if hasattr(cl, "SetDirectory"):
        cl.SetDirectory(0)
    return cl

_fineBinningSuffix = "_fineBinning"
_originalDatacardDirectory = "originalDatacards"

### Get list of mass points
#def getMassPoints(directory="."):
    ## Find out the mass points
    #mySettings = limitTools.GeneralSettings(directory,[])
    #massPoints = mySettings.getMassPoints(limitTools.LimitProcessType.TAUJETS)
    #return massPoints

### Get luminosity
#def getLuminosity(directory=".", mass=None):
    #m = mass
    #if mass == None:
        #masslist = getMassPoints(directory)
        #m = masslist[0]
    #myLuminosity = float(limitTools.readLuminosityFromDatacard(directory, mySettings.getDatacardPattern(limitTools.LimitProcessType.TAUJETS)%m))
    #return myLuminosity

#mySettings = limitTools.GeneralSettings(directory,[])
#rootFilePattern = mySettings.getRootfilePattern(limitTools.LimitProcessType.TAUJETS)

def getMassPointsForDatacardPattern(directory, datacardFilePattern, massPoints = []):
    # Find datacard files
    myList = os.listdir(directory)
    mySplit = datacardFilePattern.split("%s")
    masses = []
    for item in myList:
        myStatus = True
        myStub = item
        for part in mySplit:
            myStub = myStub.replace(part,"")
            if not part in item:
                myStatus = False
        if myStatus:
            masses.append(myStub)
    if len(masses) > 0:
        masses.sort()

    if len(massPoints) > 0:
        mlist = massPoints[:]
        if len(masses) > 0:
            i = 0
            while i < len(mlist) and len(mlist) > 0:
                if not mlist[i] in masses:
                    mlist.remove(mlist[i])
                else:
                    i += 1
        return mlist
    return masses

class DataCardDirectoryManager:
    def __init__(self, directory, datacardFilePattern, rootFilePattern, rootFileDirectory="", readOnly=False):
        self._datacards = {} # Dictionary, where key is mass and value is DataCardReader object for that mass point
        self._massPoints = getMassPointsForDatacardPattern(directory, datacardFilePattern)

        # initialize datacard objects
        print "Found mass points:",self._massPoints
        for m in self._massPoints:
            self._datacards[m] = DataCardReader(directory, m, datacardFilePattern, rootFilePattern, rootFileDirectory=rootFileDirectory, readOnly=readOnly)
        # check integrity
        self.checkIntegrity()

    def close(self):
        for key in self._datacards.keys():
            self._datacards[key].close()

    def getColumnNames(self):
        if len(self._datacards.keys()) > 0:
            return self._datacards[self._datacards.keys()[0]].getDatasetNames()
        return []

    def replaceColumnNames(self, replaceDictionary):
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            # Do replace in txt file
            for item in replaceDictionary.keys():
                for i in range(0,len(dcard.getDatasetNames())):
                    if dcard._datacardColumnNames[i] == item:
                        dcard._datacardColumnNames[i] = dcard._datacardColumnNames[i].replace(item, replaceDictionary[item])
                for i in range(0,len(dcard._datasetNuisances)):
                    if item in dcard._datasetNuisances[i].keys():
                        dcard._datasetNuisances[i][replaceDictionary[item]] = dcard._datasetNuisances[i][item]
                        del dcard._datasetNuisances[i][item]
                    if dcard._datasetNuisances[i]["name"].startswith(item+"_"):
                        name = replaceDictionary[item]+dcard._datasetNuisances[i]["name"][len(item):]
                        dcard._datasetNuisances[i]["name"] = name
            # Do Replace in root file
            for item in replaceDictionary.keys():
                myList = dcard.getRootFileObjectsWithPattern(item)
                # Loop over root objects
                for objectName in myList:
                    o = dcard.getRootFileObject(objectName)
                    if objectName.startswith(item+"_"+item+"_"):
                        s = item+"_"+item+"_"
                        name = "%s_%s_"%(replaceDictionary[item],replaceDictionary[item])+o.GetName()[len(s):]
                        o.SetName(name)
                    elif objectName.startswith(item+"_"):
                        name = replaceDictionary[item]+o.GetName()[len(item):]
                        o.SetName(name)
                    elif item == objectName:
                        o.SetName(replaceDictionary[item])
    
    def replaceNuisanceNames(self, replaceDictionary):
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            # Do replace in txt file
            for item in replaceDictionary.keys():
                for i in range(0,len(dcard._datasetNuisances)):
                    if dcard._datasetNuisances[i]["name"] == item:
                        dcard._datasetNuisances[i]["name"] = dcard._datasetNuisances[i]["name"].replace(item, replaceDictionary[item])
            # Do Replace in root file
            for item in replaceDictionary.keys():
                myList = dcard.getRootFileObjectsWithPattern(item)
                # Loop over root objects
                for objectName in myList:
                    o = self._datacards[m].getRootFileObject(objectName)
                    if "_"+item+"Up" in o.GetName() or "_"+item+"Down" in o.GetName():
                        o.SetName(o.GetName().replace(item, replaceDictionary[item]))

    def removeStatUncert(self):
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            # Remove previous entries from datacard
            i = 0
            while i < len(dcard._datasetNuisances):
                nuisanceName = dcard._datasetNuisances[i]["name"]
                if "stat" in nuisanceName or "Stat" in nuisanceName:
                    dcard._datasetNuisances.remove(dcard._datasetNuisances[i])
                else:
                    i += 1
            # Remove previous histograms from datacard
            i = 0
            while i < len(dcard._hCache):
                histoName = dcard._hCache[i].GetName()
                if "stat" in histoName or "Stat" in histoName:
                    dcard._hCache[i].Delete()
                    dcard._hCache.remove(dcard._hCache[i])
                else:
                    i += 1

    def recreateShapeStatUncert(self):
        # Remove previous entries from datacard
        self.removeStatUncert()
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            # Loop over columns and
            for c in dcard.getDatasetNames():
                hRate = dcard.getRateHisto(c)
                # Loop over bins in rate
                for nbin in range(1, hRate.GetNbinsX()+1):
                    # Check for overlapping bin-by-bin stat. uncertainties
                    myList = dcard.getRootFileObjectsWithPattern(c)
                    if not ("bin%s"%nbin in myList or "Bin%s"%nbin in myList):
                        # Add entries to datacard
                        myDict = {}
                        myDict["name"] = "%s_statBin%d"%(c, nbin)
                        myDict["distribution"] = "shape"
                        for cc in dcard.getDatasetNames():
                            if cc == c:
                                myDict[cc] = "1"
                            else:
                                myDict[cc] = "-"
                        dcard._datasetNuisances.append(myDict)
                        # Add histograms
                        hUp = Clone(hRate)
                        hDown = Clone(hRate)
                        hUp.SetName("%s_%s_statBin%dUp"%(c, c, nbin))
                        hDown.SetName("%s_%s_statBin%dDown"%(c, c, nbin))
                        hUp.SetBinContent(nbin, hUp.GetBinContent(nbin)+hUp.GetBinError(nbin))
                        myMinValue = max(hDown.GetBinContent(nbin)-hDown.GetBinError(nbin), 0.0)
                        hDown.SetBinContent(nbin, myMinValue)
                        for k in range(1, hRate.GetNbinsX()+1):
                            hUp.SetBinError(k, 0.0)
                            hDown.SetBinError(k, 0.0)
                        dcard.addHistogram(hUp)
                        dcard.addHistogram(hDown)
                myTotalUp = 0.0
                myTotal = 0.0
                for nbin in range(1, hRate.GetNbinsX()+1):
                    myTotalUp += hRate.GetBinError(nbin)**2
                    myTotal += hRate.GetBinContent(nbin)
                print "  %s: stat.uncert.: %f"%(c, math.sqrt(myTotalUp)/myTotal)

    def removeColumn(self, name):
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            # Loop over nuisances
            i = 0
            while i < len(dcard._datasetNuisances):
                if name in dcard._datasetNuisances[i].keys():
                    del dcard._datasetNuisances[i][name]
                i += 1
            # Loop over histograms
            i = 0
            while i < len(dcard._hCache):
                hName = dcard._hCache[i].GetName()
                if hName == name or hName.startswith(name+"_"):
                    del dcard._hCache[i]
                else:
                    i += 1
            # Remove column from lists
            i = 0
            while i < len(dcard._datacardColumnNames):
                if dcard._datacardColumnNames[i] == name:
                    del dcard._datacardColumnNames[i]
                    del dcard._rateValues[i]
                else:
                    i += 1

    def addNuisance(self, name, distribution, columns, value):
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            myDict = None
            for n in dcard._datasetNuisances:
                if n["name"] == name:
                    myDict = n
            if myDict == None:
                myDict = {}
                myDict["name"] = name
                myDict["distribution"] = distribution
                dcard._datasetNuisances.append(myDict)
            for c in dcard.getDatasetNames():
                if c in columns:
                    myDict[c] = value
                else:
                    if c not in myDict.keys():
                        myDict[c] = "-"

    def removeNuisance(self, name):
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            # Remove histograms
            i = 0
            while i < len(dcard._hCache):
                if "_"+name+"Up" in dcard._hCache[i].GetName() or "_"+name+"Down" in dcard._hCache[i].GetName():
                    dcard._hCache[i].Delete()
                    dcard._hCache.remove(dcard._hCache[i])
                else:
                    i += 1
            # Remove nuisances
            i = 0
            while i < len(dcard._datasetNuisances):
                if dcard._datasetNuisances[i]["name"] == name:
                    del dcard._datasetNuisances[i]
                else:
                    i += 1
                    
    def removeManyNuisances(self, nameList):
        if nameList == None:
            return
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            for n in nameList:
                if n == "*":
                    # Remove all
                    while len(dcard._datasetNuisances) > 0:
                        self.removeNuisance(dcard._datasetNuisances[i]["name"])
                elif "*" in n:
                    # Find wildcarded nuisances
                    mySplit = n.split("*")
                    if len(mySplit) > 2:
                        raise Exception("only one wild card supported")
                    i = 0
                    while i < len(dcard._datasetNuisances):
                        name = dcard._datasetNuisances[i]["name"]
                        if name.startswith(mySplit[0]) and name.endswith(mySplit[1]):
                            self.removeNuisance(name)
                        else:
                            i += 1
                else:
                    self.removeNuisance(n)
                
    def keepManyNuisances(self, nameList):
        if nameList == None:
            return
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            myKeepList = []
            for n in nameList:
                if n == "*":
                    # Remove all
                    i = 0
                    while i < len(dcard._datasetNuisances):
                        myKeepList.append(dcard._datasetNuisances[i]["name"])
                        i += 1
                elif "*" in n:
                    # Find wildcarded nuisances
                    mySplit = n.split("*")
                    if len(mySplit) > 2:
                        raise Exception("only one wild card supported")
                    i = 0
                    while i < len(dcard._datasetNuisances):
                        name = dcard._datasetNuisances[i]["name"]
                        if name.startswith(mySplit[0]) and name.endswith(mySplit[1]):
                            myKeepList.append(name)
                        i += 1
                else:
                    myKeepList.append(n)
            # Obtain remove list
            myRemoveList = []
            for n in dcard._datasetNuisances:
                if not n["name"] in myKeepList:
                    myRemoveList.append(n["name"])
            # Remove items on remove list
            for n in myRemoveList:
                self.removeNuisance(n)

    def replaceNuisanceValue(self, name, newValue, columns=[]):
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            myColumns = []
            if isinstance(columns, list):
                myColumns.extend(columns)
            elif isinstance(columns, str):
                myColumns.append(columns)
            else:
                raise Exception("should not happen")
            if len(myColumns) == 0:
                myColumns = dcard.getDatasetNames()
            for i in range(0,len(dcard._datasetNuisances)):
                if dcard._datasetNuisances[i]["name"] == name:
                    if dcard._datasetNuisances[i]["distribution"] == "shape":
                        raise Exception("Error: replaceNuisanceValue works only for normalization nuisances; '%s' is a shape nuisance!"%name)
                    for k in myColumns:
                        if k in dcard.getDatasetNames():
                            dcard._datasetNuisances[i][k] = newValue
                        #else:
                        #    print k

    def convertShapeToNormalizationNuisance(self, nameList, columnList=[]):
        myList = []
        if isinstance(nameList, str):
            myList.append(nameList)
        elif isinstance(nameList, list):
            myList.extend(nameList)
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            myAffectedColumns = columnList[:]
            if len(myAffectedColumns) == 0:
                myAffectedColumns.extend(dcard.getDatasetNames())
            for item in myList:
                for i in range(0,len(dcard._datasetNuisances)):
                    if dcard._datasetNuisances[i]["name"] == item:
                        hasShapesStatus = False
                        for c in dcard.getDatasetNames():
                            if dcard._datasetNuisances[i][c] == "1":
                                if c in myAffectedColumns:
                                    # Find histograms
                                    hup = dcard.getRootFileObject("%s_%sUp"%(c, dcard._datasetNuisances[i]["name"]))
                                    hdown = dcard.getRootFileObject("%s_%sDown"%(c, dcard._datasetNuisances[i]["name"]))
                                    hRate = dcard.getRateHisto(c)
                                    # Calculate nuisance value by integrating
                                    myNominalRate = hRate.Integral()
                                    myMinus = hdown.Integral()/myNominalRate
                                    myPlus = hup.Integral()/myNominalRate
                                    s = ""
                                    if abs(myMinus-myPlus) > 0.0005:
                                        s = "%.3f/%.3f"%(myMinus, myPlus)
                                    else:
                                        s = "%.3f"%(myPlus)
                                    # Remove histograms
                                    dcard._hCache.remove(hup)
                                    dcard._hCache.remove(hdown)
                                    hup.Delete()
                                    hdown.Delete()
                                    # Replace value for column in datacard
                                    dcard._datasetNuisances[i][c] = s
                                else:
                                    hasShapesStatus = True
                        if hasShapesStatus:
                            dcard._datasetNuisances[i]["distribution"] = "shape?"
                        else:
                            dcard._datasetNuisances[i]["distribution"] = "lnN"
    
    def mergeShapeNuisances(self, namesList, newName):
        if len(namesList) < 2:
            raise Exception("Error: mergeShapeNuisances needs at least two nuisance names for the merge!")
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            # Look for first item
            targetIndex = None
            for i in range(0,len(dcard._datasetNuisances)):
                if dcard._datasetNuisances[i]["name"] == namesList[0]:
                    if dcard._datasetNuisances[i]["distribution"] != "shape":
                        raise Exception("Error: mergeShapeNuisances: nuisance '%s' is not a shape nuisance!"%namesList[0])
                    targetIndex = i
            # Do merge
            for item in namesList[1:]:
                for i in range(0,len(dcard._datasetNuisances)):
                    if dcard._datasetNuisances[i]["name"] == item:
                        if dcard._datasetNuisances[i]["distribution"] != "shape":
                            raise Exception("Error: mergeShapeNuisances: nuisance '%s' is not a shape nuisance!"%item)
                        # Update nuisance histograms and datacard nuisance lines
                        for c in dcard.getDatasetNames():
                            if dcard._datasetNuisances[i][c] == "1":
                                if dcard._datasetNuisances[targetIndex][c] == "1":
                                    # Add histogram contents
                                    myTargetList = dcard.getRootFileObjectsWithPattern("%s_%s"%(c, dcard._datasetNuisances[targetIndex]["name"]))
                                    mySourceList = dcard.getRootFileObjectsWithPattern("%s_%s"%(c, dcard._datasetNuisances[i]["name"]))
                                    myRateHisto = dcard.getRateHisto(c)
                                    if len(myTargetList) != len(mySourceList):
                                        raise Exception("This should not happen")
                                    for h in range(0, len(myTargetList)):
                                        if myTargetList[h].startswith(c):
                                            hTarget = dcard.getRootFileObject(myTargetList[h])
                                            hSource = dcard.getRootFileObject(mySourceList[h])
                                            for k in range(1, hTarget.GetNbinsX()+1):
                                                myOffset = myRateHisto.GetBinContent(k)
                                                myVariation = (hTarget.GetBinContent(k) - myOffset)**2
                                                myVariation += (hSource.GetBinContent(k) - myOffset)**2
                                                #print c, hTarget.GetBinContent(k), hSource.GetBinContent(k), myOffset, math.sqrt(myVariation), math.sqrt(myVariation)+myOffset, myOffset-math.sqrt(myVariation)
                                                if mySourceList[h].endswith("Up"):
                                                    hTarget.SetBinContent(k, math.sqrt(myVariation)+myOffset)
                                                elif mySourceList[h].endswith("Down"):
                                                    hTarget.SetBinContent(k, myOffset-math.sqrt(myVariation))
                                else:
                                    # Update nuisance line
                                    dcard._datasetNuisances[i][c] = "1"
                                    # Copy histogram
                                    mySourceList = dcard.getRootFileObjectsWithPattern("%s_%s"%(c, dcard._datasetNuisances[i]["name"]))
                                    for h in mySourceList:
                                        hSource = dcard.getRootFileObject(h)
                                        if hSource.GetName().endswith("Up"):
                                            hnew = Clone(hSource, "%s_%sUp"%(c, dcard._datasetNuisances[i]["name"]))
                                            dcard._hCache.append(hnew)
                                        elif hSource.GetName().endswith("Down"):
                                            hnew = Clone(hSource, "%s_%sDown"%(c, dcard._datasetNuisances[i]["name"]))
                                            dcard._hCache.append(hnew)
        # Rename
        myDict = {namesList[0]: newName}
        self.replaceNuisanceNames(myDict)
        # Remove items
        for item in namesList[1:]:
            self.removeNuisance(item)

    ## This method subtracts a systematic shift from the shape
    def subtractPedestalFromShapeNuisances(self, target):
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            # Look for target nuisance (for determining which columns are affected)
            myTargetNuisance = None
            for i in range(0,len(dcard._datasetNuisances)):
                if dcard._datasetNuisances[i]["name"] == target:
                    myTargetNuisance = dcard._datasetNuisances[i]
            if myTargetNuisance == None:
                raise Exception("Error: Could not find target nuisance '%s'!"%target)
            if myTargetNuisance["distribution"] != "shape":
                raise Exception("Error: Target is not a shape nuisance!")
            # Loop over columns
            for c in dcard.getDatasetNames():
                if myTargetNuisance[c] == "1":
                    # Find target histograms
                    hTargetUp = dcard.getRootFileObject("%s_%sUp"%(c,target))
                    hTargetDown = dcard.getRootFileObject("%s_%sDown"%(c,target))
                    hNominal = dcard.getRateHisto(c)
                    # Do correction
                    for h in [hTargetUp, hTargetDown]:
                        for k in range(1, hTargetUp.GetNbinsX()+1):
                            myDelta = (hTargetUp.GetBinContent(k) + hTargetDown.GetBinContent(k)) / 2.0 - hNominal.GetBinContent(k)
                            #print hTargetUp.GetBinContent(k), hTargetDown.GetBinContent(k), hNominal.GetBinContent(k), "delta=", myDelta
                            hTargetUp.SetBinContent(k, hTargetUp.GetBinContent(k) - myDelta)
                            hTargetDown.SetBinContent(k, hTargetDown.GetBinContent(k) - myDelta)
                            #print "after:",hTargetUp.GetBinContent(k), hTargetDown.GetBinContent(k)
                    myNominalRate = hNominal.Integral()
                    #print "... Pedestal correction applied to shape '%s': new nuisance up: %f down: %f"%(target, hTargetUp.Integral() / myNominalRate, hTargetDown.Integral() / myNominalRate)

    ## Set minimum stat. uncert. for bins with zero rate or very small rate
    def fixTooSmalltatUncertProblem(self, signalMinimumAbsStatValue, bkgMinimumAbsStatValue):
        for m in self._datacards.keys():
            dcard = self._datacards[m]
            # Loop over columns
            for c in dcard.getDatasetNames():
                # Find min value by background
                minValue = 0
                if c == dcard.getDatasetNames()[0]:
                    minValue = signalMinimumAbsStatValue
                else:
                    for k in bkgMinimumAbsStatValue.keys():
                        if "_"+k in c:
                            minValue = bkgMinimumAbsStatValue[k]
                # Loop over rate histogram
                hRate = dcard.getRateHisto(c)
                for k in range(1, hRate.GetNbinsX()+1):
                    a = hRate.GetBinContent(k)
                    if abs(a) < minValue or hRate.GetBinError(k) < minValue:
                        hRate.SetBinError(k, minValue)

    ## Checks if the root file background and observation items are the same between the datacards
    def checkIntegrity(self):
        if len(self._datacards.keys()) == 0:
            return
        refCard = self._datacards[self._datacards.keys()[0]]
        cardList = self._datacards.keys()[1:]
        for testCardKey in cardList:
            print "Integrity check, test: m%s ref: m%s"%(self._datacards.keys()[0], testCardKey)
            testCard = self._datacards[testCardKey]
            # Compare root objects
            nHistos = len(refCard._hCache)
            for i in range(nHistos):
                refName = refCard._hCache[i].GetName()
                testName = testCard._hCache[i].GetName()
                if refName == testName:
                    nbins = refCard._hCache[i].GetNbinsX()
                    for k in range(1, nbins+1):
                        if abs(refCard._hCache[i].GetBinContent(k) - testCard._hCache[i].GetBinContent(k)) > 0.00000001:
                            if not (testName.startswith("%s_"%testCard.getDatasetNames()[0]) or testName == testCard.getDatasetNames()[0]):
                                print "  bin %d mismatch: test %s %f vs. ref %s %f"%(k, testName, testCard._hCache[i].GetBinContent(k), refName, refCard._hCache[i].GetBinContent(k))
                        else:
                            if testName.startswith("%s_"%testCard.getDatasetNames()[0]) or testName == testCard.getDatasetNames()[0]:
                                if refCard._hCache[i].GetBinContent(k) > 0:
                                    print "  signal bin %d is the same: test %s %f vs. ref %s %f"%(k, testName, testCard._hCache[i].GetBinContent(k), refName, refCard._hCache[i].GetBinContent(k))
                else:
                    if not refName.startswith(refCard.getDatasetNames()[0]):
                        print "  Name mismatch:",refName, testName
            # Compare nuisances
            nNuisances = len(refCard._datasetNuisances)
            for i in range(nNuisances):
                for c in testCard.getDatasetNames()[1:]:
                    if c in refCard._datasetNuisances[i].keys():
                        if refCard._datasetNuisances[i][c] != testCard._datasetNuisances[i][c]:
                            print "  nuisance %s / column %s mismatch: test %s vs. ref. %s"%(refCard._datasetNuisances[i]["name"], c, testCard._datasetNuisances[i][c], refCard._datasetNuisances[i][c])
        print "Integrity test passed"

## Calculates maximum width of each table cell
def calculateCellWidths(widths,table):
    myResult = widths
    # Initialise widths if necessary
    if len(table) == 0:
      return myResult

    for i in range(len(widths),len(table[0])):
        myResult.append(0)
    # Loop over table cells
    for row in table:
        for i in range(0,len(row)):
            if len(row[i]) > myResult[i]:
                myResult[i] = len(row[i])
    return myResult

## Returns a separator line of correct total width
def getSeparatorLine(widths):
    myTotalSize = 0
    for cell in widths:
        myTotalSize += cell+1
    myTotalSize -= 1
    myResult = ""
    for i in range(0,myTotalSize):
        myResult += "-"
    myResult += "\n"
    return myResult

## Converts a list into a string
def getTableOutput(widths,table,latexMode=False):
    myResult = ""
    for row in table:
        for i in range(0,len(row)):
            if i != 0:
                myResult += " "
                if latexMode:
                    myResult += "& "
            myResult += row[i].ljust(widths[i])
        if latexMode:
            myResult += " \\\\ "
        myResult += "\n"
    return myResult

## Class for containing all information related to a single datacard
class DataCardReader:
    def __init__(self, directory, mass, datacardFilePattern, rootFilePattern, rootFileDirectory="", readOnly=True):
        # Initialize
        self._directory = directory
        self._mass = mass
        self._datacardFilePattern = datacardFilePattern
        self._rootFilePattern = rootFilePattern
        self._rootFileDirectory = rootFileDirectory
        self._readOnly = readOnly
        self._rootFilename = None
        self._datacardFilename = None
        self._hCache = [] # Cache for persistent histograms
        # DatacardInfo
        self._datacardColumnNames = [] # List of columns in datacard
        self._datacardBinName = None
        self._datacardColumnStartIndex = None # Index of first column
        self._datacardHeaderLines = []
        self._observationValue = None
        self._rateValues = {} # Dictionary, where key is dataset name and value is a string of the rate value
        self._datasetNuisances = [] # List of dictionaries, where key is nuisance name

        # Read contents
        self._readDatacardContents(directory, mass)
        self._readRootFileContents(directory, mass)
        
    def close(self, silent=False):
        if not silent:
            print "Writing datacard:",self._datacardFilename
        self._writeDatacardContents()
        
        if not silent:
            print "Closing file:",self._rootFilename
        self._writeRootFileContents()

    def getDatasetNames(self):
        return self._datacardColumnNames

    def getNuisanceNamesByDatasetName(self, datasetName):
        self.hasDatasetByName(datasetName, exceptionOnFail=True)
        return self._datasetNuisances[datasetName]

    def hasDatasetByName(self, datasetName, exceptionOnFail=False):
        if not datasetName in self._datacardColumnNames:
            if exceptionOnFail:
                raise Exception("Dataset '%s' not found!"%datasetName)
            return False
        return True

    def datasetHasNuisance(self, datasetName, nuisanceName, exceptionOnFail=False):
        self.hasDatasetByName(datasetName)
        if not nuisanceName in self._datasetNuisances[datasetName]:
            if exceptionOnFail:
                raise Exception("Dataset '%s' does not have nuisance '%s'!"%(datasetName,nuisanceName))
            return False
        return True
      
    def getRateHisto(self, datasetName, fineBinned=False, exceptionOnFail=True):
        self.hasDatasetByName(datasetName, exceptionOnFail=True)
        name = datasetName
        if fineBinned:
            name += _fineBinningSuffix
        for item in self._hCache:
            if item.GetName() == name:
                return item # no clone should be returned
        if exceptionOnFail:
            raise Exception("Could not find histogram '%s'!"%name)
        return None
    
    def getNuisanceNames(self, datasetName):
        l = []
        for n in self._datasetNuisances:
            if datasetName not in n.keys():
                raise Exception("Error '%s' not found in datasets!"%datasetName)
            if n[datasetName] != "-" and n[datasetName] != "1.000" and n[datasetName] != "1.0":
                l.append(n["name"])
        return l
    
    def getShapeNuisanceNames(self, datasetName):
        l = []
        for n in self._datasetNuisances:
            if datasetName not in n.keys():
                raise Exception("Error '%s' not found in datasets!"%datasetName)
            if n["distribution"] == "shape":
                if n[datasetName] == "1":
                    l.append(n["name"])
        return l
    
    def getNuisanceHistos(self, datasetName, nuisanceName, exceptionOnFail=True, fineBinned=False):
        self.datasetHasNuisance(datasetName, nuisanceName, exceptionOnFail=True)
        name = "%s_%s"%(datasetName, nuisanceName)
        if "Bin" in name:
            name = "%s_%s"%(datasetName, name) # bin-by-bin uncert. replicate the dataset name
        if fineBinned:
            name += _fineBinningSuffix
        up = None
        down = None
        for item in self._hCache:
            if item.GetName == name+"Up":
                up = item
            elif item.GetName == name+"Down":
                down = item
        if up == None:
            if exceptionOnFail:
                raise Exception("Could not find histogram '%s'!"%name+"Up")
            return (None, None)
        if down == None:
            if exceptionOnFail:
              raise Exception("Could not find histogram '%s'!"%name+"Down")
            return (None, None)
        return (up, down) # no clone should be returned

    def debug(self):
        print "DEBUG info of DataCardReader:"
        names = self.getDatasetNames()
        #for n in names:
            #print "..  dset=%s has shape nuisances:"%n
            #print ".... %s"%", ".join(map(str,self.getNuisanceNamesByDatasetName(n)))
    
    def scaleSignal(self, value):
        signalColumn = self._datacardColumnNames[0]
        # Update rate
        a = float(self._rateValues[0])*value
        self._rateValues[0] = "%.3f"%a
        # Update rate and nuisance histograms
        # Note: both need to be scaled 
        olist = self.getRootFileObjectsWithPattern(signalColumn)
        hRate = self.getRateHisto(signalColumn)
        hOriginalRate = Clone(hRate)
        hRate.Scale(value)
        for oname in olist:
            if oname.startswith(signalColumn+"_"): # Do not apply twice to rate histogram
                h = self.getRootFileObject(oname)
                deltaOriginal = None
                deltaOriginal = h.Integral() / hOriginalRate.Integral()
                backup = ROOT.gErrorIgnoreLevel
                ROOT.gErrorIgnoreLevel = ROOT.kError # suppress complaints about different bin labels
                h.Add(hOriginalRate, -1.0)
                h.Scale(value)
                h.Add(hRate, 1.0)
                ROOT.gErrorIgnoreLevel = backup
                deltaNew = h.Integral() / hRate.Integral()
                if abs(deltaOriginal-deltaNew) > 0.0001:
                    print "Something is wrong, the rel. uncertainty is not concerved: %f->%f!"%(deltaOriginal, deltaNew)

    def addHistogram(self, h):
        self._hCache.append(Clone(h))
    
    def _readRootFileContents(self, directory, mass):
        self._rootFilename = os.path.join(directory, self._rootFilePattern%mass)
        # Make backup of original cards
        if not self._readOnly:
            if not os.path.exists(_originalDatacardDirectory):
                os.mkdir(_originalDatacardDirectory)
            if not os.path.exists(os.path.join(_originalDatacardDirectory,self._rootFilename)):
                os.system("cp %s %s/."%(os.path.join(directory,self._rootFilename), _originalDatacardDirectory))
            else:
                os.system("cp %s ."%(os.path.join(_originalDatacardDirectory,self._rootFilename)))
        # Open file
        print "Opening file:",self._rootFilename
        backup = ROOT.gErrorIgnoreLevel
        ROOT.gErrorIgnoreLevel = ROOT.kError
        f = ROOT.TFile.Open(self._rootFilename)
        ROOT.gErrorIgnoreLevel = backup
        if f == None:
            raise Exception("Error opening file '%s'!"%self._rootFilename)
        f.Cd(self._rootFileDirectory)
        # Read histograms to cache
        myHistoNames = ["data_obs"]
        for c in self._datacardColumnNames:
            myHistoNames.append(c)
            for n in self._datasetNuisances:
                if n["distribution"] == "shape" and n[c] == "1":
                    myHistoNames.append("%s_%sUp"%(c,n["name"]))
                    myHistoNames.append("%s_%sDown"%(c,n["name"]))
        myDir = f.GetDirectory(self._rootFileDirectory)
        klist = myDir.GetListOfKeys()
        for name in myHistoNames:
            k = klist.FindObject(name)
            if k == None:
                raise Exception("Error: cannot find histo '%s' in root file '%s'!"%(name, self._rootFilename))
            o = k.ReadObj()
            o.SetName(k.GetName()) # The key has the correct name, but the histogram name might be something else
            self._hCache.append(Clone(o))
        f.Close()

    def _writeRootFileContents(self):
        if self._readOnly:
            return
        myFilename = self._rootFilename
        if len(self._rootFileDirectory) > 0:
            myFilename = myFilename.replace(".root","_%s.root"%self._rootFileDirectory)
        f = ROOT.TFile.Open(myFilename, "RECREATE")
        if f == None:
            raise Exception("Error opening file '%s'!"%self._rootFilename)
        for h in self._hCache:
            h.SetDirectory(f)
            #print h.GetName()
        f.Write()
        f.Close()
        self._hCache = []

    def getRootFileObjectsWithPattern(self, pattern):
        myOutList = []
        for item in self._hCache:
            if pattern in item.GetName():
                myOutList.append(item.GetName())
        return myOutList

    def getRootFileObject(self, objectName):
        for item in self._hCache:
            if item.GetName() == objectName:
                return item
        raise Exception("Error: Cannot find root object '%s' in root file '%s'!"%(objectName, self._rootFilename))

    def _readDatacardContents(self, directory, mass):
        self._datacardFilename = os.path.join(directory, self._datacardFilePattern%mass)
        # Make backup of original cards
        if not self._readOnly:
            if not os.path.exists(_originalDatacardDirectory):
                os.mkdir(_originalDatacardDirectory)
            if not os.path.exists(os.path.join(_originalDatacardDirectory,self._datacardFilename)):
                os.system("cp %s %s/."%(os.path.join(directory,self._datacardFilename), _originalDatacardDirectory))
            else:
                os.system("cp %s ."%(os.path.join(_originalDatacardDirectory,self._datacardFilename)))
        # Obtain datacard
        myOriginalCardFile = open(self._datacardFilename)
        myOriginalCardLines = myOriginalCardFile.readlines()
        myOriginalCardFile.close()
        # Parse datacard contents
        self._parseDatacardHeader(myOriginalCardLines)
        self._parseDatacardColumnNames(myOriginalCardLines)
        self._parseDatacardNuisanceNames(myOriginalCardLines)
        #print self._datacardHeaderLines
        #print self._observationValue
        #print self._rateValues
        #print self._datasetNuisances
    
    def _writeDatacardContents(self):
        if self._readOnly:
            return
        
        # Determine order of columns (sort them descending by count)
        mySortList = []
        for i in range(len(self._datacardColumnNames)):
            if i <= -self._datacardColumnStartIndex:
                mySortList.append((i, 100000000-i))
            else:
                mySortList.append((i, float(self._rateValues[i])))
        mySortList.sort(key=lambda x: x[1], reverse=True)
        myOutput = ""
        myObservedLine = ""
        # Create header
        for l in self._datacardHeaderLines:
            mySplit = l.split()
            if mySplit[0] == "observation":
                myOutput += "observation    %s\n"%self._observationValue
            elif "%s/"%self._rootFileDirectory in l:
                myOutput += l.replace("%s/"%self._rootFileDirectory,"").replace(".root","_%s.root"%self._rootFileDirectory)
            else:
                myOutput += l
        # Create process lines
        myProcessTable = []
        myLine = ["bin",""]
        for c in self._datacardColumnNames:
            myLine.append(self._datacardBinName)
        myProcessTable.append(myLine)
        myProcessLine = ["process",""]
        for i in range(len(self._datacardColumnNames)):
            myProcessLine.append(self._datacardColumnNames[mySortList[i][0]])
        myProcessTable.append(myProcessLine)
        myLine = ["process",""]
        for i in range(0, len(self._datacardColumnNames)):
            myLine.append("%d"%(self._datacardColumnStartIndex+i))
        myProcessTable.append(myLine)
        # Create rate table
        myRateTable = []
        myLine = ["rate",""]
        for i in range(len(self._datacardColumnNames)):
            myLine.append(self._rateValues[mySortList[i][0]])
        myRateTable.append(myLine)
        # Create nuisance table
        myNuisanceTable = []
        myStatTable = []
        for n in self._datasetNuisances:
            myRow = []
            # add first two entries
            myRow.append(n["name"])
            myRow.append(n["distribution"])
            # add data from columns
            for c in myProcessLine[2:]:
                myRow.append(n[c])
            # store
            if "stat" in n["name"] or "Stat" in n["name"]:
                myStatTable.append(myRow)
            else:
                myNuisanceTable.append(myRow)
        # Create stat.uncert. table
        
        # Do formatting
        myWidths = []
        for c in self._datacardColumnNames:
            myWidths.append(0)
        calculateCellWidths(myWidths, myProcessTable)
        calculateCellWidths(myWidths, myRateTable)
        calculateCellWidths(myWidths, myNuisanceTable)
        calculateCellWidths(myWidths, myStatTable)
        for i in range(0,len(myWidths)):
            if myWidths[i] < 9:
                myWidths[i] = 9
        mySeparatorLine = getSeparatorLine(myWidths)
        # Add tables to output
        myOutput += getTableOutput(myWidths, myProcessTable)
        myOutput += mySeparatorLine
        myOutput += getTableOutput(myWidths, myRateTable)
        myOutput += mySeparatorLine
        myOutput += getTableOutput(myWidths, myNuisanceTable)
        myOutput += mySeparatorLine
        myOutput += getTableOutput(myWidths, myStatTable)
        myOutput += mySeparatorLine
        # Save
        myOriginalCardFile = open(self._datacardFilename, "w")
        myOriginalCardFile.write(myOutput)
        myOriginalCardFile.close()


    ## Parse header from datacard file
    def _parseDatacardHeader(self, lines):
        self._datacardHeaderLines = []
        for l in lines:
            mySplit = l.split()
            if mySplit[0] == "bin" and self._datacardBinName == None:
                self._datacardBinName = mySplit[1]
            if mySplit[0] == "process":
                del self._datacardHeaderLines[len(self._datacardHeaderLines)-1]
                return
            self._datacardHeaderLines.append(l)
        raise Exception("This line should never be reached")
    
    ## Parse column names from datacard file
    def _parseDatacardColumnNames(self, lines):
        for i in range(0, len(lines)):
            mySplit = lines[i].split()
            if mySplit[0] == "process":
                self._datacardColumnNames = mySplit[1:]
                mySplitNext = lines[i+1].split()
                if mySplitNext[0] != "process":
                    raise Exception("Failed to find two consecutive rows starting with 'process'!")
                self._datacardColumnStartIndex = int(mySplitNext[1])
                #print self._datacardColumnStartIndex
                return
        raise Exception("This line should never be reached")

    ## Parse info of nuisances from datacard file
    def _parseDatacardNuisanceNames(self, lines):
        if len(self._datacardColumnNames) == 0:
            raise Exception("No column names found in datacard!")
        myNames = []
        myRateLinePassedStatus = False
        for l in lines:
            if l != "\n":
                mySplit = l.split()
                if myRateLinePassedStatus and len(mySplit) > 1:# and not "statBin" in mySplit[0]:
                    # store nuisance
                    myDict = {}
                    myDict["name"] = mySplit[0]
                    myDict["distribution"] = mySplit[1]
                    for i in range(0,len(self._datacardColumnNames)):
                        myDict[self._datacardColumnNames[i]] = mySplit[i+2]
                    # Ignore stat. uncertainty
                    if not myDict["name"].endswith("stat"):
                        self._datasetNuisances.append(myDict)
                if len(mySplit[0]) > 3:
                    if mySplit[0] == "observation":
                    # store observation
                        self._observationValue = mySplit[1]
                    if mySplit[0] == "rate":
                        # store rate
                        self._rateValues = mySplit[1:]
                        myRateLinePassedStatus = True
        if len(self._datasetNuisances) == 0:
            raise Exception("No nuisances found!")

#def validateDatacards(directory="."):
    #def checkItem(testName, booleanTest, failMsg):
        #if booleanTest:
            #print ".. Test: %s: %sPASSED%s"%(testName, ShellStyles.TestPassedStyle(), ShellStyles.NormalStyle())
        #else:
            #print ".. Test: %s: %sFAILED%s"%(testName, ShellStyles.ErrorStyle(), ShellStyles.NormalStyle())
            #print failMsg
            #raise Exception()
        #return 1
  
    #nTests = 0
    #nMassPoints = 0
    #print "\n%sValidating datacards in directory: %s%s"%(ShellStyles.HighlightStyle(),directory,ShellStyles.NormalStyle())
    #massPoints = getMassPoints(directory)
    #if len(massPoints) == 0:
        #raise Exception ("No datacards found in directory '.'!"%directory)
    #for m in massPoints:
        #nMassPoints += 1
        #print "%sConsidering mass: %s%s"%(ShellStyles.HighlightStyle(),m,ShellStyles.NormalStyle())
        #reader = DataCardReader(directory, m)
        #for dset in reader.getDatasetNames():
            #hRate = reader.getRateHisto(dset)
            #myNuisanceNames = reader.getNuisanceNamesByDatasetName(dset)
            ## Check integral of fine binned and non-fine binned histogram
            #hRateFine = reader.getRateHisto(dset, fineBinned=True, exceptionOnFail=False)
            #if hRateFine != None and not "QCD" in dset: # for QCD there can be a difference because negative rate bins are forced to zero in rate histo
                #nTests += checkItem("(%s) Nominal rate vs. fine binned rate "%dset, 
                          #abs(hRate.Integral() / hRateFine.Integral()-1.0) < 0.0000001,
                          #"Nominal rate = %f, fine binned rate = %f"%(hRate.Integral(), hRateFine.Integral()))
            #else:
                #print "   (skipping test for Nominal rate vs. fine binned rate)"
            ## Check if rate is negative
            #for i in range(1,hRate.GetNbinsX()+1):
                #nTests += checkItem("(%s) rate >= 0 for bin %d"%(dset,i), hRate.GetBinContent(i) >= 0.0, "")
            ## Check bin-by-bin nuisances
            #if not "NoFitUncert" in directory and not "noSystUncert" in directory:
                #for i in range(1,hRate.GetNbinsX()+1):
                    #myNames = []
                    #for n in myNuisanceNames:
                        #if n.endswith("Bin%d"%i):
                            #myNames.append(n)
                    ## Check existence of bin-by-bin uncert.
                    #nTests += checkItem("(%s) has at least one bin-by-bin uncert. for bin %d"%(dset,i), len(myNames) > 0, "")
                    #nTests += checkItem("(%s) has exactly one bin-by-bin uncert. for bin %d"%(dset, i), len(myNames) == 1, "found nuisances: %s"%", ".join(map(str,myNames)))
                    #(up,down) = reader.getNuisanceHistos(dset, myNames[0])
                    #rate = hRate.GetBinContent(i)
                    #if (rate < 0.000001):
                        ## Check if zero rate bins are treated properly
                        #nTests += checkItem("(%s) rate=0 and bin-by-bin uncert. (%s) up != 0 for bin %d"%(dset,myNames[0],i), up.GetBinContent(i) > 0.000001, "You need to a non-zero value for the up uncert. in this case!")
                    #else:
                        ## Check that non-zero bins are no have a proper treatment
                        #nTests += checkItem("(%s) rate>0 and bin-by-bin uncert. (%s) up != rate for bin %d"%(dset,myNames[0],i), abs(rate-up.GetBinContent(i)) > 0.000001, "Sounds like a bug")
                        #nTests += checkItem("(%s) rate>0 and bin-by-bin uncert. (%s) down != rate for bin %d"%(dset,myNames[0],i), abs(rate-down.GetBinContent(i)) > 0.000001, "Sounds like a bug")
    #return (nTests, nMassPoints)
