# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 07:27:08 2021

@author: anastasia anagnostou
"""

import csv
import getopt
import sys

import stats as s

RANDOM_SEED = 4518651015
SIM_END = 0 # sim end in days 
OUT_HEADERS = []

# Input parameters
#triangular distribution parameters (min, max, mode)
distEmergencyArrivals = [None] * 3 
distElectiveArrivals = [None] * 3 
distEmergencyLoS = [None] * 3 
distEmergencyRecoveryLoS = [None] * 3 
distElectiveLoS = [None] * 3 
distElectiveRecoveryLoS = [None] * 3 
distCovidLoS = [None] * 3 
distCovidRecoveryLoS = [None] * 3 
#probability
probEmergencyMortality = 0 
probEmergencyRecoveryMortality = 0
probElectiveMortality = 0
probElectiveRecoveryMortality = 0
probCovidMortality = 0
probCovidRecoveryMortality = 0
#percentage
upThreshold = 0
loThreshold = 0
replications = 0

#read from files
cArrivals = []
zList = []


"""
OPTIONS arguments
"""
#variables to hold the input files
zonesFile = ""
paramsFile = ""
cArrivalsFile = ""

def args():
    argv = sys.argv[1:]
    try:
       options, args = getopt.getopt(argv, "z:p:c:", ["zonesFile =", "paramsFile=", "cArrivalsFile="])
    except:
       print("error")
       print('[Required arguments: -z ZONES.csv -p ICU_INPUT_PARAMS.csv -c DAILY_ARRIVALS.csv i.e. <zones filename> <input params filename> <daily covid arrivales filenema>]')
       sys.exit(2)
    if len(argv)==0:
       print("error")
       print('[Required arguments: -z ZONES.csv -p ICU_INPUT_PARAMS.csv -c DAILY_ARRIVALS.csv i.e. <zones filename> <input params filename> <daily covid arrivales filenema>]')
       sys.exit(2)
    else:
       for name, value in options:
          if name in ['-z', '--zonesFile']:
             global zonesFile
             zonesFile = value
          elif name in ['-p', '--paramsFile']:
             global paramsFile      
             paramsFile = value
          elif name in ['-c', '--cArrivalsFile']:
             global cArrivalsFile
             cArrivalsFile = value

"""
FILE UTILS
"""

def outHeadersList():
    OUT_HEADERS.append('DAY')                                  #0
    OUT_HEADERS.append('EM_ARRIVALS-daily')                    #1
    OUT_HEADERS.append('EL_ARRIVALS-daily')                    #2
    OUT_HEADERS.append('C+_ARRIVALS-daily')                    #3
    OUT_HEADERS.append('PATIENTS_MOVED_ICU-cumulative')        #4
    OUT_HEADERS.append('PATIENTS_MOVED_RECOVERY-cumulative')   #5
    OUT_HEADERS.append('PATIENTS_DISCHARGED-cumulative')       #6
    OUT_HEADERS.append('PATIENTS_DIED-cumulative')             #7
    OUT_HEADERS.append('EM_CAPACITY')                          #8
    OUT_HEADERS.append('EM_AVAILABLE')                         #9
    OUT_HEADERS.append('EM_OCCUPANCY (%)')                     #10
    OUT_HEADERS.append('EMR_CAPACITY')                         #11
    OUT_HEADERS.append('EMR_AVAILABLE')                        #12
    OUT_HEADERS.append('EMR_OCCUPANCY (%)')                    #13
    OUT_HEADERS.append('EL_CAPACITY')                          #14
    OUT_HEADERS.append('EL_AVAILABLE')                         #15
    OUT_HEADERS.append('EL_OCCUPANCY (%)')                     #16
    OUT_HEADERS.append('ELR_CAPACITY')                         #17
    OUT_HEADERS.append('ELR_AVAILABLE')                        #18
    OUT_HEADERS.append('ELR_OCCUPANCY (%)')                    #19
    OUT_HEADERS.append('C_CAPACITY')                           #20
    OUT_HEADERS.append('C_AVAILABLE')                          #21
    OUT_HEADERS.append('C_OCCUPANCY (%)')                      #22
    OUT_HEADERS.append('CR_CAPACITY')                          #23
    OUT_HEADERS.append('CR_AVAILABLE')                         #24
    OUT_HEADERS.append('CR_OCCUPANCY (%)')                     #25
    OUT_HEADERS.append('C_7DAYAVG_OCCUPANCY (%)')              #26
    
    #headers & dictionary for all zones -- size depends on user input 
    for i in range(len(zList)):
        z = zList[i][0]
        OUT_HEADERS.append('ZONE%s_TYPE' %z)
        OUT_HEADERS.append('ZONE%s_AVAILABLE' %z)
        OUT_HEADERS.append('ZONE%s_OCCUPANCY' %z)
        s.outDict['zone%s-type-mean' %z] = []
        s.outDict['zone%s-type-s' %z] = []
        s.outDict['zone%s-type-sd' %z] = []
        s.outDict['zone%s-type-ci' %z] = []
        s.outDict['zone%s-available-mean' %z] = []
        s.outDict['zone%s-available-s' %z] = []
        s.outDict['zone%s-available-sd' %z] = []
        s.outDict['zone%s-available-ci' %z] = []

def readZones():
    #with open('ZONES.csv') as csvfile:
    with open('./input/%s' %zonesFile) as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None) # skip header
        for row in reader:
            zList.append(row)
    
def readInputParams():
    #with open('ICU_INPUT_PARAMS.csv') as csvfile:
    with open('./input/%s' %paramsFile) as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the header
        for row in reader:
            global distEmergencyArrivals # 0:min, 1:max, 2:mode
            distEmergencyArrivals[0] = int(row[0])
            distEmergencyArrivals[1] = int(row[1])
            distEmergencyArrivals[2] = int(row[2])
            global distElectiveArrivals # 0:min, 1:max, 2:mode
            distElectiveArrivals[0] = int(row[3])
            distElectiveArrivals[1] = int(row[4])
            distElectiveArrivals[2] = int(row[5])
            global distEmergencyLoS # 0:min, 1:max, 2:mode
            distEmergencyLoS[0] = int(row[6])
            distEmergencyLoS[1] = int(row[7])
            distEmergencyLoS[2] = int(row[8])
            global distEmergencyRecoveryLoS # 0:min, 1:max, 2:mode
            distEmergencyRecoveryLoS[0] = int(row[9])
            distEmergencyRecoveryLoS[1] = int(row[10])
            distEmergencyRecoveryLoS[2] = int(row[11])
            global distElectiveLoS # 0:min, 1:max, 2:mode
            distElectiveLoS[0] = int(row[12])
            distElectiveLoS[1] = int(row[13])
            distElectiveLoS[2] = int(row[14])
            global distElectiveRecoveryLoS # 0:min, 1:max, 2:mode
            distElectiveRecoveryLoS[0] = int(row[15])
            distElectiveRecoveryLoS[1] = int(row[16])
            distElectiveRecoveryLoS[2] = int(row[17])
            global distCovidLoS # 0:min, 1:max, 2:mode
            distCovidLoS[0] = int(row[18])
            distCovidLoS[1] = int(row[19])
            distCovidLoS[2] = int(row[20])
            global distCovidRecoveryLoS # 0:min, 1:max, 2:mode
            distCovidRecoveryLoS[0] = int(row[21])
            distCovidRecoveryLoS[1] = int(row[22])
            distCovidRecoveryLoS[2] = int(row[23])
            global probEmergencyMortality
            probEmergencyMortality = float(row[24])
            global probEmergencyRecoveryMortality
            probEmergencyRecoveryMortality = float(row[25])
            global probElectiveMortality
            probElectiveMortality = float(row[26])
            global probElectiveRecoveryMortality
            probElectiveRecoveryMortality = float(row[27])
            global probCovidMortality
            probCovidMortality = float(row[28])
            global probCovidRecoveryMortality
            probCovidRecoveryMortality = float(row[29])
            global upThreshold
            upThreshold = int(row[30])
            global loThreshold
            loThreshold = int(row[31])
            global replications
            replications = int(row[32])

def readCArrivals():
    #with open('DAILY_ARRIVALS.csv') as csvfile:
    with open('./input/%s' %cArrivalsFile) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            cArrivals.append(int(row[2]))
    global SIM_END
    SIM_END = len(cArrivals)

def writeHeader(rep):
    with open('OUT_%d.csv' %rep, 'a') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\r')
        writer.writerow(OUT_HEADERS)
            
def writeOut(rep, ls):
    with open('OUT_%d.csv' %rep, 'a') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\r')
        writer.writerow(ls)

def writeStatsHeader():
    with open('./output/OUT_STATS.csv', 'w+') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\r')
        writer.writerow(s.outDict)

def writeStatsOut(idx):
    values = s.outDict. values()
    values_list = list(values)
    row_values_list = []
    for i in range(len(values_list)):
        row_values_list.append(values_list[i][idx])
    with open('./output/OUT_STATS.csv', 'a+') as csvfile:
        writer = csv.writer(csvfile, lineterminator='\r')
        writer.writerow(row_values_list)

def clearOut(rep):
    with open('OUT_%d.csv' %rep, 'w+') as csvfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(csvfile, lineterminator='\r')
        for row in reader:
           writer. writerow()   
           
def clearStatsOut():
    with open('./output/OUT_STATS.csv', 'w+') as csvfile:
        reader = csv.reader(csvfile)
        writer = csv.writer(csvfile, lineterminator='\r')
        for row in reader:
           writer. writerow()   

