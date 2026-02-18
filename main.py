import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Saving Evolution - ROI & Engineering", layout="wide")

st.title("⚡ Saving Evolution: Suite de Optimización Industrial")
st.markdown("---")

# --- LÓGICA DE NEGOCIO (SIDEBAR) ---
with st.sidebar:
    st.header("💰 Parámetros Financieros")
    costo_hora_tecnico = st.number_input("Costo Hora-Hombre (USD)", value=15.0)
    valor_subestacion = st.number_input("Precio Venta Subestación (USD)", value=45000.0)
    st.markdown("---")
    st.header("⚙️ Producción")
    demanda = st.number_input("Meta Mensual (Und)", value=10)
    takt_time = (22 * 8 * 0.85) / demanda

# --- NAVEGACIÓN ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Productividad", "📦 Suministros", "🛡️ Calidad", "💸 ROI Financiero"])

# --- MÓDULO 1: PRODUCTIVIDAD ---
with tab1:
    st.header("Balanceo de Línea (Takt vs Cycle)")
    data = {"Estación": ["Estructura", "Montaje Transfo", "Celdas MT", "Cableado", "Pruebas"],
            "Horas": [12.0, 8.0, 18.0, 25.0, 10.0]}
    df = pd.DataFrame(data)
    edited_df = st.data_editor(df)
    fig = px.bar(edited_df, x="Estación", y="Horas", color="Horas", color_continuous_scale="Viridis")
    fig.add_hline(y=takt_time, line_dash="dash", line_color="red", annotation_text=f"Meta: {takt_time:.1f}h")
    st.plotly_chart(fig, use_container_width=True)

# --- MÓDULO 2: SUMINISTROS ---
with tab2:
    st.header("Gestión de Kitting")
    st.info("💡 El Kitting reduce hasta un 30% el tiempo de ensamble al eliminar búsquedas.")
    inv_data = {"Componente": ["Transformador", "Interruptor MT", "Cables 15kV"], "Estado": ["OK", "FALTANTE", "OK"]}
    st.table(pd.DataFrame(inv_data))

# --- MÓDULO 3: CALIDAD ---
with tab3:
    st.header("Control de Fallas (Jidoka)")
    col_a, col_b = st.columns(2)
    with col_a:
        fallas = pd.DataFrame({"Defecto": ["Torque", "Cableado", "Aislamiento"], "Cant": [10, 5, 2]})
        st.bar_chart(fallas.set_index("Defecto"))
    with col_b:
        st.success("🎯 Objetivo: Reducir retrabajos del 15% al 2% mediante Poka-Yokes.")

# --- MÓDULO 4: ROI FINANCIERO (EL CIERRE) ---
with tab4:
    st.header("📈 Retorno de Inversión Proyectado")
    
    # Cálculos de impacto
    horas_ahorradas_unidad = 10 # Supuesto de mejora por Lean
    ahorro_mensual = horas_ahorradas_unidad * demanda * costo_hora_tecnico
    liberacion_wip = valor_subestacion * 0.10 # 10% de mejora en flujo de caja
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Ahorro Operativo Mensual", f"${ahorro_mensual:,.2f} USD")
    c2.metric("Capital de Trabajo Liberado", f"${liberacion_wip:,.2f} USD")
    c3.metric("Aumento Capacidad", "+20%")

    st.markdown("---")
    st.subheader("Análisis de Impacto Económico")
    roi_data = pd.DataFrame({
        "Concepto": ["Costo Actual", "Costo con Lean (Saving Evolution)"],
        "Valor": [valor_subestacion * 0.85, (valor_subestacion * 0.85) - ahorro_mensual]
    })
    fig_roi = px.pie(roi_data, values="Valor", names="Concepto", hole=0.4, title="Impacto en Costos de Fabricación")
    st.plotly_chart(fig_roi)
    
    st.warning(f"🚀 **CONCLUSIÓN:** La implementación se paga sola en {(ahorro_mensual / 2000):.1f} meses solo con ahorros de eficiencia.")

st.caption("Saving Evolution SAS - Consultoría de Ingeniería Mecánica y Estrategia")
