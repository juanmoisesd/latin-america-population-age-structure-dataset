all: prepare forecast visualizations site metadata

prepare:
	python3 scripts/prepare_data.py

forecast:
	python3 scripts/forecast_data.py

visualizations:
	python3 scripts/generate_visualizations.py

site:
	python3 scripts/generate_site.py

metadata:
	python3 scripts/update_metadata.py

clean:
	rm -rf visualizations/ docs/countries/ docs/index.html data/population_evolution_latin_america_by_age_2000_2023.csv data/population_evolution_latin_america_by_age_2000_2030_forecast.csv
