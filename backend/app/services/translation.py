import logging

import httpx

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
            # Fallback to OpenRouter
    
    # 2. Try OpenRouter
    if settings.OPENROUTER_API_KEY:
        try:
            payload = {
                "model": settings.LLM_MODEL,
                "messages": [
                    {"role": "system", "content": "You are a professional translator."},
                    {
                        "role": "user", 
                        "content": (
                            f'Translate the word "{word}" to Russian. '
                            "Return only the translation, no explanations."
                        )
                    }
                ],
                "temperature": 0.1,
            }
            headers = {
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            }
            async with httpx.AsyncClient(timeout=5.0) as http_client:
                response = await http_client.post(
                    settings.OPENROUTER_URL,
                    json=payload,
                    headers=headers
                )
                if response.status_code == 200:
                    data = response.json()
                    choices = data.get("choices", [])
                    if choices and choices[0].get("message", {}).get("content"):
                        return choices[0]["message"]["content"].strip()
                else:
                    logger.warning(
                        f"OpenRouter API returned status {response.status_code}: {response.text}"
                    )
        except Exception as e:
            logger.warning(f"OpenRouter API failed: {e}")

    # 3. Both failed or not configured
    logger.error("All translation services failed or are unconfigured.")
    return None
