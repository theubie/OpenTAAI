IF NOT EXIST venv\Scripts\activate.bat (
    call install.bat
)
call venv\Scripts\activate.bat && (
    python main.py --api_key_file api_key.txt --verbose --streamer Ubie --assistant StreamAI --context_file context.txt --custom_pronunciations_file custom_words.txt --tts_model "tts_models/en/ljspeech/vits--neon" --poll_quiet_chat 100 --coqui_studio_api_token coqui_api_key.txt
) && (
    deactivate
) && pause
