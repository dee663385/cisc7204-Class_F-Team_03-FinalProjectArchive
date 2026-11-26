# CISC7204 Class F Team 03 - Final Project Archive

## Submission identity

- Course: CISC7204 Data Science and Data Visualization
- Academic year: 2026/2027, Semester 1
- Class: F
- Team: 03
- Project: Macao Tourism Recovery and Economic Performance, 2000-2024
- Deadline: 2026DEC05, 11:00 pm

## Public GitHub repository

**Required before submission:** add the verified public repository URL below.

`https://github.com/dee663385/cisc7204-Class_F-Team_03-FinalProjectArchive`

The repository should contain the same files as this archive. See `UPLOAD_TO_GITHUB.md` for a short upload procedure.

## Project overview

This project studies whether international overnight tourist arrivals track Macao's real GDP per capita between 2000 and 2024. The analysis is descriptive and observational. It compares three questions:

- RQ1: Are tourist arrivals and real GDP per capita associated in levels, both across the full sample and before the pandemic?
- RQ2: Is the association weaker when the shared trend is removed by using annual growth rates?
- RQ3: By 2024, how far have arrivals and real GDP per capita recovered relative to their 2019 levels?

The analysis deliberately avoids causal and forecast claims. The main point is that tourism and economic performance share a long-run path, but arrivals alone do not track year-to-year output closely enough to be treated as a single indicator of the other.

## Data

The complete analytic sample is:

- `data/macao_tourism_gdp_clean.csv` - 25 annual observations, 2000-2024.
- `data/source_extracts/arrivals_un_tourism_owid_2000_2024.csv` - full arrivals extract used in the analysis.
- `data/source_extracts/gdp_per_capita_world_bank_2000_2024.csv` - full GDP per capita extract used in the analysis.

Definitions:

- Arrivals: UN Tourism overnight tourist trips via Our World in Data. Repeat visits count; same-day visitors are excluded.
- GDP per capita: World Bank indicator `NY.GDP.PCAP.PP.KD`, real GDP per capita at purchasing power parity in constant 2021 international dollars.
- Unit of analysis: one Macao observation per calendar year.
- Coverage: 25 complete observations from 2000 through 2024.

See `data/DATA_SOURCES.md` and `CODEBOOK.md` for source URLs, units, transformations, and validation rules.

## Key results

| Analysis | n | Pearson r | Spearman rho |
| --- | ---: | ---: | ---: |
| Full-sample levels | 25 | 0.819 | 0.834 |
| Pre-pandemic levels | 20 | 0.811 | 0.820 |
| Full-sample annual growth | 24 | 0.795 | 0.751 |
| Pre-pandemic annual growth | 19 | 0.559 | 0.567 |

The log-log slope is 0.536. A 10% higher arrivals level is associated with approximately 5.2% higher real GDP per capita over the period.

Pandemic and recovery comparisons:

- Arrivals fell by 84.9% from 2019 to 2020; real GDP per capita fell by 55.3%.
- In 2024, arrivals reached 86.1% of their 2019 level.
- In 2024, real GDP per capita reached 83.7% of its 2019 level.
- The recovery gap is 2.4 percentage points.

These estimates are descriptive. They do not identify a causal tourism effect.

## Repository structure

```text
cisc7204-Class_F-Team_03-FinalProjectArchive/
├── README.md
├── CODEBOOK.md
├── requirements.txt
├── SUBMISSION_CHECKLIST.md
├── UPLOAD_TO_GITHUB.md
├── data/
│   ├── macao_tourism_gdp_clean.csv
│   ├── DATA_SOURCES.md
│   └── source_extracts/
├── notebooks/
│   └── CISC7204_Team03_Macao_Tourism_GDP_Analysis.ipynb
├── code/
│   └── analysis.py
├── results/
│   ├── correlation_results.json
│   ├── summary_stats.json
│   └── analysis_summary.csv
├── visuals/
│   ├── fig1_index_and_scatter.png
│   ├── fig2_yoy_growth.png
│   ├── fig3_recovery_2024_vs_2019.png
│   ├── fig4_correlation_comparison.png
│   └── original project figure copies
├── project_docs/
│   ├── proposal/
│   ├── work_plan/
│   ├── meeting_minutes/
│   ├── team_roles/
│   └── feasibility/
└── presentation/
    ├── cisc7204-Class_F-Team_03-FinalPPT.pptx
    ├── cisc7204-Class_F-Team_03-MC663385-FinalStory.mp4
    ├── Wang_Di_Personal_Storytelling_Video_Script.pdf
    └── Q&A_for_Presentation_Macao_Tourism_Recovery.pdf
```

## Installation and test-run guide

### Requirements

- Python 3.10 or later
- `pip`
- Jupyter Notebook or JupyterLab

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
jupyter notebook notebooks/CISC7204_Team03_Macao_Tourism_GDP_Analysis.ipynb
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
jupyter notebook notebooks/CISC7204_Team03_Macao_Tourism_GDP_Analysis.ipynb
```

### One-command reproducibility check

From the project root:

```powershell
jupyter nbconvert --to notebook --execute notebooks/CISC7204_Team03_Macao_Tourism_GDP_Analysis.ipynb --output CISC7204_Team03_Macao_Tourism_GDP_Analysis_executed.ipynb --ExecutePreprocessor.timeout=120
```

Alternatively, run the standalone analysis script:

```powershell
python code/analysis.py
```

The script regenerates the four analysis figures and the JSON/CSV result files.

## Notebook contents

The executed notebook includes:

1. Data loading and validation.
2. Definition of the 2000-2024 analysis window.
3. Indexed level and growth calculations.
4. Pearson and Spearman correlation estimates with sample sizes.
5. Log-log regression.
6. Recovery comparisons against 2019.
7. Four story-telling visuals.
8. A markdown review of each visual using the five Alberto Cairo questions:
   - How does the visual follow effective visual-design guidelines?
   - Is it truthful?
   - Is it functional?
   - Is it beautiful?
   - Is it insightful?

## Team roles and contributions

| Member | Student ID | Main roles | Main contributions |
| --- | --- | --- | --- |
| WANG DI | MC663385 | Team Coordinator, Project Tracker, Quality Assurance Reviewer, Submission Manager | Meeting coordination, minutes, task tracking, quality assurance, reproducibility review, forum management, final submission coordination |
| QIU QIZU | MC663472 | Project Analyst, Quality Reviewer | Correlation analysis, sensitivity checks, notebook, interpretation safeguards |
| MA LEKAI | MC661324 | Project Analyst, Team Liaison | Source verification, definitions, research design, liaison |
| ZHAO WEI | MC663692 | Project Developer, Team Scribe | Data import and merge, data dictionary, repository and minutes |
| CHEN LIN | MC659981 | Project Developer, Quality Reviewer | Trend panels, indexed charts, scatter plots, visual checks |
| GUO MIAOYING | MC662701 | Team Reporter | Proposal integration, feasibility checks, chart development, presentation support |

## Presentation and video

The final presentation package is in `presentation/`. It includes the 22-slide PPTX, the final storytelling video, the personal narration script, and the Q&A preparation document.

The recording order is:

1. Slides 1-20
2. Demo video
3. Slide 21 - Reflection
4. Slide 22 - Q&A

## Citation

Suggested citation:

> Wang Di, Qiu Qizu, Ma Lekai, Zhao Wei, Chen Lin, and Guo Miaoying. (2026). *Macao Tourism Recovery and Economic Performance, 2000-2024* [Final project archive]. CISC7204 Data Science and Data Visualization, University of Macau.

## Limitations

- The annual sample contains only 25 observations, with 20 pre-pandemic levels and 19 pre-pandemic growth observations.
- The series share long-run trends and common shocks.
- Tourist arrivals do not capture visitor spending, gaming revenue, investment, or other economic drivers.
- The recovery period has only two annual observations, so no separate recovery-period correlation is reported.
- No causal effect is identified.

## Data source trail

- UN Tourism via Our World in Data: https://ourworldindata.org/grapher/international-tourist-trips
- World Bank indicator page: https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD?locations=MO
- World Bank API: https://api.worldbank.org/v2/country/MAC/indicator/NY.GDP.PCAP.PP.KD?format=json&per_page=100

