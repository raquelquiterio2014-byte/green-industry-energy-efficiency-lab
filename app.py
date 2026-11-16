"""Green Industry & Energy Efficiency Lab V1.0 — COP31 Day 8."""
import json
import os
from pathlib import Path
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from core import Factory, compare, sha256
from ai_gateway import generate_interpretation
from storage import get_reviews, save_review

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / '.env')
FACTORIES = [Factory.model_validate(x) for x in json.loads((ROOT/'data/factories.json').read_text(encoding='utf-8'))]
BASELINE = FACTORIES[0]
ROWS = [compare(f, BASELINE) for f in FACTORIES]
DB = ROOT / 'local_data' / 'reviews.sqlite3'

st.set_page_config(page_title='Green Industry & Energy Efficiency Lab', page_icon='🏭', layout='wide')
st.markdown('''<style>.stApp{background:#081b30;color:#eaf6ff}
[data-testid="stMetric"]{background:#123653;padding:15px;border-radius:12px}</style>''', unsafe_allow_html=True)
st.title('🏭 Green Industry & Energy Efficiency Lab V1.0')
st.caption('COP31 AI Solutions Lab | Day 8 | November 16, 2026')
st.warning('All three factories are SYNTHETIC educational examples, not measured industrial facilities.')
t1,t2,t3,t4 = st.tabs(['📊 Industrial Overview','⚡ Energy Efficiency Analysis','🤖 AI & Human Review','📤 Export & Methodology'])
with t1:
    st.subheader('Factory comparison')
    c1,c2,c3 = st.columns(3)
    c1.metric('Synthetic factories',len(FACTORIES))
    c2.metric('Monthly production per factory','1,000 units')
    c3.metric('Baseline energy','50,000 kWh')
    st.dataframe(pd.DataFrame(ROWS),hide_index=True,use_container_width=True)
    st.bar_chart(pd.DataFrame(ROWS).set_index('factory')['energy_kwh'])
with t2:
    st.subheader('Energy intensity and hypothetical differences')
    st.dataframe(pd.DataFrame(ROWS)[['factory','kwh_per_unit','energy_difference_kwh','energy_difference_pct']],hide_index=True,use_container_width=True)
    st.bar_chart(pd.DataFrame(ROWS).set_index('factory')['kwh_per_unit'])
    st.info('Example: 50,000 → 40,000 kWh represents a 20% lower energy use for the same 1,000-unit output. This is not a measured saving.')
    st.markdown('**Formulas:** energy intensity = kWh / units produced; difference (%) = (baseline kWh − scenario kWh) / baseline kWh × 100.')
with t3:
    st.subheader('Optional AI explanation and required human review')
    st.caption('Clicking Generate sends the synthetic comparison table to the Google Gemini API. No API key is required for the other tabs.')
    if 'interpretation' not in st.session_state: st.session_state.interpretation = None
    if st.button('Generate AI explanation'):
        try:
            with st.spinner('Requesting structured interpretation...'):
                result=generate_interpretation(ROWS,os.getenv('GEMINI_API_KEY','').strip(),os.getenv('GEMINI_MODEL','gemini-2.5-flash'))
            st.session_state.interpretation=result.model_dump()
        except Exception as exc:
            st.error(f'AI request unavailable: {exc}')
    if st.session_state.interpretation:
        st.json(st.session_state.interpretation)
        with st.form('review'):
            reviewer=st.text_input('Reviewer role or pseudonym',value='Educational reviewer')
            decision=st.selectbox('Decision',['needs_revision','approved','rejected'])
            rationale=st.text_area('Rationale',value='Verify all numerical comparisons and limitations.')
            if st.form_submit_button('Save human review'):
                try:
                    save_review(DB,reviewer,decision,rationale,ROWS,st.session_state.interpretation)
                    st.success('Human review recorded locally.')
                except ValueError as exc:
                    st.error(str(exc))
    st.caption('A structured response is not evidence of factual correctness. Human approval does not establish scientific validation.')
with t4:
    st.subheader('Data exports and methodology')
    st.download_button('Download indicators CSV',pd.DataFrame(ROWS).to_csv(index=False).encode('utf-8'),'energy_indicators.csv','text/csv')
    reviews=get_reviews(DB)
    st.download_button('Download review log CSV',pd.DataFrame(reviews,columns=['id','timestamp_utc','reviewer','decision','rationale','input_hash','response_hash']).to_csv(index=False).encode('utf-8'),'reviews.csv','text/csv')
    package={'source_type':'synthetic','factories':[f.model_dump() for f in FACTORIES],'indicators':ROWS,'reviews':reviews,'input_sha256':sha256([f.model_dump() for f in FACTORIES])}
    st.download_button('Download full JSON',json.dumps(package,indent=2),'green_industry_lab.json','application/json')
    st.markdown('**Limitations:** No actual factory measurements, emissions factors, cost estimates, equipment engineering, operational feasibility or verified savings. Equal production volumes are required for direct comparisons. SHA-256 helps identify content changes but does not make the local database tamper-proof.')
    st.markdown('**Methods:** Pydantic input validation → deterministic calculations → optional Gemini interpretation → human review → CSV/JSON export.')
