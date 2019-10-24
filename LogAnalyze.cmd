@echo Off
setlocal enabledelayedexpansion
echo %date% %time%

D:\Python27\python.exe LogAnalyze.py
:Exit
echo -------------------------end----------------------------
:Loop
pause
goto Loop

