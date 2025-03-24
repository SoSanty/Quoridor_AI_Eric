@echo off

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

pip install -r requirements.txt

echo Starts the Gui in background...
start /B python gui.py


echo Starts the game Quoridor...
python main.py


deactivate