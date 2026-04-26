import pandas as pd
from prophet import Prophet

def generer_previsions():

    # =========================
    # 1. CHARGEMENT DES DONNÉES
    # =========================
    df = pd.read_excel("tresorerie.xlsx")

    # sécurisation des colonnes
    df = df[['Mois', 'Encaissements']].copy()
    df.columns = ['ds', 'y']

    df['ds'] = pd.to_datetime(df['ds'])

    # =========================
    # 2. MODÈLE PROPHET
    # =========================
    model = Prophet()
    model.fit(df)

    # =========================
    # 3. PRÉVISIONS
    # =========================
    future = model.make_future_dataframe(periods=6, freq='ME')
    forecast = model.predict(future)

    # =========================
    # 4. NETTOYAGE DES COLONNES (IMPORTANT)
    # =========================
    resultat = forecast[['ds', 'yhat']].copy()

    # scénarios
    resultat['optimiste'] = resultat['yhat'] * 1.10
    resultat['pessimiste'] = resultat['yhat'] * 0.90

    # renommage propre pour Streamlit
    resultat = resultat.rename(columns={
        'ds': 'Date',
        'yhat': 'Prévision normale'
    })

    return resultat
