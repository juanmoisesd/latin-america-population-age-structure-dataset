import json, pandas as pd
INPUT='data/dataset.csv'; OUTPUT_JSON='docs/atlas/data/atlas_data.json'; OUTPUT_CSV='docs/atlas/data/atlas_data_with_indicators.csv'
df=pd.read_csv(INPUT)
work_pct=df['Pct_15_24']+df['Pct_25_54']+df['Pct_55_64']
work_pop=df['Pob_15_24_Miles']+df['Pob_25_54_Miles']+df['Pob_55_64_Miles']
dep_pop=df['Pob_0_14_Miles']+df['Pob_65_más_Miles']
df['Indice_Envejecimiento']=(df['Pob_65_más_Miles']/df['Pob_0_14_Miles'])*100
df['Razon_Dependencia_Total']=dep_pop/work_pop
df['Indice_Bono_Demografico']=work_pop/dep_pop
df['Pct_Edad_Laboral']=work_pct
df['Pct_Joven_Total']=df['Pct_0_14']+df['Pct_15_24']
df['Pob_Edad_Laboral_Miles']=work_pop
records=[]
for _,r in df.iterrows():
    records.append({'country':r['País'],'year':int(r['Año']),'population_total_millions':float(r['Población_Total_Millones']),'age_groups_pct':{'0_14':float(r['Pct_0_14']),'15_24':float(r['Pct_15_24']),'25_54':float(r['Pct_25_54']),'55_64':float(r['Pct_55_64']),'65_plus':float(r['Pct_65_más'])},'age_groups_thousands':{'0_14':float(r['Pob_0_14_Miles']),'15_24':float(r['Pob_15_24_Miles']),'25_54':float(r['Pob_25_54_Miles']),'55_64':float(r['Pob_55_64_Miles']),'65_plus':float(r['Pob_65_más_Miles'])},'indicators':{'aging_index':round(float(r['Indice_Envejecimiento']),4),'dependency_ratio_total':round(float(r['Razon_Dependencia_Total']),6),'demographic_dividend_index':round(float(r['Indice_Bono_Demografico']),6),'working_age_pct':round(float(r['Pct_Edad_Laboral']),4),'youth_pct':round(float(r['Pct_Joven_Total']),4),'working_age_thousands':round(float(r['Pob_Edad_Laboral_Miles']),2)},'source':r['Fuente']})
with open(OUTPUT_JSON,'w',encoding='utf-8') as f: json.dump({'title':'Atlas Demográfico Interactivo de América Latina','author':'Juan Moisés de la Serna','year_published':2026,'records':records},f,ensure_ascii=False,indent=2)
df.to_csv(OUTPUT_CSV,index=False,encoding='utf-8-sig')
print('Archivos del atlas regenerados correctamente.')
