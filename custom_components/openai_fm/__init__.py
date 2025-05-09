DOMAIN = "openai_fm"

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry):
    
    await hass.config_entries.async_forward_entry_setups(entry, ["tts"])
    return True

async def async_unload_entry(hass, entry):
    
    return await hass.config_entries.async_forward_entry_unload(entry, "tts")
