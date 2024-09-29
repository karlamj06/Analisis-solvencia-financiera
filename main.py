import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import openai

# Cargar los datos desde el repositorio de GitHub
url = "https://raw.githubusercontent.com/karlamj06/Analisis-solvencia-financiera/refs/heads/main/Datos_proyecto_limpio.csv"
data = pd.read_csv(url)

# Visualizar los primeros registros del DataFrame
st.title("Análisis de Solvencia Financiera")
st.write("Este dashboard permite analizar los ratios de solvencia de diferentes empresas.")

# Mostrar los datos
if st.checkbox("Mostrar Datos"):
    st.write(data)

# Cálculo de ratios
data['Ratio Liquidez'] = data['Current_Assets'] / data['Current_Liabilities']
data['Ratio Deuda a Patrimonio'] = (data['Short_Term_Debt'] +data['Long_Term_Debt'])/ data['Equity']
data['Cobertura de Gastos Financieros'] = data['Total_Revenue'] / data['Financial_Expenses']
data['Ratio de Deuda Total a Activos'] = (data['Short_Term_Debt'] +data['Long_Term_Debt'])/data['Current_Assets']
data['Ratio de Rentabilidad'] = data['Total_Revenue'] / data['Equity'] 

# Aplicar filtros
empresa = st.selectbox("Selecciona la empresa:", data['Company_ID'].unique())

# Filtrar datos para la empresa seleccionada
filtered_data = data[data['Company_ID'] == empresa]

# Mostrar ratios calculados
st.subheader(f"Ratios para {empresa}")
st.write(filtered_data[['Ratio Liquidez', 'Ratio Deuda a Patrimonio', 'Cobertura de Gastos Financieros', 'Ratio de Deuda Total a Activos', 'Ratio de Rentabilidad']])

# Gráficos interativos
st.subheader("Visualizaciones")

# Gráfico de Ratio de Liquidez
fig1 = px.bar(filtered_data, x='Company_ID', y='Ratio Liquidez', title='Ratio de Liquidez')
st.plotly_chart(fig1)

# Gráfico de Ratio de Deuda a Patrimonio
fig2 = px.bar(filtered_data, x='Company_ID', y='Ratio Deuda a Patrimonio', title='Ratio de Deuda a Patrimonio')
st.plotly_chart(fig2)

# Gráfico de Cobertura de Gastos Financieros
fig3 = px.bar(filtered_data, x='Company_ID', y='Cobertura de Gastos Financieros', title='Cobertura de Gastos Financieros')
st.plotly_chart(fig3)

# Gráfico de Ratio de Deuda Total a Activos
fig4 = px.bar(filtered_data, x='Company_ID', y='Ratio de Deuda Total a Activos', title='Ratio de Deuda Total a Activos')
st.plotly_chart(fig4)

# Gráfico de Ratio de Rentabilidad
fig5 = px.bar(filtered_data, x='Company_ID', y='Ratio de Rentabilidad' , title='Ratio de Rentabilidad')
st.plotly_chart(fig5)

# Comparativa de todas las empresas
st.subheader("Comparativa de Ratios entre Empresas")
fig6 = px.bar(data, x='Company_ID', y=['Ratio Liquidez', 'Ratio Deuda a Patrimonio', 'Cobertura de Gastos Financieros', 'Ratio de Deuda Total a Activos', 'Ratio de Rentabilidad'], 
       title='Comparativa de Ratios entre Empresas', barmode='group')
st.plotly_chart(fig6)

# Finalizar
st.write("Estos ratios permiten analizar la solvencia de las empresas en función de su liquidez y su capacidad para cubrir sus deudas.")

#Interpretación de la empresa C0027
st.write("A coninuación se interpretarán los resultados de la empresa C0027")
st.write("Para iniciar, la empresa C0027 cuenta con un ratio de liquidez mayor a 1, lo que le permitiría tener los recursos suficientes para cubrir sus obligciones financieras.")
st.write("Lo anterior está en sintonía con el ratio de deuda a patrimonio, el cual es menor a 1, lo que le permite tener una mayor capacidad para cubrir sus deudas. Esto significa que la mayoría de los activos de la empresa están financiados con capital propio, y no con deuda.")
st.write("Sin embargo, la cobertura de gastos financieros es mayor a 1, lo cual indica que esto puede representar un riesgo para la empresa ya que el ratio de deuda a patrimonio es mayor a 1, significa que las deudas de una empresa o persona son mayores que el valor de sus activos. Esto puede ser un riesgo, ya que la empresa depende en gran medida de financiamiento externo.")
st.write("Si bien la mpresa presenta indicadores a lo que se debería prestar especial atención, podemos visualizar que el ratio de deuda total a activos es menor a 1, lo que nos indica que los activos no están en mayor proporción financiados con deuda.")
st.write("Finalmente, el ratio de rentabilidad de la empresa es menor a 1, lo que nos indica que la empresa no es viable. Para ello se aconsejaría llevar a cabo una junta con los accionistas para tomar una decisión y no afectar a las partes interesadas en caso de que la empresa quiebre")

#openai_api_key ='URL API KEY'

# Instanciar el cliente de OpenAI
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=openai_api_key)

def obtener_respuesta(prompt):
  response = client.chat.completions.create(
      model="gpt-4o-mini",  # Ajusta el modelo según lo que necesites
      messages=[
          {"role": "system", "content": """
          Eres un analista que es experto para determinarla solvencia de una entidad
          entonces vas a responder todo para ver si cada empresa tiene los recursos
          suficientes para hacer frente a sus obligaciones. Contesta en un máximo de 50
          palabras.
          """}, #Solo podemos personalizar la parte de content
          {"role": "user", "content": prompt}
      ]
  )
  output = response.choices[0].message.content
  return output

prompt_user= st.text_area("Ingresa tu pregunta: ")

# Obtener la respuesta del modelo
output_modelo = obtener_respuesta(prompt_user)

# Mostrar la respuesta del modelo
st.write(output_modelo)
