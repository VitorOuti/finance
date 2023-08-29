import pandas as pd
import matplotlib.pyplot as plt

def analize(inf, cad, cdi):

    # Renomear coluna e atualizar o DataFrame no lugar
   
    inf.rename(columns={'DT_COMPTC':'Data'}, inplace=True)
    inf['Data'] = pd.to_datetime(inf['Data'])
    inf['Data'] = inf['Data'].dt.strftime('%d/%m/%Y')
    df = pd.merge(inf,cdi,on='Data',how='left').dropna()
    print(df)
    
    