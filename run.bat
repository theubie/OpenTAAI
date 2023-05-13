IF NOT EXIST venv\Scripts\activate.bat (
    call install.bat
)
call venv\Scripts\activate.bat && (
    python main.py --api_key_file api_key.txt --verbose --streamer Ubie --assistant "Stream AI" --context_file context.txt --custom_pronunciations_file custom_words.txt --tts_model coqui_studio/en/OpenTAAI-Lisa/coqui_studio --poll_quiet_chat 20 --coqui_studio_api_token coqui_api_key.txt --streamer_twitch theubie --command_users command_users.txt --tts_engine coqui --pyttsx3_voice 1 --llm_api openai_api --microphone "Microphone (NVIDIA Broadcast)" --attitude "snarky and sarcastic" 
) && (
    deactivate
) && pause
