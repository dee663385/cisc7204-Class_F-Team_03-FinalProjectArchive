# Codebook - Macao Tourism and GDP Analysis

## Dataset

`data/macao_tourism_gdp_clean.csv` is the complete merged annual analysis file used in the project.

- Unit of analysis: one calendar year in Macao.
- Coverage: 2000-2024.
- Rows: 25.
- Primary key: `year`.
- Missing values in `arrivals` and `gdp_pc`: none.

## Variables

| Variable | Type | Unit | Description | Source / transformation |
| --- | --- | --- | --- | --- |
| `year` | integer | calendar year | Observation year | Join key |
| `arrivals` | decimal | tourist trips per year | International overnight tourist trips; repeat visits count and same-day visits are excluded | UN Tourism via Our World in Data |
| `gdp_pc` | decimal | constant 2021 international dollars at PPP | Real GDP per capita for Macao | World Bank `NY.GDP.PCAP.PP.KD` |
| `period` | text | category | `Pre-pandemic (2000-2019)`, `Pandemic (2020-2022)`, or `Recovery (2023-2024)` | Assigned from year |
| `arrivals_index` | decimal | index, 2000 = 100 | `arrivals / arrivals_2000 * 100` | Derived |
| `gdp_index` | decimal | index, 2000 = 100 | `gdp_pc / gdp_pc_2000 * 100` | Derived |
| `arrivals_yoy` | decimal | percent | Year-on-year percentage change in arrivals | `arrivals.pct_change() * 100` |
| `gdp_yoy` | decimal | percent | Year-on-year percentage change in GDP per capita | `gdp_pc.pct_change() * 100` |

## Period definitions

| Period | Years | Intended use |
| --- | --- | --- |
| Pre-pandemic | 2000-2019 | Stable-period levels and growth comparisons |
| Pandemic | 2020-2022 | Descriptive shock period only; sample too small for stable correlation inference |
| Recovery | 2023-2024 | 2024 versus 2019 recovery-gap comparison |

## Analysis samples

| Analysis | Years used | n | Notes |
| --- | --- | ---: | --- |
| Full-sample levels | 2000-2024 | 25 | Complete annual observations |
| Pre-pandemic levels | 2000-2019 | 20 | Excludes pandemic and recovery years |
| Full-sample annual growth | 2001-2024 | 24 | First year has no prior observation |
| Pre-pandemic annual growth | 2001-2019 | 19 | Excludes 2020-2024 and the first year |
| Recovery gap | 2019 and 2024 | 2 | Ratio comparison only; no correlation reported |

## Validation rules

The notebook checks:

1. The file contains exactly 25 rows.
2. `year` is unique.
3. `arrivals` and `gdp_pc` contain no missing values.
4. The year range is exactly 2000-2024.
5. Index values start at 100 in 2000.
6. Growth rates are missing only for 2000.
7. The full-sample level correlation reproduces approximately 0.819.

## Derived measures

### Index

```text
arrivals_index = arrivals / arrivals_2000 * 100
gdp_index = gdp_pc / gdp_pc_2000 * 100
```

The index preserves relative movement and makes variables with different units visually comparable. It does not remove time trends.

### Annual growth

```text
arrivals_yoy = (arrivals_t / arrivals_t-1 - 1) * 100
gdp_yoy = (gdp_pc_t / gdp_pc_t-1 - 1) * 100
```

Annual growth reduces the influence of the shared long-run trend, but it does not solve all time-series dependence problems.

### Log-log slope

```text
log(gdp_pc) = a + b * log(arrivals) + error
```

The fitted slope is reported as a descriptive elasticity. It is not interpreted as a causal effect.

### Recovery compared with 2019

```text
arrivals_recovery = arrivals_2024 / arrivals_2019 * 100
gdp_recovery = gdp_pc_2024 / gdp_pc_2019 * 100
recovery_gap = arrivals_recovery - gdp_recovery
```

## Output files

- `results/correlation_results.json`: correlation estimates and p-values.
- `results/summary_stats.json`: headline descriptive and recovery statistics.
- `results/analysis_summary.csv`: compact table of correlation results.

## Interpretation rules

- Use associational language: "associated with", "co-moves with", or "tracks".
- Do not use causal language: "causes", "leads to", or "drives".
- Do not treat the 2020-2022 and 2023-2024 correlations as stable findings.
- Always report the sample size beside correlation estimates.
- Report the log-log slope as descriptive.

## Data limitations

- Small annual sample.
- Shared trends and common shocks.
- Omitted economic factors such as gaming revenue, visitor spending, investment, and external demand.
- No causal identification.
- No out-of-sample forecast evaluation.
