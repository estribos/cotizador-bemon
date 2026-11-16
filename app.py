import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Estribos Colima Bemon", layout="centered")

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
        if password_ingresada == "bemon2026":
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
    st.image("Logo Bemon estribos.jpeg", width=200)
except:
    pass

st.title("Estribos Colima Bemon")
st.subheader("Sistema de Cotización y Cálculo de Acero")

# Constante de peso teórico alambrón 1/4" (kg/m)
PESO_METRO_ALAMBRON = 0.248  

# Selector de producto
tipo_elemento = st.selectbox("Selecciona el producto a cotizar:", ["Estribos Cerrados", "Grapas de Alambrón"])

if tipo_elemento == "Estribos Cerrados":
    st.markdown("### 📐 Cotizador de Estribos Cerrados")
    
    col1, col2 = st.columns(2)
    with col1:
        base = st.number_input("Base del estribo (cm):", min_value=5.0, value=15.0, step=1.0)
        altura = st.number_input("Altura del estribo (cm):", min_value=5.0, value=20.0, step=1.0)
    with col2:
        cantidad = st.number_input("Cantidad de estribos (pzas):", min_value=1, value=100, step=10)
        precio_kilo = st.number_input("Precio por kg ($ MXN):", min_value=0.0, value=26.0, step=0.5)

    ganchos = 10.0  # 10 cm adicionales para los ganchos del estribo
    perimetro_m = (2 * (base + altura) + ganchos) / 100.0
    peso_unidad = perimetro_m * PESO_METRO_ALAMBRON
    peso_total = cantidad * peso_unidad
    costo_total = peso_total * precio_kilo

    st.markdown("---")
    st.success("### 📊 RESUMEN DE COTIZACIÓN")
    st.write(f"• **Medida:** {int(base)} x {int(altura)} cm")
    st.write(f"• **Desarrollo por pieza:** {perimetro_m:.2f} m ({peso_unidad:.3f} kg/pza)")
    st.write(f"• **Cantidad:** {cantidad:,} piezas")
    st.write(f"• **Peso Total:** {peso_total:.2f} kg")
    st.write(f"• **Precio por Kilo:** ${precio_kilo:.2f} MXN")
    st.markdown(f"## **Total a Cotizar: ${costo_total:,.2f} MXN**")

elif tipo_elemento == "Grapas de Alambrón":
    st.markdown("### 📌 Cotizador de Grapas de Alambrón")
    
    col1, col2 = st.columns(2)
    with col1:
        altura_grapa = st.selectbox("Altura de la grapa (cm):", [15, 20, 25])
        base_grapa = st.number_input("Ancho / Base de la grapa (cm):", min_value=5.0, value=10.0, step=1.0)
        ganchos_grapa = st.number_input("Dobleces / Ganchos totales (cm):", min_value=0.0, value=8.0, step=1.0)
    with col2:
        cantidad_grapas = st.number_input("Cantidad de grapas (pzas):", min_value=1, value=100, step=10)
        precio_kilo_grapa = st.number_input("Precio por kg para Grapas ($ MXN):", min_value=0.0, value=26.0, step=0.5)

    desarrollo_grapa_m = (base_grapa + altura_grapa + ganchos_grapa) / 100.0
    peso_unidad_grapa = desarrollo_grapa_m * PESO_METRO_ALAMBRON
    peso_total_grapas = cantidad_grapas * peso_unidad_grapa
    costo_total_grapas = peso_total_grapas * precio_kilo_grapa

    st.markdown("---")
    st.success("### 📊 RESUMEN DE COTIZACIÓN (GRAPAS)")
    st.write(f"• **Altura:** {altura_grapa} cm | **Base:** {int(base_grapa)} cm")
    st.write(f"• **Desarrollo por pieza:** {desarrollo_grapa_m:.2f} m ({peso_unidad_grapa:.3f} kg/pza)")
    st.write(f"• **Cantidad:** {cantidad_grapas:,} piezas")
    st.write(f"• **Peso Total:** {peso_total_grapas:.2f} kg")
    st.write(f"• **Precio por Kilo:** ${precio_kilo_grapa:.2f} MXN")
    st.markdown(f"## **Total a Cotizar: ${costo_total_grapas:,.2f} MXN**")