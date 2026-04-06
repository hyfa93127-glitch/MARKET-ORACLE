@echo off
echo.
echo ==========================================
echo 📈 Stock Predictor Dashboard Launcher
echo ==========================================
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python from python.org.
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b
)

echo [1/3] Installing/Updating required software...
pip install -r requirements.txt --quiet

echo [2/3] Fetching latest market data and training AI...
python pipeline.py

echo [3/3] Starting the interactive Dashboard...
echo.
echo Your web browser should open automatically in a few seconds.
echo To stop everything, close this window.
echo.
python -m streamlit run app/dashboard.py

pause
