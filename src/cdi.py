import requests
from datetime import datetime, timedelta

def cdi(data_inicial, data_final): 
    # Converta as strings de data em objetos datetime
    dt_inicial = datetime.strptime(data_inicial, "%d/%m/%Y")
    dt_final = datetime.strptime(data_final, "%d/%m/%Y")

    # Ajuste as datas para um dia antes e um dia depois
    dt_inicial -= timedelta(days=1)
    dt_final += timedelta(days=1)

    # Converta de volta para string no formato dd/mm/aaaa
    data_inicial_adjusted = dt_inicial.strftime("%d/%m/%Y")
    data_final_adjusted = dt_final.strftime("%d/%m/%Y")

    URL_BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json&dataInicial={data_inicial}&dataFinal={data_final}"

    codigo_serie = 12  # 12 é o código da série diária de CDI
    url = URL_BASE.format(codigo_serie=codigo_serie, data_inicial=data_inicial_adjusted, data_final=data_final_adjusted)
    
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    return data

def taxa_cdi_mensal(cdi_dict):
    # Separa as taxas por mês
    taxa_por_mes = {}
    for data, taxa in cdi_dict.items():
        mes_ano = datetime.strptime(data, "%d/%m/%Y").strftime("%m/%Y")
        if mes_ano not in taxa_por_mes:
            taxa_por_mes[mes_ano] = []
        taxa_por_mes[mes_ano].append(float(taxa)/100)
    
    # Calcula a taxa acumulada para cada mês completo
    taxa_acumulada_por_mes = {}
    for mes_ano, taxas in taxa_por_mes.items():
        # Verifica se o mês é completo (com base no número de dias úteis)
        if len(taxas) >= 15:
            principal = 1.0
            for taxa in taxas:
                principal *= (1 + taxa)
            taxa_acumulada_por_mes[mes_ano] = principal - 1.0
    
    return taxa_acumulada_por_mes

def taxa_cdi_anual(cdi_dict):
    
    anos = set(datetime.strptime(date, '%d/%m/%Y').year for date in cdi_dict.keys())
    cdi_anual = {}

    for ano in anos:
        principal = 1.0
        for data, taxa in cdi_dict.items():
            if datetime.strptime(data, '%d/%m/%Y').year == ano:
                principal *= (1 + float(taxa)/100)
        
        taxa_acumulada = principal - 1.0
        cdi_anual[ano] = taxa_acumulada

    return cdi_anual

def taxa_cdi_12_meses(cdi_dict):
   
    # Ordena as datas e pega a mais recente
    datas_ordenadas = sorted(cdi_dict.keys(), key=lambda x: datetime.strptime(x, '%d/%m/%Y'))
    data_final = datetime.strptime(datas_ordenadas[-1], '%d/%m/%Y')
    data_inicial = data_final - timedelta(days=365)  # 12 meses antes da data final
    
    if datetime.strptime(datas_ordenadas[0], '%d/%m/%Y') > data_inicial:
        print(' - Não há 12 meses de histórico de CDI para que seja realizado o cálculo')
        return None  # Não cobre 12 meses

    principal = 1.0
    for data, taxa in cdi_dict.items():
        data_atual = datetime.strptime(data, '%d/%m/%Y')
        if data_inicial <= data_atual <= data_final:
            principal *= (1 + float(taxa)/100)

    taxa_acumulada = principal - 1.0
    return taxa_acumulada
