import google.generativeai as genai
from src.core.config import settings

class AIAnalyst:
    def __init__(self):
        # Configuramos Gemini con la key de settings
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def ask_llm(self, data_context: str, question: str) -> str:
        prompt = f"""
        ROL: Eres el Consultor Senior de Confiabilidad para una empersa importante en Chile.
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

    def ask_llm_operational(self, machine_id: str, telemetry_context: str, events_context: str, question: str) -> str:
        prompt = f"""
        ROL: Ingeniero de Confiabilidad de Terreno para una empresa importante en Chile.
        ACTIVO: Máquina ID {machine_id}
        
        CONTEXTO OPERACIONAL (Última Telemetría):
        {telemetry_context}
        
        HISTORIAL RECIENTE (Errores y Fallas):
        {events_context}
        
        TAREA: Analizar los signos vitales de la máquina y responder la consulta técnica.
        
        REGLAS:
        1. Analiza tendencias en Voltaje, Rotación, Presión y Vibración.
        2. Relaciona los errores recientes con los datos de telemetría.
        3. Si hay vibración alta, advierte sobre posible falla mecánica.
        4. Sé directo, técnico y enfocado en la disponibilidad del activo.

        PREGUNTA DEL OPERADOR: {question}
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error en el análisis operativo: {str(e)}"