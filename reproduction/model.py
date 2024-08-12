# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 11:35:01 2021

@author: anastasia anagnostou
"""

import itertools
import random
import utils as u
import resource as r 
import patient as p
import stats as s

import simpy

emPatientArrivedList = [] # List to hold emergency patient objects that arrive in the system
elPatientArrivedList = [] # List to hold elective patient objects that arrive in teh system
cPatientArrivedList = [] # List to hold covid patient object that arrive in the system

# pid: patient ID is increamentally assigned to patients upon arrival -- in patient generators
pid = 0
def patientId():
    global pid
    pid += 1

icuPatientMovedList = [] # List to hold patient objects that were moved due to bed unavailability in ICU
recoveryPatientMovedList = [] # List to hold patient objects that were moved due to bed unavailability in recovery
patientDischargedList = [] # List to hold patient objects that were discharged after recovery
patientDiedList = [] # List to hold patient objects that died
zBedResourcesList = [] # List to hold bed resource objects -- rid is the id of the resource and doesn't change --rtype is the type of the resource and changes when wards are reconfigured

outList = [] # List to hold the outputs -- idx 0-25 + zones * 3

def initialiseOutList():
    u.outHeadersList()
    for i in range(len(u.OUT_HEADERS)):
        outList.append(0)

def reset():
    emPatientArrivedList.clear()
    elPatientArrivedList.clear()
    cPatientArrivedList.clear()
    global pid
    pid = 0
    icuPatientMovedList.clear()
    recoveryPatientMovedList.clear()
    patientDischargedList.clear()
    patientDiedList.clear()
    zBedResourcesList.clear()
    

"""
Write to the output file
"""            
def recordOut(env, rep: int):
    while True:
       outList[0] = env.now
       #idx 1, 2, 3 EM EL and C arrivals are updated in the respective patient generators 
       outList[4] = len(icuPatientMovedList)
       outList[5] = len(recoveryPatientMovedList)
       outList[6] = len(patientDischargedList)
       outList[7] = len(patientDiedList)
       #idx 8-25 zone related outputs total per type
       zoneTotal()
       outList[26] = calculate7DayAvg(env)
       #idx 27-29 ++ zone related outputs per zone id (number)
       zone(rep)       
      
       #######
       #update stats dictionaries
       #idx: days -- outList[0], count: rep, value: outList[x]
       
       s.daysStats(outList[0], rep, outList[0])
       s.emArrivalsStats(outList[0], rep, outList[1])
       s.elArrivalsStats(outList[0], rep, outList[2])
       s.cArrivalsStats(outList[0], rep, outList[3])
       s.icuPatMovedStats(outList[0], rep, outList[4])
       s.recoveryPatMovedStats(outList[0], rep, outList[5])
       s.patDischargedStats(outList[0], rep, outList[6])
       s.patDiedStats(outList[0], rep, outList[7])
       s.emCapacityStats(outList[0], rep, outList[8])
       s.emAvailableStats(outList[0], rep, outList[9])
       #10 emoccupancy %
       s.emrCapacityStats(outList[0], rep, outList[11])
       s.emrAvailableStats(outList[0], rep, outList[12])
       #13 emroccupancy %
       s.elCapacityStats(outList[0], rep, outList[14])
       s.elAvailableStats(outList[0], rep, outList[15])
       #16 eloccupancy %
       s.elrCapacityStats(outList[0], rep, outList[17])
       s.elrAvailableStats(outList[0], rep, outList[18])
       #19 elroccupancy %
       s.cCapacityStats(outList[0], rep, outList[20])
       s.cAvailableStats(outList[0], rep, outList[21])
       #22 c occupancy%
       s.crCapacityStats(outList[0], rep, outList[23])
       s.crAvailableStats(outList[0], rep, outList[24])
       #25 cr occupancy%
       #26 7 day avg c occupancy 
       #>=27 individual zones type / available beds / bed occupancy %

       #u.writeOut(rep, outList)

       u.writeStatsOut(outList[0])
       yield env.timeout(1)

"""
Resources --- capacity - beds available - occupancy 
"""
daysCOccupancy = []

def zoneTotal():
     for i in range(8, 26):
         outList[i] = 0

     for i in range(len(zBedResourcesList)):
         if  zBedResourcesList[i].rtype == 1:
             outList[8] += zBedResourcesList[i].capacity
             outList[9] += bedsAvailable(zBedResourcesList[i])
         elif  zBedResourcesList[i].rtype == 2:
             outList[11] += zBedResourcesList[i].capacity
             outList[12] += bedsAvailable(zBedResourcesList[i])
         elif  zBedResourcesList[i].rtype == 3:
             outList[14] += zBedResourcesList[i].capacity
             outList[15] += bedsAvailable(zBedResourcesList[i])
         elif  zBedResourcesList[i].rtype == 4:
             outList[17] += zBedResourcesList[i].capacity
             outList[18] += bedsAvailable(zBedResourcesList[i])
         elif  zBedResourcesList[i].rtype == 5:
             outList[20] += zBedResourcesList[i].capacity
             outList[21] += bedsAvailable(zBedResourcesList[i])
         elif  zBedResourcesList[i].rtype == 6:
             outList[23] += zBedResourcesList[i].capacity
             outList[24] += bedsAvailable(zBedResourcesList[i])
         
     if outList[8] != 0:
         outList[10] = ((outList[8]-outList[9])/outList[8])*100
     else:
         outList[10] = 0
         
     if outList[11] != 0:
         outList[13] = ((outList[11]-outList[12])/outList[11])*100
     else:
         outList[13] = 0
     
     if outList[14] != 0:
         outList[16] = ((outList[14]-outList[15])/outList[14])*100
     else:
         outList[16] = 0
        
     if outList[17] != 0:
         outList[19] = ((outList[17]-outList[18])/outList[17])*100
     else:
         outList[19] = 0 
         
     if outList[20] != 0:
         outList[22] = ((outList[20]-outList[21])/outList[20])*100
     else:
         outList[22] = 0 
        
     if outList[23] != 0:
         outList[25] = ((outList[23]-outList[24])/outList[23])*100
     else:
         outList[25] = 0 
     
     daysCOccupancy.append(outList[22])
        
def zone(rep):
    j = 0
    for i in range(len(zBedResourcesList)):
        
        x = 27+j
        y = 28+j
        z = 29+j
     
        outList[x] = zBedResourcesList[i].rtype
        outList[y] = bedsAvailable(zBedResourcesList[i])
        if zBedResourcesList[i].capacity != 0:
            outList[z] = calculateCOccupancy(zBedResourcesList[i])
        else:
            outList[z] = 0
        rid = str(zBedResourcesList[i].rid)
        s.zoneStats(outList[0], rep, outList[x], rid)
        s.zoneAvalableStats(outList[0], rep, outList[y], rid)
    
        j +=3      

"""
zone check   
"""       

def calculate7DayAvg(env):
    
    if len(daysCOccupancy) > 6:
      a = 0
      result = 0
      for i in range(7):
          a += daysCOccupancy[env.now-i]
    else:
        a = 0
    result = a/7
    return result

def reconfigureZones(env):
    while True:
        if outList[26] >= u.upThreshold:
            for i in range(len(zBedResourcesList)):
                if  zBedResourcesList[i].rtype == 3:
                    if zBedResourcesList[i].capacity > 0:
                        zBedResourcesList[i].setRtype(5)
                        break
                    elif zBedResourcesList[i].rtype == 1:
                        if zBedResourcesList[i].capacity > 0:
                           zBedResourcesList[i].setRtype(5)
                           break
        if outList[26] <= u.loThreshold:
            for i in range(len(zBedResourcesList)):
               if zBedResourcesList[i].rtype == 5:
                   for j in range(len(u.zList)):
                       if int(zBedResourcesList[i].rid) == int(u.zList[j][0]):
                            if int(u.zList[j][1]) == 1:
                               zBedResourcesList[i].setRtype(1)
                               break
                            elif int(u.zList[j][1]) == 3:
                               zBedResourcesList[i].setRtype(3)
                               break
        yield env.timeout(1)

"""
GENERATE PATIENTS -- daily arrivals
"""

"""
Generate emergency patient arrivals
"""

def emPatientGenerator(env):
    for i in itertools.count():
        gen1 = int(random.triangular(u.distEmergencyArrivals[0], u.distEmergencyArrivals[1], \
               u.distEmergencyArrivals[2]))
        outList[1] = gen1
        if gen1 != 0:
            for j in range(gen1):
                ICULoS = random.triangular(u.distEmergencyLoS[0], u.distEmergencyLoS[1], \
                         u.distEmergencyLoS[2])
                recoveryLoS = random.triangular(u.distEmergencyRecoveryLoS[0], \
                              u.distEmergencyRecoveryLoS[1], u.distEmergencyRecoveryLoS[2])
                ICUmortality = u.probEmergencyMortality
                recoveryMortality = u.probEmergencyRecoveryMortality
                patientId()
                p1 = p.Patient(env, pid, '1', '1', env.now, ICULoS, recoveryLoS, \
                               ICUmortality, recoveryMortality, -1, -1, -1)
                emPatientArrivedList.append(p1)
                env.process(admissionProcess(env, p1))
        yield env.timeout(1)

"""
Generate elective patient arrivals
"""

def elPatientGenerator(env):
    for i in itertools.count():
        gen1 = int(random.triangular(u.distElectiveArrivals[0], u.distElectiveArrivals[1], \
               u.distElectiveArrivals[2]))
        outList[2] = gen1
        if gen1 != 0:
            for j in range(gen1):
                ICULoS = random.triangular(u.distElectiveLoS[0], u.distElectiveLoS[1], \
                         u.distElectiveLoS[2])
                recoveryLoS = random.triangular(u.distElectiveRecoveryLoS[0], \
                              u.distElectiveRecoveryLoS[1], u.distElectiveRecoveryLoS[2])
                ICUmortality = u.probElectiveMortality
                recoveryMortality = u.probElectiveRecoveryMortality
                patientId()
                p1 = p.Patient(env, pid, '3', '3', env.now, ICULoS, recoveryLoS, \
                               ICUmortality, recoveryMortality, -1, -1, -1)
                elPatientArrivedList.append(p1)
                env.process(admissionProcess(env, p1))
        yield env.timeout(1)

"""
Generate Covid patient arrivals
"""

def cPatientGenerator(env):
     for i in itertools.count():
        gen = u.cArrivals[i]
        outList[3] = gen
        if gen != 0:
            for j in range(gen):
                ICULoS = random.triangular(u.distCovidLoS[0], u.distCovidLoS[1], u.distCovidLoS[2])
                recoveryLoS = random.triangular(u.distCovidRecoveryLoS[0], \
                              u.distCovidRecoveryLoS[1], u.distCovidRecoveryLoS[2])
                ICUmortality = u.probCovidMortality
                recoveryMortality = u.probCovidRecoveryMortality
                patientId()
                p1 = p.Patient(env, pid, '5', '5', env.now, ICULoS, recoveryLoS, \
                               ICUmortality, recoveryMortality, -1, -1, -1)
                cPatientArrivedList.append(p1)
                env.process(admissionProcess(env, p1))
        yield env.timeout(1)

"""
Create bed resources
"""

## Create bed resources for each zone

def createResources(env):
    for i in range(len(u.zList)):
        bedsInZones = r.IdResource(env, int(u.zList[i][2]), int(u.zList[i][0]), int(u.zList[i][1]))
        zBedResourcesList.append(bedsInZones)
            
def bedsAvailable(rsc: r.IdResource):
    return (rsc.capacity - rsc.count)

def calculateCOccupancy(rsc: r.IdResource):
    return ((rsc.count/rsc.capacity)*100)     

"""
Upon patient arrival, check available beds and move patients to wards or remove from systems (move to other hospital)
"""

def admissionProcess (env, pat: p.Patient):
    for i in range(len(zBedResourcesList)):
        if (int(zBedResourcesList[i].rtype) == int(pat.pNextWard)) and \
            ((zBedResourcesList[i].capacity - zBedResourcesList[i].count) > 0) and \
                (int(pat.pNextWard) == 1 or int(pat.pNextWard) == 3 or int(pat.pNextWard) == 5):
            with zBedResourcesList[i].request() as req:  
                    yield req
                    pat.pNextWard = int(pat.pType) + 1
                    yield env.timeout(pat.pICULoS) 
            if (int(pat.pNextWard) == 2 or int(pat.pNextWard) == 4 or int(pat.pNextWard) == 6) and \
                (pat.pICUMortality > random.uniform(0, 1) and pat.pDiedTime <0):
               pat.pDiedTime = env.now
               patientDiedList.append(pat)
        elif ((int(pat.pDiedTime) < 0) and int(zBedResourcesList[i].rtype) == int(pat.pNextWard)) and \
            ((zBedResourcesList[i].capacity - zBedResourcesList[i].count) > 0) and \
                (int(pat.pNextWard) == 2 or int(pat.pNextWard) == 4 or int(pat.pNextWard) == 6):
            with zBedResourcesList[i].request() as req:  
                    yield req
                    pat.pNextWard = 0
                    yield env.timeout(pat.pRecoveryLoS) 
            if int(pat.pNextWard) == 0 and pat.pRecoveryMortality > random.uniform(0, 1) and \
                pat.pDiedTime < 0:
                  pat.pDiedTime = env.now
                  patientDiedList.append(pat)
            elif int(pat.pDiedTime < 0) and int(pat.pDischargedTime < 0) and int(pat.pNextWard) == 0:
                  pat.pDischargedTime = env.now
                  patientDischargedList.append(pat)
        elif i == len(zBedResourcesList)-1 and int(pat.pDiedTime) < 0 and int(pat.pDischargedTime < 0):
            pat.pMovedTime = env.now
            if  (int(pat.pNextWard) == 1 or int(pat.pNextWard) == 3 or int(pat.pNextWard) == 5):
                icuPatientMovedList.append(pat)
            elif (int(pat.pNextWard) == 2 or int(pat.pNextWard) == 4 or int(pat.pNextWard) == 6):    
                recoveryPatientMovedList.append(pat)
        
"""
RUN THE SIMULATION 
"""

def runSim(randomSeed: int, replications: int):
    random.seed(randomSeed)
    u.readCArrivals()
    u.readInputParams()
    u.readZones()
    initialiseOutList()
    replications = u.replications

    for i in range(replications):
       print("Replication ", i+1, "out of ", replications) 
       rs = int(random.uniform(0, 1)*randomSeed)
       reset()

       u.clearStatsOut()
       u.writeStatsHeader()
    
       random.seed(rs)

       env = simpy.Environment()
       createResources(env)

       env.process(reconfigureZones(env))
       env.process(emPatientGenerator(env))
       env.process(elPatientGenerator(env))
       env.process(cPatientGenerator(env))
       env.process(recordOut(env, i+1))
            
       env.run(u.SIM_END)


