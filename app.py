import streamlit as st
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

# Cargar las variables de entorno del archivo .env
load_dotenv()

# 1. CONFIGURACIÓN DE LA PÁGINA Y CLIENTE IA
st.set_page_config(page_title="SmartBite OS", page_icon="🍳", layout="wide")

# Inicializar el cliente de OpenAI usando la clave segura del archivo .env
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

# 2. BASE DE DATOS EN MEMORIA (Simulación con Pandas)
if 'insumos' not in st.session_state:
    st.session_state.insumos = pd.DataFrame([
        {"ID": 1, "Nombre": "Queso Mozzarella", "Stock_Actual": 15.0, "Stock_Minimo": 10.0, "Precio_Unitario_COP": 25000, "Proveedor": "Lácteos del Campo"},
        {"ID": 2, "Nombre": "Tomate Chonto", "Stock_Actual": 4.0, "Stock_Minimo": 12.0, "Precio_Unitario_COP": 4500, "Proveedor": "Fruver Central"},
        {"ID": 3, "Nombre": "Pechuga de Pollo", "Stock_Actual": 3.5, "Stock_Minimo": 8.0, "Precio_Unitario_COP": 14000, "Proveedor": "Distribuidora Avícola"},
        {"ID": 4, "Nombre": "Harina de Trigo", "Stock_Actual": 50.0, "Stock_Minimo": 20.0, "Precio_Unitario_COP": 3200, "Proveedor": "Molinos del Norte"}
    ])

if 'mermas' not in st.session_state:
    st.session_state.mermas = pd.DataFrame([
        {"Fecha": "2026-05-24", "Insumo": "Tomate Chonto", "Cantidad": 2.0, "Motivo": "Vencimiento", "Costo_Perdida": 9000},
        {"Fecha": "2026-05-25", "Insumo": "Pechuga de Pollo", "Cantidad": 1.5, "Motivo": "Error de preparación", "Costo_Perdida": 21000}
    ])

if 'ordenes' not in st.session_state:
    st.session_state.ordenes = []

# 3. INTERFAZ DE USUARIO Y ROLES (Módulo 1)
st.title("🍳 SmartBite OS — Gestión Inteligente de Mermas y Costos")
rol = st.sidebar.radio("Módulo de Visualización (Demo):", ["Chef (Cocina)", "Gerente (Administración)"])

st.sidebar.markdown("---")
st.sidebar.info("*Enfoque Empresarial:* Este prototipo integra el control operativo de mermas con la toma de decisiones asistida por IA generativa para mitigar la fuga de utilidades.")

# --- VISTA OPERATIVA: CHEF ---
if rol == "Chef (Cocina)":
    st.header("Sección Operativa de Cocina")
    
    # Módulo 2: Registro de Datos
    with st.expander("📝 Registrar Nueva Merma / Descarte", expanded=True):
        with st.form("form_merma", clear_on_submit=True):
            insumo_sel = st.selectbox("Insumo descartado:", st.session_state.insumos["Nombre"].tolist())
            cantidad = st.number_input("Cantidad botada (Kg/Lt/Unidades):", min_value=0.1, step=0.1)
            motivo = st.selectbox("Motivo del descarte:", ["Vencimiento", "Error de preparación", "Mal estado al recibir"])
            btn_guardar = st.form_submit_button("Registrar Descarte")
            
            if btn_guardar:
                precio_u = st.session_state.insumos.loc[st.session_state.insumos["Nombre"] == insumo_sel, "Precio_Unitario_COP"].values[0]
                costo_p = cantidad * precio_u
                
                # Modificar stock
                st.session_state.insumos.loc[st.session_state.insumos["Nombre"] == insumo_sel, "Stock_Actual"] -= cantidad
                
                # Registrar merma
                nueva_merma = {"Fecha": str(datetime.now().date()), "Insumo": insumo_sel, "Cantidad": cantidad, "Motivo": motivo, "Costo_Perdida": costo_p}
                st.session_state.mermas = pd.concat([st.session_state.mermas, pd.DataFrame([nueva_merma])], ignore_index=True)
                st.success(f"✅ Registro exitoso. Pérdida calculada para el negocio: ${costo_p:,.0f} COP")

    # Módulo 6: Capa de IA Visible
    st.subheader("🤖 Chef Assistant: Recomendador de Aprovechamiento")
    ingredientes_disponibles = st.text_area("¿Qué ingredientes tienen un exceso de stock o están maduros en bodega?", placeholder="Ej: Tomate chonto muy maduro y un bloque de queso mozzarella...")
    
    if st.button("Generar Receta de Rescate Financiero"):
        if not client:
            st.error("❌ No se detectó la OpenAI API Key en el archivo .env")
        elif ingredientes_disponibles:
            with st.spinner("La IA está estructurando una propuesta de menú rentable..."):
                prompt = f"Actúas como un Chef Mentor experto en costos. Propón una receta comercial rápida para usar: {ingredientes_disponibles}. Estructura la respuesta con: Nombre del plato, precio sugerido de venta en COP y pasos simplificados."
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}]
                )
                st.markdown(response.choices[0].message.content)

# --- VISTA ESTRATÉGICA: GERENTE ---
else:
    st.header("Panel de Control Financiero y Cadena de Suministro")
    
    # Módulo 4: Dashboard
    total_perdido = st.session_state.mermas["Costo_Perdida"].sum()
    insumos_criticos = st.session_state.insumos[st.session_state.insumos["Stock_Actual"] <= st.session_state.insumos["Stock_Minimo"]]
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Pérdida Acumulada en Mermas", f"${total_perdido:,.0f} COP")
    col2.metric("Insumos en Stock Crítico", f"{len(insumos_criticos)} Alertas")
    col3.metric("Eficiencia Operativa (Mermas)", f"{len(st.session_state.mermas)} Registros")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.write("*Impacto Financiero por Insumo ($ COP)*")
        df_g1 = st.session_state.mermas.groupby("Insumo")["Costo_Perdida"].sum().reset_index()
        st.bar_chart(data=df_g1, x="Insumo", y="Costo_Perdida")
    with col_g2:
        st.write("*Volumen de Desperdicio según Motivo*")
        df_g2 = st.session_state.mermas.groupby("Motivo")["Cantidad"].sum().reset_index()
        st.bar_chart(data=df_g2, x="Motivo", y="Cantidad")

    # Módulo 3: Base Operativa
    st.subheader("📦 Monitor de Inventario de Materia Prima")
    df_inventario = st.session_state.insumos.copy()
    # Módulo 12: Lógica de priorización
    df_inventario["Estado del Recurso"] = df_inventario.apply(lambda r: "🚨 RECOMPRA URGENTE" if r["Stock_Actual"] <= r["Stock_Minimo"] else "✅ ÓPTIMO", axis=1)
    st.dataframe(df_inventario, use_container_width=True)

    # Módulo 5 y 7: Eficiencia Interna y Seguimiento
    st.subheader("🛒 Sugerencias de Abastecimiento Automatizado")
    if len(insumos_criticos) > 0:
        insumo_a_pedir = st.selectbox("Seleccione el insumo crítico para gestionar con IA:", insumos_criticos["Nombre"].tolist())
        
        if st.button("Redactar Orden de Compra Automática"):
            if not client:
                st.error("❌ Configura la OpenAI API Key en el archivo .env")
            else:
                info_insumo = insumos_criticos[insumos_criticos["Nombre"] == insumo_a_pedir].iloc[0]
                with st.spinner("La IA interna está redactando la solicitud formal..."):
                    prompt_compras = f"Redacta un correo profesional, corporativo y muy breve solicitando una cotización y despacho urgente de {info_insumo['Nombre']} al proveedor {info_insumo['Proveedor']}."
                    response_compras = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt_compras}]
                    )
                    st.session_state.ordenes.append({
                        "Insumo": insumo_a_pedir, "Proveedor": info_insumo['Proveedor'], "Estado": "Sugerido por IA", "Borrador": response_compras.choices[0].message.content
                    })
                    st.success("Borrador estratégico guardado en el pipeline de compras.")
                    
    if st.session_state.ordenes:
        st.write("*Tablero de Seguimiento de Adquisiciones:*")
        for i, orden in enumerate(st.session_state.ordenes):
            st.markdown(f"📦 *Pedido #{i+1}: {orden['Insumo']} ➡️ {orden['Proveedor']}* | Estado: {orden['Estado']}")
            with st.expander("Inspeccionar borrador de correo generado"):
                st.text(orden["Borrador"])
                if orden["Estado"] == "Sugerido por IA":
                    if st.button(f"Aprobar y Despachar Pedido #{i+1}"):
                        st.session_state.ordenes[i]["Estado"] = "Enviado al Proveedor"
                        st.rerun()

# Módulo 8: Gobierno y Confianza
st.markdown("---")
st.caption("🛡️ *SmartBite OS - Gobierno de IA:* Los algoritmos generativos actúan bajo un modelo de 'Human-in-the-loop' donde el personal calificado debe aprobar cada propuesta culinaria o comercial. Aplicación académica de simulación.")
