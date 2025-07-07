import streamlit as st
import requests
import json
import time
from fpdf import FPDF
import tempfile

# Configuración de la página sin el parámetro theme (compatible con versiones anteriores)
st.set_page_config(
    page_title="Asistente Tampa Clean",
    page_icon="🧽",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items=None
)

# Establecer tema claro mediante CSS personalizado
st.markdown("""
<style>
    /* Tema claro personalizado para Tampa Clean */
    body {
        color: #262626;
        background-color: #ffffff;
    }
    .stApp {
        background-color: #ffffff;
    }
    .stTextInput>div>div>input {
        background-color: #f8f9fa;
        color: #262626;
        border: 1px solid #dee2e6;
    }
    .stSlider>div>div>div {
        color: #262626;
    }
    .stSelectbox>div>div>div {
        background-color: #f8f9fa;
        color: #262626;
    }
    .css-1d391kg, .css-12oz5g7 {
        background-color: #f8f9fa;
    }
    
    /* Estilos personalizados para Tampa Clean - Tema claro */
    .main-header {
        font-size: 2.5rem;
        color: #004085;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0, 64, 133, 0.1);
        border-bottom: 3px solid #007bff;
        padding-bottom: 1rem;
    }
    .subheader {
        font-size: 1.5rem;
        color: #004085;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f8f9fa;
        text-align: center;
        padding: 10px;
        font-size: 0.8rem;
        border-top: 1px solid #dee2e6;
        color: #6c757d;
    }
    /* Estilos para la barra lateral */
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .sidebar .sidebar-content h1, 
    .sidebar .sidebar-content h2, 
    .sidebar .sidebar-content h3,
    .css-1outpf7 {
        color: #004085 !important;
    }
    
    /* Estilos para los ejemplos de preguntas */
    .example-questions {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin-bottom: 2rem;
    }
    
    /* Estilos para botones */
    .stButton > button {
        background-color: transparent;
        color: #007bff;
        border-radius: 5px;
        border: 2px solid #007bff;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: rgba(0, 123, 255, 0.1);
        color: #0056b3;
        border-color: #0056b3;
    }
    
    /* Contenedor de mensajes de chat */
    .stChatMessage {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Función para inicializar variables de sesión
def initialize_session_vars():
    if "is_configured" not in st.session_state:
        st.session_state.is_configured = False
    if "agent_endpoint" not in st.session_state:
        # Endpoint fijo para Tampa Clean
        st.session_state.agent_endpoint = "https://e2bveggk4tn4y4gxty7a6ere.agents.do-ai.run"
    if "agent_access_key" not in st.session_state:
        st.session_state.agent_access_key = ""
    if "messages" not in st.session_state:
        st.session_state.messages = []

# Inicializar variables
initialize_session_vars()

# Título y descripción de la aplicación
st.markdown("<h1 class='main-header'>🧽 Asistente Virtual Tampa Clean</h1>", unsafe_allow_html=True)

# Pantalla de configuración inicial si aún no se ha configurado
if not st.session_state.is_configured:
    st.markdown("<h2 class='subheader'>🔐 Acceso al Asistente Tampa Clean</h2>", unsafe_allow_html=True)
    
    st.info("💡 **Tampa Clean** - Bienvenido al asistente virtual. Por favor ingresa tu clave de acceso para comenzar.")
    
    # Solo solicitar clave de acceso, el endpoint ya está fijo
    agent_access_key = st.text_input(
        "🔑 Clave de Acceso", 
        type="password",
        placeholder="Ingresa tu clave de acceso",
        help="Tu clave de acceso para autenticar las solicitudes al asistente Tampa Clean"
    )
    
    if st.button("🚀 Iniciar Asistente Tampa Clean"):
        if not agent_access_key:
            st.error("⚠️ Por favor, ingresa la clave de acceso")
        else:
            # Guardar configuración en session_state (el endpoint ya está preconfigurado)
            st.session_state.agent_access_key = agent_access_key
            st.session_state.is_configured = True
            st.success("✅ ¡Acceso autorizado! Iniciando asistente Tampa Clean...")
            time.sleep(1)
            st.rerun()
    
    # Parar ejecución hasta que se configure
    st.stop()

# Una vez configurado, mostrar la interfaz normal
st.markdown("<p class='subheader'>💬 Chatea con tu asistente virtual de Tampa Clean</p>", unsafe_allow_html=True)

# Agregar ejemplos de preguntas específicos para Tampa Clean en dos columnas
st.markdown("""
<div class="example-questions">
    <p style="font-size: 1.1rem; color: #004085; margin-bottom: 1.5rem; font-weight: 600; font-family: 'Segoe UI', Arial, sans-serif; text-align: center;">
        💡 Ejemplos de preguntas que puedes hacer:
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background-color: rgba(0, 123, 255, 0.08); padding: 1rem; border-radius: 8px; border-left: 3px solid #007bff; margin-bottom: 1rem;">
        <div style="margin-bottom: 0.8rem; padding: 0.5rem; background-color: rgba(0, 123, 255, 0.05); border-radius: 4px;">
            <span style="font-weight: 500; color: #004085;">🏠 ¿Qué servicios de limpieza residencial ofrecen?</span>
        </div>
        <div style="margin-bottom: 0.8rem; padding: 0.5rem; background-color: rgba(0, 123, 255, 0.05); border-radius: 4px;">
            <span style="font-weight: 500; color: #004085;">🏢 ¿Cómo funciona la limpieza comercial de oficinas?</span>
        </div>
        <div style="margin-bottom: 0.8rem; padding: 0.5rem; background-color: rgba(0, 123, 255, 0.05); border-radius: 4px;">
            <span style="font-weight: 500; color: #004085;">👔 ¿Cuáles son las políticas para empleados nuevos?</span>
        </div>
        <div style="margin-bottom: 0.8rem; padding: 0.5rem; background-color: rgba(0, 123, 255, 0.05); border-radius: 4px;">
            <span style="font-weight: 500; color: #004085;">🧽 ¿Qué productos de limpieza debo usar para baños?</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background-color: rgba(0, 123, 255, 0.08); padding: 1rem; border-radius: 8px; border-left: 3px solid #007bff; margin-bottom: 1rem;">
        <div style="margin-bottom: 0.8rem; padding: 0.5rem; background-color: rgba(0, 123, 255, 0.05); border-radius: 4px;">
            <span style="font-weight: 500; color: #004085;">💰 ¿Cómo funcionan los pagos y cuándo se realizan?</span>
        </div>
        <div style="margin-bottom: 0.8rem; padding: 0.5rem; background-color: rgba(0, 123, 255, 0.05); border-radius: 4px;">
            <span style="font-weight: 500; color: #004085;">📞 ¿Cuáles son los números de contacto de emergencia?</span>
        </div>
        <div style="margin-bottom: 0.8rem; padding: 0.5rem; background-color: rgba(0, 123, 255, 0.05); border-radius: 4px;">
            <span style="font-weight: 500; color: #004085;">🕐 ¿Cómo solicito permisos y días libres?</span>
        </div>
        <div style="margin-bottom: 0.8rem; padding: 0.5rem; background-color: rgba(0, 123, 255, 0.05); border-radius: 4px;">
            <span style="font-weight: 500; color: #004085;">🚨 ¿Qué hacer en caso de emergencias durante el servicio?</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar para configuración
st.sidebar.title("⚙️ Configuración Tampa Clean")

# Mostrar información de conexión actual
st.sidebar.success("✅ Asistente configurado")
with st.sidebar.expander("📋 Ver configuración actual"):
    st.code(f"Endpoint: {st.session_state.agent_endpoint}\nClave de acceso: {'*'*len(st.session_state.agent_access_key) if st.session_state.agent_access_key else 'No configurada'}")
    st.info("🔒 El endpoint está preconfigurado para mayor seguridad")

# Información de Tampa Clean
with st.sidebar.expander("ℹ️ Información de Tampa Clean"):
    st.markdown("""
    **Tampa Clean**
    - 🏆 +20 años de experiencia
    - 🏠 Limpieza residencial
    - 🏢 Limpieza comercial
    - 📍 Tampa, FL y alrededores
    - 📞 (813) 998-4553
    - 💬 WhatsApp: (813) 365-9970
    """)

# Ajustes avanzados
with st.sidebar.expander("🔧 Ajustes avanzados"):
    temperature = st.slider("🌡️ Temperatura", min_value=0.0, max_value=1.0, value=0.2, step=0.1,
                          help="Valores más altos generan respuestas más creativas, valores más bajos generan respuestas más deterministas.")
    
    max_tokens = st.slider("📏 Longitud máxima", min_value=100, max_value=2000, value=1000, step=100,
                          help="Número máximo de tokens en la respuesta.")

# Sección para probar conexión con el agente
with st.sidebar.expander("🔍 Probar conexión"):
    if st.button("🌐 Verificar endpoint"):
        with st.spinner("Verificando conexión..."):
            try:
                agent_endpoint = st.session_state.agent_endpoint
                agent_access_key = st.session_state.agent_access_key
                
                if not agent_endpoint or not agent_access_key:
                    st.error("❌ Falta configuración del endpoint o clave de acceso")
                else:
                    # Asegurarse de que el endpoint termine correctamente
                    if not agent_endpoint.endswith("/"):
                        agent_endpoint += "/"
                    
                    # Verificar si la documentación está disponible
                    docs_url = f"{agent_endpoint}docs"
                    
                    # Preparar headers
                    headers = {
                        "Authorization": f"Bearer {agent_access_key}",
                        "Content-Type": "application/json"
                    }
                    
                    try:
                        # Intentar verificar documentación
                        response = requests.get(docs_url, timeout=10)
                        
                        if response.status_code < 400:
                            st.success(f"✅ Documentación accesible: {docs_url}")
                        
                        # Intentar solicitud de prueba
                        completions_url = f"{agent_endpoint}api/v1/chat/completions"
                        test_payload = {
                            "model": "n/a",
                            "messages": [{"role": "user", "content": "Hello Tampa Clean"}],
                            "max_tokens": 5,
                            "stream": False
                        }
                        
                        response = requests.post(completions_url, headers=headers, json=test_payload, timeout=10)
                        
                        if response.status_code < 400:
                            st.success(f"✅ ¡Conexión exitosa con Tampa Clean!")
                            with st.expander("📄 Ver detalles de la respuesta"):
                                try:
                                    st.json(response.json())
                                except:
                                    st.code(response.text)
                            st.info("🔍 El asistente de Tampa Clean está listo para atender consultas.")
                        else:
                            st.error(f"❌ Error al conectar. Código: {response.status_code}")
                            with st.expander("📄 Ver detalles del error"):
                                st.code(response.text)
                    except Exception as e:
                        st.error(f"❌ Error de conexión: {str(e)}")
            except Exception as e:
                st.error(f"❌ Error al verificar endpoint: {str(e)}")

# Opciones de gestión de conversación
st.sidebar.markdown("### 💬 Gestión de conversación")

# Botón para limpiar conversación
if st.sidebar.button("🗑️ Limpiar conversación"):
    st.session_state.messages = []
    st.rerun()

# Botón para guardar conversación en PDF
if st.sidebar.button("💾 Guardar conversación en PDF"):
    if len(st.session_state.messages) == 0:
        st.sidebar.warning("⚠️ No hay conversación para guardar")
    else:
        # Crear PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Añadir título con estilo Tampa Clean
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "Conversacion con Asistente Tampa Clean", ln=True, align='C')
        pdf.ln(10)
        
        # Añadir información de la empresa
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(200, 5, "Tampa Clean - Servicios de Limpieza Profesional", ln=True, align='C')
        pdf.cell(200, 5, "Telefono: (813) 998-4553 | WhatsApp: (813) 365-9970", ln=True, align='C')
        pdf.ln(5)
        
        # Añadir fecha
        from datetime import datetime
        pdf.cell(200, 10, f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True)
        pdf.ln(10)
        
        # Recuperar mensajes
        pdf.set_font("Arial", size=12)
        for i, msg in enumerate(st.session_state.messages, 1):
            if msg["role"] == "user":
                pdf.set_text_color(0, 100, 0)  # Verde para usuario
                pdf.cell(200, 10, f"Usuario (#{i}):", ln=True)
            else:
                pdf.set_text_color(0, 0, 150)  # Azul para asistente
                pdf.cell(200, 10, f"Asistente Tampa Clean (#{i}):", ln=True)
            
            pdf.set_text_color(0, 0, 0)  # Negro para el contenido
            
            # Partir el texto en múltiples líneas si es necesario
            text = msg["content"]
            pdf.multi_cell(190, 8, text.encode('latin-1', 'replace').decode('latin-1'))
            pdf.ln(5)
        
        # Guardar el PDF en un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf_path = tmp_file.name
            pdf.output(pdf_path)
        
        # Abrir y leer el archivo para la descarga
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
        
        # Botón de descarga
        st.sidebar.download_button(
            label="📥 Descargar PDF",
            data=pdf_data,
            file_name=f"conversacion_tampa_clean_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
        )

# Botón para cerrar sesión
if st.sidebar.button("🚪 Cerrar sesión"):
    st.session_state.is_configured = False
    st.session_state.agent_access_key = ""
    # El endpoint permanece fijo, no se limpia
    st.rerun()

# Función para enviar consulta al agente
def query_agent(prompt, history=None):
    try:
        # Obtener configuración del agente
        agent_endpoint = st.session_state.agent_endpoint
        agent_access_key = st.session_state.agent_access_key
        
        if not agent_endpoint or not agent_access_key:
            return {"error": "Las credenciales de API no están configuradas correctamente."}
        
        # Asegurarse de que el endpoint termine correctamente
        if not agent_endpoint.endswith("/"):
            agent_endpoint += "/"
        
        # Construir URL para chat completions
        completions_url = f"{agent_endpoint}api/v1/chat/completions"
        
        # Preparar headers con autenticación
        headers = {
            "Authorization": f"Bearer {agent_access_key}",
            "Content-Type": "application/json"
        }
        
        # Preparar los mensajes en formato OpenAI
        messages = []
        if history:
            messages.extend([{"role": msg["role"], "content": msg["content"]} for msg in history])
        messages.append({"role": "user", "content": prompt})
        
        # Construir el payload
        payload = {
            "model": "n/a",  # El modelo no es relevante para el agente
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        # Enviar solicitud POST
        try:
            response = requests.post(completions_url, headers=headers, json=payload, timeout=60)
            
            # Verificar respuesta
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    
                    # Procesar la respuesta en formato OpenAI
                    if "choices" in response_data and len(response_data["choices"]) > 0:
                        choice = response_data["choices"][0]
                        if "message" in choice and "content" in choice["message"]:
                            result = {
                                "response": choice["message"]["content"]
                            }
                            return result
                    
                    # Si no se encuentra la estructura esperada
                    return {"error": "Formato de respuesta inesperado", "details": str(response_data)}
                except ValueError:
                    # Si no es JSON, devolver el texto plano
                    return {"response": response.text}
            else:
                # Error en la respuesta
                error_message = f"Error en la solicitud. Código: {response.status_code}"
                try:
                    error_details = response.json()
                    return {"error": error_message, "details": str(error_details)}
                except:
                    return {"error": error_message, "details": response.text}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Error en la solicitud HTTP: {str(e)}"}
        
    except Exception as e:
        return {"error": f"Error al comunicarse con el asistente: {str(e)}"}

# Mostrar historial de conversación
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada para el mensaje
prompt = st.chat_input("💬 Pregúntame sobre Tampa Clean - servicios, políticas, procedimientos...")

# Procesar la entrada del usuario
if prompt:
    # Añadir mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Mostrar mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Preparar historial para la API
    api_history = st.session_state.messages[:-1]  # Excluir el mensaje actual
    
    # Mostrar indicador de carga mientras se procesa
    with st.chat_message("assistant"):
        with st.spinner("🔍 Consultando base de conocimiento de Tampa Clean..."):
            # Enviar consulta al agente
            response = query_agent(prompt, api_history)
            
            if "error" in response:
                st.error(f"❌ Error: {response['error']}")
                if "details" in response:
                    with st.expander("📋 Detalles del error"):
                        st.code(response["details"])
                
                # Añadir mensaje de error al historial
                error_msg = f"Lo siento, ocurrió un error al procesar tu consulta sobre Tampa Clean: {response['error']}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            else:
                # Mostrar respuesta del asistente
                response_text = response.get("response", "No se recibió respuesta del asistente de Tampa Clean.")
                st.markdown(response_text)
                
                # Añadir respuesta al historial
                st.session_state.messages.append({"role": "assistant", "content": response_text})

# Pie de página
st.markdown("""
<div class='footer'>
    🧽 Asistente Tampa Clean © 2025 | 📞 (813) 998-4553 | 💬 WhatsApp: (813) 365-9970 | 📧 manager@tampacleaning.org
</div>
""", unsafe_allow_html=True)
