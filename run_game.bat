@echo off

echo Starting the GUI in background...
start /B python gui.py


echo Starting the game Quoridor...
python main_try.py
pause