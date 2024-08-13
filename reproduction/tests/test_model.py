'''
Model testing

This module contains a test which checks whether the simulation model is
producing consistent results. The model is run using the provided input
parameters from the original code.
'''

import subprocess
import pandas as pd
from pathlib import Path
import tempfile
import pytest

# Path to file with expected results and to store test run results
EXP_FILE = 'exp_results/OUT_STATS.csv'
TEMP_FILE = Path(tempfile.mkdtemp()).joinpath('test_result.csv')


# Create fixture with path to file with expected results
@pytest.fixture
def exp_file():
    return EXP_FILE


# Create fixture with path to temporary file to contain results from tests
@pytest.fixture
def temp_file():
    return TEMP_FILE


def test_equal_df(temp_file, exp_file):
    '''
    Test that model results with the default/provided input parameters are
    consistent with expected results.
    '''
    # Construct the command
    command = [
        'python', 'scripts/main.py',
        '-z', 'input/ZONES.csv',
        '-p', 'input/ICU_INPUT_PARAMS.csv',
        '-c', 'input/DAILY_ARRIVALS.csv',
        '-o', temp_file
    ]

    # Run the model and check for errors
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the script ran successfully
    if result.returncode != 0:
        print('Error running model script:', result.stderr)
        raise RuntimeError('Model script did not run successfully')

    # Import test and expected results
    test_result = pd.read_csv(Path(__file__).parent.joinpath(temp_file))
    exp_result = pd.read_csv(Path(__file__).parent.joinpath(exp_file))

    # Check that dataframes are equal
    pd.testing.assert_frame_equal(test_result, exp_result)
