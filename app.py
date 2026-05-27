import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="SmartBite OS", page_icon="🍳", layout="wide")

if 'insumos' not in st.session_state:
    st.session_state.insumos = pd.DataFrame([
        {
            "ID": 1,
            "Nombre": "Queso Mozzarella",
            "Stock_Actual": 15.0,
            "Stock_Minimo": 10.0,
            "Precio_Unitario_COP": 25000,
            "Proveedor": "Lácteos del Campo",
        },
        {
            "ID": 2,
            "Nombre": "Tomate Chonto",
            "Stock_Actual": 4.0,
            "Stock_Minimo": 12.0,
            "Precio_Unitario_COP": 4500,
            "Proveedor": "Fruver Central",
        },
        {
            "ID": 3,
            "Nombre": "Pechuga de Pollo",
            "Stock_Actual": 3.5,
            "Stock_Minimo": 8.0,
            "Precio_Unitario_COP": 14000,
            "Proveedor": "Distribuidora Avícola",
        },
        {
            "ID": 4,
            "Nombre": "Harina de Trigo",
            "Stock_Actual": 50.0,
            "Stock_Minimo": 20.0,
            "Precio_Unitario_COP": 3200,
            "Proveedor": "Molinos del Norte",
        },
    ])

if 'mermas' not in st.session_state:
    st.session_state.mermas = pd.DataFrame([
        {
            "Fecha": "2026-05-24",
            "Insumo": "Tomate Chonto",
            "Cantidad": 2.0,
            "Motivo": "Vencimiento",
            "Costo_Perdida": 9000,
        },
        {
            "Fecha": "2026-05-25",
            "Insumo": "Pechuga de Pollo",
            "Cantidad": 1.5,
            "Motivo": "Error de preparación",
            "Costo_Perdida": 21000,
        },
    ])

if 'ordenes' not in st.session_state:
    st.session_state.ordenes = []

st.title("🍳 SmartBite OS — Gestión Inteligente de Mermas y Costos")
rol = st.sidebar.radio("Módulo de Visualización (Demo):", ["Chef (Cocina)", "Gerente (Administración)"])

st.sidebar.markdown("---")
st.sidebar.info(
    "*Enfoque Empresarial:* Este prototipo integra el control operativo de mermas con la toma de decisiones estratégicas sobre inventario y costos."
)

st.sidebar.markdown("Última actualización: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

low_stock = st.session_state.insumos[st.session_state.insumos['Stock_Actual'] < st.session_state.insumos['Stock_Minimo']]
total_merma = st.session_state.mermas['Costo_Perdida'].sum()

if rol == "Chef (Cocina)":
    st.subheader("Panel de Cocina")
    st.markdown("### Mermas recientes")
    st.dataframe(st.session_state.mermas)
    st.markdown("### Insumos con alerta de stock")
    if low_stock.empty:
        st.success("No hay insumos por debajo del stock mínimo.")
    else:
        st.dataframe(low_stock)
    st.markdown("### Resumen de pérdidas")
    st.write(f"Costo total registrado por mermas: COP {int(total_merma):,}")

else:
    st.subheader("Panel de Gerencia")
    st.markdown("### Inventario de insumos")
    st.dataframe(st.session_state.insumos)
    st.markdown("### Alertas de stock bajo")
    if low_stock.empty:
        st.success("Todos los insumos tienen stock suficiente.")
    else:
        st.dataframe(low_stock)
    st.markdown("### Control de costos y mermas")
    st.write(f"Total de pérdidas por mermas: COP {int(total_merma):,}")

    st.markdown("---")
    st.markdown("#### Nueva orden de compra (simulada)")
    with st.form(key='orden_form'):
        proveedor = st.selectbox("Proveedor", sorted(st.session_state.insumos['Proveedor'].unique()))
        insumo = st.selectbox("Insumo", st.session_state.insumos['Nombre'].tolist())
        cantidad = st.number_input("Cantidad a solicitar", min_value=1.0, value=5.0, step=0.5)
        submitted = st.form_submit_button("Registrar orden")
        if submitted:
            st.session_state.ordenes.append({
                "Proveedor": proveedor,
                "Insumo": insumo,
                "Cantidad": cantidad,
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })
            st.success("Orden registrada correctamente.")

    if st.session_state.ordenes:
        st.markdown("#### Órdenes registradas")
        st.dataframe(pd.DataFrame(st.session_state.ordenes))
