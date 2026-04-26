import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from prevision import generer_previsions

# =========================
# CONFIG PAGE
# =========================
st.set_page_config(
    page_title="Dashboard Trésorerie - DAF",
    layout="wide",
    page_icon="💼"
)

# =========================
# TITRE
# =========================
st.title("📊 Tableau de Bord de Trésorerie")
st.markdown("Prévision des flux de trésorerie et analyse du risque financier")

# =========================
# CHARGEMENT DONNÉES
# =========================
df = generer_previsions()

# bouton refresh
if st.button("🔄 Actualiser les prévisions"):
    df = generer_previsions()
    st.success("Données mises à jour")

# =========================
# RENOMMAGE POUR AFFICHAGE (IMPORTANT)
# =========================
df_affichage = df.rename(columns={
    "ds": "Date",
    "yhat": "Prévision",
    "optimiste": "Optimiste",
    "pessimiste": "Pessimiste"
})

# =========================
# KPI
# =========================
cash_min = df["pessimiste"].min()
cash_max = df["optimiste"].max()
cash_moyen = df["yhat"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Cash minimum", f"{cash_min:,.0f} FCFA")
col2.metric("📊 Cash moyen", f"{cash_moyen:,.0f} FCFA")
col3.metric("🚀 Cash maximum", f"{cash_max:,.0f} FCFA")

# =========================
# RISQUE
# =========================
st.subheader("🚦 Analyse du risque")

if cash_min < 0:
    st.error("🔴 Risque critique : déficit possible")
    reco = "Demander un financement court terme"
elif cash_min < 500000:
    st.warning("🟠 Tension de trésorerie")
    reco = "Accélérer les encaissements"
else:
    st.success("🟢 Situation saine")
    reco = "Situation stable"

st.info(reco)

# =========================
# TABLEAU PROPRE
# =========================
st.subheader("📋 Tableau des prévisions")

st.dataframe(df_affichage, use_container_width=True)

# =========================
# GRAPHIQUE
# =========================
st.subheader("📈 Évolution de la trésorerie")

fig, ax = plt.subplots(figsize=(12,6))

ax.plot(df["ds"], df["yhat"], label="Prévision")
ax.plot(df["ds"], df["optimiste"], linestyle="--", label="Optimiste")
ax.plot(df["ds"], df["pessimiste"], linestyle="--", label="Pessimiste")

ax.axhline(0, color="red", linestyle="--", label="Seuil critique")

ax.set_xlabel("Date")
ax.set_ylabel("Trésorerie (FCFA)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# =========================
# FOOTER
# =========================
st.caption("Dashboard de gestion prévisionnelle de trésorerie")
