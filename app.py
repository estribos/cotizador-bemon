import streamlit as st

# --- SISTEMA DE ACCESO PRIVADO ---
def verificar_password():
    if "password_correcta" not in st.session_state:
        st.session_state.password_correcta = False

    if st.session_state.password_correcta:
        return True

    st.markdown("## 🔐 Acceso Restringido")
    st.subheader("Estribos Bemon - Sistema Privado")
    
    password_ingresada = st.text_input("Introduce la contraseña de acceso:", type="password")
    
    if st.button("Iniciar Sesión"):
        if password_ingresada == "bemon2026": # Puedes cambiar tu contraseña aquí si lo deseas
            st.session_state.password_correcta = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta. Acceso denegado.")
            
    return False

if not verificar_password():
    st.stop()

# ==========================================
# PANEL PRINCIPAL - ESTRIBOS Y GRAPAS BEMON
# ==========================================
try:
    st.image("Logo Bemon estribos.jpeg", width=200) # Asegúrate de que el nombre del logo coincida en GitHub
except:
    pass

st.title("Estribos Colima Bemon")
st.subheader("Sistema de Cotización y Cálculo de Acero")

# Selector de producto
tipo_elemento = st.selectbox("Selecciona el producto a cotizar:", ["Estribos Cerrados", "Grapas de Alambrón"])

peso_metro_alambron = 0.248  # Peso teórico aproximado del alambrón de 1/4" (kg/m)

if tipo_elemento == "Estribos Cerrados":
    st.markdown("### 📐 Cálculo de Estribos Cerrados")
    
    precio_kilo = st.number_input("Precio por kilogramo ($ MXN):", min_value=0.0, value=26.0, step=0.5)
    base = st.number_input("Base del estribo (cm):", min_value=1.0, value=15.0, step=1.0)
    altura = st.number_input("Altura del estribo (cm):", min_value=1.0, value=20.0, step=1.0)
    cantidad = st.number_input("Cantidad de estribos (pzas):", min_value=1, value=100, step=10)
    
    # Perímetro en metros (2 bases + 2 alturas + 10 cm de ganchos)
    perimetro_m = (2 * (base + altura) + 10.0) / 100.0  
    peso_total = cantidad * perimetro_m * peso_metro_alambron
    costo_total = peso_total * precio_kilo
    
    st.info(
        f"📊 **Resultados Estribos Cerrados:**\n\n"
        f"- Desarrollo por pieza: **{perimetro_m:.2f} m**\n"
        f"- Cantidad: **{cantidad} pzas**\n"
        f"- Peso Total: **{peso_total:.2f} kg**\n"
        f"- Precio por kg: **${precio_kilo:.2f} MXN**\n"
        f"- **Costo Total: ${costo_total:,.2f} MXN**"
    )

elif tipo_elemento == "Grapas de Alambrón":
    st.markdown("### 📌 Cálculo de Grapas de Alambrón")
    
    precio_kilo_grapa = st.number_input("Precio por kilogramo para Grapas ($ MXN):", min_value=0.0, value=26.0, step=0.5)
    
    # Alturas solicitadas
    altura_grapa = st.selectbox("Selecciona la altura de la grapa (cm):", [15, 20, 25])
    base_grapa = st.number_input("Ancho o base de la grapa (cm):", min_value=1.0, value=10.0, step=1.0)
    ganchos_grapa = st.number_input("Longitud total de ganchos/patillas (cm):", min_value=0.0, value=8.0, step=1.0)
    cantidad_grapas = st.number_input("Cantidad de grapas (pzas):", min_value=1, value=100, step=10)
    
    # Cálculo del desarrollo de la grapa en metros
    desarrollo_grapa_m = (base_grapa + altura_grapa + ganchos_grapa) / 100.0
    
    peso_total_grapas = cantidad_grapas * desarrollo_grapa_m * peso_metro_alambron
    costo_total_grapas = peso_total_grapas * precio_kilo_grapa
    
    st.success(
        f"📌 **Resultados Grapas ({altura_grapa} cm de alto):**\n\n"
        f"- Desarrollo por pieza: **{desarrollo_grapa_m:.2f} m**\n"
        f"- Cantidad: **{cantidad_grapas} pzas**\n"
        f"- Peso Total: **{peso_total_grapas:.2f} kg**\n"
        f"- Precio por kg: **${precio_kilo_grapa:.2f} MXN**\n"
        f"- **Costo Total: ${costo_total_grapas:,.2f} MXN**"
    )