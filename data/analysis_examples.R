# Ejemplo de análisis del dataset demográfico
# Autor: Juan Moisés de la Serna
# Dataset DOI: https://doi.org/10.5281/zenodo.18883431

# cargar librerías
library(readr)
library(dplyr)
library(ggplot2)

# cargar dataset
df <- read_csv("dataset.csv")

# mostrar primeras filas
head(df)

# promedio regional de población mayor de 65 años por año
aging <- df %>%
  group_by(Año) %>%
  summarise(promedio_65 = mean(Pct65ms, na.rm = TRUE))

print(aging)

# gráfico de evolución del envejecimiento
ggplot(aging, aes(x = Año, y = promedio_65)) +
  geom_line() +
  labs(
    title = "Promedio regional de población mayor de 65 años",
    x = "Año",
    y = "Porcentaje"
  )

# país con mayor envejecimiento en el último año
latest_year <- max(df$Año)

latest <- df %>%
  filter(Año == latest_year)

top_country <- latest %>%
  arrange(desc(Pct65ms)) %>%
  slice(1)

print(top_country)
