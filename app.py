import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from prevision import generer_previsions

st.set_page_config(
    page_title="Dashboard Trésorerie",
    layout="wide"
)

st.title("📊 Tableau de Bord de Trésorerie")

df = generer_previsions()

# refresh
if st.button("🔄 Actualiser"):
    df = generer_previsions()
    st.success("Données mises à jour")

# ================= KPI =================
cash_min = df["Pessimiste"].min()
cash_max = df["Optimiste"].max()
cash_moyen = df["Prévision"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Minimum", f"{cash_min:,.0f} FCFA")
col2.metric("📊 Moyen", f"{cash_moyen:,.0f} FCFA")
col3.metric("🚀 Maximum", f"{cash_max:,.0f} FCFA")

# ================= RISQUE =================
st.subheader("🚦 Analyse du risque")

if cash_min < 0:
    st.error("🔴 Risque critique")
    reco = "Demander financement"
elif cash_min < 500000:
    st.warning("🟠 Tension de trésorerie")
    reco = "Accélérer encaissements"
else:
    st.success("🟢 Situation saine")
    reco = "Stable"

st.info(reco)

# ================= TABLEAU =================
st.subheader("📋 Données")

st.dataframe(df, use_container_width=True)

# ================= GRAPHIQUE =================
st.subheader("📈 Évolution")

fig, ax = plt.subplots(figsize=(12,6))

ax.plot(df["Date"], df["Prévision"], label="Prévision")
ax.plot(df["Date"], df["Optimiste"], linestyle="--", label="Optimiste")
ax.plot(df["Date"], df["Pessimiste"], linestyle="--", label="Pessimiste")

ax.axhline(0, color="red", linestyle="--")
ax.set_xlabel("Date")
ax.set_ylabel("FCFA")
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.caption("Dashboard trésorerie - version finale")
