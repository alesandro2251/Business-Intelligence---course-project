@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing required packages...
pip install --upgrade pip
pip install streamlit pandas plotly openpyxl

echo Freezing requirements to requirements.txt...
pip freeze > requirements.txt

echo.
echo Setup complete. To activate your environment later, run:
echo     venv\Scripts\activate
echo To run the app, run:
echo     streamlit run app.py
pause
