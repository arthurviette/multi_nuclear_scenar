#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 11:30:28 2018

@author: Arthur
"""

#-------------------------------------------------------------------#
# Code for Multidisciplinary Nuclear Scenarios Simulations (CMNSS)  #
# Version 0.1 - 12/17/18                                            #
# Tom Verrier, Romain Pic, Aymeric Delon, Arthur Viette             #
# ENS Paris-Saclay                                                  #
#-------------------------------------------------------------------#

# HYP 1: le type de reacteurs deploye n'est influence par aucun parametre 
# de sociologie 

from matplotlib import pyplot as plt

#----------------------------------------------------------------------------#
duration=60
step=0.25
n_step=int(duration/step)
T=[]

for i in range(n_step+1):
    T.append(i*step)

power_UOx=1. #GWe    
#----------------------------------------------------------------------------#
# Sociology 

# definir une evolution temporelle pour les grandeurs suivantes :
# social movement mobilization (SOC) 
# political allies (POL)
# state-industry relationship (SIR)
# arena shift (ANS)
# focusion event (FOC) 

# a la fin de cette partie, 8 tableaux : t + SOC,POL,SIR,ANS,FOC 
# + policyChange qui donne a partir des 5 gdeurs la "quantite de changement"
# + pNuc la puissance nuc demandee

# hyp : pNuc(t+step)=pNuc(t)*(1-policyChange(t-decisionTime))

soc=[]
pol=[]
sir=[]
ans=[]
foc=[]

P_0=60 # puissance initiale en GWe

policyChange=[]
pNuc=[P_0]
pNuc_react=[60]

decisionTime=0

# Strategie 1 : pas de changement
#def funcSoc(t):
#    return(0)
#    
#def funcPol(t):
#    return(0)
#    
#def funcSir(t):
#    return(0)
#    
#def funcAns(t):
#    return(0)
#    
#def funcFoc(t):    
#    return(0)
    
# Strategie 2 : social movement et political allies apres 20 ans, accident
# entre 10 et 10,5 ans   
# /!\ modifie pour l'exemple ... 
    
def funcSoc(t):
    
    if t<20:
        return(0)
    else : 
        return(1)
    
def funcPol(t):
    
    if t<20:
        return(0)
    else : 
        return(1)
    
def funcSir(t):
    
    return(0)
    
def funcAns(t):
    
    return(0)
    
def funcFoc(t):
    
    if t<10 :    
        return(0)
    elif t>=10 and t<=10.5 : # simule un accident
        return(0.2)
    elif t>=15 and t<=15.5 : # simule un accident
        return(0.2)
    else : 
        return(0)
    
inputCLASS_nUOx=open('inputCLASS_nUOx.txt','w')
        
for i in range(len(T)-1):
    
    soc.append(funcSoc(i*step))
    pol.append(funcPol(i*step))
    sir.append(funcSir(i*step))
    ans.append(funcAns(i*step))
    foc.append(funcFoc(i*step))
    
    policyChange.append((1*soc[-1]+1*pol[-1]+1*sir[-1]+1*ans[-1]+1*foc[-1])/5)

    pNuc.append(pNuc[-1]*(1-policyChange[-1-decisionTime]))
    pNuc_react.append(int(pNuc[-1]//power_UOx)*power_UOx)
    
    
    inputCLASS_nUOx.write(str(int(pNuc[-1]//power_UOx))+'\n' )
    
inputCLASS_nUOx.close()    
    
plt.plot(T,pNuc)
plt.plot(T,pNuc_react)
plt.xlabel('time(year)')
plt.ylabel('pNuc (GWe)')
plt.title('Nuclear power demand versus time')
plt.show()


# /!\ reprendre la discretisation de la puissance demandee


#----------------------------------------------------------------------------#
# Physics 

# cette partie redige un script C++ pour CLASS qui modifie le scenario en
# faisant evoluer la puissance demandee au cours du temps (en ouvrant/fermant)
# des REP en restant toujours >=
# + differentes strategies : 
# S1 : que des REP UOx
# S2 : REP UOx et REP MOx
# S3 : S1 puis RNR
# S4 : S2 puis RNR
#
# chacune declinee en Sn(E,typeGestion,BUmax) 
# avec E = enrichissement max 
# et typeGestion=LIFO/FIFO
# et BUmax le Burn-Up final des réacteurs (libre si non renseigne)
#
# puis appel CLASS, stocke les resultats avec qte tot dechets
# puis pour chaque strategie, execute SMURE pour calculer le alpha_rho max
# de chacune 

data_CLASS=open('data_CLASS.txt','w')

# faire ça avec une boucle
data_CLASS.write('S     E      typeGestion      BUmax  \n')
data_CLASS.write('1     15          1              58')

data_CLASS.close()

#----------------------------------------------------------------------------#
# Economics 

# pour chaque strategie, appel de FLORE pour evaluer le regret de chacune 
# ainsi que la trajectoire optimale sachant le "contexte social"
# et stocke les resultats
#
# donne aussi cost(Strategy) le cout total estime pour suivre Strategy
# qui comprend Uranium, assurances, constructions centrales, etc. 



#----------------------------------------------------------------------------#
# Data Processing

# script pour tracer tous les tableaux en fonction du temps, et d'autres 
# comme alpha_rho_max(policyChangeTot) ou cost(policyChangeTot)
# affiche aussi la trajectoire optimale, avec les incertitudes 
