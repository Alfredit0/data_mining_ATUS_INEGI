# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 01:26:58 2018

@author: Alfredo
"""
# librerias
import numpy as np
from pandas import Series,DataFrame
import pandas as pd
from paretochart import pareto
import matplotlib.pyplot as plt
from pandas.tools.plotting import table
import os # módulo que provee funciones del sistema operativo

#Se definen las columnas a analizar como variables nominales
columnas=['ABREVIATURA_ENTIDAD','NOM_MUNICIPIO','MES','ID_HORA','ID_DIA',
       'DIASEMANA', 'URBANA', 'SUBURBANA', 'TIPACCID', 'AUTOMOVIL', 'CAMPASAJ',
       'MICROBUS','PASCAMION','OMNIBUS','TRANVIA','CAMIONETA','CAMION',
       'TRACTOR','FERROCARRI','MOTOCICLET','BICICLETA','OTROVEHIC',
       'CAUSAACCI','CAPAROD','SEXO','ALIENTO','CINTURON',
       'CONDMUERTO','CONDHERIDO','PASAMUERTO','PASAHERIDO','PEATMUERTO',
       'PEATHERIDO','CICLMUERTO','CICLHERIDO','OTROMUERTO','OTROHERIDO',
       'NEMUERTO','NEHERIDO','CLASACC']

#Cargar el data set
datos=pd.read_table('ATUS_2012.csv', usecols=columnas,
                    skipinitialspace=True, sep=','); #usecols=field
for columna in columnas:
    #columna = 'MES'
    #convirtiendo datos numericos a cadenas
    datos[columna] = datos[columna].astype(str)
    #calculando el conteo de las frecuencias para variable (columna)
    frecuencias = datos[columna].value_counts(ascending=False)
      
    #se obtiene el tamanio de la muestra
    tam_muestra=frecuencias.sum(axis=0)
    
    #Frecuencias relativas
    frecuencias_rel=frecuencias.transform(lambda x: (x/tam_muestra) * 100)
    
    #Frecuencias relativas acumuladas
    frecuencias_acum=frecuencias_rel.copy()
    i=1
    while i<frecuencias_acum.size:
        frecuencias_acum[i]=frecuencias_acum[i]+frecuencias_acum[i-1]
        i+=1    
    
    #Formateando datos
    frecuencias_rel=frecuencias_rel.transform(lambda x: '{0:.1f}%'.format(x))
    
    frecuencias_acum=frecuencias_acum.transform(lambda x: '{0:.1f}%'.format(x))
    
    #Se crea directorio para guardar el analisis de cada variable
    os.mkdir(columna) # crea una carpeta en la ruta del script
    #Dibujando Grafica de Pareto
    data = frecuencias
    
    labels = frecuencias_rel.keys()
    
    plt.rcParams['figure.figsize']=(20,8)
    
    # create a grid of subplots
    fig, axes = plt.subplots(1, 1)
    if (labels.size>20):
        pareto(data, labels, axes=0, limit=0.80, line_args=('r',), data_kw={'width': 0.8,
        'color': 'b'}, limit_kw={'color': 'g'})
    else:
        pareto(data, labels, axes=0, line_args=('r',), data_kw={'width': 0.8,
        'color': 'b'}, limit_kw={'color': 'g'})
    plt.ylabel('Frecuencia relativa acumulada', fontsize=14)
    #plt.title('Pareto - Analisis', fontsize=14)
    
    fig.canvas.set_window_title('Pareto Plot')
    
    plt.savefig(columna+'/analisis-pareto.tif', dpi=100)
    
    #Guardando imagen de las tablas de informacion
    df = frecuencias.to_frame()
    
    df.columns = ['Hechos de tránsito']
    df['Frec. Rel'] = frecuencias_rel
    df['Frec. Rel. Acum.'] = frecuencias_acum
    #Añandiendo columa principal
    df[columna] = df.index
    colnames = df.columns.tolist()
    colnames = colnames[-1:] + colnames[:-1]
    df = df[colnames]
    df.to_excel(columna+'/tabla-pareto.xls')
    fig, ax = plt.subplots(figsize=(12, 8)) # set size frame
    ax.axis('off')
    tabla = table(ax, df, loc='upper center', colWidths=[0.20]*len(df.columns))  # where df is your data frame
    tabla.auto_set_font_size(False) # Activate set fontsize manually
    tabla.set_fontsize(12) # if ++fontsize is necessary ++colWidths
    tabla.scale(1.2, 1.2) # change size table
    plt.savefig(columna+'/tabla-analisis-pareto.tif', dpi=100)