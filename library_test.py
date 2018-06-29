import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

DATE_CORPUS = '''
I was born 2015-07-25.
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # Fourth unit test; prove that we correctly extract dates in iso8601 format.
    def test_date_iso8601(self):
        self.assert_extract('I was born on 2015-07-25.', library.dates_iso8601, '2015-07-25')

    # Fifth unit test; prove that if we do not extract dates in iso8601 format
    # (YYYY-MM-DD) where the month is greater than 12 or the day is greater than
    # 31.
    def test_date_iso8601_invalid_month_or_day(self):
        # Prove that an invalid month is ignored
        self.assert_extract('I was born on 2015-13-25.', library.dates_iso8601)
        # Prove that an invalid day is ignored
        self.assert_extract('I was born on 2015-07-32.', library.dates_iso8601)

    # Sixth unit test; prove that we correctly extract dates in YYYY MMM DD
    # format.
    def test_date_dd_mmm_yyyy(self):
        self.assert_extract('My younger sister was born 25 Jan 2017.',
                            library.dates_dd_mmm_yyyy, '25 Jan 2017')


if __name__ == '__main__':
    unittest.main()
