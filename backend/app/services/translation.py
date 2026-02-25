import logging

import httpx
from openai import AsyncOpenAI

from app.core.config import get_settings

logger = logging.getLogger(__name__)

async def translate_word(word: str) -> str | None:
    settings = get_settings()
    
    # 1. Try DeepL
    if settings.DEEPL_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=5.0) as http_client:
                # Check if it is a free API key (ends with ':fx')
                host = (
                    "api-free.deepl.com" 
                    if settings.DEEPL_API_KEY.endswith(":fx") 
                    else "api.deepl.com"
                )
                deepl_url = f"https://{host}/v2/translate"
                
                response = await http_client.post(
                    deepl_url,
                    headers={"Authorization": f"DeepL-Auth-Key {settings.DEEPL_API_KEY}"},
                    data={"text": [word], "target_lang": "RU"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("translations"):
                        return data["translations"][0]["text"]
                else:
                    logger.warning(
                        f"DeepL API returned status {response.status_code}: {response.text}"
                    )
        except Exception as e:
            logger.warning(f"DeepL API failed: {e}")
            # Fallback to OpenAI
    
    # 2. Try OpenAI
    if settings.OPENAI_API_KEY:
        try:
            client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional translator."},
                    {
                        "role": "user", 
                        "content": (
                            f'Translate the word "{word}" to Russian. '
                            "Return only the translation, no explanations."
                        )
                    }
                ],
                timeout=5.0,
            )
            if response.choices and response.choices[0].message.content:
                return response.choices[0].message.content.strip()
        except Exception as e:
            logger.warning(f"OpenAI API failed: {e}")

    # 3. Both failed or not configured
    logger.error("All translation services failed or are unconfigured.")
    return None
