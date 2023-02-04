#%% Import required package
import pandas as pd
pd.set_option('display.float_format', lambda x: '%.1f' % x)

#%% Read all separate files
enero = pd.read_csv('./Datasets/dataset_multas_enero.csv', delimiter=';')
febrero = pd.read_csv('./Datasets/dataset_multas_febrero.csv', delimiter=';')
marzo = pd.read_csv('./Datasets/dataset_multas_marzo.csv', delimiter=';')
abril = pd.read_csv('./Datasets/dataset_multas_abril.csv', delimiter=';')
mayo = pd.read_csv('./Datasets/dataset_multas_mayo.csv', delimiter=';')
junio = pd.read_csv('./Datasets/dataset_multas_junio.csv', delimiter=';')


#%% Concatenate all files into a single dataframe
raw = pd.concat([enero, febrero, marzo, abril, mayo, junio])


#%% Adjust date and time data to correct formats
raw['HORA'] = [str(int(i))+':'+str(round(i%1,2))[str(round(i%1,2)).find('.')+1:].ljust(2, '0') + ':00' \
               for i in raw['HORA']]

raw['MES'] = ['2022' + '/' + str(i).rjust(2, '0') + '/01' for i in raw['MES']]


#%% Drop unnecessary / dirty fields
raw = raw.drop(['LUGAR', 'DESCUENTO', 'ANIO', 'COORDENADA-X', 'COORDENADA-Y                                                                                                                                  '], axis=1)

#%% Change datatypes as needed
raw['VEL_LIMITE'] = pd.to_numeric(raw['VEL_LIMITE'], errors='coerce', downcast='integer')
raw['VEL_CIRCULA '] = pd.to_numeric(raw['VEL_CIRCULA '], errors='coerce', downcast='integer')

#%% Create new reference fields from infraction name field
raw['ALCOHOL'] = [True if i.find('ALCOHOL') != -1 else False for i in raw['HECHO-BOL']]
raw['VELOCIDAD'] = [True if i != '' else False for i in raw['VEL_LIMITE']]
raw['NEGLIGENTE'] = [True if i.find('CONDUCCION NEGLIGENTE') != -1 else False for i in raw['HECHO-BOL']]
raw['TEMERARIA'] = [True if i.find('CONDUCCION TEMERARIA') != -1 else False for i in raw['HECHO-BOL']]
raw['ESTACIONAR'] = [True if i.find('ESTACIONAR') != -1 else False for i in raw['HECHO-BOL']]
raw['OBEDECER'] = [True if i.find('NO OBECEDER') != -1 else False for i in raw['HECHO-BOL']]

#%% Fix whitespace in field names

processed = raw.rename({' PUNTOS':'PUNTOS', 'VEL_CIRCULA ': 'VEL_CIRCULA'}, axis=1)


#%% Save dataset into new file to use in dashboarding
processed.to_csv('./Datasets/processed_data.csv', index=False)


#%% Extra Code
# Code to obtain points histogram:
#processed.hist(column='PUNTOS')
# Code to obtain fines box plot:
#processed.boxplot(column='IMP_BOL')
    