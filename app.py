import streamlit as st
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# --- 1. ESTILO: AMISTOSO, NO EMPALAGOSO ---
st.set_page_config(page_title="Publisher - Camino a Casa", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    
    /* Texto principal en gris muy oscuro para lectura perfecta */
    h1, h2, h3, p, label { color: #2C3E50 !important; }
    
    /* 1. Sidebar: Texto BLANCO para la configuración de la izquierda */
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #FFFFFF !important;
    }

    /* 2. Vista previa: Tipografía en NEGRO absoluto para que se lea siempre */
    .tinder-card, 
    .tinder-card h2, 
    .tinder-card p, 
    .tinder-card span,
    .tinder-card b {
        color: #000000 !important;
    }

    /* Card de Preview estilo Tinder */
    .tinder-card {
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #EEEEEE;
        background-color: #F9F9F9;
        margin-bottom: 20px;
    }
    
    .tag {
        background: #E0E0E0;
        padding: 4px 10px;
        border-radius: 10px;
        font-size: 13px;
        font-weight: bold;
        margin-right: 5px;
        color: #000000 !important; /* Texto negro en los tags también */
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. CONFIGURACIÓN (SIDEBAR) ---
with st.sidebar:
    st.markdown("### Configuración")
    api_key = st.secrets.get("GOOGLE_API_KEY") or st.text_input("Google API Key:", type="password")

# --- 3. LÓGICA DE AUDITORÍA ---
def auditar_perfil(texto):
    if not api_key: return "APPROVED"
    try:
        os.environ["GOOGLE_API_KEY"] = api_key
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Responde REJECTED si hay indicios de venta o precio. De lo contrario APPROVED."),
            ("human", texto)
        ])
        return "REJECTED" if "REJECTED" in (prompt | llm).invoke({"texto": texto}).content.upper() else "APPROVED"
    except: return "APPROVED"

# --- 4. INTERFAZ DE CARGA ---
st.title("Preparemos su perfil para encontrarle una familia")

with st.form("perfil_form"):
    st.subheader("🔹 Datos del Rescatado")
    c1, c2 = st.columns(2)
    nombre = c1.text_input("Nombre")
    etapa = c2.selectbox("Etapa", ["Cachorro", "Joven", "Adulto", "Senior"])
    tamanio = c1.selectbox("Tamaño", ["Chico", "Mediano", "Grande"])
    energia = c2.select_slider("Nivel de energía", options=["Bajo", "Medio", "Alto"])
    
    st.write("**Compatibilidad**")
    f1, f2, f3 = st.columns(3)
    ninos = f1.checkbox("Apto niños")
    perros = f2.checkbox("Apto perros")
    gatos = f3.checkbox("Apto gatos")

    st.divider()
    st.subheader("🔹 Requisitos del hogar ideal")
    h1, h2 = st.columns(2)
    tipo_hogar = h1.selectbox("Tipo de hogar", ["Departamento", "Casa", "No importa"])
    patio = h2.selectbox("Patio/Terraza", ["Sí", "No", "Deseable"])
    tiempo_solo = h1.selectbox("Tiempo solo", ["Tolera", "No tolera"])
    experiencia = h2.selectbox("Experiencia del adoptante", ["Primera vez", "Con experiencia"])
    
    st.divider()
    historia = st.text_area("Historia corta (necesidades y carácter)", height=100)
    
    # --- CÁLCULO DE SCORE ---
    campos = [nombre, historia]
    score = 60 + (len([c for c in campos if c]) * 20)
    faltantes = []
    if not nombre: faltantes.append("Nombre")
    if not historia: faltantes.append("Historia")
    
    st.write(f"**Completitud del perfil: {min(score, 100)}%**")
    if faltantes: st.caption(f"Falta: {', '.join(faltantes)}")
    
    submit = st.form_submit_button("FINALIZAR PERFIL")

# --- 5. RESULTADO Y PREVIEW ---
if submit:
    if not nombre or not historia:
        st.error("Por favor, completa los campos obligatorios.")
    else:
        status = auditar_perfil(historia)
        if status == "REJECTED":
            st.warning("El perfil no cumple con las normas de adopción responsable (posible venta).")
        else:
            st.success("Perfil procesado correctamente.")
            
            # PREVIEW ESTILO TINDER
            st.markdown("### 🔹 Vista previa del perfil")
            st.markdown(f"""
                <div class="tinder-card">
                    <h2 style='margin:0;'>{nombre}</h2>
                    <p><b>{etapa} • {tamanio}</b></p>
                    <div style='margin: 10px 0;'>
                        <span class="tag">{'👶 Niños' if ninos else 'No niños'}</span>
                        <span class="tag">{'🐕 Perros' if perros else 'No perros'}</span>
                        <span class="tag">⚡ Energía {energia}</span>
                    </div>
                    <p>{historia}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # JSON TÉCNICO (Oculto en expander)
            with st.expander("Ver JSON técnico"):
                perfil_data = {
                    "perro": {"nombre": nombre, "etapa": etapa, "tamanio": tamanio, "energia": energia},
                    "match_rules": {"ninos": ninos, "perros": perros, "gatos": gatos},
                    "hogar_ideal": {"tipo": tipo_hogar, "patio": patio, "tiempo_solo": tiempo_solo, "experiencia": experiencia},
                    "bio": historia
                }
                st.json(perfil_data)
