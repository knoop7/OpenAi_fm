"""Config flow for OpenAI.fm TTS integration."""
from __future__ import annotations
import voluptuous as vol
import yaml
from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.selector import (
    TemplateSelector,
)
from .const import (CONF_PROMPT, DEFAULT_PROMPT, SUPPORTED_VOICES, DOMAIN)

DISCLAIMER = """
**免责声明**
- 本集成由Knoop7开源开发，仅供学习和个人使用
- 不得用于商业用途，使用中产生的任何问题开发者不承担责任
- 使用本集成即表示您同意上述条款

**关于开发者**
- 开发者：Knoop7
- 项目地址：https://github.com/knoop7/openai_stt
- 问题反馈：请在GitHub项目页面提交issue
"""

class OpenAIFmConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    
    async def async_step_user(self, user_input=None) -> FlowResult:
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
            
        if user_input is not None:
            return await self.async_step_config()
            
        return self.async_show_form(
            step_id="user",
            description_placeholders={"disclaimer": DISCLAIMER},
            data_schema=vol.Schema({}),  
        )
        
    async def async_step_config(self, user_input=None) -> FlowResult:
        errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title=f"OpenAI.fm",
                data=user_input,
            )
        return self.async_show_form(
            step_id="config",
            data_schema=vol.Schema({
                vol.Required(CONF_PROMPT, default=DEFAULT_PROMPT): TemplateSelector(),
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        return OpenAIFmOptionsFlow(config_entry)

class OpenAIFmOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.entry_id = config_entry.entry_id
        self.entry_data = dict(config_entry.data)
        self.entry_options = dict(config_entry.options)

    async def async_step_init(self, user_input=None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return self.async_show_form(
            step_id="init",
            description_placeholders={"disclaimer": DISCLAIMER},
            data_schema=vol.Schema({
                vol.Required(
                    CONF_PROMPT, default=self.entry_options.get(CONF_PROMPT, self.entry_data.get(CONF_PROMPT, DEFAULT_PROMPT))
                ): TemplateSelector(),
            }),
        )
