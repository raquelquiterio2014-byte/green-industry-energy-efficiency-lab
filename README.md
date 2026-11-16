# Green Industry & Energy Efficiency Lab V1.0

**COP31 AI Solutions Lab — Day 8 | November 16, 2026**

An independent educational Python application for comparing industrial energy intensity across three **synthetic** factories with identical output. The software illustrates transparent arithmetic, optional AI-assisted interpretation, and human oversight.

## Four modules

1. **Industrial Overview:** compare production and energy use across three factories.
2. **Energy Efficiency Analysis:** calculate kWh/unit and percentage differences relative to a conventional baseline.
3. **AI & Human Review:** optional Gemini 2.5 Flash structured explanations, followed by a locally stored reviewer decision.
4. **Export & Methodology:** CSV/JSON exports, SHA-256 fingerprinting and limitations.

## Run on Windows / PyCharm

Python 3.11 or 3.12 recommended. No GPU required.

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
python -m streamlit run app.py
```

Optional AI: copy `.env.example` to `.env`, replace the placeholder with your own Gemini API key, then restart Streamlit. Never commit `.env`.

## Data and formulas

| Scenario | Production | Energy | Intensity | Difference from baseline |
| --- | ---: | ---: | ---: | ---: |
| Conventional | 1,000 units | 50,000 kWh | 50 kWh/unit | 0% |
| Efficient | 1,000 units | 40,000 kWh | 40 kWh/unit | 20% lower |
| Optimized | 1,000 units | 32,000 kWh | 32 kWh/unit | 36% lower |

- Energy intensity = energy (kWh) / units produced.
- Difference (%) = (baseline kWh − scenario kWh) / baseline kWh × 100.
- The percentage is undefined when baseline consumption is zero.
- Direct comparison rejects different production volumes.

All values are **invented for teaching** and are not sourced from COP31, a factory, or an external dataset. These differences do not demonstrate real energy savings or causation.

## Validation

Run `python -m pytest -q`. The repository includes 20 automated tests covering formulas, schema validation, missing baseline handling, audit logging, and the optional AI-key guard. A live Gemini request and Streamlit visual inspection require separate manual testing.

## Limitations

No real industrial data, emissions conversion, cost calculation, life-cycle assessment, or engineering feasibility assessment. The Gemini model may produce inaccurate interpretations; human review is required. SHA-256 is a content fingerprint, not an immutable audit trail. SQLite stores local reviews and should not be published.

**Evidence first. Engineering second. Measurable impact as the goal.**
