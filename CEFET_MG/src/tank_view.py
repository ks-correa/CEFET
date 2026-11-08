import streamlit as st
from .data_processing import ROOT

_renderer=st.components.v2.component('cefet_tanks',
    html=(ROOT/'assets/tanks.html').read_text(encoding='utf-8'),
    css=(ROOT/'assets/tanks.css').read_text(encoding='utf-8'),
    js=(ROOT/'assets/tanks.js').read_text(encoding='utf-8'))

def tank_view(trajectory,title,key='tank_scene'):
    columns=['t','h1','h2','u_applied','qin','q12','qout']
    rows=trajectory[columns].astype(object).where(trajectory[columns].notna(),None).to_dict('records')
    return _renderer(data=dict(title=title,rows=rows),key=key,width='stretch',height='content')
