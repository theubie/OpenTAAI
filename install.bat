@echo off
echo Please select your installation:
echo [A] NVIDIA GPU version (requires CUDA capable GPU)
echo [B] CPU version

choice /c AB /n /m "Select A or B: "

if errorlevel 1 (
    pip install -r requirements.txt
) else (
    pip install -r requirements-cpu.txt
)

pause
