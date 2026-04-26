import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# =========================
# 1. CHARGEMENT DES DONNÉES
# =========================
try:
    df = pd.read_excel("tresorerie.xlsx")
except FileNotFoundError:
    print("❌ Fichier tresorerie.xlsx introuvable")
    exit()

# =========================
# 2. VALIDATION DES COLONNES
# =========================
if 'Mois' not in df.columns or 'Encaissements' not in df.columns:
    print("❌ Colonnes requises : Mois, Encaissements")
    exit()

df = df[['Mois', 'Encaissements']]
df.columns = ['ds', 'y']
df['ds'] = pd.to_datetime(df['ds'])

# =========================
# 3. MODÈLE PROPHET
# =========================
model = Prophet()
model.fit(df)

# =========================
# 4. PRÉVISIONS
# =========================
future = model.make_future_dataframe(periods=6, freq='ME')
forecast = model.predict(future)

# =========================
# 5. SCÉNARIOS
# =========================
forecast['optimiste'] = forecast['yhat'] * 1.10
forecast['pessimiste'] = forecast['yhat'] * 0.90

# =========================
# 6. GRAPHIQUE PROPHET
# =========================
fig1 = model.plot(forecast)
plt.title("Prévision de trésorerie - Prophet")

# =========================
# 7. GRAPHIQUE SCÉNARIOS
# =========================
plt.figure(figsize=(10,5))

plt.plot(forecast['ds'], forecast['yhat'], label='Normal')
plt.plot(forecast['ds'], forecast['optimiste'], label='Optimiste', linestyle="--")
plt.plot(forecast['ds'], forecast['pessimiste'], label='Pessimiste', linestyle="--")

plt.axhline(0, color='red', linestyle='--', label="Seuil de crise")

plt.title("Scénarios de trésorerie")
plt.xlabel("Mois")
plt.ylabel("Flux de trésorerie")
plt.legend()
plt.grid(True)

plt.tight_layout()

# =========================
# 8. EXPORT EXCEL FINAL
# =========================
resultat = forecast[['ds', 'yhat', 'optimiste', 'pessimiste']]

resultat.to_excel("previsions_tresorerie_resultats.xlsx", index=False)

print("✔ Prévisions générées avec succès")
print("✔ Fichier Excel créé : previsions_tresorerie_resultats.xlsx")