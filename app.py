from prevision import generer_previsions

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# CONFIG PAGE PRO
# =========================
st.set_page_config(
    page_title="Dashboard Trésorerie - DAF",
    layout="wide",
    page_icon="💼"
)

# =========================
# TITRE
# =========================
st.title("📊 Tableau de Bord de Trésorerie - Direction Financière")
st.markdown("Analyse prédictive des flux de trésorerie et gestion du risque financier")

# =========================
# CHARGEMENT DES DONNÉES
# =========================
forecast = generer_previsions()

# Bouton refresh (IMPORTANT : doit recréer les données)
if st.button("🔄 Actualiser les prévisions"):
    forecast = generer_previsions()
    st.success("Prévisions mises à jour avec succès !")

# =========================
# NETTOYAGE DES DONNÉES
# =========================
df = forecast[['ds', 'yhat', 'optimiste', 'pessimiste']].copy()

df.rename(columns={
    "ds": "Date",
    "yhat": "Prévision normale",
    "optimiste": "Scénario optimiste",
    "pessimiste": "Scénario pessimiste"
}, inplace=True)

# Format date propre
df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m")

# =========================
# KPI FINANCIERS
# =========================
cash_min = forecast['pessimiste'].min()
cash_max = forecast['optimiste'].max()
cash_moyen = forecast['yhat'].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Cash minimum", f"{cash_min:,.0f} FCFA")
col2.metric("📈 Cash moyen", f"{cash_moyen:,.0f} FCFA")
col3.metric("🚀 Cash potentiel max", f"{cash_max:,.0f} FCFA")

# =========================
# SCORE DE RISQUE /100
# =========================
score_risque = 100

if cash_min < 0:
    score_risque -= 50
elif cash_min < 500000:
    score_risque -= 25
else:
    score_risque -= 5

if cash_moyen < 1000000:
    score_risque -= 10

if cash_max < 2000000:
    score_risque -= 10

score_risque = max(0, min(100, score_risque))

st.subheader("📊 Score de risque financier")

if score_risque >= 75:
    st.success(f"🟢 Risque faible : {score_risque}/100")
elif score_risque >= 50:
    st.warning(f"🟠 Risque modéré : {score_risque}/100")
else:
    st.error(f"🔴 Risque élevé : {score_risque}/100")

# =========================
# ANALYSE DU RISQUE
# =========================
st.subheader("🚦 Analyse du risque")

if cash_min < 0:
    risque = "🔴 RISQUE CRITIQUE : déficit de trésorerie possible"
    recommandation = "👉 Demander un crédit ou un découvert bancaire"
elif cash_min < 500000:
    risque = "🟠 RISQUE MODÉRÉ : tension de trésorerie"
    recommandation = "👉 Accélérer les encaissements clients"
else:
    risque = "🟢 TRÉSORERIE SAINE"
    recommandation = "👉 Situation stable, possibilité d’investissement"

st.warning(risque)
st.info(recommandation)

# =========================
# TABLEAU PROPRE
# =========================
st.subheader("📋 Données de prévision")

st.dataframe(df, use_container_width=True)

# =========================
# EXPORT EXCEL
# =========================
st.subheader("📥 Export des résultats")

with open("previsions_tresorerie_resultats.xlsx", "rb") as file:
    st.download_button(
        label="📥 Télécharger le rapport financier",
        data=file,
        file_name="rapport_tresorerie_DAF.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# =========================
# GRAPHIQUE PROPRE
# =========================
st.subheader("📈 Projection des flux de trésorerie")

fig, ax = plt.subplots(figsize=(12,6))

ax.plot(forecast['ds'], forecast['yhat'], label="Scénario normal", linewidth=2)
ax.plot(forecast['ds'], forecast['optimiste'], label="Scénario optimiste", linestyle="--")
ax.plot(forecast['ds'], forecast['pessimiste'], label="Scénario pessimiste", linestyle="--")

ax.axhline(0, color='red', linestyle='--', label="Seuil de crise")

ax.set_xlabel("Mois")
ax.set_ylabel("Trésorerie (FCFA)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# =========================
# FOOTER
# =========================
st.caption("Dashboard financier automatisé - Mise à jour via modèle Prophet")


