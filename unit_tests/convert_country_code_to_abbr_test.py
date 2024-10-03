import unittest

# The original function
country_code_to_abbr = {
    33: 'FR',  # France
    44: 'GB',  # United Kingdom
    1: 'US',   # United States/Canada
    39: 'IT',  # Italy
    34: 'ES',  # Spain
    68: 'Unknown',  # Undefined or not standard
    26: 'Unknown',  # Undefined or not standard
    59: 'Unknown',  # Undefined or not standard
    689: 'PF',  # French Polynesia
    687: 'NC',  # New Caledonia
    262: 'RE',  # Réunion (note: previously it was YT, but overwritten here)
    590: 'GP',  # Guadeloupe
    351: 'PT',  # Portugal
    40: 'RO',  # Romania
}

def convert_country_code_to_abbr(country_code):
    return country_code_to_abbr.get(country_code, 'Unknown')


# Unit test class for the function
class TestConvertCountryCodeToAbbr(unittest.TestCase):

    def test_valid_country_codes(self):
        # Test valid country codes that are in the dictionary
        self.assertEqual(convert_country_code_to_abbr(33), 'FR')  # France
        self.assertEqual(convert_country_code_to_abbr(44), 'GB')  # United Kingdom
        self.assertEqual(convert_country_code_to_abbr(1), 'US')   # United States/Canada
        self.assertEqual(convert_country_code_to_abbr(39), 'IT')  # Italy
        self.assertEqual(convert_country_code_to_abbr(34), 'ES')  # Spain
        self.assertEqual(convert_country_code_to_abbr(689), 'PF') # French Polynesia
        self.assertEqual(convert_country_code_to_abbr(687), 'NC') # New Caledonia
        self.assertEqual(convert_country_code_to_abbr(262), 'RE') # Réunion (overwritten)

    def test_unknown_country_codes(self):
        # Test country codes that are mapped to 'Unknown'
        self.assertEqual(convert_country_code_to_abbr(68), 'Unknown')  # Undefined
        self.assertEqual(convert_country_code_to_abbr(26), 'Unknown')  # Undefined
        self.assertEqual(convert_country_code_to_abbr(59), 'Unknown')  # Undefined

    def test_non_existing_country_codes(self):
        # Test country codes that do not exist in the dictionary
        self.assertEqual(convert_country_code_to_abbr(999), 'Unknown')  # Non-existent code
        self.assertEqual(convert_country_code_to_abbr(100), 'Unknown')  # Non-existent code

    def test_invalid_inputs(self):
        # Test invalid inputs (non-integer types)
        self.assertEqual(convert_country_code_to_abbr(None), 'Unknown')    # None
        self.assertEqual(convert_country_code_to_abbr('33'), 'Unknown')    # String input
        self.assertEqual(convert_country_code_to_abbr(-1), 'Unknown')      # Negative number


if __name__ == '__main__':
    unittest.main()
