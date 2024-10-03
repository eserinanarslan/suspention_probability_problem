import unittest
import pandas as pd
import numpy as np
import warnings

# Ignore warnings
warnings.filterwarnings("ignore")

# Assuming the fill_null_values function is already defined
# Method for filling the null values
def fill_null_values(df):
    for column in df.columns:
        if df[column].dtype == 'object':
            df[column].fillna('unknown', inplace=True)
        elif df[column].dtype in ['int64', 'float64']:
            df[column].fillna(0, inplace=True)
            df[column][np.isnan(df[column])] = 0
    return df

class TestFillNullValues(unittest.TestCase):

    def setUp(self):
        # This method will run before each test
        self.df = pd.DataFrame({
            'name': ['Alice', None, 'Charlie', None],
            'age': [25, np.nan, 30, 22],
            'score': [90.5, np.nan, 88.0, None]
        })

    def test_fill_object_columns(self):
        # Test if 'object' columns (e.g., 'name') are filled with 'unknown'
        result_df = fill_null_values(self.df.copy())
        expected_names = ['Alice', 'unknown', 'Charlie', 'unknown']
        self.assertEqual(list(result_df['name']), expected_names)

    def test_fill_numeric_columns(self):
        # Test if 'int64' and 'float64' columns are filled with 0
        result_df = fill_null_values(self.df.copy())
        expected_ages = [25, 0, 30, 22]
        expected_scores = [90.5, 0, 88.0, 0]
        self.assertEqual(list(result_df['age']), expected_ages)
        self.assertEqual(list(result_df['score']), expected_scores)

    def test_no_unfilled_null_values(self):
        # Test that there are no remaining NaN values in the DataFrame
        result_df = fill_null_values(self.df.copy())
        self.assertFalse(result_df.isnull().values.any())

if __name__ == '__main__':
    unittest.main()
