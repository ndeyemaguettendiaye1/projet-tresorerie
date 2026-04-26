import pandas as pd
from prophet import Prophet

def generer_previsions():

    df = pd.read_excel("tresorerie.xlsx")

    df = df[['Mois', 'Encaissements']].copy()
    df.columns = ['ds', 'y']
    df['ds'] = pd.to_datetime(df['ds'])

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=6, freq='ME')
    forecast = model.predict(future)

    # IMPORTANT : structure stable
    resultat = pd.DataFrame()
    resultat["Date"] = forecast["ds"]
    resultat["Prévision"] = forecast["yhat"]
    resultat["Optimiste"] = forecast["yhat"] * 1.10
    resultat["Pessimiste"] = forecast["yhat"] * 0.90

    return resultat
