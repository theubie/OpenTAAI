@echo off
python -m venv venv
echo Please select your installation:
echo [A] NVIDIA GPU version (requires CUDA capable GPU)
echo [B] CPU version

choice /c AB /n /m "Select A or B: "

if errorlevel 1 (
	call venv\Scripts\activate.bat && (pip install -r requirements.txt) && (pip install -r requirements-cuda.txt) && (deactivate)
) else (
	call venv\Scripts\activate.bat && (pip install -r requirements.txt) && (deactivate)
)

pause
