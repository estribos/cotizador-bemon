import datetime
import os
import pandas as pd
import streamlit as st

# Importaciones de ReportLab para el PDF y manejo de imágenes
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

# Configuración de la página
st.set_page_config(
    page_title="Cotizador Oficial - Estribos Bemon", layout="wide"
)

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

# --- FUNCIÓN PARA GENERAR EL PDF PROFESIONAL ---
def generar_pdf_en_memoria(
    num_cot, cliente_nom, fecha_e, fecha_v, items, subtotal, iva, total, incluir_iva_val
):
    nombre_archivo = f"Cotizacion_{num_cot}_{cliente_nom.replace(' ', '_')}.pdf"
    ruta_temp = os.path.join(os.getcwd(), nombre_archivo)

    doc = SimpleDocTemplate(
        ruta_temp,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )
    story = []
    styles = getSampleStyleSheet()

    estilo_negocio = ParagraphStyle(
        'NegocioInfo',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1f2937'),
        fontName='Helvetica',
    )
    estilo_normal = ParagraphStyle(
        'TextoNormal',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1f2937'),
        fontName='Helvetica',
    )
    estilo_right = ParagraphStyle(
        'TextoRight',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11.5,
        alignment=2,
        textColor=colors.HexColor('#1f2937'),
        fontName='Helvetica',
    )
    estilo_th = ParagraphStyle(
        'TextoTH',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        fontName='Helvetica-Bold',
    )
    estilo_pie = ParagraphStyle(
        'TextoPie',
        parent=styles['Normal'],
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#374151'),
        fontName='Helvetica',
    )
    estilo_frase = ParagraphStyle(
        'FraseFinal',
        parent=styles['Heading3'],
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#1e3a8a'),
        fontName='Helvetica-Bold',
    )

    texto_izq = Paragraph(
        "<b>ESTRIBOS COLIMA BEMON</b><br/>"
        "Col. San José II, Francisco Márquez #250, Villa de Álvarez, Colima<br/>"
        "Correo: estriboscolima@gmail.com | Cel: 312-233-7192",
        estilo_negocio
    )

    logo_paths = ["logo bemon estribo.jpeg", "logo bemon estribo.jpg", "Logo Bemon estribos.jpeg", "logo.png", "logo.jpg"]
    logo_encontrado = None
    for p in logo_paths:
        if os.path.exists(os.path.join(os.getcwd(), p)):
            logo_encontrado = os.path.join(os.getcwd(), p)
            break

    if logo_encontrado:
        img = Image(logo_encontrado, width=180, height=62)
        img.hAlign = 'RIGHT'
        celda_derecha = img
    else:
        celda_derecha = Paragraph("", estilo_normal)

    t_header = Table([[texto_izq, celda_derecha]], colWidths=[310, 230])
    t_header.setStyle(
        TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ])
    )
    story.append(t_header)
    story.append(Spacer(1, 15))

    info_general = [
        [
            Paragraph(f"<b>Cotización:</b> #{num_cot}", estilo_normal),
            Paragraph(f"<b>Fecha de Expedición:</b> {fecha_e.strftime('%d/%m/%Y')}", estilo_normal),
        ],
        [
            Paragraph(f"<b>Cliente:</b> {cliente_nom}", estilo_normal),
            Paragraph(f"<b>Vencimiento:</b> {fecha_v.strftime('%d/%m/%Y')}", estilo_normal),
        ],
    ]
    t_info = Table(info_general, colWidths=[270, 270])
    t_info.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ])
    )
    story.append(t_info)
    story.append(Spacer(1, 12))

    tabla_data = [
        [
            Paragraph("Clave", estilo_th),
            Paragraph("Cant. KG", estilo_th),
            Paragraph("Piezas", estilo_th),
            Paragraph("Descripción", estilo_th),
            Paragraph("P.U.", estilo_th),
            Paragraph("Total", estilo_th),
        ]
    ]

    for item in items:
        tabla_data.append(
            [
                Paragraph(str(item["Clave"]), estilo_normal),
                Paragraph(f"{item['Cant. KG']:.2f}", estilo_normal),
                Paragraph(str(item["Piezas"]), estilo_normal),
                Paragraph(str(item["Descripción"]), estilo_normal),
                Paragraph(f"$ {item['P.U.']:,.2f}", estilo_normal),
                Paragraph(f"$ {item['Total']:,.2f}", estilo_normal),
            ]
        )

    t_partidas = Table(tabla_data, colWidths=[50, 60, 45, 235, 55, 95])
    
    estilo_tabla_partidas = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3a8a')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    
    for i in range(1, len(tabla_data)):
        if i % 2 == 0:
            estilo_tabla_partidas.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f8fafc')))

    t_partidas.setStyle(TableStyle(estilo_tabla_partidas))
    story.append(t_partidas)
    story.append(Spacer(1, 12))

    totales_rows = [
        [Paragraph("<b>SUBTOTAL:</b>", estilo_normal), Paragraph(f"$ {subtotal:,.2f} MXN", estilo_right)]
    ]
    if incluir_iva_val:
        totales_rows.append([Paragraph("<b>IVA (16%):</b>", estilo_normal), Paragraph(f"$ {iva:,.2f} MXN", estilo_right)])
    totales_rows.append([
        Paragraph("<font size='10' color='#1e3a8a'><b>TOTAL:</b></font>", estilo_normal),
        Paragraph(f"<font size='10' color='#1e3a8a'><b>$ {total:,.2f} MXN</b></font>", estilo_right)
    ])

    t_totales_struct = Table(totales_rows, colWidths=[85, 115])
    t_totales_struct.setStyle(
        TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEABOVE', (0, len(totales_rows)-1), (-1, len(totales_rows)-1), 1, colors.HexColor('#1e3a8a')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ])
    )

    notas_texto = """
    <b>ESPECIFICACIONES Y CONDICIONES:</b><br/>
    • Forma de pago al contado<br/>
    • Piezas fabricadas con alambrón de 1/4'', con dobleces según norma estructural.<br/>
    • Revisar medidas solicitadas. Las medidas son reales del elemento.<br/><br/>
    <b>DATOS PARA DEPÓSITO BANCARIO:</b><br/>
    <b>Titular:</b> HUITZAL MONTOYA PEREZ<br/>
    • Banco: BANAMEX | Sucursal: 7014<br/>
    • Cuenta: 8585855 | CLABE: 002090701485858553
    """

    t_inferior_data = [
        [
            Paragraph(notas_texto, estilo_pie),
            t_totales_struct
        ]
    ]
    t_inferior = Table(t_inferior_data, colWidths=[320, 220])
    t_inferior.setStyle(
        TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ])
    )
    story.append(t_inferior)
    story.append(Spacer(1, 15))

    story.append(Paragraph('"Estribos Bemon: El alma de tu concreto"', estilo_frase))

    doc.build(story)
    return ruta_temp, nombre_archivo

# --- ESTILO CSS ---
st.markdown(
    """
    <style>
    @media print {
        [data-testid="stSidebar"], header, button, .stButton, .stNumberInput, .stDateInput, .stTextInput, hr {
            display: none !important;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- PANEL LATERAL ---
st.sidebar.markdown("### ⚙️ Configuración Interna")
precio_kg = st.sidebar.number_input("Precio por kg ($ MXN)", value=26.00, format="%.2f")
peso_nominal = st.sidebar.number_input("Peso nominal alambrón (kg/m)", value=0.248, format="%.3f")
incluir_iva = st.sidebar.checkbox("Incluir IVA (16%)", value=True)

st.sidebar.divider()
st.sidebar.info("💡 Selecciona el producto y agrega las partidas necesarias.")

# --- PANEL DE CONTROL ---
st.markdown("### 🛠️ Panel de Control y Captura")

col1, col2, col3 = st.columns(3)
with col1:
    num_cotizacion = st.text_input("Número de Cotización", value="175")
    cliente = st.text_input("Cliente", value="PÚBLICO GENERAL")
with col2:
    fecha_exp = st.date_input("Fecha de Expedición", datetime.date(2026, 11, 15))
with col3:
    fecha_ven = st.date_input("Fecha de Vencimiento", datetime.date(2026, 11, 18))

st.divider()

# --- PARTIDAS ---
st.subheader("📋 Especificaciones del Material")

if "partidas" not in st.session_state:
    st.session_state.partidas = [{"tipo": "Estribo Cerrado", "ancho": 10.0, "alto": 10.0, "gancho": 5.0, "piezas": 100}]

col_b1, col_b2 = st.columns([1, 5])
with col_b1:
    if st.button("➕ Agregar Partida"):
        st.session_state.partidas.append({"tipo": "Estribo Cerrado", "ancho": 10.0, "alto": 15.0, "gancho": 5.0, "piezas": 50})
with col_b2:
    if st.button("🗑️ Eliminar última partida") and len(st.session_state.partidas) > 1:
        st.session_state.partidas.pop()

items_calculados = []
subtotal_general = 0.0

for i, partida in enumerate(st.session_state.partidas):
    st.markdown(f"**Partida #{i+1}**")
    
    # Selector de tipo por partida
    partida["tipo"] = st.selectbox(f"Tipo de Elemento #{i+1}", ["Estribo Cerrado", "Grapa de Alambrón"], key=f"tipo_{i}")
    
    if partida["tipo"] == "Estribo Cerrado":
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            partida["ancho"] = st.number_input(f"Ancho (cm) #{i+1}", value=float(partida.get("ancho", 10.0)), key=f"ancho_{i}")
        with c2:
            partida["alto"] = st.number_input(f"Alto (cm) #{i+1}", value=float(partida.get("alto", 10.0)), key=f"alto_{i}")
        with c3:
            partida["gancho"] = st.number_input(f"Gancho (cm) #{i+1}", value=float(partida.get("gancho", 5.0)), key=f"gancho_{i}")
        with c4:
            partida["piezas"] = st.number_input(f"Piezas #{i+1}", value=int(partida["piezas"]), step=1, key=f"piezas_{i}")

        desarrollo_m = (2 * ((partida["ancho"] + partida["alto"]) / 100.0)) + (2 * (partida["gancho"] / 100.0))
        ancho_i, alto_i = int(partida["ancho"]), int(partida["alto"])
        clave_str = f"E{ancho_i}{alto_i}"
        descripcion_str = f"ESTRIBO DE ALAMBRÓN {ancho_i}X{alto_i} CM (1/4'', dobleces 135°)"

    else: # Grapa de Alambrón
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            # Selector de alturas fijas (15, 20, 25)
            partida["alto"] = st.selectbox(f"Altura Grapa (cm) #{i+1}", [15.0, 20.0, 25.0], key=f"alto_{i}")
        with c2:
            partida["ancho"] = st.number_input(f"Base (cm) #{i+1}", value=float(partida.get("ancho", 10.0)), key=f"ancho_{i}")
        with c3:
            partida["gancho"] = st.number_input(f"Patillas/Dobleces (cm) #{i+1}", value=float(partida.get("gancho", 8.0)), key=f"gancho_{i}")
        with c4:
            partida["piezas"] = st.number_input(f"Piezas #{i+1}", value=int(partida["piezas"]), step=1, key=f"piezas_{i}")

        desarrollo_m = (partida["ancho"] + partida["alto"] + partida["gancho"]) / 100.0
        ancho_i, alto_i = int(partida["ancho"]), int(partida["alto"])
        clave_str = f"G{int(partida['alto'])}-{ancho_i}"
        descripcion_str = f"GRAPA DE ALAMBRÓN {int(partida['alto'])} CM ALTO X {ancho_i} CM BASE (1/4'')"

    metros_totales = desarrollo_m * partida["piezas"]
    kilos_totales = metros_totales * peso_nominal
    total_partida = kilos_totales * precio_kg

    subtotal_general += total_partida

    items_calculados.append({
        "Clave": clave_str,
        "Cant. KG": round(kilos_totales, 2),
        "Piezas": int(partida["piezas"]),
        "Descripción": descripcion_str,
        "P.U.": precio_kg,
        "Total": round(total_partida, 2),
    })
    
    st.markdown(f"*Resumen Parcial:* **{partida['piezas']} pzas** | Desarrollo: **{desarrollo_m:.2f} m** | **{kilos_totales:.2f} kg** | Subtotal: **$ {total_partida:,.2f} MXN**")
    st.divider()

iva_general = subtotal_general * 0.16 if incluir_iva else 0.0
gran_total = subtotal_general + iva_general

# --- VISTA PREVIA EN PANTALLA ---
st.markdown("<br><hr><br>", unsafe_allow_html=True)

col_prev1, col_prev2 = st.columns([3, 1])
with col_prev1:
    st.markdown(
        """
        <h4>ESTRIBOS COLIMA BEMON</h4>
        <p><b>Col. San José II, Francisco Márquez #250, Villa de Álvarez, Colima</b><br>
        Correo: estriboscolima@gmail.com | Cel: 312-233-7192</p>
        """,
        unsafe_allow_html=True,
    )
with col_prev2:
    logo_paths = ["logo bemon estribo.jpeg", "logo bemon estribo.jpg", "Logo Bemon estribos.jpeg", "logo.png", "logo.jpg"]
    logo_encontrado_preview = None
    for p in logo_paths:
        if os.path.exists(os.path.join(os.getcwd(), p)):
            logo_encontrado_preview = os.path.join(os.getcwd(), p)
            break
    if logo_encontrado_preview:
        st.image(logo_encontrado_preview, width=200)

st.markdown(f"""
**Cotización:** #{num_cotizacion} &nbsp;&nbsp;|&nbsp;&nbsp; **Cliente:** {cliente}  
**Fecha de Expedición:** {fecha_exp.strftime('%d/%m/%Y')} &nbsp;&nbsp;|&nbsp;&nbsp; **Vencimiento:** {fecha_ven.strftime('%d/%m/%Y')}
""")

df_cotizacion = pd.DataFrame(items_calculados)
st.dataframe(df_cotizacion, use_container_width=True, hide_index=True)

col_notas, col_fin = st.columns(2)
with col_notas:
    st.markdown("""
    **ESPECIFICACIONES Y CONDICIONES:**  
    * Forma de pago al contado  
    * Piezas fabricadas con alambrón de 1/4'', con dobleces según norma estructural.  
    * Revisar medidas solicitadas. Las medidas son reales del elemento.  
    
    **DATOS PARA DEPÓSITO**  
    **Titular:** HUITZAL MONTOYA PEREZ  
    * **Banco:** BANAMEX | **Sucursal:** 7014  
    * **Cuenta:** 8585855  
    * **Cuenta CLABE:** 002090701485858553  
    """)

with col_fin:
    st.markdown(f"""
    ### Resumen de Importes
    * **SUBTOTAL:** \$ {subtotal_general:,.2f} MXN
    """)
    if incluir_iva:
        st.markdown(f"* **IVA (16%):** \$ {iva_general:,.2f} MXN")
    st.markdown(f"### **TOTAL:** \$ {gran_total:,.2f} MXN")

st.markdown("<br><h4 style='text-align: center; color: #555;'>\"Estribos Bemon: El alma de tu concreto\"</h4>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- BOTÓN DE DESCARGA DIRECTA ---
ruta_pdf, nombre_pdf = generar_pdf_en_memoria(
    num_cotizacion, cliente, fecha_exp, fecha_ven, items_calculados, subtotal_general, iva_general, gran_total, incluir_iva
)

with open(ruta_pdf, "rb") as archivo_pdf:
    st.download_button(
        label="📥 Descargar PDF Oficial de Alta Gama",
        data=archivo_pdf,
        file_name=nombre_pdf,
        mime="application/pdf",
        type="primary"
    )