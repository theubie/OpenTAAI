#!/bin/bash

if [ ! -f ./venv/Scripts/activate.bat ]; then
    ./install.bat
fi

source ./venv/Scripts/activate.bat && python main.py --chat_file chat.txt --api_key_file api_key.txt --poll_interval 5 --context_file context.txt --custom_pronunciations_file custom_words.txt && deactivate

echo "Press any key to continue..."
read -n 1 -s