import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="SmartBite OS", page_icon="🍳", layout="wide")

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

# 3. INTERFAZ DE USUARIO Y ROLES
st.title("🍳 SmartBite OS — Gestión Inteligente de Mermas y Costos")
rol = st.sidebar.radio("Módulo de Visualización (Demo):", ["Chef (Cocina)", "Gerente (Administración)"])

st.sidebar.markdown("---")
st.sidebar.info("*Enfoque Empresarial:* Este prototipo integra el control operativo de mermas con la toma de decisiones asistida por un motor lógico de optimización de costos.")

# --- VISTA OPERATIVA: CHEF ---
if rol == "Chef (Cocina)":
    st.header("Sección Operativa de Cocina")
    
    with st.expander("📝 Registrar Nueva Merma / Descarte", expanded=True):
        with st.form("form_merma", clear_on_submit=True):
            insumo_sel = st.selectbox("Insumo descartado:", st.session_state.insumos["Nombre"].tolist())
            cantidad = st.number_input("Cantidad botada (Kg/Lt/Unidades):", min_value=0.1, step=0.1)
            motivo = st.selectbox("Motivo del descarte:", ["Vencimiento", "Error de preparación", "Mal estado al recibir"])
            btn_guardar = st.form_submit_button("Registrar Descarte")
            
            if btn_guardar:
                precio_u = st.session_state.insumos.loc[st.session_state.insumos["Nombre"] == insumo_sel, "Precio_Unitario_COP"].values[0]
                costo_p = cantidad * precio_u
                
                st.session_state.insumos.loc[st.session_state.insumos["Nombre"] == insumo_sel, "Stock_Actual"] -= cantidad
                
                nueva_merma = {"Fecha": str(datetime.now().date()), "Insumo": insumo_sel, "Cantidad": cantidad, "Motivo": motivo, "Costo_Perdida": costo_p}
                st.session_state.mermas = pd.concat([st.session_state.mermas, pd.DataFrame([nueva_merma])], ignore_index=True)
                st.success(f"✅ Registro exitoso. Pérdida calculada para el negocio: ${costo_p:,.0f} COP")

    st.subheader("🤖 Chef Assistant: Recomendador de Aprovechamiento")
    ingredientes_disponibles = st.text_area("¿Qué ingredientes tienen un exceso de stock o están maduros en bodega?", placeholder="Ej: Tomate chonto muy maduro...", value="Tomate chonto dañado")
    
    if st.button("Generar Receta de Reskate Financiero"):
        with st.spinner("El motor de optimización culinaria está estructurando la propuesta..."):
            # Simulación inteligente basada en palabras clave
            texto_usuario = ingredientes_disponibles.lower()
            
            if "tomate" in texto_usuario:
                receta_simulada = """
                ### 🍅 Propuesta de Aprovechamiento: Mermelada Comercial de Tomate Chonto
                * *Análisis de Costo:* Costo de recuperación estimado en $4.500 COP por kilo.
                * *Precio Sugerido de Venta:* $18.000 COP (Frasco de 250g como souvenir/acompañamiento premium).
                * *Margen de Contribución:* *75%*
                
                *Pasos de Preparación:*
                1. Blanquear los tomates maduros para retirar la piel con facilidad.
                2. Sancochar a fuego lento con un 50% de su peso en azúcar y una pizca de canela para espesar.
                3. Envasar al vacío en frascos de vidrio esterilizados. Ideal para acompañar tablas de quesos en el menú de entradas.
                """
            elif "pollo" in texto_usuario:
                receta_simulada = """
                ### 🍗 Propuesta de Aprovechamiento: Croquetas de Pollo Cremosas (Aperitivo)
                * *Análisis de Costo:* Reaprovechamiento de mermas de producción de pechuga.
                * *Precio Sugerido de Venta:* $22.000 COP (Porción de 6 unidades para compartir).
                * *Margen de Contribución:* *68%*
                
                *Pasos de Preparación:*
                1. Desmechar los excedentes de pechuga de pollo cocida.
                2. Crear una salsa bechamel muy densa, incorporar el pollo y dejar enfriar la masa.
                3. Bolear, pasar por harina, huevo, panko y freír a 180°C hasta dorar. Servir con alioli de la casa.
                """
            else:
                receta_simulada = """
                ### 🍳 Propuesta de Aprovechamiento Estándar: Salsa Base de la Casa
                * *Precio Sugerido de Venta:* Incorporación como cortesía premium para elevar el valor percibido de platos fuertes.
                
                *Pasos de Preparación:*
                1. Procesar los insumos vegetales o proteicos en técnicas de cocción prolongada (fondos o reducciones).
                2. Ligar con mantequilla fría para dar brillo y napar las proteínas del menú del día, reduciendo el indicador general de desperdicio culinario a cero.
                """
            st.markdown(receta_simulada)

# --- VISTA ESTRATÉGICA: GERENTE ---
else:
    st.header("Panel de Control Financiero y Cadena de Suministro")
    
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

    st.subheader("📦 Monitor de Inventario de Materia Prima")
    df_inventario = st.session_state.insumos.copy()
    df_inventario["Estado del Recurso"] = df_inventario.apply(lambda r: "🚨 RECOMPRA URGENTE" if r["Stock_Actual"] <= r["Stock_Minimo"] else "✅ ÓPTIMO", axis=1)
    st.dataframe(df_inventario, use_container_width=True)

    st.subheader("🛒 Sugerencias de Abastecimiento Automatizado")
    if len(insumos_criticos) > 0:
        insumo_a_pedir = st.selectbox("Seleccione el insumo crítico para gestionar automáticamente:", insumos_criticos["Nombre"].tolist())
        
        if st.button("Redactar Orden de Compra Automática"):
            info_insumo = insumos_criticos[insumos_criticos["Nombre"] == insumo_a_pedir].iloc[0]
            with st.spinner("El sistema de compras internas está estructurando la solicitud..."):
                correo_simulado = f"""Asunto: SOLICITUD URGENTE: Reposición de Stock - SmartBite OS

Estimado equipo de {info_insumo['Proveedor']},

Espero que se encuentren muy bien. Basados en nuestro sistema automatizado de control de inventarios SmartBite OS, hemos detectado que nuestro stock del insumo "{info_insumo['Nombre']}" ha cruzado el umbral crítico de seguridad.

Por medio de la presente, solicitamos formalmente el despacho urgente de unidades de reposición para mantener nuestros estándares operativos en cocina. Por favor, enviar la cotización correspondiente adjunta a este hilo.

Cordialmente,
Departamento de Alimentos y Bebidas / Gerencia de Operaciones
Prototipo Académico - Universidad de La Sabana
"""
                st.session_state.ordenes.append({
                    "Insumo": insumo_a_pedir, "Proveedor": info_insumo['Proveedor'], "Estado": "Sugerido automáticamente", "Borrador": correo_simulado
                })
                st.success("Borrador estratégico guardado en el pipeline de compras.")
                    
    if st.session_state.ordenes:
        st.write("*Tablero de Seguimiento de Adquisiciones:*")
        for i, orden in enumerate(st.session_state.ordenes):
            st.markdown(f"📦 *Pedido #{i+1}: {orden['Insumo']} ➡️ {orden['Proveedor']}* | Estado: {orden['Estado']}")
            with st.expander("Inspeccionar borrador de correo generado"):
                st.text(orden["Borrador"])
                if orden["Estado"] == "Sugerido automáticamente":
                    if st.button(f"Aprobar y Despachar Pedido #{i+1}"):
                        st.session_state.ordenes[i]["Estado"] = "Enviado al Proveedor"
                        st.rerun()

# 4. GOBIERNO Y NOTA
st.markdown("---")
st.caption("🛡️ *SmartBite OS - Simulación del Motor Lógico:* Módulo interactivo optimizado para presentaciones en tiempo real. Desarrollado con fines académicos.")
