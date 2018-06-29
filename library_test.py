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

# TODO: convert parameterized unittests to use pytest's @parameterized.expand
#       feature.
#
# Parameterize iso8601 date tests. Each entry in iso8601dates is a list in the
# following form: [ '<date>', <expected match> ].
# <date> is a string that will be added to the sentence "I was born <date>."
# <expected match> is either True or False.
ISO8601_DATES= [
  # Invalid month (> 12)
    ['invalid_month', '2015-13-25', False],
  # Invalid day (> 31)
    ['invalid_day', '2015-07-32', False],

  # TODO: test invalid MM-DD combinations.
    # Jan, Mar, May, Jul, Aug, Oct, and Dec have 31 days
    # Apr, Jun, Sept, and Nov have 30 days
    # Feb has 28 days except 29 on leap year

  # Minimum date format
    # True (third index) implies '2018-06-22' as the value to match
    ['yyyy_mm_dd_implicit', '2018-06-22', True],

  # Explicity pass '2018-06-22' as the value to match
    ['yyyy_mm_dd_explicit', '2018-06-22', '2018-06-22'],

  # Tests are designed to create a string with a single date.
  # However, we should test that multiple dates and their order still
  # match like all other (non-iso8061) tests.
    ['yyyy_mm_dd_multiple', '2018-06-22 2018-06-23', '2018-06-22', '2018-06-23'],

  # Date time formats with a space between date and time
    ['yyyy_mm_dd_space_hh_mm', '2018-06-22 18:22', True],
    ['yyyy_mm_dd_space_hh_mm_ss', '2018-06-22 18:22:19', True],
    ['yyyy_mm_dd_space_hh_mm_ss_ms', '2018-06-22 18:22:19.123', True],

  # Date time formats with a 'T' between date and time
    ['yyyy_mm_dd_t_hh_mm', '2018-06-22T18:22', True],
    ['yyyy_mm_dd_t_hh_mm_ss', '2018-06-22T18:22:19', True],
    ['yyyy_mm_dd_t_hh_mm_ss_ms', '2018-06-22T18:22:19.123', True],

  # All date time formats with 3 letter timezone abbreviation
    ['yyyy_mm_dd_space_hh_mm_3tz', '2018-06-22 18:22MDT', True],
    ['yyyy_mm_dd_space_hh_mm_ss_3tz', '2018-06-22 18:22:19MDT', True],
    ['yyyy_mm_dd_space_hh_mm_ss_ms_3tz', '2018-06-22 18:22:19.123MDT', True],
    ['yyyy_mm_dd_t_hh_mm_3tz', '2018-06-22T18:22MDT', True],
    ['yyyy_mm_dd_t_hh_mm_ss_3tz', '2018-06-22T18:22:19MDT', True],
    ['yyyy_mm_dd_t_hh_mm_ss_ms_3tz', '2018-06-22T18:22:19.123MDT', True],

  # All date time formats with single letter timezone abbreviation
    ['yyyy_mm_dd_space_hh_mm_1tz', '2018-06-22 18:22Z', True],
    ['yyyy_mm_dd_space_hh_mm_ss_1tz', '2018-06-22 18:22:19Z', True],
    ['yyyy_mm_dd_space_hh_mm_ss_ms_1tz', '2018-06-22 18:22:19.123Z', True],
    ['yyyy_mm_dd_t_hh_mm_1tz', '2018-06-22T18:22Z', True],
    ['yyyy_mm_dd_t_hh_mm_ss_1tz', '2018-06-22T18:22:19Z', True],
    ['yyyy_mm_dd_t_hh_mm_ss_ms_1tz', '2018-06-22T18:22:19.123Z', True],

  # All date time formats with an offset
    ['yyyy_mm_dd_space_hh_mm_offset', '2018-06-22 18:22-0800', True],
    ['yyyy_mm_dd_space_hh_mm_ss_offset', '2018-06-22 18:22:19-0800', True],
    ['yyyy_mm_dd_space_hh_mm_ss_ms_offset', '2018-06-22 18:22:19.123-0800',
     True],
    ['yyyy_mm_dd_t_hh_mm_offset', '2018-06-22T18:22-0800', True],
    ['yyyy_mm_dd_t_hh_mm_ss_offset', '2018-06-22T18:22:19-0800', True],
    ['yyyy_mm_dd_t_hh_mm_ss_ms_offset', '2018-06-22T18:22:19.123-0800', True],
]

# TODO: Parameterize DD MMM YYYY date tests. See ISO8061_DATES above for an
#       example.
# Each entry in DD_MMM_YYYY_DATES is a list in the following form:
# [ '<date>', <expected match> ].
# <date> is a string that will be added to the sentence "My sister was born
# <date>."
# <expected match> is either True or False.
# DD_MMM_YYYY_DATES = [
# ]

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for
    # mixed_ordinals, we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of
    # them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20',
                            '80')

    # TODO: Clarify if the grouping 12,4,7 should be extracted as a single
    #       value or if 12, 4, and 7 should be separately. In other words,
    #       should the expected value(s) be '12,4,7' or '12', '4', and '7'?
    # Second unit test; prove that if we look for integers, we find four of
    # them.
    def test_comma_separated_integer_groups(self):
        self.assert_extract('My locker combination is 12,4,7.',
                            library.integers, '12,4,7')

    # Third unit test; prove that if we look for integers where there are none,
    # we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # TODO: "Parameterize" DD MMM YYYY tests. See iso8601 tests, which have been
    #       refactored.
    # Sixth unit test; prove that we correctly extract dates in YYYY MMM DD
    # format.
    def test_date_dd_mmm_yyyy(self):
        self.assert_extract('My younger sister was born 25 Jan 2017.',
                            library.dates_dd_mmm_yyyy, '25 Jan 2017')

    def test_date_dd_mmm_comma_yyyy(self):
        self.assert_extract('My younger sister was born 25 Jan, 2017.',
                            library.dates_dd_mmm_yyyy, '25 Jan, 2017')

def test_iso8601_generator(text, *expected):
    def test(self):
        actual = [
          x[1].group(0) for x in library.scan(text, library.dates_iso8601)
        ]
        self.assertEquals(str(actual), str([x for x in expected]))
    return test

if __name__ == '__main__':
    for test in ISO8601_DATES:
        test_name = 'test_%s' % test[0]
        if isinstance(test[2], bool):
            # Is the test configured to expect test[1] to be found?
            if test[2]:
                # test[1] expected to be found.
                test = test_iso8601_generator('I was born {}.'.format(test[1]),
                                              test[1])
            else:
                # test[1] NOT expected to be found.
                test = test_iso8601_generator('I was born {}.'.format(test[1]))
        else:
            test = test_iso8601_generator('I was born {}.'.format(test[1]),
                                          *test[2:])
        setattr(TestCase, test_name, test)
    unittest.main()
