import requests

def cdi(data_especifica):
    URL_BASE = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo_serie}/dados?formato=json&dataInicial={data_especifica}&dataFinal={data_especifica}"

    codigo_serie = 12  # 12 é o código da série diária de CDI
    url = URL_BASE.format(codigo_serie=codigo_serie, data_especifica=data_especifica)
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # Como estamos buscando a taxa CDI de uma data específica, devemos ter apenas um registro retornado.
    # Se por acaso não houver dados para essa data (por exemplo, um feriado), a lista será vazia.
    if data:
        print(data[0])
        return data[0]
    else:
        return None

cdi('22/08/2023')