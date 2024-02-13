# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 12:11:40 2022

@author: claud
"""


import pandas as pd
import numpy as np 
import random
import math
import shutil
import time


def IG1LS():
    
    global descanso, dispcons, dia, hcor, hcc, numc, numor, wt,we,wc,wu,ctor, ctcc, cirujanos, asistentesor, cirjasoc, cirujanosconsultas, cirujanosor, ctconsultas, ctor, pacientes, pacientesaborrar, pacientesconsultas, pacientesor, tiempoacum
    global listaciruj, listaasist, listapacs
    global sumaFO
    
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
            if patients[j]==[] and dispcons[j][dia]==1:
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
            global datospacientes, pacientes, cirjasoc, dp, trp, dq, trq, u, hp, hs, dc, trc, pesos, estado, cirjasoc, tiempoacum, datoscirujanos, cirujanos, exp, uc
            
            datospacientes = pd.read_excel("data.xlsx", "Pacientes")

            pacientes = datospacientes['Número paciente'].tolist()

            dp = datospacientes['dp'].tolist()

            trp = datospacientes['trp'].tolist()

            dq = datospacientes['dq'].tolist()

            trq = datospacientes['trq'].tolist()

            u = datospacientes['u'].tolist()

            hp = datospacientes['hp'].tolist()

            hs = datospacientes['hs'].tolist()

            dc = datospacientes['dc'].tolist()

            trc = datospacientes['trc'].tolist()

            pesos = datospacientes['w'].tolist()

            estado = datospacientes['estado'].tolist()

            cirjasoc1 = datospacientes['cirujano'].fillna(999)#cambiamos cuando no hay valores por 0
            cirjasoc = [int(x) for x in cirjasoc1.tolist()]
            for x in range(len(cirjasoc)):
                if cirjasoc[x]==999:
                    cirjasoc[x]='NaN'       

            tiempoacum = datospacientes['tacum'].tolist()
    def cajanegra(secuencia,cc):
        
        global hcor, hcc, continuidad, numc, numor, wt,we,wc,wu,ctor, ctcc, cirujanos, asistentesor, cirjasoc, cirujanosor, ctconsultas, ctor, pacientes, pacientesaborrar, pacientesconsultas, pacientesor, tiempoacum
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
                    if estado[x]==0:
                        if tiempoacum[x]>trp[x]:
                            # print('el paciente {} va tarde a {}'.format(pacientes[x],estado[x]))
                            late.append((tiempoacum[x]-trp[x])*pesos[x])
                    if estado[x]==1:
                        if tiempoacum[x]>trq[x]:
                            # print('el paciente {} va tarde a {}'.format(pacientes[x],estado[x]))
                            late.append((tiempoacum[x]-trq[x])*pesos[x])
                    if estado[x]==2:
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
                global numc
                global hcc
                j=0
                cirujanosdelaunidad = []#lista de cirujanos que pertenecen a la unidad del paciente
                while j<len(cirujanos):
                    if exp[j][u[paciente]]>0:#si el cirujano que estamos viendo es de la unidad
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
                    if asignadoenconsulta!='NaN' and dispcons[asignadoenconsulta][dia]==1 and consultas[asignadoenconsulta]!='General':#el cirujano sí está asignado a la consulta asignadoenconsulta
                        if (consultas[asignadoenconsulta]=='Especialidad' and u[paciente]==especialidades[asignadoenconsulta]) or consultas[asignadoenconsulta]=='Nominativa':
                            if ctconsultas[asignadoenconsulta][-1]+dp[paciente]<=6:#ponemos 6h de consulta al dia
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
                asignadoenconsulta=asignadodia(cirjasoc[paciente],'consulta')
                asignadoenOR = asignadodia(cirjasoc[paciente],'OR')
                if asignadoenconsulta!='NaN' and asignadoenOR=='NaN'  and descanso[cirjasoc[paciente],dia]==0 and dispcons[asignadoenconsulta][dia] and consultas[asignadoenconsulta]!='General':#el cirujano sí está asignado a la consulta asignadoenconsulta
                    if (consultas[asignadoenconsulta]=='Especialidad' and u[paciente]==especialidades[asignadoenconsulta]) or consultas[asignadoenconsulta]=='Nominativa':
                        if ctconsultas[asignadoenconsulta][-1]+dc[paciente]<=6:#ponemos 6h de consulta al dia
                            return [asignadoenconsulta,cirjasoc[paciente]]
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
                    if exp[j][u[paciente]]>0 and hp[paciente]<=exp[j][u[paciente]] and descanso[j,dia]==0:#si el cirujano que estamos viendo es de la unidad y tiene experiencia suficiente
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
                if cirjasoc[paciente] in cirujanosexpunidad:
                    cirujanosexpunidad.remove(cirjasoc[paciente])
                    cirujanosexpunidad.insert(0,cirjasoc[paciente])
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
                             if ctor[asignadoenOR][-1]+dq[paciente]<=8 and [cirujanosexpunidad[j]] not in asistentesor:#ponemos 8h de OR al dia
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
                            if ctor[asignadoenOR][-1]+dq[paciente]<=8 and [i] not in asistentesor:#le asignamos este hueco en la consulta
                                # print('sí habría hueco en su OR')
                                if asistentesor[asignadoenOR]!=[]:
                                    if asistentesor[asignadoenOR][-1] in asistexp and asistentesor[asignadoenOR][-1]!=i :
                                        return [asignadoenOR,i,asistentesor[asignadoenOR][-1]]
                                        flagyatieneasist=1  
                                if asistentesor[asignadoenOR]==[]:
                                    for k in asistexp:
                                        if asignadodia(k, 'OR')=='NaN' and asignadodia(k, 'consulta') == 'NaN' and k!=i:
                                            return [asignadoenOR, i, k]
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
            atendidos=0
            pacientesaborrar=[]
            petapauno=0
            continuidad=0
            for k in pacientes:
                if k not in secuencia:
                    tiempoacum[indice(pacientes,k)]=tiempoacum[indice(pacientes,k)]+1 #los pacientes que no estén en la sec, igualmente no se van a procesar y se les añade un día a su tiempo acum
                if estado[indice(pacientes,k)]==1:
                    petapauno=petapauno+1
            for k in range(len(secuencia)): #x es el indice del paciente
                # print(' se ve al paciente {}'.format(secuencia[k]))
                if estado[indice(pacientes,secuencia[k])]==0:
                    retorno=busquedaPAE(indice(pacientes,secuencia[k])) #[consulta,cirujprincipal]
                    if retorno!='NaN':
                        pacientesconsultas[retorno[0]].append(secuencia[k])
                        ctconsultas[retorno[0]].append(ctconsultas[retorno[0]][-1]+dp[indice(pacientes,secuencia[k])])
                        hcc[retorno[1]]=hcc[retorno[1]]+dp[indice(pacientes,secuencia[k])]
                        tiempoacum[indice(pacientes,secuencia[k])]=0#se pone el +1 porque el día 0 aumenta 1 día
                        cirjasoc[indice(pacientes,secuencia[k])]=retorno[1]
                        flagcambiado=1
                        atendidos=atendidos+1
                    else: 
                        flagcambiado=0
                        tiempoacum[indice(pacientes,secuencia[k])]=tiempoacum[indice(pacientes,secuencia[k])]+1
                if estado[indice(pacientes,secuencia[k])]==1:
                    retorno=busquedaOR(indice(pacientes,secuencia[k])) #me devuelve [consulta,cirujprincipal,asistente]
                    if retorno!='NaN':
                        if retorno[1]==cirjasoc[indice(pacientes,secuencia[k])]:
                            continuidad = continuidad+1
                        cirujanosor[retorno[0]]=[retorno[1]]
                        hcor[retorno[1]]=hcc[retorno[1]]+dq[indice(pacientes,secuencia[k])]
                        pacientesor[retorno[0]].append(secuencia[k])
                        ctor[retorno[0]].append(ctor[retorno[0]][-1]+dq[indice(pacientes,secuencia[k])])
                        cirjasoc[indice(pacientes,secuencia[k])]=retorno[1]
                        tiempoacum[indice(pacientes,secuencia[k])]=0 #se actualiza el tiempo acumulado.
                        if retorno[2]!='NaN':
                            asistentesor[retorno[0]]=[retorno[2]]
                            hcor[retorno[2]]=hcor[retorno[2]]+dq[indice(pacientes,secuencia[k])]
                        flagcambiado=1
                        atendidos=atendidos+1
                    else: 
                        flagcambiado=0
                        tiempoacum[indice(pacientes,secuencia[k])]=tiempoacum[indice(pacientes,secuencia[k])]+1 #se actualiza el tiempo acumulado.
                if estado[indice(pacientes,secuencia[k])]==2:
                    retorno=busquedaPOSTOP(indice(pacientes,secuencia[k])) #me devuelve [consulta,cirujprincipal]
                    if retorno!='NaN':
                        pacientesconsultas[retorno[0]].append(secuencia[k])
                        ctconsultas[retorno[0]].append(ctconsultas[retorno[0]][-1]+dc[indice(pacientes,secuencia[k])])
                        #habría que eliminar al paciente de la lista
                        hcc[retorno[1]]=hcc[retorno[1]]+dc[indice(pacientes,secuencia[k])] 
                        flagcambiado=1
                        atendidos=atendidos+1
                        tiempoacum[indice(pacientes,secuencia[k])]=0 #se actualiza el tiempo acumulado.
                        # borramos todo lo del paciente en cuestión, ya que ya ha terminado su ciclo en el hospital#
                        pacientesaborrar.append(pacientes[indice(pacientes,secuencia[k])])
                        
                    else: 
                        flagcambiado=0
                        tiempoacum[indice(pacientes,secuencia[k])]=tiempoacum[indice(pacientes,secuencia[k])]+1
                
                if flagcambiado==1 and (estado[indice(pacientes,secuencia[k])]==0 or estado[indice(pacientes,secuencia[k])]==1):
                    estado[indice(pacientes,secuencia[k])]=estado[indice(pacientes,secuencia[k])]+1
                    if estado[indice(pacientes,secuencia[k])]==1:
                        mu=random.randint(1,4)
                        sigma=random.choice([0.1*mu,0.2*mu,0.3*mu,0.4*mu,0.5*mu])
                        dq[indice(pacientes,secuencia[k])]=abs(random.normalvariate(mu, sigma))
            
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
            utilizacion=(utilizacionor+utilizacionc)/(8*numor+6*numc)
            return eq/32*we,tarde/(332*15*len(pacientes))*wt,utilizacion*wu,eq/32*we+wt*tarde/(332*15*len(pacientes))-wu*utilizacion-wc*continuidad/petapauno
         
        #vamos a tener un libro excel, con una hoja cada día. Habrá una columna de 'cirujanos, asistente, paciente', otra para consultas y OR
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
        global hcor, hcc, continuidad, numc, numor, ctor, wt,we,wc,wu,ctcc, cirujanos, asistentesor, cirjasoc, cirujanosor, ctconsultas, ctor, pacientes, pacientesaborrar, pacientesconsultas, pacientesor, tiempoacum
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
                    if estado[x]==0:
                        if tiempoacum[x]>trp[x]:
                            late.append((tiempoacum[x]-trp[x])*pesos[x])
                    if estado[x]==1:
                        if tiempoacum[x]>trq[x]:
                            late.append((tiempoacum[x]-trq[x])*pesos[x])
                    if estado[x]==2:
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
                global numc
                global hcc
                j=0
                cirujanosdelaunidad = []#lista de cirujanos que pertenecen a la unidad del paciente
                while j<len(cirujanos):
                    if exp[j][u[paciente]]>0 and descanso[j,dia]==0:#si el cirujano que estamos viendo es de la unidad
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
                        if (consultas[asignadoenconsulta]=='Especialidad' and u[paciente]==especialidades[asignadoenconsulta]) or consultas[asignadoenconsulta]=='Nominativa':
                            if ctconsultas[asignadoenconsulta][-1]+dp[paciente]<=6:#ponemos 6h de consulta al dia
                                # print('sí hay hueco en la consulta')
                                return [asignadoenconsulta,cirujanosdelaunidad[j]]
                                flagyatieneconsulta=1
                                break                   
                    if flagyatieneconsulta==1:break
                    j=j+1
                if flagyatieneconsulta==0:#si no tiene consulta en toda la semana ningún cirujano, se le asigna al primero la primera consulta libre
                    j=0
                    
                    while j<len(cirujanosconsultas):
                        if cirujanosconsultas[j]==[] and dispcons[j][dia]==1 and consultas[j]!='General':#si la consulta está libre
                            x=0
                            for x in cirujanosdelaunidad:
                                if asignadodia(x, 'OR')=='NaN' and asignadodia(x, 'consulta')=='NaN': # or asignadodia(x, 'consulta', dia)==j):
                                    #si el cirujano no tiene OR asignado ese día, y si tiene consultas que sean esa misma,
                                    # print('entroaqui')
                                    if consultas[j]=='Especialidad' and u[paciente]==especialidades[j] and candidatos[j][x]==1:
                                        return [j,x]
                                        flagyatieneconsulta=1
                                        break#cuando se le asigna, se sale del for
                                    if consultas[j]=='Nominativa' and candidatos[j][x]==1:
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
               
                asignadoenconsulta=asignadodia(cirjasoc[paciente],'consulta')
                asignadoenOR = asignadodia(cirjasoc[paciente],'OR')
                if asignadoenconsulta!='NaN' and asignadoenOR=='NaN' and descanso[cirjasoc[paciente],dia]==0 and consultas[asignadoenconsulta]!='General':#el cirujano sí está asignado a la consulta asignadoenconsulta
                    if (consultas[asignadoenconsulta]=='Especialidad' and u[paciente]==especialidades[asignadoenconsulta]) or consultas[asignadoenconsulta]=='Nominativo':
                        if ctconsultas[asignadoenconsulta][-1]+dc[paciente]<=6:#ponemos 6h de consulta al dia
                            return [asignadoenconsulta,cirjasoc[paciente]]
                            flagyatieneconsulta=1
                if flagyatieneconsulta==0:#e ciruj asoc no está en ninguna consulta ningún día
                    #se le asigna el primer hueco que haya en la semana
                    j=0
                    
                    while j<len(cirujanosconsultas):
                        if  cirujanosconsultas[j]==[] and dispcons[j][dia]==1 and consultas[j]!='General':#este es la consulta donde se asignará el cirujano
                            if asignadoenconsulta=='NaN' and asignadoenOR=='NaN' and descanso[cirjasoc[paciente],dia]==0:#si el cirujano no tiene OR asignado ese día, puede asignarse a consultas
                                if (consultas[j]=='Especialidad' and u[paciente]==especialidades[j] and candidatos[j][cirjasoc[paciente]]==1) or (consultas[j]=='Nominativa' and candidatos[j][cirjasoc[paciente]]==1):
                                    return [j,cirjasoc[paciente]]
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
                    if exp[j][u[paciente]]>0 and hp[paciente]<=exp[j][u[paciente]] and descanso[j,dia]==0:#si el cirujano que estamos viendo es de la unidad y tiene experiencia suficiente
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
                if cirjasoc[paciente] in cirujanosexpunidad:
                    cirujanosexpunidad.remove(cirjasoc[paciente])
                    cirujanosexpunidad.insert(0,cirjasoc[paciente])
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
                             if ctor[asignadoenOR][-1]+dq[paciente]<=8 and [cirujanosexpunidad[j]] not in asistentesor:#ponemos 8h de OR al dia
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
                             if ctor[j][-1]==0 and dispq[j][dia]:#eL OR está libre, no tiene ninguna operación programada
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
                            if ctor[asignadoenOR][-1]+dq[paciente]<=8 and [i] not in asistentesor:#le asignamos este hueco en la consulta
                                # print('sí habría hueco en su OR')
                                if asistentesor[asignadoenOR]!=[]:
                                    if asistentesor[asignadoenOR][-1] in asistexp and asistentesor[asignadoenOR][-1]!=i :
                                        return [asignadoenOR,i,asistentesor[asignadoenOR][-1]]
                                        flagyatieneasist=1  
                                if asistentesor[asignadoenOR]==[]:
                                    for k in asistexp:
                                        if asignadodia(k, 'OR')=='NaN' and asignadodia(k, 'consulta') == 'NaN' and k!=i:
                                            return [asignadoenOR, i, k]
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
                                    if ctor[x][-1]==0 and dispq[x][dia]:#le asignamos este OR
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
            atendidos=0
            pacientesaborrar=[]
            petapauno=0
            continuidad=0
            for k in pacientes:
                if k not in secuencia:
                    tiempoacum[indice(pacientes,k)]=tiempoacum[indice(pacientes,k)]+1
                if estado[indice(pacientes,k)]==1:
                    petapauno=petapauno+1
            for k in range(len(secuencia)): #x es el indice del paciente
                # print(' se ve al paciente {}'.format(secuencia[k]))
                if estado[indice(pacientes,secuencia[k])]==0:
                    # print('vamos a busquedaPAE ')
                    retorno=busquedaPAE(indice(pacientes,secuencia[k])) #[consulta,cirujprincipal]
                    # print(retorno)
                    if retorno!='NaN':
                        
                        cirujanosconsultas[retorno[0]]=[retorno[1]]
                        pacientesconsultas[retorno[0]].append(secuencia[k])
                        ctconsultas[retorno[0]].append(ctconsultas[retorno[0]][-1]+dp[indice(pacientes,secuencia[k])])
                        hcc[retorno[1]]=hcc[retorno[1]]+dp[indice(pacientes,secuencia[k])]
                        tiempoacum[indice(pacientes,secuencia[k])]=0#se pone el -1 porque el día 0 aumenta 1 día
                        cirjasoc[indice(pacientes,secuencia[k])]=retorno[1]
                        # print(equilibrio(hcc,hcor))
                        # print('se asigna el paciente {} a la consulta {} el día  con el cirujano {}'.format(secuencia[x],retorno[0],retorno[1]))
                        flagcambiado=1
                        atendidos=atendidos+1
                    else:
                        flagcambiado=0
                        tiempoacum[indice(pacientes,secuencia[k])]=tiempoacum[indice(pacientes,secuencia[k])]+1
                if estado[indice(pacientes,secuencia[k])]==1:
                    # print('vamos a OR')
                    retorno=busquedaOR(indice(pacientes,secuencia[k])) #me devuelve [consulta,cirujprincipal,asistente]
                    # print(retorno)
                    if retorno!='NaN':
                        if retorno[1]==cirjasoc[indice(pacientes,secuencia[k])]:
                            continuidad = continuidad+1
                        # print('se asigna el paciente {} al OR {} el día con el cirujano {} y con asistente {}'.format(secuencia[x],retorno[0],retorno[1],retorno[2]))
                        cirujanosor[retorno[0]]=[retorno[1]]
                        hcor[retorno[1]]=hcc[retorno[1]]+dq[indice(pacientes,secuencia[k])]
                        pacientesor[retorno[0]].append(secuencia[k])
                        ctor[retorno[0]].append(ctor[retorno[0]][-1]+dq[indice(pacientes,secuencia[k])])
                        cirjasoc[indice(pacientes,secuencia[k])]=retorno[1]
                        tiempoacum[indice(pacientes,secuencia[k])]=0 #se actualiza el tiempo acumulado.
                        if retorno[2]!='NaN':
                            asistentesor[retorno[0]]=[retorno[2]]
                            hcor[retorno[2]]=hcor[retorno[2]]+dq[indice(pacientes,secuencia[k])]
                        flagcambiado=1
                        atendidos=atendidos+1
                    else:
                        flagcambiado=0
                        tiempoacum[indice(pacientes,secuencia[k])]=tiempoacum[indice(pacientes,secuencia[k])]+1
                if estado[indice(pacientes,secuencia[k])]==2:
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
                        atendidos=atendidos+1
                        tiempoacum[indice(pacientes,secuencia[k])]=0 #se actualiza el tiempo acumulado.
                        # borramos todo lo del paciente en cuestión, ya que ya ha terminado su ciclo en el hospital#
                        pacientesaborrar.append(pacientes[indice(pacientes,secuencia[k])])                      
                        
                    else:
                        flagcambiado=0
                        tiempoacum[indice(pacientes,secuencia[k])]=tiempoacum[indice(pacientes,secuencia[k])]+1
                
                if flagcambiado==1 and (estado[indice(pacientes,secuencia[k])]==0 or estado[indice(pacientes,secuencia[k])]==1):
                    estado[indice(pacientes,secuencia[k])]=estado[indice(pacientes,secuencia[k])]+1
                    if estado[indice(pacientes,secuencia[k])]==1:
                        mu=random.randint(1,4)
                        sigma=random.choice([0.1*mu,0.2*mu,0.3*mu,0.4*mu,0.5*mu])
                        dq[indice(pacientes,secuencia[k])]=abs(random.normalvariate(mu, sigma))
            
            #ASIGNACION DE CIRUJANOS A CONSULTAS GENERALES SEGÚN MENORES HORAS DE CONSULTA ACUMULADAS#
            
            cirujanoslibres = []#lista de cirujanos que pertenecen a la unidad del paciente
            j=0
            while j<len(cirujanos):
                if j not in cirujanosconsultas and [j] not in cirujanosor and [j] not in asistentesor and descanso[j][dia]==0:#si el cirujano que estamos viendo es de la unidad
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
                if consultas[i]=='General':
                    cirujanosconsultas[i]=[cirujanoslibres[j]]
                    ctconsultas[i]=[6]
                    hcc[cirujanoslibres[j]]=hcc[cirujanoslibres[j]]+6
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
            utilizacion=(utilizacionor+utilizacionc)/(8*numor+6*numc)
            return eq/32*we,tarde/(332*15*len(pacientes))*wt,utilizacion*wu,eq/32*we+wt*tarde/(332*15*len(pacientes))-wu*utilizacion-wc*continuidad/petapauno
         
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
                    del cirjasoc[x]
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
        nuevodataframepacientes = pd.DataFrame({'Número paciente':pacientes,
                                        'dp':dp,
                                        'trp':trp,
                                        'dq':dq,
                                        'trq':trq,
                                        'u':u,
                                        'hp':hp,
                                        'hs':hs,
                                        'dc':dc,
                                        'trc':trc,
                                        'w':pesos,
                                        'estado':estado,
                                        'cirujano':cirjasoc,
                                        'tacum':tiempoacum
                                        })
        datoscirujanos = pd.DataFrame({'Número Cirujano': cirujanos,
                                        'G0':exp0,
                                        'G1':exp1,
                                        'G2':exp2,
                                        'G3':exp3,
                                        'G4':exp4,
                                        'G5':exp5,
                                        'G6':exp6,
                                        'G7':exp7,
                                        'Descanso Lunes':d1,
                                        'Descanso Martes':d2,
                                        'Descanso MIércoles':d3,
                                        'Descanso Jueves':d4,
                                        'Descanso Viernes':d5,
                                        'Descanso Sábado':d6,
                                        'Descanso Domingo':d7,                   
            })
        c=0
        C=[]
        while c<numc:
            C.append('C')
            c=c+1
        disponibilidades = pd.DataFrame({'Disponibilidad': C,
                                         'Lunes': disp1,
                                         'Martes': disp2,
                                         'Miércoles': disp3,
                                         'Jueves': disp4,
                                         'Viernes': disp5,
                                         'Sábado': disp6,
                                         'Domingo': disp7
            })
        o=0
        O=[]
        while o<numor:
            O.append('O')
            o=o+1
        disponibilidadesor = pd.DataFrame({'Disponibilidad': O,
                                         'Lunes': dispq1,
                                         'Martes': dispq2,
                                         'Miércoles': dispq3,
                                         'Jueves': dispq4,
                                         'Viernes': dispq5,
                                         'Sábado': dispq6,
                                         'Domingo': dispq7
            })
        
        pestanapesos = pd.DataFrame({'Tardiness': [wt],
                                     'Equilibrio': [we],
                                     'Utilizacion': [wu],
                                     'Continuidad': [wc]
            })
        horizontetemporal = pd.DataFrame({'Días del Horizonte Temporal':[ht]})
        
        with pd.ExcelWriter('data.xlsx') as writer:
            nuevodataframepacientes.to_excel(writer, sheet_name = "Pacientes")
            datoscirujanos.to_excel(writer, sheet_name = "Cirujanos")
            datos.to_excel(writer, sheet_name = "Datos")
            disponibilidades.to_excel(writer, sheet_name = "Disponibilidades Consultas")
            disponibilidadesor.to_excel(writer, sheet_name = "Disponibilidades Quirófanos")
            pestanapesos.to_excel(writer, sheet_name = "Pesos")
            horizontetemporal.to_excel(writer, sheet_name = "HT")
            ccsdataframe.to_excel(writer, sheet_name = "Consultas")
    def escribirsol(listaciruj,listaasist,listapacs):
        
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
        dfsol1 = pd.DataFrame({'Espacio':C+O,
                              'CIRUJANOS':listaciruj[0],
                              'ASISTENTES':listaasist[0],
                              'PACIENTES':listapacs[0]
                              
            })
        dfsol2 = pd.DataFrame({'Espacio':C+O,
                              'CIRUJANOS':listaciruj[1],
                              'ASISTENTES':listaasist[1],
                              'PACIENTES':listapacs[1]
                              
            })
        dfsol3 = pd.DataFrame({'Espacio':C+O,
                              'CIRUJANOS':listaciruj[2],
                              'ASISTENTES':listaasist[2],
                              'PACIENTES':listapacs[2]
                              
            })
        dfsol4 = pd.DataFrame({'Espacio':C+O,
                              'CIRUJANOS':listaciruj[3],
                              'ASISTENTES':listaasist[3],
                              'PACIENTES':listapacs[3]
                              
            })
        dfsol5 = pd.DataFrame({'Espacio':C+O,
                              'CIRUJANOS':listaciruj[4],
                              'ASISTENTES':listaasist[4],
                              'PACIENTES':listapacs[4]
                              
            })
        dfsol6 = pd.DataFrame({'Espacio':C+O,
                              'CIRUJANOS':listaciruj[5],
                              'ASISTENTES':listaasist[5],
                              'PACIENTES':listapacs[5]
                              
            })
        dfsol7 = pd.DataFrame({'Espacio':C+O,
                              'CIRUJANOS':listaciruj[6],
                              'ASISTENTES':listaasist[6],
                              'PACIENTES':listapacs[6]
                              
            })
        
        with pd.ExcelWriter('solucion.xlsx') as writer:
             dfsol1.to_excel(writer, sheet_name = "LUNES")
             dfsol2.to_excel(writer, sheet_name = "MARTES")
             dfsol3.to_excel(writer, sheet_name = "MIERCOLES")
             dfsol4.to_excel(writer, sheet_name = "JUEVES")
             dfsol5.to_excel(writer, sheet_name = "VIERNES")
             dfsol6.to_excel(writer, sheet_name = "SABADO")
             dfsol7.to_excel(writer, sheet_name = "DOMINGO")

    #LECTURA DE EXCEL#

    datos=pd.read_excel("data.xlsx", "Datos")
    numor = datos.loc[0,'Número de quirófanos']
    # print('Número de quirófanos en el hospital', numor)
    numc = datos.loc[0,'Número de consultas']
    # print('Número de consultas en el hospital', numc)
    #cirujanos#
    datoscirujanos = pd.read_excel("data.xlsx", "Cirujanos")
    cirujanos = datoscirujanos['Número Cirujano'].tolist()   
    exp0 = datoscirujanos['G0'].tolist()
    exp1 = datoscirujanos['G1'].tolist()
    exp2 = datoscirujanos['G2'].tolist()
    exp3 = datoscirujanos['G3'].tolist()
    exp4 = datoscirujanos['G4'].tolist()
    exp5 = datoscirujanos['G5'].tolist()
    exp6 = datoscirujanos['G6'].tolist()
    exp7 = datoscirujanos['G7'].tolist()
    exp = np.array([exp0,exp1,exp2,exp3,exp4,exp5,exp6,exp7])
    exp=exp.transpose()
    
    d1 = datoscirujanos['Descanso Lunes'].tolist()
    d2 = datoscirujanos['Descanso Martes'].tolist()
    d3 = datoscirujanos['Descanso Miércoles'].tolist()
    d4 = datoscirujanos['Descanso Jueves'].tolist()
    d5 = datoscirujanos['Descanso Viernes'].tolist()
    d6 = datoscirujanos['Descanso Sábado'].tolist()
    d7 = datoscirujanos['Descanso Domingo'].tolist()
    descanso = np.array([d1,d2,d3,d4,d5,d6,d7])
    descanso = descanso.transpose()
    
    disponibilidades = pd.read_excel("data.xlsx", "Disponibilidades Consultas")
    disp1 = disponibilidades['Lunes'].tolist()
    disp2 = disponibilidades['Martes'].tolist()
    disp3 = disponibilidades['Miércoles'].tolist()
    disp4 = disponibilidades['Jueves'].tolist()
    disp5 = disponibilidades['Viernes'].tolist()
    disp6 = disponibilidades['Sábado'].tolist()
    disp7 = disponibilidades['Domingo'].tolist()
    dispcons = np.array([disp1, disp2, disp3, disp4, disp5, disp6, disp7])
    dispcons = dispcons.transpose()
    
    disponibilidadesor = pd.read_excel("data.xlsx", "Disponibilidades Quirófanos")
    dispq1 = disponibilidadesor['Lunes'].tolist()
    dispq2 = disponibilidadesor['Martes'].tolist()
    dispq3 = disponibilidadesor['Miércoles'].tolist()
    dispq4 = disponibilidadesor['Jueves'].tolist()
    dispq5 = disponibilidadesor['Viernes'].tolist()
    dispq6 = disponibilidadesor['Sábado'].tolist()
    dispq7 = disponibilidadesor['Domingo'].tolist()
    dispq = np.array([dispq1, dispq2, dispq3, dispq4, dispq5, dispq6, dispq7])
    dispq = dispq.transpose()
    
    weights=pd.read_excel("data.xlsx", "Pesos")
    wt = weights.loc[0,'Tardiness']
    we = weights.loc[0,'Equilibrio']
    wu = weights.loc[0,'Utilizacion']
    wc = weights.loc[0,'Continuidad']
    
    htemp = pd.read_excel("data.xlsx", "HT")
    ht = htemp.loc[0,'Días del Horizonte Temporal']
    
    ccsdataframe = pd.read_excel("data.xlsx", "Consultas")
    
    consultas=ccsdataframe['Tipo'].tolist()
    especialidades=ccsdataframe['Unidad'].tolist()
    candidatos=ccsdataframe.iloc[:,3:].to_numpy()  #se obtiene la matriz de candidatos de los cirujanos
    
    leerexcel()

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
    
    eficienciaor=0
    eficienciaconsultas=0
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
       
    #     #aquí ya tendríamos IG para la secuencia
    #     #aplicamos ahora el IG para la asignación de cirujanos
    #     ccsec=cirujanosconsultas.copy()#Se parte de esta asignación para realizar e NEH
        
    #     ccinicial=ccsec[:]
    #     for x in cirujanos:f
    #         if [x] not in ccinicial and descanso[x,dia]==0:
    #             ccinicial.append([x])

    #     hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #     hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #     FOcc=cajanegra(pibest,ccsec)
    #     hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #     hcor=hcorcopia.copy()
        
    #     #SE NIVELA PARA QUE LOS CIRUJANOS QUE HAN SIDO ASIGNADOS A CONSULTAS Y AL FINAL SE QUEDAN SIN PACIENTES NO SE TENGAN EN CUENTA Y PUEDAN SER ASIGNADOS A OR
    #     hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #     hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #     s=nivelar(pacientesconsultas,ccsec[:numc])
    #     FOcc=cajanegra(pibest,s)
    #     hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #     hcor=hcorcopia.copy()
        
    #     cc=[ccinicial[0]]
    #     j=1
    #     #NEH#
    #     while j<len(ccinicial):
    #         i=0
    #         ccprobando=cc[:]
    #         flagcambiado=0
    #         while i<=j:
    #             ccprobando.insert(i,ccinicial[j])
    #             hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #             hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #             FOprobando=cajanegra(pibest,ccprobando[:numc])
    #             hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #             hcor=hcorcopia.copy()
                
    #             hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #             hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #             s=nivelar(pacientesconsultas,ccprobando[:numc])
    #             FOprobando=cajanegra(pibest,s)
    #             hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #             hcor=hcorcopia.copy()
                
    #             if mejora(FOprobando,FOcc):
    #                 cc=ccprobando[:]
    #                 hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #                 hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #                 FOcc=cajanegra(pibest,cc[:numc])
    #                 hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #                 hcor=hcorcopia.copy()
                    
    #                 hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #                 hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #                 s=nivelar(pacientesconsultas,cc[:numc])
    #                 FOcc=cajanegra(pibest,s)
    #                 hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #                 hcor=hcorcopia.copy()
                    
    #                 flagcambiado=1
    #             ccprobando.pop(i)
    #             i=i+1
    #         if flagcambiado==0:
    #             ccprobando.insert(i-1,ccinicial[j])
    #             cc=ccprobando[:]
          
    #             hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #             hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #             FOcc=cajanegra(pibest,cc[:numc])
    #             hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #             hcor=hcorcopia.copy()
                
    #             hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #             hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #             s=nivelar(pacientesconsultas,cc[:numc])
    #             FOcc=cajanegra(pibest,s)
    #             hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #             hcor=hcorcopia.copy()
                
    #         j=j+1
    #         #FIN NEH#

    #     FOccbest=FOcc[:]
    #     ccbest=cc.copy()
        
    #     print('Foccbest con el que se entra a LS', FOccbest)
    #     it=0
    #     Temp=1
    #     inicio=time.time()
    #     while time.time()-inicio<len(pacientes)*(numor+numc)*0.025:
    #         # ccprima=cc.copy()
    #         # FOccprima=FOcc[:]
    #         #destruccion
    #         ccdestruida=destruccion(ccbest)
    #         ccprima=construccion(ccdestruida[0],ccdestruida[1])
    #         hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #         hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #         FOccprima=cajanegra(pibest,ccprima[:numc])
    #         hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #         hcor=hcorcopia.copy()
            
    #         hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #         hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #         s=nivelar(pacientesconsultas,ccprima[:numc])
    #         FOccprima=cajanegra(pibest,s)
    #         hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #         hcor=hcorcopia.copy()
            
    #         #LOCAL SEARCH#
            
    #         n=len(ccprima)
    #         i=0
    #         j=0
    #         ccprimaprima=ccprima.copy()
    #         hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #         hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #         FOccprimaprima=cajanegra(pibest,ccprimaprima[:numc]) #es FOccprima
    #         hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #         hcor=hcorcopia.copy()
            
    #         hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #         hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #         s=nivelar(pacientesconsultas,ccprimaprima[:numc])
    #         FOccprimaprima=cajanegra(pibest,s)
    #         hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #         hcor=hcorcopia.copy()
            
    #         while j<n:
    #             i=0
    #             while i<n:
    #                 cirujanosprima=ccprima.copy()
    #                 cirujanosprima.remove(ccprima[j])
    #                 cirujanosprima.insert(i,ccprima[j])
    #                 hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #                 hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #                 FOcirujanosprima=cajanegra(pibest,cirujanosprima[:numc])
    #                 hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #                 hcor=hcorcopia.copy()
                    
    #                 hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #                 hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #                 s=nivelar(pacientesconsultas,cirujanosprima[:numc])
    #                 FOcirujanosprima=cajanegra(pibest,s)
    #                 hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #                 hcor=hcorcopia.copy()
                    
    #                 if mejora(FOcirujanosprima,FOccprimaprima):
    #                     ccprimaprima=ccprima.copy()   
    #                     hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #                     hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #                     FOccprimaprima=cajanegra(pibest,ccprimaprima[:numc])
    #                     hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #                     hcor=hcorcopia.copy()
                        
    #                     hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #                     hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #                     s=nivelar(pacientesconsultas,ccprimaprima[:numc])
    #                     FOccprimaprima=cajanegra(pibest,s)
    #                     hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #                     hcor=hcorcopia.copy()
    #                 i=i+1
    #                 if i>numc:#cuandobya el cirujano es asignado a consultas inexistentes, break
    #                     break
    #             j=j+1
                
    #         #FIN LOCAL SEARCH
                  
    #         if mejora(FOccprimaprima,FOcc):
    #             cc=ccprimaprima.copy()
                
    #             hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #             hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #             FOcc=cajanegra(pibest,cc[:numc])
    #             hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #             hcor=hcorcopia.copy()
                
    #             s=nivelar(pacientesconsultas,cc[:numc])
    #             hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #             hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #             FOcc=cajanegra(pibest,s)
    #             hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #             hcor=hcorcopia.copy()
                
    #             if mejora(FOcc,FOccbest):
    #                 ccbest=cc.copy()
    #                 hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #                 hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #                 FOccbest=cajanegra(pibest,ccbest[:numc])
    #                 hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #                 hcor=hcorcopia.copy()
                    
    #                 s=nivelar(pacientesconsultas,ccbest[:numc])
                    
    #                 hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #                 hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #                 FOccbest=cajanegra(pibest,s)
    #                 hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #                 hcor=hcorcopia.copy()
                    
    #         elif random.uniform(0, 1)<=-math.exp(-(FOccprima[1]-FOcc[1])/Temp):
    #             print('se acepta peor solucion')
    #             cc=ccprima.copy()
    #             hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
    #             hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
    #             FOcc=cajanegra(pibest,cc)
    #             hcc=hcccopia.copy()#para que las pruebas no alteren el real
    #             hcor=hcorcopia.copy()
    #         Temp=0.99*Temp
    #         it=it+1

    # #aquí ya tendríamos FOccbest y ccbest, que serían las mejores soluciones tras el IG

        # print('FO con los cirujs tras LS', FOccbest)
        # secuencia=pibest.copy()
        # cirujanosconsultas=ccbest.copy()
        # hcorcopia = hcor.copy() #horas cirujanos en OR a la semana
        # hcccopia = hcc.copy() #horas cada cirujano en consulta a la semana
        # FO=cajanegra(secuencia, cirujanosconsultas[:numc]) #FO DEFINITIVA#
        # hcc=hcccopia.copy()#para que las pruebas no alteren el real
        # hcor=hcorcopia.copy()

        s=nivelar(pacientesconsultas,cirujanosconsultas[:numc])
        FO=cajanegrasecuencia(pibest)
        print('MEJOR FO DEFINITIVA',FO)
        print('ctor',ctor)
        print('ctconsultas', ctconsultas)
        sumaFO=sumaFO+FO[3]
        
        actualizarexcel(pacientesaborrar)
        dia=dia+1
        #para obtener las horas de finalización de las consultas y quirófanos#
        i=0
    
        while i<numc:
            eficienciaconsultas=ctconsultas[i][-1]+eficienciaconsultas
            i=i+1
        
        i=0
        while i<numor:
            eficienciaor=ctor[i][-1]+eficienciaor
            i=i+1
        print('dia y ctconsultas', dia, ctconsultas)
        print('ctor', ctor)
    eficienciaconsultas=eficienciaconsultas/(6*numc*ht)
    eficienciaor=eficienciaor/(8*numor*ht)
    escribirsol(listaciruj, listaasist, listapacs)
    return sumaFO, eficienciaor, eficienciaconsultas

sumaFO=0
original=r"D:\Documents\ETSI\EXTENSIONTFG\A2\instancia.xlsx"
nuevo=r"D:\Documents\ETSI\EXTENSIONTFG\A2\data.xlsx"
shutil.copyfile(original, nuevo)
print('empieza IG1LS')
inicio=time.time()
ig1ls=IG1LS()
tig1ls=time.time()-inicio

nc=[numc]
nor=[numor]
FOig1ls=[ig1ls[0]]
utilizacionconsultas=[ig1ls[2]]
utilizacionOR=[ig1ls[1]]
tiempoig1ls=[tig1ls]

                    
df = pd.DataFrame({'numc':nc,
                      'numor':nor,
                       'FO IG1LS':FOig1ls,
                       'UtilizaciónConsultas':utilizacionconsultas,
                       'Utilizacion OR': utilizacionOR,
                       'Tiempo IG1LS':tiempoig1ls,

                      
    })
with pd.ExcelWriter('analisis.xlsx') as writer:
      df.to_excel(writer, sheet_name = "ANÁLISIS DE RESULTADOS")        
      