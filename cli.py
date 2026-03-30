import argparse
import pandas as pd
import sys

def main():
    parser = argparse.ArgumentParser(description="CLI for Latin America Demographic Data Queries")
    parser.add_argument("--country", type=str, help="Filter by country name (e.g., Mexico, Brazil)")
    parser.add_argument("--indicator", type=str, help="Filter by indicator (e.g., Esperanza_Vida, Tasa_Dependencia_Total)")
    parser.add_argument("--year", type=int, help="Filter by year (2000-2030)")
    parser.add_argument("--forecast", action="store_true", help="Use forecast data (up to 2030)")

    args = parser.parse_args()

    file_path = 'data/population_evolution_latin_america_by_age_2000_2030_forecast.csv' if args.forecast or args.year and args.year > 2023 else 'data/population_evolution_latin_america_by_age_2000_2023.csv'

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Data file {file_path} not found. Run the pipeline first.")
        sys.exit(1)

    if args.country:
        df = df[df['País'].str.contains(args.country, case=False, na=False)]

    if args.year:
        df = df[df['Año'] == args.year]

    if args.indicator:
        cols = ['País', 'Año', args.indicator]
        cols = [c for c in cols if c in df.columns]
        df = df[cols]

    if df.empty:
        print("No data found for the given filters.")
    else:
        print(df.to_string(index=False))

if __name__ == "__main__":
    main()
