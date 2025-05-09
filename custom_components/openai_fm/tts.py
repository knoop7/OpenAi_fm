"""OpenAI.fm TTS integration for Home Assistant."""
import logging
import aiohttp
from typing import List
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.tts import (PLATFORM_SCHEMA, Provider, TextToSpeechEntity, Voice)
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.config_entries import ConfigEntry
import os
import tempfile

from .const import (
    CONF_VOICE,
    CONF_PROMPT,
    DEFAULT_VOICE,
    DEFAULT_LANG,
    DEFAULT_PROMPT,
    STATE_READY,
    STATE_SPEAKING,
    STATE_ERROR,
    SUPPORTED_VOICES,
    SUPPORTED_LANGUAGES
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_VOICE, default=DEFAULT_VOICE): vol.In(list(SUPPORTED_VOICES.keys())),
    vol.Optional(CONF_PROMPT, default=DEFAULT_PROMPT): cv.string,
})

def clean_text_for_api(text):
    return text.replace("\xa0", " ")

async def async_get_engine(hass: HomeAssistant, config: ConfigType, discovery_info: DiscoveryInfoType = None) -> Provider:
    return OpenAIFmProvider(hass, config)

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities) -> None:
    
    voice = config_entry.options.get(CONF_VOICE, config_entry.data.get(CONF_VOICE, DEFAULT_VOICE))
    name = f"OpenAI.fm ({voice})"
    
    
    config = {**config_entry.data}
    if config_entry.options:
        config.update(config_entry.options)
        
    engine = OpenAIFmProvider(hass, config)
    entity = OpenAIFmTTS(engine, config_entry, name)
    async_add_entities([entity])
    
    
    config_entry.async_on_unload(
        config_entry.add_update_listener(update_listener)
    )

async def update_listener(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)

class OpenAIFmTTS(TextToSpeechEntity):
    def __init__(self, engine, config_entry, name):
        self.engine = engine
        self.config_entry = config_entry
        self._attr_name = name
        self._attr_unique_id = config_entry.entry_id
        self._attr_default_language = DEFAULT_LANG
        self._attr_supported_languages = SUPPORTED_LANGUAGES
        self._state = STATE_READY
        self._session = None  
        
    @property
    def state(self):
        return self._state
        
    @property
    def extra_state_attributes(self):
        voice = self.config_entry.options.get(CONF_VOICE, 
                self.config_entry.data.get(CONF_VOICE, DEFAULT_VOICE))
        return {
            "state_description": self._state,
            "voice": voice,
            "prompt": self.config_entry.options.get(CONF_PROMPT, 
                     self.config_entry.data.get(CONF_PROMPT, DEFAULT_PROMPT))
        }

    @property
    def supported_options(self):
        return self.engine.supported_options

    @callback
    def async_get_supported_voices(self, language: str) -> List[Voice] | None:
        voices = []
        for voice_id, voice_info in SUPPORTED_VOICES.items():
            voices.append(Voice(voice_id=voice_id, name=voice_info["name"]))
        return voices

    async def async_get_tts_audio(self, message, language, options=None):
        if options is None:
            options = {}
        
        voice = options.get(CONF_VOICE, self.config_entry.data.get(CONF_VOICE, DEFAULT_VOICE))
        prompt = options.get(CONF_PROMPT, self.config_entry.data.get(CONF_PROMPT, DEFAULT_PROMPT))
        
        message = clean_text_for_api(message)
        prompt = clean_text_for_api(prompt)
        
        if self._session is None:
            self._session = aiohttp.ClientSession()
            
        try:
            audio_data = await self.engine._generate_audio(message, voice, prompt)
            
            
            content_type = "mp3"
            if audio_data[:4] == b'RIFF' and audio_data[8:12] == b'WAVE':
                content_type = "wav"  
            
            
            
            processed_data = bytearray(audio_data)
            
            
            return content_type, bytes(processed_data)
        except Exception as err:
            _LOGGER.info("生成 OpenAI.fm TTS 时出错：%s", err)
            raise

class OpenAIFmProvider(Provider):
    def __init__(self, hass, config):
        self.name = "OpenAI.fm"
        self.hass = hass
        self._config = config
        self._session = None

    @property
    def default_language(self):
        return DEFAULT_LANG

    @property
    def supported_languages(self):
        return SUPPORTED_LANGUAGES

    @property
    def supported_options(self):
        return [CONF_VOICE, CONF_PROMPT]

    async def async_get_tts_audio(self, message, language, options=None):
        if options is None:
            options = {}
            
        voice = options.get(CONF_VOICE, self._config.get(CONF_VOICE, DEFAULT_VOICE))
        prompt = options.get(CONF_PROMPT, self._config.get(CONF_PROMPT, DEFAULT_PROMPT))
        
        message = clean_text_for_api(message)
        prompt = clean_text_for_api(prompt)
        
        if self._session is None:
            self._session = aiohttp.ClientSession()
            
        try:
            audio_data = await self._generate_audio(message, voice, prompt)
            
            
            content_type = "mp3"
            if audio_data[:4] == b'RIFF' and audio_data[8:12] == b'WAVE':
                content_type = "wav"  
            
            
            
            processed_data = bytearray(audio_data)
            
            
            return content_type, bytes(processed_data)
        except Exception as err:
            _LOGGER.info("生成 OpenAI.fm TTS 时出错：%s", err)
            raise

    async def _generate_audio(self, message, voice, prompt):
        url = "https://www.openai.fm/api/generate"
        form_data = aiohttp.FormData()
        form_data.add_field("input", message)
        form_data.add_field("prompt", prompt)
        form_data.add_field("voice", voice)
        form_data.add_field("vibe", "null")
        
        headers = {
            "accept": "*/*",
            "accept-language": "en,zh-CN;q=0.9,zh-TW;q=0.8,zh;q=0.7",
            "dnt": "1",
            "origin": "https://www.openai.fm",
            "referer": "https://www.openai.fm/",
            "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="118", "Google Chrome";v="118"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }
        
        async with self._session.post(url, data=form_data, headers=headers) as response:
            if response.status != 200:
                error_text = await response.text()
                _LOGGER.info("OpenAI.fm API 错误：%s, %s", response.status, error_text)
                raise Exception(f"OpenAI.fm API 错误： {response.status}")
            
            
            return await response.read()
