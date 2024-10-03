import unittest
import pandas as pd
import numpy as np


# The function we are testing
def reduce_mem_usage(df, verbose=True):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024 ** 2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    end_mem = df.memory_usage().sum() / 1024 ** 2
    if verbose:
        print('Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)'.format(end_mem,
                                                                              100 * (start_mem - end_mem) / start_mem))
    return df


# Unit test class for the reduce_mem_usage function
class TestReduceMemUsage(unittest.TestCase):

    def setUp(self):
        # Set up a DataFrame with various numeric columns to test the function
        self.df = pd.DataFrame({
            'int_column': np.random.randint(0, 100, size=1000),  # Random integer values
            'float_column': np.random.rand(1000) * 100,  # Random float values
            'large_int_column': np.random.randint(0, 1e6, size=1000),  # Large integers
            'small_float_column': np.random.rand(1000) * 1e-5,  # Small float values
        })

    def test_memory_reduction(self):
        # Test if the memory usage is actually reduced
        original_memory = self.df.memory_usage().sum() / 1024 ** 2
        df_reduced = reduce_mem_usage(self.df.copy(), verbose=False)
        reduced_memory = df_reduced.memory_usage().sum() / 1024 ** 2
        self.assertLess(reduced_memory, original_memory, "Memory usage was not reduced.")

    def test_integer_downcasting(self):
        # Test if integer columns are downcasted appropriately
        df_reduced = reduce_mem_usage(self.df.copy(), verbose=False)
        self.assertTrue(pd.api.types.is_integer_dtype(df_reduced['int_column']), "int_column should be integer.")
        self.assertTrue(df_reduced['int_column'].dtype == np.int8 or df_reduced['int_column'].dtype == np.int16,
                        "int_column was not downcasted correctly.")

    def test_float_downcasting(self):
        # Test if float columns are downcasted appropriately
        df_reduced = reduce_mem_usage(self.df.copy(), verbose=False)
        self.assertTrue(pd.api.types.is_float_dtype(df_reduced['float_column']), "float_column should be float.")
        self.assertTrue(
            df_reduced['float_column'].dtype == np.float32 or df_reduced['float_column'].dtype == np.float16,
            "float_column was not downcasted correctly.")

    def test_large_int_column(self):
        # Test if a column with large integers is downcasted to an appropriate size
        df_reduced = reduce_mem_usage(self.df.copy(), verbose=False)
        self.assertTrue(pd.api.types.is_integer_dtype(df_reduced['large_int_column']),
                        "large_int_column should be integer.")
        self.assertTrue(
            df_reduced['large_int_column'].dtype == np.int32 or df_reduced['large_int_column'].dtype == np.int64,
            "large_int_column was not downcasted correctly.")


    def test_data_type_reduction(self):
        # Ensure that float64 and int64 columns were downcasted to smaller types
        df_reduced = reduce_mem_usage(self.df.copy(), verbose=False)

        # Check that the 'float_column' has been downcasted to float32 or float16
        self.assertIn(df_reduced['float_column'].dtype, [np.float16, np.float32],
                      "float_column should be downcasted to float32 or float16")

        # Check that the 'int_column' has been downcasted to int8 or int16
        self.assertIn(df_reduced['int_column'].dtype, [np.int8, np.int16],
                      "int_column should be downcasted to int8 or int16")


if __name__ == '__main__':
    unittest.main()
