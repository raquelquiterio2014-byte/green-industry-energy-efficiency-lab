import json
from pathlib import Path
import pytest
from pydantic import ValidationError
from core import Factory, compare, intensity, sha256
from storage import save_review, get_reviews
from ai_gateway import Interpretation, generate_interpretation

DATA=json.loads((Path(__file__).resolve().parents[1]/'data/factories.json').read_text())
def factory(i): return Factory.model_validate(DATA[i])
def test_three_factories(): assert len(DATA)==3
def test_baseline_intensity(): assert intensity(factory(0))==50
def test_efficient_intensity(): assert intensity(factory(1))==40
def test_optimized_intensity(): assert intensity(factory(2))==32
def test_baseline_difference(): assert compare(factory(0),factory(0))['energy_difference_pct']==0
def test_efficient_difference(): assert compare(factory(1),factory(0))['energy_difference_pct']==20
def test_optimized_difference(): assert compare(factory(2),factory(0))['energy_difference_pct']==36
def test_absolute_difference(): assert compare(factory(2),factory(0))['energy_difference_kwh']==18000
def test_reversed_comparison(): assert compare(factory(0),factory(1))['energy_difference_kwh']==-10000
def test_reject_unequal_output():
    with pytest.raises(ValueError): compare(Factory(id='x',name='x',units_produced=2000,energy_kwh=100),factory(0))
def test_reject_zero_production():
    with pytest.raises(ValidationError): Factory(id='x',name='x',units_produced=0,energy_kwh=100)
def test_reject_negative_energy():
    with pytest.raises(ValidationError): Factory(id='x',name='x',units_produced=1,energy_kwh=-1)
def test_zero_baseline_percentage_missing():
    z=Factory(id='z',name='z',units_produced=1000,energy_kwh=0)
    assert compare(factory(1),z)['energy_difference_pct'] is None
def test_hash_stable(): assert sha256({'a':1,'b':2})==sha256({'b':2,'a':1})
def test_review_roundtrip(tmp_path):
    path=tmp_path/'test.sqlite3'
    save_review(path,'Reviewer','approved','Checked arithmetic',DATA,{'summary':'ok'})
    assert len(get_reviews(path))==1
    assert get_reviews(path)[0]['decision']=='approved'
def test_invalid_review_decision(tmp_path):
    with pytest.raises(ValueError): save_review(tmp_path/'db','Reviewer','unknown','Reason provided',DATA,{})
def test_missing_review_rationale(tmp_path):
    with pytest.raises(ValueError): save_review(tmp_path/'db','Reviewer','approved','x',DATA,{})
def test_ai_schema():
    item=Interpretation(summary='Synthetic comparisons only.',observations=[],limitations=[],checks_for_reviewer=[])
    assert item.summary.startswith('Synthetic')
def test_missing_api_key():
    with pytest.raises(ValueError): generate_interpretation([], '')
def test_all_synthetic(): assert all(x['source_type']=='synthetic' for x in DATA)
