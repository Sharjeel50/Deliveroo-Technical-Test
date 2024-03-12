## Cron Parser 

### System requirements -

- Python > 3.6
- `venv` Package install (`pip install venv`)

### Usage

To use the Cron parser, make sure you have it and follow the steps below

1. Navigate to downloaded folder
2. Create a virtual environment using the folling command - `python -m venv ./venv`
3. Activate the virtual environment, for MacOS using the command `source venv/bin/activate`, for Windows run `Activate.bat` found under `/venv/bin`
4. Install requirements.txt using the following command - `pip install -r requirements.txt`
5. Run `cli.py` using `python cli.py` and you should see `Cron Expression:` which is where you can enter your cron expression

### Tests

You can run all unit tests by typing `pytest` in the base directory of the folder
