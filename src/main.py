from datetime import datetime, timedelta
from time import sleep
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

import cdi
import cvm
import process



repo = r'C:\Users\vitor\Projects\finance\data'

def get_dates(start_date, end_date):
    """
    Retorna uma lista de datas entre as datas de início e fim fornecidas.
    """
    print(f'- Obtendo dados de {start_date} a {end_date}' )
    start = datetime.strptime(start_date, "%d/%m/%Y")
    end = datetime.strptime(end_date, "%d/%m/%Y")
    months_years_list = []
    
    while start <= end:
        months_years_list.append(start.strftime("%m/%Y"))
        start = start.replace(day=1) + timedelta(days=31)
        start = start.replace(day=1)
    
    return months_years_list

def get_cdi(start_date, end_date):
    cdi_data = {item['data']: item['valor'] for item in cdi.cdi(start_date, end_date)}
    data =  pd.DataFrame(list(cdi_data.items()), columns=['Data', 'CDI'])
    print(f'- Download dados CDI finalizado. {len(data)} Registros')
    return data

def get_cvm(start_date, end_date):
    """
    Recupera informes da CVM para um intervalo de datas.
    """
    dates = get_dates(start_date, end_date)
    informes = [cvm.informes_cvm(d.split('/')[1], d.split('/')[0]) for d in dates]
    sleep(0.3)  # Pausa entre as requisições
    data = pd.concat(informes)
    print(f'- Download Informes CVM finalizado. {len(data)} Registros')
    return data

def main(start, end):
   
   # Obtendo, processando e salvando dados:
   
   # CVM
   cvm_data = cvm.process_cvm(get_cvm(start, end))
   cvm_data.to_csv(f'{repo}\cvm.csv',sep='\t')
   
   # CDI
   cdi_data = cdi.process(get_cdi(start,end))
   cdi_data.to_csv(f'{repo}\cdi.csv',sep='\t')
  
   # Cadastro CVM
   register_data = cvm.cadastro_cvm()
   register_data.to_csv(f'{repo}\cad.csv', sep='\t')

   # Teste
   process.associate(cdi_data, cvm_data, register_data)


if __name__ == "__main__":
    print('Iniciando\n')
    main("01/06/2022", "05/09/2023")
    print(' Finalizado ')