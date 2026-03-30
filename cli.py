import argparse
import pandas as pd
import sys
import json

def main():
    """
    Enhanced CLI for querying Latin America Demographic Data.
    Supports filtering by country, indicator, and year.
    Allows outputting results to terminal, CSV, or JSON.
    """
    parser = argparse.ArgumentParser(description="CLI for Latin America Demographic Data Queries (v3.0)")
    parser.add_argument("--country", type=str, help="Filter by country name (e.g., Mexico, Brazil)")
    parser.add_argument("--indicator", type=str, help="Filter by indicator (e.g., Esperanza_Vida, Tasa_Dependencia_Total)")
    parser.add_argument("--year", type=int, help="Filter by year (2000-2030)")
    parser.add_argument("--output", type=str, choices=['csv', 'json'], help="Save output to file format")

    args = parser.parse_args()

    file_path = 'data/population_evolution_latin_america_by_age_2000_2030_forecast.csv'

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Data file {file_path} not found. Run 'python3 main.py' first.")
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
        return

    if args.output == 'csv':
        df.to_csv("query_result.csv", index=False)
        print("Result saved to query_result.csv")
    elif args.output == 'json':
        df.to_json("query_result.json", orient='records', indent=2)
        print("Result saved to query_result.json")
    else:
        print(df.to_string(index=False))

if __name__ == "__main__":
    main()
