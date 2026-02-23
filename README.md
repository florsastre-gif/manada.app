🐾 Match Mascotas - Parte A: Publisher & Inventory
Esta aplicación es el Portal del Publisher. Su misión principal es transformar el conocimiento que las ONGs y rescatistas tienen de sus animales en un perfil estándar, técnico y matchable.

A diferencia de un formulario común, esta herramienta actúa como un filtro de calidad y un estructurador de datos para que la App B (Matcher) pueda operar con precisión.

🎯 El Corazón de la Idea
El éxito de un "Tinder de perros" no es solo subir fotos; es evitar el abandono mediante la compatibilidad. Esta Parte A se encarga de:

Estandarización: Convierte historias subjetivas en datos JSON rígidos.

Compliance con IA: Utiliza LangChain y Gemini 2.0 para auditar que no existan publicaciones de venta o precios, protegiendo la ética del espacio.

Definición de "Hogar Ideal": Obliga al cargador a definir no solo cómo es el perro, sino qué familia necesita (tipo de hogar, patio, experiencia).

🛠️ Componentes Técnicos
Frontend: Streamlit con CSS personalizado para una experiencia cálida, profesional y con alto contraste (texto negro sobre fondo claro).

Orquestador de IA: LangChain (LCEL) para auditoría de contenido en tiempo real.

Modelo: Gemini 2.0 Flash para validación de cumplimiento (Compliance).

Validación de Datos: Estructura compatible con Pydantic para asegurar que el JSON de salida sea siempre idéntico.

📊 Flujo de Trabajo
Carga Responsable: El rescatista completa la ficha técnica y los requisitos del hogar.

Auditoría Silenciosa: La IA analiza la descripción para descartar transacciones monetarias.

Preview de Card: Muestra una vista previa estilo "Tinder" para validar la estética antes de finalizar.

Generación de Inventario: Produce un objeto JSON técnico que alimenta directamente el algoritmo de la App B.

🚀 Requisitos de Instalación
Bash
pip install streamlit langchain-google-genai langchain-core
