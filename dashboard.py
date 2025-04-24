import json
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt

st.title("Monitoreo de Viewers - YouTube en Vivo")

canal = st.selectbox("Seleccioná un canal", ["Vorterix", "Olga", "Luzu"])
archivo = f"{canal}.json"

with open(archivo) as f:
    datos = json.load(f)

tiempos = [datetime.fromisoformat(d["time"]) for d in datos]
viewers = [d["viewers"] for d in datos]

st.write(f"Registros: {len(viewers)}")
st.line_chart(data=viewers)

st.write(f"📈 Máximo: {max(viewers)}")
st.write(f"📉 Mínimo: {min(viewers)}")
st.write(f"👀 Promedio: {sum(viewers)//len(viewers)}")



st.subheader("Comparativa entre canales")

# Diccionario para mapear canal a color
colores = {
    "Vorterix": "red",
    "Olga": "blue",
    "Luzu": "green"
}

fig, ax = plt.subplots()

for canal in ["Vorterix", "Olga", "Luzu"]:
    archivo = f"{canal}.json"
    try:
        with open(archivo) as f:
            datos = json.load(f)

        # Filtramos datos válidos
        datos = [d for d in datos if d["viewers"] is not None]
        tiempos = [datetime.fromisoformat(d["time"]) for d in datos]
        viewers = [d["viewers"] for d in datos]

        ax.plot(tiempos, viewers, label=canal, color=colores[canal])

    except Exception as e:
        st.error(f"No se pudo procesar {canal}: {e}")

ax.set_title("Evolución de viewers en canales en vivo")
ax.set_xlabel("Tiempo")
ax.set_ylabel("Viewers")
ax.legend()
ax.grid(True)

st.pyplot(fig)