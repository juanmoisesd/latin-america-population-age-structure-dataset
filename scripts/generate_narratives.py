import pandas as pd
import json
import os

def generate_narrative(row):
    country = row['País']
    ev = row['Esperanza_Vida']
    em = row['Edad_Mediana_Estimada']
    td = row['Tasa_Dependencia_Total']

    status = "avanzado" if em > 35 else "intermedio" if em > 28 else "joven"

    narrative = f"{country} presenta un perfil demográfico {status}. "
    narrative += f"Con una esperanza de vida de {ev} años y una edad mediana de {em} años, "
    narrative += f"el país enfrenta desafíos en la relación de dependencia ({td:.1f}%). "

    if status == "avanzado":
        narrative += "La prioridad debe ser la sostenibilidad de los sistemas de pensiones y salud geriátrica."
    elif status == "joven":
        narrative += "Existe una ventana de oportunidad única para invertir en educación y capital humano antes de que el bono demográfico se cierre."
    else:
        narrative += "Se encuentra en una fase crucial de transición donde debe equilibrar la inversión productiva con la preparación para el envejecimiento futuro."

    return narrative

def main():
    df = pd.read_csv('data/population_evolution_latin_america_by_age_2000_2030_forecast.csv')
    df_2023 = df[df['Año'] == 2023]

    narratives = {}
    for _, row in df_2023.iterrows():
        narratives[row['País']] = generate_narrative(row)

    os.makedirs('docs/api', exist_ok=True)
    with open('docs/api/narratives.json', 'w', encoding='utf-8') as f:
        json.dump(narratives, f, indent=2, ensure_ascii=False)

    print("Automated demographic narratives generated.")

if __name__ == "__main__": main()
