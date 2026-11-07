# Lab 4 — Smart Optimization Assistant using Dynamic Programming

## Requirements
- Python 3.10 or newer
- VS Code (recommended)
- Internet connection for installing packages

## Windows setup (PowerShell terminal)
```powershell
mkdir daa_lab4
cd daa_lab4
# Put app.py and requirements.txt in this folder
py -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```
If PowerShell blocks activation, run this once in the current terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```
Alternative activation in Command Prompt:
```cmd
venv\Scripts\activate.bat
```

## Application modules
1. LCS: accepts two strings and displays LCS, its length, DP table, heatmap, time and traced memory.
2. 0/1 Knapsack: accepts comma-separated weights and values plus capacity; displays chosen items, maximum profit and DP table.
3. Matrix Chain Multiplication: accepts matrix dimensions; displays minimum scalar multiplication cost, optimal parenthesization, cost table and split table.
4. Complexity Summary: compares theoretical time, space and subproblem counts.

## Sample inputs
- LCS: `ABCBDAB` and `BDCABA`
- Knapsack: weights `2,3,4,5`; values `3,4,5,6`; capacity `5`
- MCM dimensions: `10,30,5,60`

## GitHub
Create a new empty repository named `daa-lab4-smart-optimization-assistant`, then:
```powershell
git init
git add .
git commit -m "Complete Lab 4 dynamic programming assistant"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/daa-lab4-smart-optimization-assistant.git
git push -u origin main
```
Replace YOUR-USERNAME with your GitHub username. Never share your password or token.

## Evidence to capture
Take your own screenshots after running the app:
- application home/tabs
- LCS result and DP table
- Knapsack result and DP table
- MCM result, cost table and split table
- complexity summary
Add screenshots to a `screenshots` folder in the repository and insert them in the report.

## Notes
- Runtime and memory values are measured on the computer at execution time; they will vary.
- The application uses Streamlit as the interactive interface, and NumPy, Matplotlib and Pandas for visualization/table display.
