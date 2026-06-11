import os
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    def __init__(self):
        self.model = os.getenv("LLM_MODEL_NAME", "gpt-5")
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self._client = None

        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY no configurada. "
                "Copia .env.template a .env y agrega tu API key de OpenAI."
            )

        try:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise RuntimeError(
                "openai no está instalado. Ejecuta: pip install openai"
            )

    def chat(
        self, system: str, user: str, max_tokens: int = 600, temperature: float = 0.3
    ) -> str:
        try:
            resp = self._client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"Error en llamada a LLM: {e}")


llm = LLMClient()
