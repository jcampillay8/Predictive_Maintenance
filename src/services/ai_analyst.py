import google.generativeai as genai
from src.core.config import settings

class AIAnalyst:
    def __init__(self):
        # Configuramos Gemini con la key de settings
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def ask_llm(self, data_context: str, question: str) -> str:
        prompt = f"""
        ROL: Eres el Consultor Senior de Confiabilidad para Komatsu Chile.
        CONTEXTO: Analizando el Data Mart de KPIs de la flota.
        
        DATOS (JSON):
        {data_context}
        
        TAREA: Responder la pregunta del usuario utilizando un enfoque de ingeniería de mantenimiento (RCM).
        
        REGLAS DE RESPUESTA:
        1. Si ves un MTBF (Mean Time Between Failures) bajo, relaciónalo con la confiabilidad del activo.
        2. Si ves un MTTR (Mean Time To Repair) alto, relaciónalo con ineficiencia en el proceso de reparación o falta de repuestos.
        3. Identifica la máquina con mayor 'total_failures' y propón una acción.
        4. Usa un tono ejecutivo, técnico y breve.

        PREGUNTA: {question}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error en el análisis de IA: {str(e)}"