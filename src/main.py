
import cdi

data_inicial = "01/01/2020"
data_final = "24/08/2023"

def main(data_inicial, data_final):
    cdi_total = cdi.cdi(data_inicial, data_final)
    cdi_data = {item['data']: item['valor'] for item in cdi_total}

    print("\n- Acumulado CDI Mensal:")
    monthly_cdi = cdi.taxa_cdi_mensal(cdi_data)
    for mes_ano, taxa in monthly_cdi.items():
        print(f"{mes_ano}: {taxa:.2%}")
        
    print("\n- Acumulado CDI Anual:")
    yearly_cdi = cdi.taxa_cdi_anual(cdi_data)
    for ano, taxa in yearly_cdi.items():
        print(f"Taxa CDI acumulada em {ano}: {taxa:.2%}")

    print("\n- Acumulado CDI 12 Meses:")
    myear_cdi = cdi.taxa_cdi_12_meses(cdi_data)
    print(f"Taxa CDI acumulada nos últimos 12 meses: {myear_cdi:.2%}")

   
    
if __name__ == "__main__":
    print('Iniciando\n')
    main(data_inicial, data_final)
