# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 10:39:20 2021

@author: anastasia anagnostou
"""

"""
pID       -- patient ID is a unique identifier for the patient and is initialised when the instance is created
pType     -- patient type can take three values as follows:
              1: emergency (EM)
              3: elective (EL)
              5: covid (C)
pNextWard -- the ward that the patient will be moved next

Patient type and next ward are initialised as per the input parameters (emergency, elective and covid arrivals). 
At initialisation, patient next ward is the same as patient type indicating that the patient requires an ICU bed 
in EM, EL and C repsectively. After ICU treatment the patient can move to the repsective recovery wards (2 - EMR, 4 - ELR, 6 - CR). 
"""


class Patient:
    
    def __init__(self, env, pID, pType, pNextWard, pArrivedTime, pICULoS, pRecoveryLoS, pICUMortality,\
                 pRecoveryMortality, pDiedTime, pDischargedTime, pMovedTime):
        self.env = env
        self.pID = pID
        self.pType = pType
        self.pNextWard = pNextWard
        self.pArrivedTime = pArrivedTime
        self.pICULoS = pICULoS
        self.pRecoveryLoS = pRecoveryLoS
        self.pICUMortality = pICUMortality
        self.pRecoveryMortality = pRecoveryMortality
        self.pDiedTime = pDiedTime
        self.pDischargedTime = pDischargedTime
        self.pMovedTime = pMovedTime

