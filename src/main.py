from datetime import datetime, timedelta
from time import sleep
import pandas as pd
import threading

import cdi
import cvm
import analize

def get_dates(start_date, end_date):
    """
    Retorna uma lista de datas entre as datas de início e fim fornecidas.
    """
    start = datetime.strptime(start_date, "%d/%m/%Y")
    end = datetime.strptime(end_date, "%d/%m/%Y")
    months_years_list = []
    
    while start <= end:
        months_years_list.append(start.strftime("%m/%Y"))
        start = start.replace(day=1) + timedelta(days=31)
        start = start.replace(day=1)
    
    return months_years_list

def get_cdi_data(start_date, end_date):
    cdi_data = {item['data']: item['valor'] for item in cdi.cdi(start_date, end_date)}
    return pd.DataFrame(list(cdi_data.items()), columns=['Data', 'CDI'])

def print_cdi_results(cdi_data):
    """
    Mostra os resultados do CDI mensal, anual e dos últimos 12 meses.
    """
    print("\n- Acumulado CDI Mensal:")
    for mes_ano, taxa in cdi.taxa_cdi_mensal(cdi_data).items():
        print(f"{mes_ano}: {taxa:.2%}")
    print("\n- Acumulado CDI Anual:")
    for ano, taxa in cdi.taxa_cdi_anual(cdi_data).items():
        print(f"{ano}: {taxa:.2%}")
    print(f"\n- Acumulado CDI 12 Meses: {cdi.taxa_cdi_12_meses(cdi_data):.2%}")

def get_informes_cvm(data_inicial, data_final):
    """
    Recupera informes da CVM para um intervalo de datas.
    """
    cadastro = cvm.cadastro_cvm()
    dates = get_dates(data_inicial, data_final)
    informes = [cvm.informes_cvm(d.split('/')[1], d.split('/')[0]) for d in dates]
    sleep(0.5)  # Pausa entre as requisições
    return pd.concat(informes)

def main(data_inicial, data_final):
    cdi_df = get_cdi_data(data_inicial, data_final)
    cvm_df = get_informes_cvm(data_inicial, data_final)
    cvm_cad = cvm.cadastro_cvm()

    #Teste
    #cvm_df = cvm_df[cvm_df['CNPJ_FUNDO'].isin(['36.896.886/0001-40','42.084.488/0001-22'])]

    # A função rendimentos retorna o rendimento em % para COMPARAÇÃO COM CDI (Dias acima, etc)
    desempenho_cdi = analize.rendimentos_cdi(cvm_df,cdi_df)
    fundo_vs_cdi = analize.acima_do_cdi(desempenho_cdi)
    
    # Aqui, fica a função que calcula o RENDIMENTO TOTAL no periodo. Não confundir
    rendimentos_periodo = analize.rendimentos_total(cvm_df)

    print(fundo_vs_cdi)
    print(rendimentos_periodo)
    t = analize.consolidar(fundo_vs_cdi,rendimentos_periodo)

if __name__ == "__main__":
    print('Iniciando\n')
    main("01/05/2022", "30/08/2023")
