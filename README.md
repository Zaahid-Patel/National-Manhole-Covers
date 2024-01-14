To activate the virtual environment use:

For Linux:
.venv\Scripts\activate

For Windows:
.venv\Scripts\activate

To deactivate the virtual environment use:

deactivate

If any packages were installed use:

pip freeze > requirements.txt

To install from requirements.txt:

pip install -r requirements.txt

To create exe:

pyinstaller --onefile .\Schedule\order.py