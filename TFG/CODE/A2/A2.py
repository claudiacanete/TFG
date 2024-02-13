# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 11:45:06 2022

@author: claud
"""

import pandas as pd
import numpy as np 
import random
import math
import shutil
import time
from datetime import datetime


def IG1LS():
    
    global descanso, dispcons, dia, hcor, hcc, numc, numor, horasq, wt,we,wc,wu,ctor, ctcc, cirujanos, asistentesor, cirjasocPAE, cirjasocOR, cirujanosconsultas, cirujanosor, ctconsultas, ctor, pacientes, pacientesaborrar, pacientesconsultas, pacientesor, tiempoacum
    global listaciruj, listaasist, listapacs
    global sumaFO, eficienciaconsultas, eficienciaor, estadooriginal, pacientesoriginales
    
    def insertar(lista,pos1,pos2):
        copia=lista.copy()
        a=copia.pop(pos1)
        copia.insert(pos2,a)
        return copia
        
    def mejora(v1probando,v2best):
        if v1probando[3]<v2best[3]:
            return True
        else:
            return False
        
    def nivelar(patients,surgeons):
        
        j=min(numc-1,len(surgeons)-1)
        while j>=0:
            if patients[j]==[] and dispcons[j][dia]>0:
                surgeons.pop(j)
                patients.pop(j)
                surgeons.insert(numc-1,[])
                patients.insert(numc-1,[])
            if dispcons[j][dia]==0:
                patients[j]=[]
                surgeons[j]=[]
            j=j-1
        return surgeons

    def destruction(sequence):#la secuencia que se le pasará será secbest
        n=random.sample(sequence,4)#número de elementos que destruiremos de nuestra secuencia
        # print(n)
        a=0
        secborrar=sequence[:]
        while a<len(n):
            secborrar.remove(n[a])
            a=a+1
        return secborrar, n
    def construction(seqbest,n): #para secuenncia
        seqprobando=seqbest[:]
        a=0
        while a<len(n):
            seqprobando=seqbest[:]
            seqprobando.insert(0,n[a])#proponemos que la mejor secuencia de la fase es la primera, para luego ir tomando las que la mejoren
            seqbest=seqprobando[:]
            global hcc, hcor
            hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
            hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
            FObest=cajanegrasecuencia(seqbest)
            hcc=hcccopia.copy()#para que las pruebas no alteren el real
            hcor=hcorcopia.copy()
            # print('la primera secuencia es', secbest, FObest[1])
            seqprobando.pop(0)
            ###PROBANDO PARA NO INSERTAR DOS VECES EL MISMO NOMBRE###
            b=1
            while b<len(seqbest):
               # print('i',i)
               seqprobando.insert(b, n[a])
               # print('secuencia probando, insertamos en la posición', secprobando,i)
               hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
               hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
               FOprobando=cajanegrasecuencia(seqprobando)
               hcc=hcccopia.copy()#para que las pruebas no alteren el real
               hcor=hcorcopia.copy()
               
               # print('FO=',FOprobando[1])
               if mejora(FOprobando,FObest):
                   # print('mejora')
                   seqbest=seqprobando[:]
                   FObest=FOprobando[:]
                #no se ha añadido ningún número a la secuencia y terminamos el bucle
               seqprobando.pop(b)
               b=b+1
            a=a+1
        return seqbest

    def destruccion(cirujanosconsults): #para asignacion cirujanos a consultas
        n=random.sample(cirujanosconsults,4)
        a=0
        ccborrar=cirujanosconsults[:]
        while a<len(n):
            ccborrar.remove(n[a])
            a=a+1
        return ccborrar, n

    def construccion(ccmejor,n): #para asignacion cirujanos a consultas
        global hcc, hcor    
        ccprobando=ccmejor[:]
        a=0
        while a<len(n):
            ccprobando=ccmejor[:]
            ccprobando.append(n[a])
            ccmejor=ccprobando[:]
            
            hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
            hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
            FObest=cajanegra(pibest,ccmejor)
            hcc=hcccopia.copy()#para que las pruebas no alteren el real
            hcor=hcorcopia.copy()
            
            ccprobando.pop(-1)
            b=0
            while b<len(ccmejor):
                ccprobando.insert(b,n[a])
                
                hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
                hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
                FOprobando=cajanegra(pibest,ccprobando)
                hcc=hcccopia.copy()#para que las pruebas no alteren el real
                hcor=hcorcopia.copy()
                
                if mejora(FOprobando,FObest):
                    # print('mejora')
                    ccmejor=ccprobando[:]
                    FObest=FOprobando[:]
                ccprobando.pop(b)
                b=b+1
            a=a+1
        return ccmejor


    def leerexcel():
            global datospacientes, horasq, pacientes, cirjasoc, dp, trp, dq, trq, u, hp, hs, dc, trc, pesos, estado, cirjasocPAE, cirjasocOR, tiempoacum, datoscirujanos, cirujanos, exp, uc
            global estadooriginal, pacientesoriginales
            datospacientes=pd.read_csv('pacientes.csv',sep=';',header=None).to_numpy()
            pacientes=pd.read_csv('pacientes.csv',sep=';',header=None,usecols=[0]).to_numpy()
            pacientes=list(str(x) for [x] in pacientes)
            # pacientesoriginales=pacientes.copy()
            dp=pd.read_csv('pacientes.csv',sep=';',header=None,usecols=[4]).to_numpy()
            dp=list(int(x) for [x] in dp)
            x=0
            while x<len(dp):
               dp[x]=float(dp[x]/60)
               x=x+1

            trp=pd.read_csv('pacientes.csv',sep=';',header=None,usecols=[11]).to_numpy()
            trp=list(int(x) for [x] in trp)
            dq=pd.read_csv('pacientes.csv',sep=';',decimal=',',header=None,usecols=[5]).to_numpy()
            dq=np.float_(dq)
            dq=list(float(x) for x in dq)
            x=0
            while x<len(dq):
               dq[x]=dq[x]*horasq
               x=x+1

            trq=pd.read_csv('pacientes.csv',sep=';',header=None,usecols=[12]).to_numpy()
            trq=list(int(x) for [x] in trq)

            u=pd.read_csv('pacientes.csv',sep=';',header=None,usecols=[1]).to_numpy()
            u=list(int(x) for [x] in u)

            hp=pd.read_csv('pacientes.csv',sep=';',header=None,usecols=[7]).to_numpy()
            hp=list(int(x) for [x] in hp)
            hs=pd.read_csv('pacientes.csv',sep=';',header=None,usecols=[8]).to_numpy()
            hs=list(int(x) for [x] in hs)

            dc=pd.read_csv('pacientes.csv',sep=';',header=None,usecols=[6]).to_numpy()
            dc=list(int(x) for [x] in dc)
            x=0
            while x<len(dc):
               dc[x]=float(dc[x]/60)
               x=x+1

            trc=pd.read_csv('pacientes.csv',sep=';',header=None,usecols=[13]).to_numpy()
            trc=list(int(x) for [x] in trc)

            pesos=pd.read_csv('pacientes.csv',sep=';',header=None,usecols=[2]).to_numpy()
            pesos=list(int(x) for [x] in pesos)
            estado=pd.read_csv('pacientes.csv',sep=';',header=None,usecols=[3]).to_numpy()
            estado=list(int(x) for [x] in estado)
            # estadooriginal=estado.copy()
            cirjasoc1 = datospacientes[0:,10]#cambiamos cuando no hay valores por 999
            for x in range(len(cirjasoc1)):
                if cirjasoc1[x]==0:
                    cirjasoc1[x]=999
                else:
                    cirjasoc1[x]=cirjasoc1[x]-1
            cirjasocPAE = [int(x) for x in cirjasoc1.tolist()]
            for x in range(len(cirjasocPAE)):
                if cirjasocPAE[x]==999:
                    cirjasocPAE[x]='NaN'       
            
            cirjasoc1 = datospacientes[0:,9]#cambiamos cuando no hay valores por 999

            for x in range(len(cirjasoc1)):
                if cirjasoc1[x]==0:
                    cirjasoc1[x]=999
                else:
                    cirjasoc1[x]=cirjasoc1[x]-1
            cirjasocOR = [int(x) for x in cirjasoc1.tolist()]
            for x in range(len(cirjasocOR)):
                if cirjasocOR[x]==999:
                    cirjasocOR[x]='NaN'
                    
            tiempoacump=pd.read_csv('pacientes.csv',sep=';',header=None,usecols=[14]).to_numpy()
            tiempoacumq=pd.read_csv('pacientes.csv',sep=';',header=None,usecols=[15]).to_numpy()
            tiempoacumc=pd.read_csv('pacientes.csv',sep=';',header=None,usecols=[16]).to_numpy()
            x=0
            while x<len(tiempoacump):
                if x==0:
                    tiempoacum=[int(tiempoacump[x]+tiempoacumc[x]+tiempoacumq[x])]
                else:
                    suma=int(tiempoacump[x]+tiempoacumc[x]+tiempoacumq[x])
                    tiempoacum.append(suma)
                x=x+1

    def cajanegra(secuencia,cc):
        
        global hcor, hcc, continuidad, numc, numor, horasq, wt,we,wc,wu,ctor, ctcc, cirujanos, asistentesor, cirjasocPAE, cirjasocOR, cirujanosor, ctconsultas, ctor, pacientes, pacientesaborrar, pacientesconsultas, pacientesor, tiempoacum
        global listaciruj, listaasist, listapacs
        def asignacion(secuencia,cc):
            global pacientesconsultas, pacientesor, cirujanosor, asistentesor, ctconsultas, ctor, hcor, hcc, continuidad
            pacientesconsultas = [[]]
            x=0
            while x<numc-1:
                pacientesconsultas.append([])
                x=x+1
            
            pacientesor = [[]]
            cirujanosor = [[]]
            asistentesor = [[]]
            x=0
            while x<numor-1:
                pacientesor.append([])
                cirujanosor.append([])
                asistentesor.append([])
                x=x+1
                
            global eq
            ###FUNCIONES###

            #Función que aporta la varianza de lo que los cirujanos llevan acumulados en consulta y en quirófano
                    #sirve para medir el equilibrio de la carga de trabajo#
            def equilibrio(hcc,hcor):
                return (hcc.var()+hcor.var())
                    
            #Función para ver cuántos pacientes sobrepasan actualmente su tiempo de respuesta, ponderado con los pesos
            def lateness(pacientes):
                global pesos
                x=0
                late=[]
                for x in range(len(pacientes)):
                    if estado[x]==1:
                        if tiempoacum[x]>trp[x]:
                            # print('el paciente {} va tarde a {}'.format(pacientes[x],estado[x]))
                            late.append((tiempoacum[x]-trp[x])*pesos[x])
                    if estado[x]==2:
                        if tiempoacum[x]>trq[x]:
                            # print('el paciente {} va tarde a {}'.format(pacientes[x],estado[x]))
                            late.append((tiempoacum[x]-trq[x])*pesos[x])
                    if estado[x]==3:
                        if tiempoacum[x]>trc[x]:
                            # print('el paciente {} va tarde a {}'.format(pacientes[x],estado[x]))
                            late.append((tiempoacum[x]-trc[x])*pesos[x])
                # print('Número de pacientes que van tarde:')
                return sum(late)  #late indica cuántos pacientes van con retraso actualmente
            
            #Función para comprobar si el cirujano está  asignado a algun OR o CONSULTA ese día
            def asignadodia(cirujano,consultaor):
                # global cirujanosconsultas
                global cirujanosor
                global numc
                i=0
                flag = 0
                if consultaor=='consulta':#comprobamos si el cirujano está asignado a alguna CONSULTA
                    for i in range(len(cc[:numc])):
                        if cirujano in cc[i]:#si el cirujano está en la consulta i, nos devuelve ese valor
                            return i
                            flag=1
                    if flag==0:
                        return 'NaN'
                        # print("El cirujano no está asignado a ninguna consulta el dia ",dia)
                elif consultaor == 'OR': #comprobamos si el cirujano está asignado a alguún QUIRÓFANO
                    for i in range(numor):
                        if (cirujano in cirujanosor[i]) or (cirujano in asistentesor[i]):#si el cirujano está en el OR j, nos devuelve ese valor
                            return i
                            flag=1
                    if flag==0:
                        return 'NaN'
                    
            #funcion para calcular el indice de un vector 
            def indice(vector,valor):
                x=0
                for x in range(len(vector)):
                    if vector[x]==valor:
                        return x
                        break
                    
            #Función para asignar un paciente y un cirujano a PAE (teniendo en cuenta que en la PAE sea necesario coincidir en unidades)
            def busquedaPAE (paciente):
                global cirujanos
                global numc, horasq
                global hcc
                j=0
                cirujanosdelaunidad = []#lista de cirujanos que pertenecen a la unidad del paciente
                while j<len(cirujanos):
                    if exp[j][u[paciente]-1]>0:#si el cirujano que estamos viendo es de la unidad
                        cirujanosdelaunidad.append(j)
                    j=j+1
                #ordenamos los cirujanosdelaunidad según las horas de consulta que lleven
                j=0
                horas=[]
                for j in range(len(cirujanosdelaunidad)):
                    horas.append(hcc[cirujanosdelaunidad[j]])
                horasnumpy=np.array(horas)
                cirujanosdelaunidadnumpy = np.array(cirujanosdelaunidad)
                np.argsort(horasnumpy)
                cirujanosdelaunidad = cirujanosdelaunidadnumpy[horasnumpy.argsort()].tolist()
                j=0
                flagyatieneconsulta=0#flag para ver si pasa por los bucles y no tiene consulta en toda la semana
                #para cada cirujano, miramos si está asignado a alguna consulta el dia
                while j<len(cirujanosdelaunidad):
                    
                    asignadoenconsulta = asignadodia(cirujanosdelaunidad[j],'consulta')
                    if asignadoenconsulta!='NaN' and dispcons[asignadoenconsulta][dia]>0 and consultas[asignadoenconsulta]!='General':#el cirujano sí está asignado a la consulta asignadoenconsulta
                        if u[paciente]-1==especialidades[asignadoenconsulta]:
                            if ctconsultas[asignadoenconsulta][-1]+dp[paciente]<=dispcons[asignadoenconsulta][dia]/60:#ponemos h de consulta al dia
                                return [asignadoenconsulta,cirujanosdelaunidad[j]]
                                flagyatieneconsulta=1
                                break                   
                    if flagyatieneconsulta==1:break
                    j=j+1
                if flagyatieneconsulta==0:
                    return 'NaN' #si el flag sigue, se ve que no hay hueco para la consulta PAE para este paciente en toda la semana                
                
            # Función para asignar un paciente y un cirujano a consulta postop 
            def busquedaPOSTOP (paciente):
                #se va pasando por cada día por cada consulta, viendo dónde tiene el cirujasoc consulta asignada y si hay hueco
                
                flagyatieneconsulta=0
                asignadoenconsulta=asignadodia(cirjasocOR[paciente],'consulta')
                asignadoenOR = asignadodia(cirjasocOR[paciente],'OR')
                if asignadoenconsulta!='NaN' and asignadoenOR=='NaN'  and descanso[cirjasocOR[paciente],dia]==0 and dispcons[asignadoenconsulta][dia]>0 and consultas[asignadoenconsulta]!='General':#el cirujano sí está asignado a la consulta asignadoenconsulta
                    if u[paciente]-1==especialidades[asignadoenconsulta]:
                        if ctconsultas[asignadoenconsulta][-1]+dc[paciente]<=dispcons[asignadoenconsulta][dia]/60:#ponemos h de consulta al dia
                            return [asignadoenconsulta,cirjasocOR[paciente]]
                            flagyatieneconsulta=1
                if flagyatieneconsulta==0:
                    return 'NaN' #si el flag sigue, se ve que no hay hueco para la consulta PAE para este paciente en toda la semana                
                    
            #Función para asignar un paciente y un equipo de cirujanos a quirófanos
            def busquedaOR(paciente):
                   #se hará igual que para la consulta PAE, solo que ahora deberá haber cirujano principal y asistente. SSe tendrán en cuenta
                    #la experiencia y nivel de dificultad de la  operación.
                j=0
                cirujanosexpunidad = []#lista de cirujanos que pertenecen a la unidad del paciente y que cuentan con experiencia suficiente
                while j<len(cirujanos):
                    if exp[j][u[paciente]-1]>0 and hp[paciente]<=exp[j][u[paciente]-1] and descanso[j,dia]==0 and [j] not in cc:#si el cirujano que estamos viendo es de la unidad y tiene experiencia suficiente
                        cirujanosexpunidad.append(cirujanos[j])
                    j=j+1
                #ordenamos los cirujanosdelaunidad según las horas de OR que lleven
                j=0
                horas=[]
                for j in range(len(cirujanosexpunidad)):
                    horas.append(hcor[cirujanosexpunidad[j]])
                horasnumpy=np.array(horas)
                cirujanosexpunidadnumpy = np.array(cirujanosexpunidad)
                np.argsort(horasnumpy)
                cirujanosexpunidad = cirujanosexpunidadnumpy[horasnumpy.argsort()].tolist()
                if cirjasocPAE[paciente] in cirujanosexpunidad:
                    cirujanosexpunidad.remove(cirjasocPAE[paciente])
                    cirujanosexpunidad.insert(0,cirjasocPAE[paciente])
                #esta lista es para asignar un CIRUJANO PRINCIPAL, tras asignar un cirujano principal, se asignará el asistente                
                
                ###LISTA ASISTENTES###
                j=0
                asistexp = []#lista de cirujanos que cuentan con experiencia suficiente, para los asists nose tiene en cuenta la unidad
                while j<len(cirujanos):
                    if hs[paciente]<=max(exp[j]) and descanso[j,dia]==0:#si el cirujano que estamos viendo  tiene experiencia suficiente
                        asistexp.append(cirujanos[j])
                        # print(asistexp)
                    j=j+1
                # print(asistexp)
                #ordenamos los asistentes según las horas de consulta que lleven
                j=0
                horas=[]
                for j in range(len(asistexp)):
                    # print('asistente',asistexp[j] )
                    horas.append(hcor[asistexp[j]])
                # print(horas)
                horasnumpy=np.array(horas)
                asistexpnumpy = np.array(asistexp)
                np.argsort(horasnumpy)
                asistexp = asistexpnumpy[horasnumpy.argsort()].tolist()
                # print('listaordenadaasist',asistexp)                
                
                if hs[paciente]==0:#si no necesitamos asistente, se haría con el mismo algoritmo de buscar consulta:
                     # print('No se necesita asistente')
                     j=0
                     
                     flagyatieneOR=0#flag para ver si pasa por los bucles y no tiene consulta en toda la semana
                     #para cada cirujano, miramos si está asignado a algún OR el dia
                     while j<len(cirujanosexpunidad):
                         asignadoenOR = asignadodia(cirujanosexpunidad[j],'OR')
                         # print(' ¿está el cirujano en algun OR el dia {} ?'.format(dia))
                         if asignadoenOR!='NaN':#el cirujano sí está asignado a la OR asignadoenOR
                             # print('si, está asignado en el OR {}'.format(asignadoenOR))
                             if ctor[asignadoenOR][-1]+dq[paciente]<=horasq:#ponemos horasqh de OR al dia
                                 # print('hay hueco en este OR')
                                 return [asignadoenOR,cirujanosexpunidad[j],'NaN']
                                 flagyatieneOR=1
                                 break
                         j=j+1
                     if flagyatieneOR==0:#si no tiene OR en toda la semana ningún cirujano, se le asigna al primero el primer hueco libre
                         # print('entra')
                         j=0
                         while j<numor:
                             # print('los cirujanos no tienen consulta asignada con hueco en la semana, así que se coge el primer hueco libre y se ve si algun ciruj puede')
                             if ctor[j][-1]==0 and dispq[j][dia]==1:#eL OR está libre, no tiene ninguna operación programada y está disponible
                                 x=0
                                 for x in cirujanosexpunidad:
                                     # print('probamos con el ciruj',x)
                                     # print('asignadodia',asignadodia(x, 'consulta'))
                                     # print('asignadodOR',asignadodia(x, 'OR'))
                                     if asignadodia(x,'consulta')=='NaN' and (asignadodia(x,'OR')=='NaN' or asignadodia(x,'OR')==j ) and [x] not in asistentesor:#si el cirujano no tiene consulta asignado ese día, puede asignarse a consultas
                                         # print('este ciruj SI puede')
                                         return [j,cirujanosexpunidad[0],'NaN']
                                         flagyatieneOR=1
                                         break#cuando se le asigna, se sale del for
                                 if flagyatieneOR==1:
                                     break   
                             j=j+1
                     if flagyatieneOR==0:
                         return 'NaN' #si el flag sigue, se ve que no hay hueco para la consulta PAE para este paciente en toda la semana
                else:   #sí se necesita un asistente
                    # print('si se necesita un asistente')
                    #vamos a buscar a la vez un cirujano principal y un asistente
                    i=0
                    flagyatieneasist=0
                    for i in cirujanosexpunidad:
                        # print('probamos con el ciruj {} el dia {}'.format(i,dia))
                        asignadoenOR = asignadodia(i,'OR')
                        # print('¿está asignado en algun OR ya?')
                        if asignadoenOR!='NaN':#el cirujano sí está asignado ese día en un quirófano
                            # print('si, esta en el OR',asignadoenOR)
                            if ctor[asignadoenOR][-1]+dq[paciente]<=horasq and [i]==cirujanosor[asignadoenOR]:#le asignamos este hueco en la consulta
                                # print('sí habría hueco en su OR')
                                if asistentesor[asignadoenOR]!=[]:
                                    if asistentesor[asignadoenOR][-1] in asistexp :
                                        return [asignadoenOR,i,asistentesor[asignadoenOR][-1]]
                                        flagyatieneasist=1  
                                if asistentesor[asignadoenOR]==[]:
                                    for k in asistexp:
                                        if asignadodia(k, 'OR')=='NaN' and asignadodia(k, 'consulta') == 'NaN' and k!=i:
                                            return [asignadoenOR, i, k]
                                            flagyatieneasist=1
                            if ctor[asignadoenOR][-1]+dq[paciente]<=horasq and [i]==asistentesor[asignadoenOR]:#le asignamos este hueco en la consulta
                                if cirujanosor[asignadoenOR][-1] in asistexp:
                                    return [asignadoenOR,cirujanosor[asignadoenOR][-1],i]
                                    flagyatieneasist=1
                        
                        if flagyatieneasist==1:break
                    if flagyatieneasist==0: #hemos probado todos los cirujanos pero no hay ninguno ya asignado a un OR durante la semana. Hay que buscarle nuevo hueco
                        #Vamos buscando un hueco para el primer cirujano, y vemos si tiene asistente posible. Si no hay asistente, se pasa al sig hueco
                        # print('no hay ciruj con OR asignado, probamos a buscar el primer hueco')
                        i=0
                        for i in cirujanosexpunidad:
                            asignadoenconsulta = asignadodia(i,'consulta')
                            # print('¿está asignado en consulta este ciruj ya?',asignadoenconsulta)
                            x=0
                            while x<numor:
                                # print('está ya asignado a un OR?',asignadodia(i,'OR'))
                                if asignadoenconsulta=='NaN' and (asignadodia(i,'OR')=='NaN' or asignadodia(i,'OR')==x ):#comprobamos que el ciruj no está en ninguna consulta ese día
                                    #print(ctor[dia][x][-1])
                                    if ctor[x][-1]==0 and dispq[x][dia]==1:#el OR está libre y disponible
                                    #buscamos un asistente
                                        # print('hay hueco')
                                        for k in asistexp:
                                            # print('probamos con el asist {}, cirujanos {}, asignado en consulta? {} asignado en OR? {}'.format(k,i,asignadodia(k,'consulta'),asignadodia(k,'OR')))
                                            if k!=i and asignadodia(k,'consulta')=='NaN' and (asignadodia(k,'OR')=='NaN' or asignadodia(k,'OR')==x ):
                                                # print('asistente disponible')
                                                #asiste!=cirujasoc  asist no puede estar en consultas ese dia    asist no puede estar asignado a otro OR que no sea este ese dia
                                                #si esta condicion se cumple, se asocia este asist 
                                                return [x,i,k]
                                                flagyatieneasist=1
                                                break  
                                if flagyatieneasist==1:break
                                x=x+1
                            if flagyatieneasist==1:break
                    if flagyatieneasist==0:
                        # print('NO HAY POSIBLE COMBINACION CIRUJANO ASISTENTE')
                        return'NaN' #si tras buscar todos los cirujanos posibles con todos los asistentes en todos los huecos el flag sigue a 0,
                        #significa que no hay hueco posible para este paciente en OR esta semana
                                               
            ###COMIENZO CODIGO###
          
            global pacientesaborrar
            pacientesaborrar=[]
            petapauno=0
            continuidad=0
            p=0
            while p<numc:
                if consultas[p]=='General' and dispcons[p][dia]>0:
                    hcc[cirujanosconsultas[p]]=hcc[cirujanosconsultas[p]]+dispcons[p][dia]/60
                    ctconsultas[p].append(dispcons[p][dia]/60)
                p=p+1
            for k in pacientes:
                if k not in secuencia:
                    tiempoacum[indice(pacientes,k)]=tiempoacum[indice(pacientes,k)]+1 #los pacientes que no estén en la sec, igualmente no se van a procesar y se les añade un día a su tiempo acum
                if estado[indice(pacientes,k)]==2:
                    petapauno=petapauno+1
            for k in range(len(secuencia)): #x es el indice del paciente
                # print(' se ve al paciente {}'.format(secuencia[k]))
                if estado[indice(pacientes,secuencia[k])]==1:
                    retorno=busquedaPAE(indice(pacientes,secuencia[k])) #[consulta,cirujprincipal]
                    if retorno!='NaN':
                        pacientesconsultas[retorno[0]].append(secuencia[k])
                        ctconsultas[retorno[0]].append(ctconsultas[retorno[0]][-1]+dp[indice(pacientes,secuencia[k])])
                        hcc[retorno[1]]=hcc[retorno[1]]+dp[indice(pacientes,secuencia[k])]
                        tiempoacum[indice(pacientes,secuencia[k])]=0#se pone el +1 porque el día 0 aumenta 1 día
                        cirjasocPAE[indice(pacientes,secuencia[k])]=retorno[1]
                        flagcambiado=1
                    else: 
                        flagcambiado=0
                        tiempoacum[indice(pacientes,secuencia[k])]=tiempoacum[indice(pacientes,secuencia[k])]+1
                if estado[indice(pacientes,secuencia[k])]==2:
                    retorno=busquedaOR(indice(pacientes,secuencia[k])) #me devuelve [consulta,cirujprincipal,asistente]
                    if retorno!='NaN':
                        if retorno[1]==cirjasocPAE[indice(pacientes,secuencia[k])]:
                            continuidad = continuidad+1
                        cirujanosor[retorno[0]]=[retorno[1]]
                        hcor[retorno[1]]=hcor[retorno[1]]+dq[indice(pacientes,secuencia[k])]
                        pacientesor[retorno[0]].append(secuencia[k])
                        ctor[retorno[0]].append(ctor[retorno[0]][-1]+dq[indice(pacientes,secuencia[k])])
                        cirjasocOR[indice(pacientes,secuencia[k])]=retorno[1]
                        tiempoacum[indice(pacientes,secuencia[k])]=0 #se actualiza el tiempo acumulado.
                        if retorno[2]!='NaN':
                            asistentesor[retorno[0]]=[retorno[2]]
                            hcor[retorno[2]]=hcor[retorno[2]]+dq[indice(pacientes,secuencia[k])]
                        flagcambiado=1
                    else: 
                        flagcambiado=0
                        tiempoacum[indice(pacientes,secuencia[k])]=tiempoacum[indice(pacientes,secuencia[k])]+1 #se actualiza el tiempo acumulado.
                if estado[indice(pacientes,secuencia[k])]==3:
                    retorno=busquedaPOSTOP(indice(pacientes,secuencia[k])) #me devuelve [consulta,cirujprincipal]
                    if retorno!='NaN':
                        pacientesconsultas[retorno[0]].append(secuencia[k])
                        ctconsultas[retorno[0]].append(ctconsultas[retorno[0]][-1]+dc[indice(pacientes,secuencia[k])])
                        #habría que eliminar al paciente de la lista
                        hcc[retorno[1]]=hcc[retorno[1]]+dc[indice(pacientes,secuencia[k])] 
                        flagcambiado=1
                        tiempoacum[indice(pacientes,secuencia[k])]=0 #se actualiza el tiempo acumulado.
                        # borramos todo lo del paciente en cuestión, ya que ya ha terminado su ciclo en el hospital#
                        pacientesaborrar.append(pacientes[indice(pacientes,secuencia[k])])
                        
                    else: 
                        flagcambiado=0
                        tiempoacum[indice(pacientes,secuencia[k])]=tiempoacum[indice(pacientes,secuencia[k])]+1
                
                if flagcambiado==1 and (estado[indice(pacientes,secuencia[k])]==1 or estado[indice(pacientes,secuencia[k])]==2):
                    estado[indice(pacientes,secuencia[k])]=estado[indice(pacientes,secuencia[k])]+1
                    # if estado[indice(pacientes,secuencia[k])]==2:
                    #     mu=random.randint(1,4)
                    #     sigma=random.choice([0.1*mu,0.2*mu,0.3*mu,0.4*mu,0.5*mu])
                    #     dq[indice(pacientes,secuencia[k])]=abs(random.normalvariate(mu, sigma))
            
            eq=equilibrio(hcc,hcor)
            tarde=lateness(pacientes)
            utilizacionor=0
            utilizacionc=0
            i=0
            
            while i<numc:
                utilizacionc=ctconsultas[i][-1]+utilizacionc
                i=i+1
            
            i=0
            while i<numor:
                utilizacionor=ctor[i][-1]+utilizacionor
                i=i+1
            dispqlista=dispq[:,dia].tolist()
            dispconslista=dispcons[:,dia].tolist()
            utilizacion=(utilizacionor+utilizacionc)/(horasq*dispqlista.count(1)+sum(dispconslista)/60)
            maximo=int(max(pesos))
            return eq/((horasq/2)**2+(sum(dispconslista)/60/2)**2)*we,tarde/(332*maximo*len(pacientes))*wt,utilizacion*wu,eq/((horasq/2)**2+(sum(dispconslista)/60/2)**2)*we+wt*tarde/(332*maximo*len(pacientes))-wu*utilizacion-wc*continuidad/petapauno#vamos a tener un libro excel, con una hoja cada día. Habrá una columna de 'cirujanos, asistente, paciente', otra para consultas y OR
        # #creo las listas#
        leerexcel()
         #auxiliares#
        ctconsultas = [[0]]
        x=0
        while x<numc-1:
            ctconsultas.append([0])
            x=x+1 
        
        ctor = [[0]]
        x=0
        while x<numor-1:
            ctor.append([0])
            x=x+1
        
        global dia
        leerexcel()
        vectorFO=asignacion(secuencia,cc)
        
        listaciruj[dia] = cc[:numc] + cirujanosor
        listaasist[dia] = empty+asistentesor
        listapacs[dia] = pacientesconsultas+pacientesor
        
        return vectorFO

    def cajanegrasecuencia(secuencia):  
        global hcor, hcc, continuidad, numc, numor, horasq, ctor, wt,we,wc,wu,ctcc, cirujanos, asistentesor, cirjasocPAE, cirjasocOR, cirujanosor, ctconsultas, ctor, pacientes, pacientesaborrar, pacientesconsultas, pacientesor, tiempoacum
        global listaciruj, listaasist, listapacs
        def asignacion(secuencia):
            global pacientesconsultas, cirujanosconsultas, pacientesor, cirujanosor, asistentesor, ctconsultas, ctor, hcor, hcc, continuidad
            pacientesconsultas = [[]]
            cirujanosconsultas=[[]]
            x=0
            while x<numc-1:
                pacientesconsultas.append([])
                cirujanosconsultas.append([])
                x=x+1
            
            pacientesor = [[]]
            cirujanosor = [[]]
            asistentesor = [[]]
            x=0
            while x<numor-1:
                pacientesor.append([])
                cirujanosor.append([])
                asistentesor.append([])
                x=x+1
           
            ###FUNCIONES###        
            #Función que aporta la varianza de lo que los cirujanos llevan acumulados en consulta y en quirófano
                    #sirve para medir el equilibrio de la carga de trabajo#
            def equilibrio(hcc,hcor):
                return (hcc.var()+hcor.var())
                    
            #Función para ver cuántos pacientes sobrepasan actualmente su tiempo de respuesta
            def lateness(pacientes):
                global pesos
                x=0
                late=[]
                for x in range(len(pacientes)):
                    if estado[x]==1:
                        if tiempoacum[x]>trp[x]:
                            late.append((tiempoacum[x]-trp[x])*pesos[x])
                    if estado[x]==2:
                        if tiempoacum[x]>trq[x]:
                            late.append((tiempoacum[x]-trq[x])*pesos[x])
                    if estado[x]==3:
                        if tiempoacum[x]>trc[x]:
                            late.append((tiempoacum[x]-trc[x])*pesos[x])
                return sum(late) #late indica cuántos pacientes van con retraso actualmente
        
            #Función para comprobar si el cirujano está  asignado a algun OR o CONSULTA ese día
            def asignadodia(cirujano,consultaor):
                global cirujanosconsultas
                global cirujanosor
                global numc
                i=0
                flag = 0
                if consultaor=='consulta':#comprobamos si el cirujano está asignado a alguna CONSULTA
                    for i in range(len(cirujanosconsultas)):
                        if cirujano in cirujanosconsultas[i]:#si el cirujano está en la consulta i, nos devuelve ese valor
                            return i
                            flag=1
                    if flag==0:
                        return 'NaN'
                elif consultaor == 'OR': #comprobamos si el cirujano está asignado a alguún QUIRÓFANO
                    for i in range(numor):
                        if (cirujano in cirujanosor[i]) or (cirujano in asistentesor[i]):#si el cirujano está en el OR j, nos devuelve ese valor
                            return i
                            flag=1
                    if flag==0:
                        return 'NaN'
                    
            #funcion para calcular el indice de un vector 
            def indice(vector,valor):
                x=0
                for x in range(len(vector)):
                    if vector[x]==valor:
                        return x
                        break
                    
            #Función para asignar un paciente y un cirujano a PAE (teniendo en cuenta que en la PAE sea necesario coincidir en unidades)
            def busquedaPAE (paciente):
                global cirujanos
                global numc, horasq
                global hcc
                j=0
                cirujanosdelaunidad = []#lista de cirujanos que pertenecen a la unidad del paciente
                while j<len(cirujanos):
                    if exp[j][u[paciente]-1]>0 and descanso[j,dia]==0:#si el cirujano que estamos viendo es de la unidad
                        cirujanosdelaunidad.append(j)
                    j=j+1
                #ordenamos los cirujanosdelaunidad según las horas de consulta que lleven
                j=0
                horas=[]
                for j in range(len(cirujanosdelaunidad)):
                    horas.append(hcc[cirujanosdelaunidad[j]])
                horasnumpy=np.array(horas)
                cirujanosdelaunidadnumpy = np.array(cirujanosdelaunidad)
                np.argsort(horasnumpy)
                cirujanosdelaunidad = cirujanosdelaunidadnumpy[horasnumpy.argsort()].tolist()
                j=0
                flagyatieneconsulta=0#flag para ver si pasa por los bucles y no tiene consulta en toda la semana
                #para cada cirujano, miramos si está asignado a alguna consulta el dia
                while j<len(cirujanosdelaunidad):
                    
                    asignadoenconsulta = asignadodia(cirujanosdelaunidad[j],'consulta')
                    if asignadoenconsulta!='NaN' and consultas[asignadoenconsulta]!='General':#el cirujano sí está asignado a la consulta asignadoenconsulta
                        # print('si, está asignado el dia {} en la consulta {}'.format(dia,asignadoenconsulta))
                        if u[paciente]-1==especialidades[asignadoenconsulta]:
                            if ctconsultas[asignadoenconsulta][-1]+dp[paciente]<=dispcons[asignadoenconsulta][dia]/60:#ponemos h de consulta al dia
                                # print('sí hay hueco en la consulta')
                                return [asignadoenconsulta,cirujanosdelaunidad[j]]
                                flagyatieneconsulta=1
                                break                   
                    if flagyatieneconsulta==1:break
                    j=j+1
                if flagyatieneconsulta==0:#si no tiene consulta en toda la semana ningún cirujano, se le asigna al primero la primera consulta libre
                    j=0
                    
                    while j<len(cirujanosconsultas):
                        if cirujanosconsultas[j]==[] and dispcons[j][dia]>0 and consultas[j]!='General':#si la consulta está libre
                            x=0
                            for x in cirujanosdelaunidad:
                                if asignadodia(x, 'OR')=='NaN' and asignadodia(x, 'consulta')=='NaN': # or asignadodia(x, 'consulta', dia)==j):
                                    #si el cirujano no tiene OR asignado ese día, y si tiene consultas que sean esa misma,
                                    # print('entroaqui')
                                    if (consultas[j]=='Especialidad' or consultas[j]=='Nominativa') and u[paciente]-1==especialidades[j] and candidatos[j][x]==1:
                                        return [j,x]
                                        flagyatieneconsulta=1
                                        break#cuando se le asigna, se sale del for
                            if flagyatieneconsulta==1:
                                break   
                        j=j+1
                if flagyatieneconsulta==0:
                    return 'NaN' #si el flag sigue, se ve que no hay hueco para la consulta PAE para este paciente en toda la semana
                               
            # Función para asignar un paciente y un cirujano a consulta postop 
            def busquedaPOSTOP (paciente):
                #se va pasando por cada día por cada consulta, viendo dónde tiene el cirujasoc consulta asignada y si hay hueco
                
                flagyatieneconsulta=0
               
                asignadoenconsulta=asignadodia(cirjasocOR[paciente],'consulta')
                asignadoenOR = asignadodia(cirjasocOR[paciente],'OR')
                if asignadoenconsulta!='NaN' and asignadoenOR=='NaN' and descanso[cirjasocOR[paciente],dia]==0 and consultas[asignadoenconsulta]!='General':#el cirujano sí está asignado a la consulta asignadoenconsulta
                    if u[paciente]-1==especialidades[asignadoenconsulta]:
                        if ctconsultas[asignadoenconsulta][-1]+dc[paciente]<=dispcons[asignadoenconsulta][dia]/60:#ponemos h de consulta al dia
                            return [asignadoenconsulta,cirjasocOR[paciente]]
                            flagyatieneconsulta=1
                if flagyatieneconsulta==0:#e ciruj asoc no está en ninguna consulta ningún día
                    #se le asigna el primer hueco que haya en la semana
                    j=0
                    
                    while j<len(cirujanosconsultas):
                        if  cirujanosconsultas[j]==[] and dispcons[j][dia]>0 and consultas[j]!='General':#este es la consulta donde se asignará el cirujano
                            if asignadoenconsulta=='NaN' and asignadoenOR=='NaN' and descanso[cirjasocOR[paciente],dia]==0:#si el cirujano no tiene OR asignado ese día, puede asignarse a consultas
                                if (consultas[j]=='Especialidad' or consultas[j]=='Nominativa') and u[paciente]-1==especialidades[j] and candidatos[j][cirjasocOR[paciente]]==1 :
                                    return [j,cirjasocOR[paciente]]
                                    flagyatieneconsulta=1
                                    break#cuando se le asigna, se sale del for
                        if flagyatieneconsulta==1:
                            break   
                        j=j+1
                if flagyatieneconsulta==0:
                    return 'NaN' #si el flag sigue, se ve que no hay hueco para la consulta PAE para este paciente en toda la semana
                               
            #Función para asignar un paciente y un equipo de cirujanos a quirófanos
            def busquedaOR(paciente):
                   #se hará igual que para la consulta PAE, solo que ahora deberá haber cirujano principal y asistente. SSe tendrán en cuenta
                    #la experiencia y nivel de dificultad de la  operación.
                j=0
                cirujanosexpunidad = []#lista de cirujanos que pertenecen a la unidad del paciente y que cuentan con experiencia suficiente
                while j<len(cirujanos):
                    if exp[j][u[paciente]-1]>0 and hp[paciente]<=exp[j][u[paciente]-1] and descanso[j,dia]==0 and [j] not in cirujanosconsultas:#si el cirujano que estamos viendo es de la unidad y tiene experiencia suficiente
                        cirujanosexpunidad.append(cirujanos[j])
                    j=j+1
                #ordenamos los cirujanosdelaunidad según las horas de OR que lleven
                j=0
                horas=[]
                for j in range(len(cirujanosexpunidad)):
                    horas.append(hcor[cirujanosexpunidad[j]])
                horasnumpy=np.array(horas)
                cirujanosexpunidadnumpy = np.array(cirujanosexpunidad)
                np.argsort(horasnumpy)
                cirujanosexpunidad = cirujanosexpunidadnumpy[horasnumpy.argsort()].tolist()
                if cirjasocPAE[paciente] in cirujanosexpunidad:
                    cirujanosexpunidad.remove(cirjasocPAE[paciente])
                    cirujanosexpunidad.insert(0,cirjasocPAE[paciente])
                #esta lista es para asignar un CIRUJANO PRINCIPAL, tras asignar un cirujano principal, se asignará el asistente                
                
                ###LISTA ASISTENTES###
                j=0
                asistexp = []#lista de cirujanos que cuentan con experiencia suficiente, para los asists nose tiene en cuenta la unidad
                while j<len(cirujanos):
                    if hs[paciente]<=max(exp[j]) and descanso[j,dia]==0:#si el cirujano que estamos viendo  tiene experiencia suficiente
                        asistexp.append(cirujanos[j])
                        # print(asistexp)
                    j=j+1
                # print(asistexp)
                #ordenamos los asistentes según las horas de consulta que lleven
                j=0
                horas=[]
                for j in range(len(asistexp)):
                    # print('asistente',asistexp[j] )
                    horas.append(hcor[asistexp[j]])
                # print(horas)
                horasnumpy=np.array(horas)
                asistexpnumpy = np.array(asistexp)
                np.argsort(horasnumpy)
                asistexp = asistexpnumpy[horasnumpy.argsort()].tolist()
                # print('listaordenadaasist',asistexp)                
                
                if hs[paciente]==0:#si no necesitamos asistente, se haría con el mismo algoritmo de buscar consulta:
                     # print('No se necesita asistente')
                     j=0
                     
                     flagyatieneOR=0#flag para ver si pasa por los bucles y no tiene consulta en toda la semana
                     #para cada cirujano, miramos si está asignado a algún OR el dia
                     while j<len(cirujanosexpunidad):
                         asignadoenOR = asignadodia(cirujanosexpunidad[j],'OR')
                         # print(' ¿está el cirujano en algun OR el dia {} ?'.format(dia))
                         if asignadoenOR!='NaN':#el cirujano sí está asignado a la OR asignadoenOR
                             # print('si, está asignado en el OR {}'.format(asignadoenOR))
                             if ctor[asignadoenOR][-1]+dq[paciente]<=horasq:#ponemos horasqh de OR al dia
                                 # print('hay hueco en este OR')
                                 return [asignadoenOR,cirujanosexpunidad[j],'NaN']
                                 flagyatieneOR=1
                                 break
                         j=j+1
                     if flagyatieneOR==0:#si no tiene OR en toda la semana ningún cirujano, se le asigna al primero el primer hueco libre
                         # print('entra')
                         j=0
                         while j<numor:
                             # print('los cirujanos no tienen consulta asignada con hueco en la semana, así que se coge el primer hueco libre y se ve si algun ciruj puede')
                             if ctor[j][-1]==0 and dispq[j][dia]==1:#eL OR está libre, no tiene ninguna operación programada y está disponible
                                 x=0
                                 for x in cirujanosexpunidad:
                                     # print('probamos con el ciruj',x)
                                     # print('asignadodia',asignadodia(x, 'consulta'))
                                     # print('asignadodOR',asignadodia(x, 'OR'))
                                     if asignadodia(x,'consulta')=='NaN' and (asignadodia(x,'OR')=='NaN' or asignadodia(x,'OR')==j ) and [x] not in asistentesor:#si el cirujano no tiene consulta asignado ese día, puede asignarse a consultas
                                         # print('este ciruj SI puede')
                                         return [j,cirujanosexpunidad[0],'NaN']
                                         flagyatieneOR=1
                                         break#cuando se le asigna, se sale del for
                                 if flagyatieneOR==1:
                                     break   
                             j=j+1
                     if flagyatieneOR==0:
                         return 'NaN' #si el flag sigue, se ve que no hay hueco para la consulta PAE para este paciente en toda la semana
                else:   #sí se necesita un asistente
                    # print('si se necesita un asistente')
                    #vamos a buscar a la vez un cirujano principal y un asistente
                    i=0
                    flagyatieneasist=0
                    for i in cirujanosexpunidad:
                        # print('probamos con el ciruj {} el dia {}'.format(i,dia))
                        asignadoenOR = asignadodia(i,'OR')
                        # print('¿está asignado en algun OR ya?')
                        if asignadoenOR!='NaN':#el cirujano sí está asignado ese día en un quirófano
                            # print('si, esta en el OR',asignadoenOR)
                            if ctor[asignadoenOR][-1]+dq[paciente]<=horasq and [i]==cirujanosor[asignadoenOR]:#le asignamos este hueco en la consulta
                                # print('sí habría hueco en su OR')
                                if asistentesor[asignadoenOR]!=[]:
                                    if asistentesor[asignadoenOR][-1] in asistexp :
                                        return [asignadoenOR,i,asistentesor[asignadoenOR][-1]]
                                        flagyatieneasist=1  
                                if asistentesor[asignadoenOR]==[]:
                                    for k in asistexp:
                                        if asignadodia(k, 'OR')=='NaN' and asignadodia(k, 'consulta') == 'NaN' and k!=i:
                                            return [asignadoenOR, i, k]
                                            flagyatieneasist=1
                            if ctor[asignadoenOR][-1]+dq[paciente]<=horasq and [i]==asistentesor[asignadoenOR]:#le asignamos este hueco en la consulta
                                if cirujanosor[asignadoenOR][-1] in asistexp:
                                    return [asignadoenOR,cirujanosor[asignadoenOR][-1],i]
                                    flagyatieneasist=1
                        
                        if flagyatieneasist==1:break
                    if flagyatieneasist==0: #hemos probado todos los cirujanos pero no hay ninguno ya asignado a un OR durante la semana. Hay que buscarle nuevo hueco
                        #Vamos buscando un hueco para el primer cirujano, y vemos si tiene asistente posible. Si no hay asistente, se pasa al sig hueco
                        # print('no hay ciruj con OR asignado, probamos a buscar el primer hueco')
                        i=0
                        for i in cirujanosexpunidad:
                            asignadoenconsulta = asignadodia(i,'consulta')
                            # print('¿está asignado en consulta este ciruj ya?',asignadoenconsulta)
                            x=0
                            while x<numor:
                                # print('está ya asignado a un OR?',asignadodia(i,'OR'))
                                if asignadoenconsulta=='NaN' and (asignadodia(i,'OR')=='NaN' or asignadodia(i,'OR')==x ):#comprobamos que el ciruj no está en ninguna consulta ese día
                                    #print(ctor[dia][x][-1])
                                    if ctor[x][-1]==0 and dispq[x][dia]==1:#el OR está libre y disponible
                                    #buscamos un asistente
                                        # print('hay hueco')
                                        for k in asistexp:
                                            # print('probamos con el asist {}, cirujanos {}, asignado en consulta? {} asignado en OR? {}'.format(k,i,asignadodia(k,'consulta'),asignadodia(k,'OR')))
                                            if k!=i and asignadodia(k,'consulta')=='NaN' and (asignadodia(k,'OR')=='NaN' or asignadodia(k,'OR')==x ):
                                                # print('asistente disponible')
                                                #asiste!=cirujasoc  asist no puede estar en consultas ese dia    asist no puede estar asignado a otro OR que no sea este ese dia
                                                #si esta condicion se cumple, se asocia este asist 
                                                return [x,i,k]
                                                flagyatieneasist=1
                                                break  
                                if flagyatieneasist==1:break
                                x=x+1
                            if flagyatieneasist==1:break
                    if flagyatieneasist==0:
                        # print('NO HAY POSIBLE COMBINACION CIRUJANO ASISTENTE')
                        return'NaN' #si tras buscar todos los cirujanos posibles con todos los asistentes en todos los huecos el flag sigue a 0,
                        #significa que no hay hueco posible para este paciente en OR esta semana
                                                                               
            ###COMIENZO CODIGO###
          
            global pacientesaborrar
            pacientesaborrar=[]
            petapauno=0
            continuidad=0
            
            p=0
            while p<numc:
                if consultas[p]=='Nominativa' and dispcons[p][dia]>0:
                    j=0
                    while j<len(cirujanos):
                        if candidatos[p][j]==1 and dispcons[p,dia]>0 and descanso[j,dia]==0:
                            cirujanosconsultas[p]=[j]
                            break
                        j=j+1
                p=p+1
                
            for k in pacientes:
                if k not in secuencia:
                    tiempoacum[indice(pacientes,k)]=tiempoacum[indice(pacientes,k)]+1
                if estado[indice(pacientes,k)]==2:
                    petapauno=petapauno+1
            for k in range(len(secuencia)): #x es el indice del paciente
                # print(' se ve al paciente {}'.format(secuencia[k]))
                if estado[indice(pacientes,secuencia[k])]==1:
                    # print('vamos a busquedaPAE ')
                    retorno=busquedaPAE(indice(pacientes,secuencia[k])) #[consulta,cirujprincipal]
                    # print(retorno)
                    if retorno!='NaN':
                        
                        cirujanosconsultas[retorno[0]]=[retorno[1]]
                        pacientesconsultas[retorno[0]].append(secuencia[k])
                        ctconsultas[retorno[0]].append(ctconsultas[retorno[0]][-1]+dp[indice(pacientes,secuencia[k])])
                        hcc[retorno[1]]=hcc[retorno[1]]+dp[indice(pacientes,secuencia[k])]
                        tiempoacum[indice(pacientes,secuencia[k])]=0#se pone el -1 porque el día 0 aumenta 1 día
                        cirjasocPAE[indice(pacientes,secuencia[k])]=retorno[1]
                        # print(equilibrio(hcc,hcor))
                        # print('se asigna el paciente {} a la consulta {} el día  con el cirujano {}'.format(secuencia[x],retorno[0],retorno[1]))
                        flagcambiado=1
                    else:
                        flagcambiado=0
                        tiempoacum[indice(pacientes,secuencia[k])]=tiempoacum[indice(pacientes,secuencia[k])]+1
                if estado[indice(pacientes,secuencia[k])]==2:
                    # print('vamos a OR')
                    retorno=busquedaOR(indice(pacientes,secuencia[k])) #me devuelve [consulta,cirujprincipal,asistente]
                    # print(retorno)
                    if retorno!='NaN':
                        if retorno[1]==cirjasocPAE[indice(pacientes,secuencia[k])]:
                            continuidad = continuidad+1
                        # print('se asigna el paciente {} al OR {} el día con el cirujano {} y con asistente {}'.format(secuencia[x],retorno[0],retorno[1],retorno[2]))
                        cirujanosor[retorno[0]]=[retorno[1]]
                        hcor[retorno[1]]=hcor[retorno[1]]+dq[indice(pacientes,secuencia[k])]
                        pacientesor[retorno[0]].append(secuencia[k])
                        ctor[retorno[0]].append(ctor[retorno[0]][-1]+dq[indice(pacientes,secuencia[k])])
                        cirjasocOR[indice(pacientes,secuencia[k])]=retorno[1]
                        tiempoacum[indice(pacientes,secuencia[k])]=0 #se actualiza el tiempo acumulado.
                        if retorno[2]!='NaN':
                            asistentesor[retorno[0]]=[retorno[2]]
                            hcor[retorno[2]]=hcor[retorno[2]]+dq[indice(pacientes,secuencia[k])]
                        flagcambiado=1
                    else:
                        flagcambiado=0
                        tiempoacum[indice(pacientes,secuencia[k])]=tiempoacum[indice(pacientes,secuencia[k])]+1
                if estado[indice(pacientes,secuencia[k])]==3:
                    # print('vamos a POSTOP')
                    retorno=busquedaPOSTOP(indice(pacientes,secuencia[k])) #me devuelve [consulta,cirujprincipal]
                    # print('retorno',retorno)
                    if retorno!='NaN':
                        cirujanosconsultas[retorno[0]]=[retorno[1]]
                        pacientesconsultas[retorno[0]].append(secuencia[k])
                        ctconsultas[retorno[0]].append(ctconsultas[retorno[0]][-1]+dc[indice(pacientes,secuencia[k])])
                        #habría que eliminar al paciente de la lista
                        hcc[retorno[1]]=hcc[retorno[1]]+dc[indice(pacientes,secuencia[k])] 
                        flagcambiado=1
                        tiempoacum[indice(pacientes,secuencia[k])]=0 #se actualiza el tiempo acumulado.
                        # borramos todo lo del paciente en cuestión, ya que ya ha terminado su ciclo en el hospital#
                        pacientesaborrar.append(pacientes[indice(pacientes,secuencia[k])])                      
                        
                    else:
                        flagcambiado=0
                        tiempoacum[indice(pacientes,secuencia[k])]=tiempoacum[indice(pacientes,secuencia[k])]+1
                
                if flagcambiado==1 and (estado[indice(pacientes,secuencia[k])]==1 or estado[indice(pacientes,secuencia[k])]==2):
                    estado[indice(pacientes,secuencia[k])]=estado[indice(pacientes,secuencia[k])]+1
                    # if estado[indice(pacientes,secuencia[k])]==2:
                    #     mu=random.randint(1,4)
                    #     sigma=random.choice([0.1*mu,0.2*mu,0.3*mu,0.4*mu,0.5*mu])
                    #     dq[indice(pacientes,secuencia[k])]=abs(random.normalvariate(mu, sigma))
            
            #ASIGNACION DE CIRUJANOS A CONSULTAS GENERALES SEGÚN MENORES HORAS DE CONSULTA ACUMULADAS#
            
            cirujanoslibres = []#lista de cirujanos que pertenecen a la unidad del paciente
            j=0
            while j<len(cirujanos):
                if [j] not in cirujanosconsultas and [j] not in cirujanosor and [j] not in asistentesor and descanso[j][dia]==0:#si el cirujano que estamos viendo es de la unidad
                    cirujanoslibres.append(j)
                j=j+1
            #ordenamos los cirujanoslibres según las horas de consulta que lleven
            j=0
            horas=[]
            for j in range(len(cirujanoslibres)):
                horas.append(hcc[cirujanoslibres[j]])
            horasnumpy=np.array(horas)
            cirujanoslibresnumpy = np.array(cirujanoslibres)
            np.argsort(horasnumpy)
            cirujanoslibres = cirujanoslibresnumpy[horasnumpy.argsort()].tolist()
            
            j=0
            i=0
            while i<numc and j<len(cirujanoslibres):
                if consultas[i]=='General' and dispcons[i][dia]>0:
                    cirujanosconsultas[i]=[cirujanoslibres[j]]
                    ctconsultas[i].append(dispcons[i][dia]/60)
                    hcc[cirujanoslibres[j]]=hcc[cirujanoslibres[j]]+dispcons[i][dia]/60
                    j=j+1
                i=i+1
            
            eq=equilibrio(hcc,hcor)
            tarde=lateness(pacientes)
            
            utilizacionor=0
            utilizacionc=0
            i=0
            
            while i<numc:
                utilizacionc=ctconsultas[i][-1]+utilizacionc
                i=i+1
            
            i=0
            while i<numor:
                utilizacionor=ctor[i][-1]+utilizacionor
                i=i+1
            dispqlista=dispq[:,dia].tolist()
            dispconslista=dispcons[:,dia].tolist()            
            utilizacion=(utilizacionor+utilizacionc)/(sum(dispconslista)/60+horasq*dispqlista.count(1))
            maximo=int(max(pesos))
            # print('pesos', pesos)
            # print('continuidad', continuidad)
            # print('petapauno',petapauno)
            # print('utilizacion', utilizacion)
            return eq/((horasq/2)**2+(sum(dispconslista)/60/2)**2)*we,tarde/(332*maximo*len(pacientes))*wt,utilizacion*wu,eq/((horasq/2)**2+(sum(dispconslista)/60/2)**2)*we+wt*tarde/(332*maximo*len(pacientes))-wu*utilizacion-wc*continuidad/petapauno
        #vamos a tener un libro excel, con una hoja cada día. Habrá una columna de 'cirujanos, asistente, paciente', otra para consultas y OR
        # #creo las listas#
        leerexcel()
        ctconsultas = [[0]]
        x=0
        while x<numc-1:
            ctconsultas.append([0])
            x=x+1 
        
        ctor = [[0]]
        x=0
        while x<numor-1:
            ctor.append([0])
            x=x+1
        
        global dia
        leerexcel()
        vectorFO=asignacion(secuencia)
        
        listaciruj[dia] = cirujanosconsultas+cirujanosor
        listaasist[dia] = empty+asistentesor
        listapacs[dia] = pacientesconsultas+pacientesor

        return vectorFO

    def actualizarexcel(pacientesaborrar):
        #borro los pacientesaborrar para que no los coja en la siguiente ronda y actualizo el excel
        j=0
        x=0
        # print('pacientes a borrar', pacientesaborrar)
        while j < len(pacientesaborrar):
            x=0
            # print('j',j)
            while x<len(pacientes):
                # print('x',x)
                if pacientesaborrar[j]==pacientes[x]:
                    # print('se borra el paciente', pacientesaborrar[j])
                    del pacientes[x]
                    del cirjasocPAE[x]
                    del cirjasocOR[x]
                    del dc[x]
                    del dp[x]
                    del dq[x]
                    del estado[x]
                    del hp[x]
                    del hs[x]
                    del pesos[x]
                    del tiempoacum[x]
                    del trc[x]
                    del trp[x]
                    del trq[x]
                    del u[x]
                else:x=x+1
            j=j+1        
                    
        #actualización del excel#
        x=0
        while x<len(pacientes):
            dp[x]=int(dp[x]*60)
            dc[x]=int(dc[x]*60)
            dq[x]=float(dq[x]/horasq)
            x=x+1
        # dp=[int(x) for [x] in dp]
        # dq=[int(x) for [x] in dq]
        # dc=[int(x) for [x] in dc]
        
        
        x=0
        while x<len(cirjasocPAE):
              if cirjasocPAE[x]=='NaN':
                  cirjasocPAE[x]=0
              else:
                  cirjasocPAE[x]=cirjasocPAE[x]+1
              x=x+1
        x=0
        while x<len(cirjasocOR):
              if cirjasocOR[x]=='NaN':
                  cirjasocOR[x]=0
              else:
                  cirjasocOR[x]=cirjasocOR[x]+1
              x=x+1
        x=0
        tiempoacumPAE=[]
        tiempoacumq=[]
        tiempoacumpost=[]

        while x<len(pacientes):
            tiempoacumPAE.append(aux)
            tiempoacumq.append(aux)
            tiempoacumpost.append(aux)
            x=x+1
        x=0
        while x<len(pacientes):
            if estado[x]==1:
                tiempoacumPAE[x]=tiempoacum[x]
                tiempoacumq[x]=0
                tiempoacumpost[x]=0
            elif estado[x]==2:
                tiempoacumPAE[x]=0
                tiempoacumq[x]=tiempoacum[x]
                tiempoacumpost[x]=0
            else:
                tiempoacumPAE[x]=0
                tiempoacumq[x]=0
                tiempoacumpost[x]=tiempoacum[x]
            x=x+1
        nuevodataframepacientes = pd.DataFrame({'Número paciente':pacientes,
                                        'u':u,
                                        'w':pesos,
                                        'estado':estado,
                                        'dp':dp,
                                        'dq':dq,
                                        'dc':dc,
                                        'hp':hp,
                                        'hs':hs,
                                        'cirujano OR': cirjasocOR,
                                        'cirujano PAE':cirjasocPAE,
                                        'trp':trp,
                                        'trq':trq,
                                        'trc':trc,
                                        'tacumpae':tiempoacumPAE,
                                        'tacumq':tiempoacumq,
                                        'tacumpost':tiempoacumpost
                                        })
        
        nuevodataframepacientes.to_csv('pacientes.csv', index=0,encoding='utf-8', sep=';',header=None)
        nuevodataframeconfig = pd.DataFrame({'Num paciente': [len(pacientes)],
                                             'Num cirujs': [len(cirujanos)],
                                             'nose': [config[0,2]],
                                                      'nose1': [config[0,3]],
                                                      'nose2': [config[0,4]],
                                                      'nose3': [config[0,5]],
                                                      'nose4': [config[0,6]],
                                                      'nose5': [config[0,7]],
                                                      'nose6': [config[0,8]]      
                                             })
        nuevodataframeconfig.to_csv('config.csv', index=0,encoding='utf-8', sep=';',header=None)
    def escribirsol(listaciruj,listaasist,listapacs, estadooriginal, pacientesoriginales):
        
        listaid=[]
        listafecha=[]
        listacirujano=[]
        listapaciente=[]
        listaconsulta=[]
        listaconsultapae=[]
        listaconsultapost=[]
        listaquirofano=[]
        listadia=[]
        listatipo=[]
        listadescripcion=[]
        
        c=0
        C=[]
        while c<numc:
            C.append('C')
            c=c+1
        o=0
        O=[]
        while o<numor:
            O.append('O')
            o=o+1
        # dfsol1 = pd.DataFrame({'Espacio':C+O,
        #                       'CIRUJANOS':listaciruj[0],
        #                       'ASISTENTES':listaasist[0],
        #                       'PACIENTES':listapacs[0]
                              
        #     })
        # dfsol2 = pd.DataFrame({'Espacio':C+O,
        #                       'CIRUJANOS':listaciruj[1],
        #                       'ASISTENTES':listaasist[1],
        #                       'PACIENTES':listapacs[1]
                              
        #     })
        # dfsol3 = pd.DataFrame({'Espacio':C+O,
        #                       'CIRUJANOS':listaciruj[2],
        #                       'ASISTENTES':listaasist[2],
        #                       'PACIENTES':listapacs[2]
                              
        #     })
        # dfsol4 = pd.DataFrame({'Espacio':C+O,
        #                       'CIRUJANOS':listaciruj[3],
        #                       'ASISTENTES':listaasist[3],
        #                       'PACIENTES':listapacs[3]
                              
        #     })
        # dfsol5 = pd.DataFrame({'Espacio':C+O,
        #                       'CIRUJANOS':listaciruj[4],
        #                       'ASISTENTES':listaasist[4],
        #                       'PACIENTES':listapacs[4]
                              
        #     })
        # dfsol6 = pd.DataFrame({'Espacio':C+O,
        #                       'CIRUJANOS':listaciruj[5],
        #                       'ASISTENTES':listaasist[5],
        #                       'PACIENTES':listapacs[5]
                              
        #     })
        # dfsol7 = pd.DataFrame({'Espacio':C+O,
        #                       'CIRUJANOS':listaciruj[6],
        #                       'ASISTENTES':listaasist[6],
        #                       'PACIENTES':listapacs[6]
                              
        #     })
        
        # with pd.ExcelWriter('solucion.xlsx') as writer:
        #      dfsol1.to_excel(writer, sheet_name = "LUNES")
        #      dfsol2.to_excel(writer, sheet_name = "MARTES")
        #      dfsol3.to_excel(writer, sheet_name = "MIERCOLES")
        #      dfsol4.to_excel(writer, sheet_name = "JUEVES")
        #      dfsol5.to_excel(writer, sheet_name = "VIERNES")
        #      dfsol6.to_excel(writer, sheet_name = "SABADO")
        #      dfsol7.to_excel(writer, sheet_name = "DOMINGO")
         
        j=0
        c=0
        ide=0
        def indice(vector,valor):
            x=0
            for x in range(len(vector)):
                if vector[x]==valor:
                    return x
                    break
        while j<ht:
            c=0
            while c<len(C+O):
                if listaciruj[j][c]!=[]: #Cirujano principal
                    listaid.append(ide)
                    listacirujano.append(listaciruj[j][c][0])
                    listapaciente.append(' ')
                    if c<numc:
                        listaconsulta.append(c+1)
                        listaconsultapae.append(' ')
                        listaconsultapost.append(' ')
                        listaquirofano.append(' ')
                        listatipo.append('Z')
                        listadescripcion.append('Consulta' +' '+ str(c+1))
                    elif c>=numc:
                        listaconsulta.append(' ')
                        listaconsultapae.append(' ')
                        listaconsultapost.append(' ')
                        listaquirofano.append(c-numc+1)
                        listatipo.append('Zprima')
                        listadescripcion.append('Quirofano' + ' '+str(c-numc+1))
                    listadia.append(j)
                    date=datetime.today().strftime('%d/%m/%Y')
                    listafecha.append(date)
                    ide=ide+1
                if listaasist[j][c]!=[]: #cirujano asistente
                    listaid.append(ide)
                    listacirujano.append(listaasist[j][c][0])
                    listapaciente.append(' ')
                    listaconsulta.append(' ')
                    listaconsultapae.append(' ')
                    listaconsultapost.append(' ')
                    listaquirofano.append(c-numc+1)
                    listatipo.append('Zprima_asis')
                    listadescripcion.append('Quirofano' + ' '+str(c-numc+1))
                    listadia.append(j)
                    date=datetime.today().strftime('%d/%m/%Y')
                    listafecha.append(date)
                    ide=ide+1
                if listapacs[j][c]!=[]:#pacientes
                    p=0
                    while p<len(listapacs[j][c]):
                        if listapacs[j][c][p]!=[]:
                            listaid.append(ide)
                            listacirujano.append(' ')
                            listapaciente.append(listapacs[j][c][p])
                            listaconsulta.append(' ')
                            if estadooriginal[indice(pacientesoriginales,listapacs[j][c][p])]==1:
                                listaconsultapae.append(c+1)
                                listaconsultapost.append(' ')
                                listaquirofano.append(' ')
                                estadooriginal[indice(pacientesoriginales,listapacs[j][c][p])]=estadooriginal[indice(pacientesoriginales,listapacs[j][c][p])]+1
                                listatipo.append('X')
                                listadescripcion.append('Consulta' + ' ' + str(c+1) + ' ' +'PAE')
                            elif estadooriginal[indice(pacientesoriginales,listapacs[j][c][p])]==2:
                                listaconsultapae.append(' ')
                                listaconsultapost.append(' ')
                                listaquirofano.append(c-numc+1)
                                listatipo.append('Xprima')
                                listadescripcion.append('Quirofano' + ' ' + str(c-numc+1))
                                estadooriginal[indice(pacientesoriginales,listapacs[j][c][p])]=estadooriginal[indice(pacientesoriginales,listapacs[j][c][p])]+1
                            else:
                                listaconsultapae.append(' ')
                                listaconsultapost.append(c+1)
                                listaquirofano.append(' ')
                                listatipo.append('Xprima_2')
                                listadescripcion.append('Consulta' + ' ' + str(c+1) + ' ' +'POST')
                                estadooriginal[indice(pacientesoriginales,listapacs[j][c][p])]=estadooriginal[indice(pacientesoriginales,listapacs[j][c][p])]+1
                            listadia.append(j)
                            date=datetime.today().strftime('%d/%m/%Y')
                            listafecha.append(date)
                            
                            ide=ide+1
                        p=p+1
                c=c+1
            j=j+1
                        
        nuevodataframesol = pd.DataFrame({'ID':listaid,
                                        'FECHA_SALIDA':listafecha,
                                        'Cirujano':listacirujano,
                                        'Paciente':listapaciente,
                                        'Consulta':listaconsulta,
                                        'Consulta_PAE':listaconsultapae,
                                        'Consulta_POST':listaconsultapost,
                                        'Quirófano':listaquirofano,
                                        'Dia':listadia,
                                        'Tipo': listatipo,
                                        'Descripcion':listadescripcion
                                        
                                        })
        
        nuevodataframesol.to_csv('salida.csv', index=0,encoding='utf-8', sep=';')                
                        
                        
                        
                        
                        
    #LECTURA DE EXCEL#

    
    config=pd.read_csv('config.csv',sep=';',header=None).to_numpy()
    numpacientes=config[0,0]
    numcirujs=config[0,1]
    numc=config[0,2]
    numor=config[0,3]
    ht=config[0,4]
    numunidades=config[0,7]

    horasq=8
    # print('Número de consultas en el hospital', numc)
    #cirujanos#
    cirujanos = list(range(0,numcirujs))
    
    exp=pd.read_csv('cirujanos.csv',sep=';',header=None, nrows=numcirujs,skiprows=numcirujs).to_numpy()
    col=list(range(0,ht))
    descanso=pd.read_csv('cirujanos.csv',sep=';',header=None, usecols=col, nrows=numcirujs,skiprows=numcirujs*2).to_numpy()
    i=0
    j=0
    while i<len(cirujanos):
        j=0
        while j<ht:
            if descanso[i][j]==0:
                descanso[i][j]=1
            elif descanso[i][j]==1:
                descanso[i][j]=0
            j=j+1
        i=i+1

    dispcons=pd.read_csv('consultas.csv',sep=';',header=None,nrows=numc,skiprows=2, usecols=list(range(0,ht)) ).to_numpy()
    candidatos=pd.read_csv('consultas.csv',sep=';',header=None,nrows=numc,skiprows=2+numc, usecols=list(range(0,numcirujs)) ).to_numpy()
    dispq=pd.read_csv('quirofanos.csv',sep=';',header=None,nrows=numor, usecols=list(range(0,ht)) ).to_numpy()

    pesosobjetivo=pd.read_csv('objetivo.csv',sep=';',header=None).to_numpy()
    wt=pesosobjetivo[0,0]
    we=pesosobjetivo[0,1]
    wc=pesosobjetivo[0,2]
    wu=pesosobjetivo[0,3]
    
    especialidades=pd.read_csv('consultas.csv',sep=';',header=None,nrows=1,skiprows=1, usecols=list(range(0,numc)) ).to_numpy()
    especialidades=especialidades.transpose()
    for x in range(len(especialidades)):
        if especialidades[x]==0:
            especialidades[x]=999
        else:
            especialidades[x]=especialidades[x]-1
    especialidades = [int(x) for x in especialidades]
    for x in range(len(especialidades)):
        if especialidades[x]==999:
            especialidades[x]='NaN'
    
    

    t=0
    while t<numc:
        lista=candidatos[t].tolist()
        unos=lista.count(1)
        if unos==len(cirujanos):
            if t==0:
                consultas=['General']
            else:
                consultas.append('General')
        elif unos==1:
            if t==0:
                consultas=['Nominativa']
            else:
                consultas.append('Nominativa')
        else:
            if t==0:
                consultas=['Especialidad']
            else:
                consultas.append('Especialidad')
        t=t+1
    leerexcel()
    pacientesoriginales=pacientes.copy()
    estadooriginal=estado.copy()
    
    #arrays que deben empezar siendo vacíos, y luego se irán rellenando#
    hcor = np.array([0.0]*len(cirujanos)) #horas cirujanos en OR a la semana
    hcc = np.array([0.0]*len(cirujanos)) #horas cada cirujano en consulta a la semana 
    continuidad=0
    aux=[[]]

    x=0
    while x<(numc+numor)-1:
        aux.append([])
        x=x+1
    x=0
    listaciruj=[]
    listaasist=[]
    listapacs=[]
    while x<7:
        listaciruj.append(aux)
        listaasist.append(aux)
        listapacs.append(aux)
        x=x+1

    empty =[[]]
    x=0
    while x<numc-1:
        empty.append([])
        x=x+1
    
    utilior=0
    utilicons=0
    dia=0
    while dia<ht: 
        
        inicio=time.time()
        #NEH#
        #1- ORDENAR LA SECUENCIA INICIAL
        sumatiempos=np.array([0.0]*len(pacientes))
        for x in range(len(pacientes)):
            # print(x, dc[x], dp[x], dq[x])
            sumatiempos[x]=dc[x]+dq[x]+dp[x]
        pacientesnumpy = np.array(pacientes)
        ordennumpy = np.array(sumatiempos)
        np.argsort(sumatiempos)
        secinicial0=pacientesnumpy[ordennumpy.argsort()].tolist()#ordena de menor a mayor
        secinicial1=np.flip(secinicial0)
        secinicial=secinicial1.tolist()
        #en este punto ya tenemos la secuencia inicial, ordenada de mayor a menor por la suma de sus tiempos de proceso
        #para las secuencias que vamos viendo, se probará con unos cirujanos que asigne el método a cada consulta. 
        # print(secinicial)
        pi=[secinicial[0]]#el primer elemento de la secuencia es el primero de la inicial
        hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
        hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
        FOpi=cajanegrasecuencia(pi)
        hcc=hcccopia.copy()#para que las pruebas no alteren el real
        hcor=hcorcopia.copy()
        
        piinicial=secinicial.copy()#el primer elemento de la secuencia es el primero de la inicial
        hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
        hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
        FOpiinicial=cajanegrasecuencia(piinicial)
        hcc=hcccopia.copy()#para que las pruebas no alteren el real
        hcor=hcorcopia.copy()
        print('FOpiinicial antes de NEH', FOpiinicial)
        
        j=1
        while j<len(secinicial):
            
            i=0
            secprobando=pi[:]
            # print('secuencia que estamos probando', secprobando)
            flagcambiado=0
            while i<=j:
                secprobando.insert(i, secinicial[j])
                # print('secuencia probando, insertamos en la posición', secprobando,i)
               
                hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
                hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
                FOprobando=cajanegrasecuencia(secprobando)
                hcc=hcccopia.copy()#para que las pruebas no alteren el real
                hcor=hcorcopia.copy()
                
                if mejora(FOprobando,FOpi):
                    
                    pi=secprobando.copy()
                    hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
                    hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
                    FOpi=cajanegrasecuencia(pi)
                    hcc=hcccopia.copy()#para que las pruebas no alteren el real
                    hcor=hcorcopia.copy()
                    
                    
                    flagcambiado=1
                 #no se ha añadido ningún número a la secuencia y terminamos el bucle
                secprobando.pop(i)
                i=i+1
            if flagcambiado==0: #si no ha mejorado, se inserta el paciente en última posición
                secprobando.insert(i-1,secinicial[j])
                pi=secprobando[:]
                hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
                hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
                FOpi=cajanegrasecuencia(pi)
                hcc=hcccopia.copy()#para que las pruebas no alteren el real
                hcor=hcorcopia.copy()
            j=j+1
            #fin del NEH. Tenemos FOpi y pi
        print('NEH tarda', time.time()-inicio)
            
        if mejora(FOpi,FOpiinicial):#si el NEH ha mejorado la secuencia que teniamos inicialmente
            pibest=pi.copy()
            hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
            hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
            FOpibest=cajanegrasecuencia(pibest)
            hcc=hcccopia.copy()#para que las pruebas no alteren el real
            hcor=hcorcopia.copy()
        else:
            pibest=piinicial.copy()
            hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
            hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
            FOpibest=cajanegrasecuencia(piinicial)
            hcc=hcccopia.copy()#para que las pruebas no alteren el real
            hcor=hcorcopia.copy()   
            
        print('FOpibest con la secuencia tras NEH y antes de LS', FOpibest)        
        
        Temp=1
        inicio=time.time()
        while time.time()-inicio<len(pacientes)*(numor+numc)*0.025:#tiempo de parada según TFG MARIANGELES
            piprima=pi.copy()
            destruida=destruction(piprima)#destruction phase
            inicio1=time.time()
            piprima=construction(destruida[0],destruida[1]) #construction phase
            print('construccion tarda',time.time()-inicio1)
            
            #LOCAL SEARCH#
            iniciols=time.time()
            n=len(piprima)
            i=0
            j=0
            piprimaprima=piprima.copy()
            hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
            hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
            FOpiprimaprima=cajanegrasecuencia(piprimaprima)
            print('FO tras construccion', FOpiprimaprima)
            hcc=hcccopia.copy()#para que las pruebas no alteren el real
            hcor=hcorcopia.copy()
            while j<n:
                i=0
                while i<n:
                    secprima=piprima.copy()
                    secprima.remove(piprima[j])
                    secprima.insert(i,piprima[j])
                    hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
                    hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
                    FOsecprima=cajanegrasecuencia(secprima)
                    hcc=hcccopia.copy()#para que las pruebas no alteren el real
                    hcor=hcorcopia.copy()
                    
                    if mejora(FOsecprima,FOpiprimaprima):
                        piprimaprima=secprima.copy()
                        hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
                        hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
                        FOpiprimaprima=cajanegrasecuencia(piprimaprima)
                        hcc=hcccopia.copy()#para que las pruebas no alteren el real
                        hcor=hcorcopia.copy()
                    i=i+1
                j=j+1
            #FIN LOCAL SEARCH
            print('LS tarda',time.time()-iniciols)
            if mejora(FOpiprimaprima,FOpi):
                pi=piprimaprima.copy()
                hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
                hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
                FOpi=cajanegrasecuencia(pi)
                hcc=hcccopia.copy()#para que las pruebas no alteren el real
                hcor=hcorcopia.copy()
                if mejora(FOpi,FOpibest):
                    pibest=pi.copy()
                    hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
                    hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
                    FOpibest=cajanegrasecuencia(pibest)
                    hcc=hcccopia.copy()#para que las pruebas no alteren el real
                    hcor=hcorcopia.copy()
            elif random.uniform(0, 1)<=-math.exp(-(FOpiprimaprima[1]-FOpi[1])/Temp):
                print('se acepta peor solucion')
                pi=piprimaprima.copy()
                hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
                hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
                FOpi=cajanegrasecuencia(pi)
                hcc=hcccopia.copy()#para que las pruebas no alteren el real
                hcor=hcorcopia.copy()
            Temp=0.99*Temp
        
        hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
        hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
        FOpibest=cajanegrasecuencia(pibest)
        hcc=hcccopia.copy()#para que las pruebas no alteren el real
        hcor=hcorcopia.copy()
        print('FOpibest tras LS', FOpibest)            
       
        #aquí ya tendríamos IG para la secuencia
        #aplicamos ahora el IG para la asignación de cirujanos
        ccpibest=cirujanosconsultas.copy()
        ccsec=cirujanosconsultas.copy()#Se parte de esta asignación para realizar e NEH
        

        hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
        hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
        FOcc=cajanegra(pibest,ccsec)
        hcc=hcccopia.copy()#para que las pruebas no alteren el real
        hcor=hcorcopia.copy()
        
        #Se realiza una búsqueda para en cada consulta de especialidad insertar todos los cirujanos posibles y analizar con cuál de ellos se comporta mejor el programa
        j=0
        cirujanosdelaunidad=[]
        while j<numc:
            if consultas[j]=='General':
                ccsec[j]=[]
            j=j+1
        j=0
        while j<numc:
            if consultas[j]=='Especialidad':
                for i in cirujanos:
                    
                    if exp[i][especialidades[j]]>0 and descanso[i][dia]==0 and [i] not in ccsec:
                        cirujanosdelaunidad.append(i)
                k=0
                while k<len(cirujanosdelaunidad):
                    ccsec[j]=[cirujanosdelaunidad[k]]
                    hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
                    hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
                    FOcc=cajanegra(pibest,ccsec)
                    
                    #ASIGNACION DE CIRUJANOS A CONSULTAS GENERALES SEGÚN MENORES HORAS DE CONSULTA ACUMULADAS#
                    
                    cirujanoslibres = []#lista de cirujanos que pertenecen a la unidad del paciente
                    r=0
                    while r<len(cirujanos):
                        if [r] not in ccsec and [r] not in cirujanosor and [r] not in asistentesor and descanso[r][dia]==0:#si el cirujano que estamos viendo es de la unidad
                            cirujanoslibres.append(r)
                        r=r+1
                    #ordenamos los cirujanoslibres según las horas de consulta que lleven
                    r=0
                    horas=[]
                    for r in range(len(cirujanoslibres)):
                        horas.append(hcc[cirujanoslibres[r]])
                    horasnumpy=np.array(horas)
                    cirujanoslibresnumpy = np.array(cirujanoslibres)
                    np.argsort(horasnumpy)
                    cirujanoslibres = cirujanoslibresnumpy[horasnumpy.argsort()].tolist()
                    
                    r=0
                    i=0
                    while i<numc and r<len(cirujanoslibres):
                        if consultas[i]=='General' and dispcons[i][dia]>0:
                            ccsec[i]=[cirujanoslibres[r]]
                            r=r+1
                        i=i+1
                    
                    hcc=hcccopia.copy()#para que las pruebas no alteren el real
                    hcor=hcorcopia.copy()
                    
                    
                    hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
                    hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
                    FOcc=cajanegra(pibest,ccsec)
                    hcc=hcccopia.copy()#para que las pruebas no alteren el real
                    hcor=hcorcopia.copy()
                    
                    if mejora(FOcc,FOpibest):
                        FOpibest=FOcc[:]
                        ccpibest=ccsec.copy()
                    k=k+1
            j=j+1
                        
        FOccbest=FOpibest[:]
        ccbest=ccpibest.copy()
        

    # #aquí ya tendríamos FOccbest y ccbest, que serían las mejores soluciones tras el IG

        print('FO con los cirujs tras LS', FOccbest)
        secuencia=pibest.copy()
        cirujanosconsultas=ccbest.copy()
        FO=cajanegra(secuencia, cirujanosconsultas) #FO DEFINITIVA#

        print('MEJOR FO DEFINITIVA',FO)
        print('ctor',ctor)
        print('ctconsultas', ctconsultas)
        sumaFO=sumaFO+FO[3]
        
        actualizarexcel(pacientesaborrar)
        dia=dia+1
        #para obtener las horas de finalización de las consultas y quirófanos#
        i=0
        while i<numc:
            utilicons=ctconsultas[i][-1]+utilicons
            i=i+1
        
        i=0
        while i<numor:
            utilior=ctor[i][-1]+utilior
            i=i+1
        print('dia y ctconsultas', dia, ctconsultas)
        print('ctor', ctor)
    
    eficienciaconsultas=utilicons/(sum(sum(dispcons))/60)
    eficienciaor=utilior/(horasq*np.count_nonzero(dispq == 1))
    escribirsol(listaciruj, listaasist, listapacs, estadooriginal, pacientesoriginales)
    return sumaFO, eficienciaor, eficienciaconsultas

eficienciaconsultas=0
eficienciaor=0
sumaFO=0
# original=r"D:\Documents\ETSI\EXTENSIONTFG\A2\instancia.xlsx"
# nuevo=r"D:\Documents\ETSI\EXTENSIONTFG\A2\data.xlsx"
# shutil.copyfile(original, nuevo)
print('empieza IG1LS')
inicio=time.time()
ig1ls=IG1LS()
# tig1ls=time.time()-inicio

# nc=[numc]
# nor=[numor]
# FOig1ls=[ig1ls[0]]
# utilizacionconsultas=[ig1ls[2]]
# utilizacionOR=[ig1ls[1]]
# tiempoig1ls=[tig1ls]

                    
# df = pd.DataFrame({'numc':nc,
#                       'numor':nor,
#                        'FO IG1LS':FOig1ls,
#                        'UtilizaciónConsultas':utilizacionconsultas,
#                        'Utilizacion OR': utilizacionOR,
#                        'Tiempo IG1LS':tiempoig1ls,

                      
#     })
# with pd.ExcelWriter('analisis.xlsx') as writer:
#       df.to_excel(writer, sheet_name = "ANÁLISIS DE RESULTADOS")        
      