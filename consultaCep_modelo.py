# Programa de consulta de CEP no site cepaberto.com

# Busca do CEP pelo número
# Link: http://www.cepaberto.com/api/v3/cep?cep=40010000

# Importar biblioteca
import pandas as pd
import requests
import csv

#Incluir na lista os CEPs que serão pesquisados
listaCep = [
64002350,64002490
]

print('-' * 50)
print('Busca de CEP pelo número.')
print('-' * 50)

#Incluir a cidade e o estado

print('Devido ao limite de consultas diárias, e recomendado que você pesquisa os CEPs por cidade/estado.\n')
print('Incluir os dados da cidade e estado que você está pesquisando.')
	
cidade = input('Cidade: ')
estado = input('Estado(UF - Exemplo PA): ')

print('Informa o nome do arquivo aonde será salvo os CEPs encontrados.')
print('Obs.: É necessário incluir a extensão do arquivo csv.')
file_name = input('Nome do arquivo (exemplo ceps.csv):')

for i in listaCep:
	url = ('http://www.cepaberto.com/api/v3/cep?cep=%s' %i)
	print(url)
	
	#Token de autorização de consulta
	# Ao se cadastrar no site www.cepaberto.com é gerada um token
	TOKEN = 'XXXXXXXXXXX'
	
	auth = {'Authorization': 'Token token=%s' % TOKEN}
	
	#Passar a consulta para o site
	resposta = requests.get(url, headers=auth)
	try:
		df = pd.DataFrame(resposta.json(), index=[0])
	
		df.columns = ['Altitude','Cep','Latitude','Longitude','Logradouro','Bairro','Cidade','Estado']
		
		
		#Dados da Cidade e do Estado inseridos manualmente
		df['Cidade'] = cidade.upper()
		df['Estado'] = estado.upper()
	
		print(df.head(10))
	
		file = ('C:/Users/frank/Documents/BcGestao/01-Projetos/JSB Teresina/BI/%s' %file_name)
	
		if file == False:
			openFile = open(file,mode='w', newline='')
			df.to_csv(openFile, sep=';', encoding='utf-8', index=False, columns=['Cep','Cidade','Estado','Bairro','Logradouro'])
			openFile.close()
	
		else:
			openFile = open(file,mode='a', newline='')
			df.to_csv(openFile, sep=';', encoding='utf-8', index=False, columns=['Cep','Cidade','Estado','Bairro','Logradouro'], header=False)
			openFile.close()
	except ValueError:
		print('Cep não encontrado!')
		
		ceps = str(i)
		
		print(ceps)
		
		with open('C:/Users/frank/Documents/BcGestao/01-Projetos/JSB Teresina/BI/ceps_log.csv',mode='a', newline='') as logFile:
				logCep = csv.writer(logFile, delimiter=';')
				logCep.writerow(ceps)
		logFile.close()
		