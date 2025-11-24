import streamlit as st

def init_state():
    if 'logs_ex' not in st.session_state:
        st.session_state['logs_ex'] = []
    if 'logs_nn' not in st.session_state:
        st.session_state['logs_nn'] = []
    if 'resultado_ex' not in st.session_state:
        st.session_state['resultado_ex'] = None   # (ruta, dist, tiempo, historial)
    if 'resultado_nn' not in st.session_state:
        st.session_state['resultado_nn'] = None   # (ruta, dist, tiempo, historial)

def append_log_ex(msg):
    st.session_state['logs_ex'].append(str(msg))

def clear_logs_ex():
    st.session_state['logs_ex'] = []

def append_log_nn(msg):
    st.session_state['logs_nn'].append(str(msg))

def clear_logs_nn():
    st.session_state['logs_nn'] = []

def get_logs_ex():
    return st.session_state.get('logs_ex', [])

def get_logs_nn():
    return st.session_state.get('logs_nn', [])

def set_resultado_ex(ruta, dist, tiempo, historial):
    st.session_state['resultado_ex'] = (ruta, dist, tiempo, historial)

def get_resultado_ex():
    return st.session_state.get('resultado_ex')

def set_resultado_nn(ruta, dist, tiempo, historial):
    st.session_state['resultado_nn'] = (ruta, dist, tiempo, historial)

def get_resultado_nn():
    return st.session_state.get('resultado_nn')