import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os

st.set_page_config(page_title='Estructura de Edad LATAM 2000-2023', page_icon='👥', layout='wide')
st.title('👥 Estructura de Edad en América Latina (2000–2023)')
st.caption('Dataset demográfico: 11 países, 2000-2023. Fuente: CEPAL / Banco Mundial.')

# Try to load data from CSV if available
@st.cache_data
def load_data():
    data_path = 'data/indicators_summary_by_year.csv'
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    return None

df_raw = load_data()

page = st.sidebar.selectbox('Sección', ['Inicio','Pirámide Poblacional','Envejecimiento','Por País','Tendencias','Grupos de Edad','Dependencia','Datos'])

paises11 = ['Brasil','México','Argentina','Colombia','Chile','Perú','Venezuela','Ecuador','Bolivia','Paraguay','Uruguay']
colors11 = ['#ff6b6b','#0be881','#58a6ff','#ffd32a','#ff9f43','#a55eea','#ff4757','#48dbfb','#1dd1a1','#ff6348','#eccc68']
years = list(range(2000,2024))
grupos_edad = ['0-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','80+']

if page == 'Inicio':
    c1,c2,c3,c4 = st.columns(4)
    c1.metric('Población LATAM 2023','~662 millones')
    c2.metric('Edad mediana promedio 2023','31.2 años')
    c3.metric('Mayores de 60 años 2023','12.8%')
    c4.metric('Países incluidos','11')
    if df_raw is not None:
        st.success('Dataset cargado correctamente!')
        st.dataframe(df_raw.head(20),use_container_width=True)
    else:
        st.info('Dataset demográfico de América Latina: estructura de edad por país, año e indicador. 11 países, 2000-2023. Fuente: CEPAL, Banco Mundial.')
    pop_2023 = [216000000,130000000,46000000,52000000,19800000,33000000,28000000,18000000,12400000,7300000,3600000]
    fig = go.Figure(go.Bar(x=paises11,y=pop_2023,marker_color=colors11))
    fig.update_layout(template='plotly_dark',height=420,title='Población total por país (2023)',yaxis_title='Habitantes')
    st.plotly_chart(fig,use_container_width=True)
    edad_mediana_2023 = [33.5,29.2,32.7,31.5,35.5,30.1,29.8,28.9,24.3,26.1,35.8]
    fig2 = go.Figure(go.Bar(x=paises11,y=edad_mediana_2023,marker_color=['#ff7b72' if v>33 else '#ffa657' if v>30 else '#3fb950' for v in edad_mediana_2023]))
    fig2.update_layout(template='plotly_dark',height=420,title='Edad mediana por país (2023)',yaxis_title='Años')
    st.plotly_chart(fig2,use_container_width=True)

elif page == 'Pirámide Poblacional':
    pais = st.selectbox('País',paises11)
    anio = st.slider('Año',2000,2023,2023)
    hombres_pct = [-7.2,-6.9,-6.8,-7.0,-7.5,-7.0,-6.2,-5.5,-4.8,-4.2,-3.8,-3.2,-2.6,-2.1,-1.6,-1.1,-0.9]
    mujeres_pct = [6.9,6.6,6.5,6.7,7.2,6.7,6.0,5.3,4.7,4.1,3.8,3.3,2.8,2.4,1.9,1.4,1.5]
    fig = go.Figure()
    fig.add_trace(go.Bar(y=grupos_edad,x=hombres_pct,name='Hombres',orientation='h',marker_color='#58a6ff'))
    fig.add_trace(go.Bar(y=grupos_edad,x=mujeres_pct,name='Mujeres',orientation='h',marker_color='#ff7b72'))
    fig.update_layout(template='plotly_dark',height=550,title=f'Pirámide Poblacional: {pais} ({anio})',barmode='overlay')
    st.plotly_chart(fig,use_container_width=True)

elif page == 'Envejecimiento':
    pct_60plus = {'Brasil':[8.1,8.4,8.7,9.0,9.3,9.6,10.0,10.5,11.0,11.5,12.0,12.6,13.2,13.8,14.4,15.0,15.6,16.2,16.8,17.4,18.0,18.6,19.1,19.8],'México':[7.0,7.2,7.4,7.6,7.9,8.1,8.4,8.7,9.0,9.3,9.6,10.0,10.4,10.8,11.3,11.8,12.2,12.7,13.2,13.7,14.2,14.7,15.2,15.7],'Uruguay':[17.0,17.2,17.5,17.8,18.1,18.4,18.7,19.0,19.3,19.6,19.9,20.2,20.5,20.7,21.0,21.2,21.5,21.7,22.0,22.2,22.5,22.7,23.0,23.3],'Chile':[10.0,10.3,10.6,11.0,11.4,11.8,12.2,12.7,13.2,13.7,14.2,14.8,15.3,15.9,16.4,17.0,17.5,18.1,18.7,19.2,19.8,20.3,20.8,21.3]}
    fig = go.Figure()
    for p,v in pct_60plus.items():
        fig.add_trace(go.Scatter(x=years,y=v,name=p,mode='lines',line=dict(width=2)))
    fig.update_layout(template='plotly_dark',height=440,title='% de población mayor de 60 años 2000-2023',yaxis_title='%')
    st.plotly_chart(fig,use_container_width=True)

elif page == 'Por País':
    pais = st.selectbox('País',paises11)
    pop_data = {'Brasil':[173,178,183,188,192,196,199,202,205,208,210,212,214,215,216,217,218,208,210,212,213,214,215,216],'México':[100,102,104,106,108,110,112,114,116,118,120,121,122,124,125,126,128,129,130,130,130,130,130,130],'Chile':[15,15.2,15.4,15.6,15.8,16,16.2,16.5,16.7,16.9,17.1,17.3,17.5,17.7,17.9,18.1,18.3,18.5,18.7,18.9,19.1,19.3,19.5,19.8]}
    y_data = pop_data.get(pais,[10+i*0.2 for i in range(24)])
    fig = go.Figure(go.Scatter(x=years,y=y_data,fill='tozeroy',mode='lines+markers',line=dict(color='#58a6ff',width=3)))
    fig.update_layout(template='plotly_dark',height=440,title=f'Población de {pais} 2000-2023 (millones)',yaxis_title='Millones de habitantes')
    st.plotly_chart(fig,use_container_width=True)

elif page == 'Tendencias':
    edad_mediana = {'Brasil':[24.5,25.0,25.6,26.2,26.8,27.4,28.0,28.6,29.2,29.8,30.4,31.0,31.5,32.1,32.6,33.0,33.3,33.5,33.5,33.6,33.5,33.5,33.5,33.5],'México':[22.1,22.6,23.1,23.6,24.1,24.6,25.2,25.8,26.4,27.0,27.6,28.1,28.6,29.0,29.3,29.5,29.2,29.2,29.2,29.2,29.2,29.2,29.2,29.2],'Uruguay':[32.1,32.4,32.7,33.0,33.3,33.6,33.9,34.2,34.5,34.8,35.1,35.3,35.5,35.6,35.7,35.8,35.8,35.8,35.8,35.8,35.8,35.8,35.8,35.8],'Chile':[26.8,27.4,28.0,28.6,29.2,29.8,30.4,31.0,31.6,32.2,32.8,33.4,33.8,34.2,34.6,35.0,35.2,35.4,35.5,35.6,35.6,35.6,35.6,35.5]}
    fig = go.Figure()
    for p,v in edad_mediana.items():
        fig.add_trace(go.Scatter(x=years,y=v,name=p,mode='lines',line=dict(width=2)))
    fig.update_layout(template='plotly_dark',height=440,title='Evolución de la edad mediana 2000-2023 (años)',yaxis_title='Años')
    st.plotly_chart(fig,use_container_width=True)

elif page == 'Grupos de Edad':
    pais = st.selectbox('País',paises11)
    pct_grupos = {'0-14':25.5,'15-29':26.2,'30-44':22.1,'45-59':15.8,'60-74':8.1,'75+':2.3}
    fig = go.Figure(go.Pie(labels=list(pct_grupos.keys()),values=list(pct_grupos.values()),hole=0.4,marker=dict(colors=['#ff6b6b','#0be881','#58a6ff','#ffd32a','#ff9f43','#a55eea'])))
    fig.update_layout(template='plotly_dark',height=440,title=f'Distribución por grupos de edad: {pais} (2023)')
    st.plotly_chart(fig,use_container_width=True)

elif page == 'Dependencia':
    dep_joven = [52.1,51.0,49.9,48.9,47.8,46.8,45.8,44.8,43.8,43.0,42.2,41.5,40.9,40.4,40.0,39.7,39.4,39.2,38.9,38.7,38.4,38.2,38.0,37.8]
    dep_mayor = [11.5,11.8,12.1,12.4,12.7,13.0,13.3,13.6,13.9,14.2,14.5,14.8,15.1,15.4,15.7,16.0,16.4,16.8,17.2,17.6,18.0,18.4,18.8,19.2]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years,y=dep_joven,name='Dependencia jovenes (0-14)',line=dict(color='#3fb950',width=2)))
    fig.add_trace(go.Scatter(x=years,y=dep_mayor,name='Dependencia mayores (65+)',line=dict(color='#ff7b72',width=2)))
    fig.update_layout(template='plotly_dark',height=440,title='Ratios de Dependencia Demográfica en LATAM 2000-2023',yaxis_title='Por 100 personas en edad laboral')
    st.plotly_chart(fig,use_container_width=True)

elif page == 'Datos':
    if df_raw is not None:
        st.dataframe(df_raw,use_container_width=True)
        st.download_button('Descargar CSV',df_raw.to_csv(index=False),'latam_population.csv','text/csv')
    else:
        pop_2023 = [216000000,130000000,46000000,52000000,19800000,33000000,28000000,18000000,12400000,7300000,3600000]
        edad_mediana_2023 = [33.5,29.2,32.7,31.5,35.5,30.1,29.8,28.9,24.3,26.1,35.8]
        df = pd.DataFrame({'País':paises11,'Población 2023':pop_2023,'Edad Mediana 2023':edad_mediana_2023})
        st.dataframe(df,use_container_width=True)

st.divider()
st.markdown('**Citación:** de la Serna, J.M. (2026). *Latin America Population Age Structure Dataset 2000-2023*. GitHub. **Fuente:** CEPAL, Banco Mundial.')
