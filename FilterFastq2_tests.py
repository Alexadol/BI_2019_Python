import unittest
import FilterFastq2
import io
import sys


class TestFilter(unittest.TestCase):

    def test_len_list_equal_four(self):
        self.assertTrue(FilterFastq2.len_list_equal_four(['one', 'two', 'three', 'four']))

    def test_gc_bounds_all_in_one_maker_one_arg(self):
        self.assertFalse(FilterFastq2.gc_bounds_all_in_one_maker([60], 34), False)

    def test_gc_bounds_all_in_one_maker_two_arg(self):
        self.assertFalse(FilterFastq2.gc_bounds_all_in_one_maker([50, 60], 34), False)

    def test_check_name_return_not_none(self):
        self.assertIsNotNone(FilterFastq2.check_name('Name0', 'Name'))

    def test_check_name_cut_fastq(self):
        self.assertEqual(FilterFastq2.check_name(None, 'Read.fastq'), 'Read')

    def test_headcrop(self):
        self.assertEqual(FilterFastq2.headcrop('ATGTGCTGCGT', 3), 'TGCTGCGT')

    def test_crop(self):
        self.assertEqual(FilterFastq2.crop('ATGTGCTGCGTTT', 5), 'ATGTG')

    def test_cut_string_quality_start_drop(self):
        self.assertEqual(FilterFastq2.cut_quality_string(10, 'SOMERANDOMSYMBOLS', 'start'), 'DOMSYMBOLS')

    def test_cut_string_quality_end_drop(self):
        self.assertEqual(FilterFastq2.cut_quality_string(10, 'SOMERANDOMSYMBOLS', 'end'), 'SOMERANDOM')

    def test_slidingwindow(self):
        self.assertEqual(FilterFastq2.slidingwindow('GAAGAGCACACGTCTGAACTCCAGTCACCGT',
                                                                 '9?<9;@23538<88>@348<396;;365/=4', 4, 20),
                         'GAAGAGCACA')

    def test_trailing(self):
        self.assertEqual(
            FilterFastq2.trailing('GTTTTTTTTTTTTTTTTTACCCCCCCCACAC', '8EEEEEEEEEEEEEEEEB=@<<<<<;=4/40',
                                               25), 'GTTTTTTTTTTTTTTTTTACCCCCCCC')

    def test_leading(self):
        self.assertEqual(
            FilterFastq2.leading('CCCCCCCCCCAAATCGGAAAAACACACCCCC', '0;;71;;;<@3:??=8>:@;?=>8>9453;/', 27),
            'CCAAATCGGAAAAACACACCCCC')


if __name__ == '__main__':
    unittest.main()
