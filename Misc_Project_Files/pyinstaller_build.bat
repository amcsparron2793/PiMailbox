@echo off

echo Prepping for Pyinstaller build..

REM %HOMEDRIVE%%HOMEPATH% = home drive letter \ path to home dir
set project_root=%HOMEDRIVE%%HOMEPATH%\Desktop\Python_Projects\PiMailbox
set build_dir=%project_root%\Misc_Project_Files\pyinstaller_build_dir
set specfile_name=Main.spec
set dist_dir=%build_dir%\dist

IF %ERRORLEVEL% NEQ 0 (
    GOTO ERROR
    )

echo variables set successfully

cd %build_dir%
IF %ERRORLEVEL% NEQ 0 (
    GOTO WRONG_CD
    )

set curr_dir=%cd%

REM this is just for a double check that we are in the correct directory.
REM Any issues changing to %build_dir% should be caught above
IF NOT %curr_dir% == %build_dir% GOTO WRONG_CD

echo building in %build_dir% based on %specfile_name%

REM attempt to run pyinstaller,
REM if there is an error, goto ERROR.
REM Otherwise goto COMPLETE
pyinstaller --noconfirm -D %specfile_name%

IF %ERRORLEVEL% EQU 3 (
    GOTO PATH_ERROR
    )

IF %ERRORLEVEL% NEQ 0 (
    GOTO ERROR
    )
GOTO COMPLETE

REM these are all labels that the script can jump to
:WRONG_CD
color 0c
echo ERROR: The system could not switch the current directory to build_dir
GOTO ERROR

:PATH_ERROR
color 0c
echo ERROR: The system could not find the path specified, please try again
GOTO ERROR

:ERROR
color 0c
echo ERROR: Could not Build EXE, please try again
cd %project_root%
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: could not change directory back to project root after previous ERROR
    pause
    GOTO END
    )
pause
GOTO END

:COMPLETE
color 0a
echo build complete see %dist_dir%
cd %project_root%
pause
GOTO END

:END
color