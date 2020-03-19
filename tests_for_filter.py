import unittest
import filter_fastqc_for_test
import io
import sys



class TestFilter(unittest.TestCase):

    def test_gc_content(self):
        self.assertAlmostEqual(filter_fastqc_v1_for_test.gc_content('ATGTGCTGCGT'), 54.55)

    def test_len_list_equal_four(self):
        self.assertTrue(filter_fastqc_v1_for_test.len_list_equal_four(['one', 'two', 'three', 'four']))

    def test_gc_bounds_all_in_one_maker_one_arg(self):
        self.assertFalse(filter_fastqc_v1_for_test.gc_bounds_all_in_one_maker([60], 34), False)

    def test_gc_bounds_all_in_one_maker_two_arg(self):
        self.assertFalse(filter_fastqc_v1_for_test.gc_bounds_all_in_one_maker([50, 60], 34), False)

    def test_check_name_return_not_none(self):
        self.assertIsNotNone(filter_fastqc_v1_for_test.check_name('Name0', 'Name'))

    def test_check_name_cut_fastq(self):
        self.assertEqual(filter_fastqc_v1_for_test.check_name(None, 'Read.fastq'), 'Read')

    def test_min_length(self):
        self.assertFalse(filter_fastqc_v1_for_test.min_length_check(23, 'ATGCCGCT'))

    def test_filtered_list_printer(self):
        text_trap = io.StringIO()
        sys.stdout = text_trap
        filter_fastqc_v1_for_test.filtered('WORK')
        sys.stdout = sys.__stdout__
        self.assertEqual(text_trap.getvalue().strip(), 'WORK')


if __name__ == '__main__':
    unittest.main()
