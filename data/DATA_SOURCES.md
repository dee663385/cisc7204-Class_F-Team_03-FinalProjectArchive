# Data Sources

## Primary analysis data

### Tourism arrivals

- Variable: International overnight tourist trips per year.
- Institutional source: UN Tourism.
- Distribution source: Our World in Data.
- OWID dataset slug: `international-tourist-trips`.
- URL: https://ourworldindata.org/grapher/international-tourist-trips
- Coverage used: 2000-2024.
- Definition: overnight tourist trips; repeat visits count; same-day visits are excluded.
- Location: Macao.

### Real GDP per capita

- Variable: GDP per capita, PPP, constant 2021 international dollars.
- Source: World Bank World Development Indicators.
- Indicator: `NY.GDP.PCAP.PP.KD`.
- Indicator page: https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD?locations=MO
- API endpoint: https://api.worldbank.org/v2/country/MAC/indicator/NY.GDP.PCAP.PP.KD?format=json&per_page=100
- Coverage used: 2000-2024.
- Location: Macao.

## Why UN Tourism arrivals rather than World Bank arrivals

The World Bank arrivals indicator `ST.INT.ARVL` ended in 2020 for Macao in the supplied project materials and includes a broader definition of arrivals, including same-day visitors. The project therefore uses the UN Tourism overnight-tourist-trips series distributed by OWID. This gives a consistent definition and full coverage through 2024.

## Data files in this archive

- `data/macao_tourism_gdp_clean.csv`: complete merged analytic dataset.
- `data/source_extracts/arrivals_un_tourism_owid_2000_2024.csv`: arrivals extract used in the analysis.
- `data/source_extracts/gdp_per_capita_world_bank_2000_2024.csv`: GDP per capita extract used in the analysis.

## Reproducibility note

The complete analytic sample is included in the archive, so the notebook runs without network access. The source URLs above are retained so that a reader can verify definitions and retrieve updated versions if needed. Data access dates and source decisions are also documented in `project_docs/feasibility/Feasibility_Check_Macao_Tourism.docx` and the project proposal.

## Citation guidance

Suggested source wording in the report and notebook:

> UN Tourism (2025), distributed by Our World in Data, "International tourist trips"; World Bank (2025), World Development Indicators, indicator NY.GDP.PCAP.PP.KD.
