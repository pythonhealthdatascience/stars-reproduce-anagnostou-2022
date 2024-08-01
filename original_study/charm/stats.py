# -*- coding: utf-8 -*-

import math 

outDict = dict()
#outList 0
outDict['day-mean'] = []
outDict['day-s'] = []
outDict['day-sd'] = []
outDict['day-ci'] = []
#outList 1
outDict['emArrivals-mean'] = []
outDict['emArrivals-s'] = []
outDict['emArrivals-sd'] = []
outDict['emArrivals-ci'] = []
#outList 2
outDict['elArrivals-mean'] = []
outDict['elArrivals-s'] = []
outDict['elArrivals-sd'] = []
outDict['elArrivals-ci'] = []
#outList 3
outDict['cArrivals-mean'] = []
outDict['cArrivals-s'] = []
outDict['cArrivals-sd'] = []
outDict['cArrivals-ci'] = []
#outList 4
outDict['icu-pat-moved-mean'] = []
outDict['icu-pat-moved-s'] = []
outDict['icu-pat-moved-sd'] = []
outDict['icu-pat-moved-ci'] = []
#outList 5
outDict['recovery-pat-moved-mean'] = []
outDict['recovery-pat-moved-s'] = []
outDict['recovery-pat-moved-sd'] = []
outDict['recovery-pat-moved-ci'] = []
#outList 6
outDict['pat-discharged-mean'] = []
outDict['pat-discharged-s'] = []
outDict['pat-discharged-sd'] = []
outDict['pat-discharged-ci'] = []
#outList 7
outDict['pat-died-mean'] = []
outDict['pat-died-s'] = []
outDict['pat-died-sd'] = []
outDict['pat-died-ci'] = []
#outList 8
outDict['em-capacity-mean'] = []
outDict['em-capacity-s'] = []
outDict['em-capacity-sd'] = []
outDict['em-capacity-ci'] = []
#outList 9
outDict['em-available-mean'] = []
outDict['em-available-s'] = []
outDict['em-available-sd'] = []
outDict['em-available-ci'] = []
#outList 10 em occupancy%

#outList 11
outDict['emr-capacity-mean'] = []
outDict['emr-capacity-s'] = []
outDict['emr-capacity-sd'] = []
outDict['emr-capacity-ci'] = []
#outList 12
outDict['emr-available-mean'] = []
outDict['emr-available-s'] = []
outDict['emr-available-sd'] = []
outDict['emr-available-ci'] = []
#outList 13 emr occupancy%

#outList 14
outDict['el-capacity-mean'] = []
outDict['el-capacity-s'] = []
outDict['el-capacity-sd'] = []
outDict['el-capacity-ci'] = []
#outList 15
outDict['el-available-mean'] = []
outDict['el-available-s'] = []
outDict['el-available-sd'] = []
outDict['el-available-ci'] = []
#outList 16 el occupancy%

#outList 17
outDict['elr-capacity-mean'] = []
outDict['elr-capacity-s'] = []
outDict['elr-capacity-sd'] = []
outDict['elr-capacity-ci'] = []
#outList 18
outDict['elr-available-mean'] = []
outDict['elr-available-s'] = []
outDict['elr-available-sd'] = []
outDict['elr-available-ci'] = []
#outList 19 elr occupancy%
#outList 20
outDict['c-capacity-mean'] = []
outDict['c-capacity-s'] = []
outDict['c-capacity-sd'] = []
outDict['c-capacity-ci'] = []
#outList 21
outDict['c-available-mean'] = []
outDict['c-available-s'] = []
outDict['c-available-sd'] = []
outDict['c-available-ci'] = []
#outList 22 c occupancy%
#outList 23
outDict['cr-capacity-mean'] = []
outDict['cr-capacity-s'] = []
outDict['cr-capacity-sd'] = []
outDict['cr-capacity-ci'] = []
#outList 24
outDict['cr-available-mean'] = []
outDict['cr-available-s'] = []
outDict['cr-available-sd'] = []
outDict['cr-available-ci'] = []

#outList 25 cr occupancy%
#>=27 individual zones type / available / occupancy % in utils

## idx: days / count: replication / value: from updates / mean, s, sd, ci: from dictionary 
#Welford’s algorithm
def wStats(idx, count, value, dictKey):
    if count==1:
       outDict[dictKey + '-mean'].append(value)
       outDict[dictKey + '-s'].append(0)
       outDict[dictKey + '-sd'].append(0)
       outDict[dictKey + '-ci'].append(0)
    elif count > 1:
       meanOld = outDict[dictKey + '-mean'][idx]
       outDict[dictKey + '-mean'][idx] = outDict[dictKey + '-mean'][idx] + (value-outDict[dictKey + '-mean'][idx])/count
       outDict[dictKey + '-s'][idx] = outDict[dictKey + '-s'][idx] + (value - outDict[dictKey + '-mean'][idx])*(value - meanOld)
       variance = outDict[dictKey + '-s'][idx]/(count - 1) 
       outDict[dictKey + '-sd'][idx] = math.sqrt(variance)
       outDict[dictKey + '-ci'][idx] = 1.96*outDict[dictKey + '-sd'][idx]/math.sqrt(count) 

#outList 0
def daysStats(idx, count, value):
    wStats(idx, count, value, 'day')
#outList 1      
def emArrivalsStats(idx, count, value):
    wStats(idx, count, value, 'emArrivals')
#outList 2    
def elArrivalsStats(idx, count, value):
    wStats(idx, count, value, 'elArrivals')
#outList 3        
def cArrivalsStats(idx, count, value):
    wStats(idx, count, value, 'cArrivals')
#outList 4        
def icuPatMovedStats(idx, count, value):
    wStats(idx, count, value, 'icu-pat-moved')
#outList 5        
def recoveryPatMovedStats(idx, count, value):
    wStats(idx, count, value, 'recovery-pat-moved')
#outList 6
def patDischargedStats(idx, count, value):
    wStats(idx, count, value, 'pat-discharged')
#outList 7
def patDiedStats(idx, count, value):
    wStats(idx, count, value, 'pat-died')
#outList 8
def emCapacityStats(idx, count, value):
    wStats(idx, count, value, 'em-capacity')
#outList 9
def emAvailableStats(idx, count, value):
    wStats(idx, count, value, 'em-available')
#outList 10 em occupancy%
#######
#outList 11
def emrCapacityStats(idx, count, value):
    wStats(idx, count, value, 'emr-capacity')
#outList 12
def emrAvailableStats(idx, count, value):
    wStats(idx, count, value, 'emr-available')
#outList 13 emr occupancy%
#######
#outList 14
def elCapacityStats(idx, count, value):
    wStats(idx, count, value, 'el-capacity')
#outList 15
def elAvailableStats(idx, count, value):
    wStats(idx, count, value, 'el-available')
#outList 16 el occupancy%
#######
#outList 17
def elrCapacityStats(idx, count, value):
    wStats(idx, count, value, 'elr-capacity')
#outList 18
def elrAvailableStats(idx, count, value):
    wStats(idx, count, value, 'elr-available')
#outList 19 elr occupancy%
#outList 20
def cCapacityStats(idx, count, value):
    wStats(idx, count, value, 'c-capacity')
#outList 21
def cAvailableStats(idx, count, value):
    wStats(idx, count, value, 'c-available')
#outList 22 c occupancy%
#######
#outList 23
def crCapacityStats(idx, count, value):
    wStats(idx, count, value, 'cr-capacity')
#outList 24
def crAvailableStats(idx, count, value):
    wStats(idx, count, value, 'cr-available')
#outList 25 cr occupancy%
#######
#outList 26 c 7-day avg occupancy%
#######
#outList >=27
def zoneStats(idx, count, value, zoneId):
    s = 'zone%s-type' %zoneId
    wStats(idx, count, value, s)
def zoneAvalableStats(idx, count, value, zoneId):
    wStats(idx, count, value, 'zone%s-available' %zoneId)




