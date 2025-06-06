# Recreate the python virtual environment and reinstall libs on Windows.
# Note: This script works with Python 3.12.9.
# python --version -> Python 3.12.9
# Chris Joakim, 2025

# Delete the previous venv files; will be recreated below
$dirs = ".\venv\", ".\pyvenv.cfg"
foreach ($d in $dirs) {
    if (Test-Path $d) {
        Write-Host "deleting $d ..."
        del $d -Force -Recurse
    } 
}

$tmp_dir = ".\tmp\"
if (-not(Test-Path $tmp_dir -PathType Container)) {
    Write-Host 'creating the tmp directory ...'
    New-Item -path $tmp_dir -ItemType Directory
}

Write-Host 'creating new venv ...'
python -m venv .\venv\

Write-Host 'activating new venv ...'
.\venv\Scripts\Activate.ps1

Write-Host 'upgrading pip ...'
python -m pip install --upgrade pip 

Write-Host 'install pip-tools ...'
pip install --upgrade pip-tools

.\venv\Scripts\Activate.ps1

# Enable Long Paths in Windows
# See https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation?tabs=powershell#enable-long-paths-in-windows-10-version-1607-and-later
# Win Key + X, then Windows Terminal (admin), the run the following PowerShell command:
# New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
