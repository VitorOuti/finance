from datetime import datetime, timedelta
from time import sleep
import pandas as pd
import cdi
import cvm

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

def retrieve_cdi_data(start_date, end_date):
    """
    Obtém os dados de CDI para um intervalo de datas.
    """
    try:
        cdi_data = {item['data']: item['valor'] for item in cdi.cdi(start_date, end_date)}
        return pd.DataFrame(list(cdi_data.items()), columns=['Data', 'CDI']), cdi_data
    except Exception as e:
        print('- A função "cdi" não funcionou conforme esperado.\n\n Erro:', e)
        return None, {}

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
    cdi_df, cdi_data = retrieve_cdi_data(data_inicial, data_final)
    if cdi_df is not None and cdi_data:
        #print_cdi_results(cdi_data)
        print(cdi_df)
    informes_df = get_informes_cvm(data_inicial, data_final)
    cvm_df = cvm.processar_cvm(informes_df)
    print(cvm_df)
    # Adicione o código do gráfico aqui

if __name__ == "__main__":
    print('Iniciando\n')
    main("01/07/2022", "01/08/2023")
