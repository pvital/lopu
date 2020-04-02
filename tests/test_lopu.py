#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# log parsing utility
# Copyright (c) 2020 Paulo Vital <pvital@gmail.com>
#

import unittest


import util as target


class CommandLineTestCase(unittest.TestCase):
    '''
    Base TestCase class, sets up a CLI parser
    '''
    @classmethod
    def setUpClass(cls):
        parser = target.init_argparse()
        cls.parser = parser


class TestUtil(CommandLineTestCase):
    '''
    Test Util script
    '''

    @unittest.skip('not covered by main tests')
    def test_help(self):
        '''
        Test the print of help
        '''
        args = self.parser.parse_args(['-h'])
        result = target.parse_log(args)
        self.assertEqual(result,
            '''
usage: util.py [OPTION]... [FILE]

log parsing utility.

positional arguments:
  FILE

optional arguments:
  -h, --help           show this help message and exit
  -f NUM, --first NUM  Print first NUM lines
  -l NUM, --last NUM   Print last NUM lines
  -t, --timestamps     Print lines that contain a timestamp in HH:MM:SS format
  -i, --ipv4           Print lines that contain an IPv4 address, matching IPs are highlighted
  -I, --ipv6           Print lines that contain an IPv6 address, (standard notation), matching IPs are highlighted
  -v, --version        show program's version number and exit'''
        )

    @unittest.skip('not covered by main tests')
    def test_version(self):
        '''
        Test print of version
        '''
        args = self.parser.parse_args(['--version'])
        result = target.parse_log(args)
        self.assertEqual(result,'util.py version 1.01')

    def test_head(self):
        '''
        Test print of a given number of first lines
        '''
        test_args = ['-f', '5', 'tests/test.log']
        args = self.parser.parse_args(test_args)
        result = target.parse_log(args, test_args)

        expected = [
            '# LOG FILE EXAMPLE',
            '2015-10-02 17:16:15.833793+00:00 heroku fwd="12.34.56.78" connection=OK',
            '2015-10-02 17:16:24.270610+00:00 heroku fwd="11.22.33.44" connection=OK',
            '2015-10-02 18:16:15.842297+00:00 heroku fwd="684D:1111:222:3333:4444:5555:6:77" connection=OK',
            '2015-10-02 18:16:24.271826+00:00 heroku fwd="2607:f0d0:1002:51::4" connection=OK',
        ]

        self.assertEqual(result,expected)

    def test_tail(self):
        '''
        Test print of a given number of last lines
        '''
        test_args = ['-l', '3', 'tests/test.log']
        args = self.parser.parse_args(test_args)
        result = target.parse_log(args, test_args)

        expected = [
            '2015-10-04 04:00:01.049123+00:00 heroku fwd="::1/128" connection=FAILED',
            '2015-10-04 05:02:59.049123+00:00 heroku fwd="127.0.0.1" connection=FAILED',
            '#EOF',
        ]

        self.assertEqual(result,expected)

    def test_timestamps_01(self):
        '''
        Test print of a lines with timestamp
        '''
        test_args = ['-t', 'tests/test.log']
        args = self.parser.parse_args(test_args)
        result = target.parse_log(args, test_args)

        expected = [
            '2015-10-02 17:16:15.833793+00:00 heroku fwd="12.34.56.78" connection=OK',
            '2015-10-02 17:16:24.270610+00:00 heroku fwd="11.22.33.44" connection=OK',
            '2015-10-02 18:16:15.842297+00:00 heroku fwd="684D:1111:222:3333:4444:5555:6:77" connection=OK',
            '2015-10-02 18:16:24.271826+00:00 heroku fwd="2607:f0d0:1002:51::4" connection=OK',
            '2015-10-02 21:16:16.486789+00:00 heroku fwd="192.168.1.15" connection=FAILED',
            '2015-10-02 22:16:24.047899+00:00 heroku fwd="129.42.38.10" connection=OK',
            '2015-10-02 23:17:17.035437+00:00 heroku fwd="52.6.158.18" connection=FAILED',
            '2015-10-03 00:16:24.047899+00:00 heroku fwd="2001:db8:85a3:8d3:1319:8a2e:370:7348" connection=OK',
            '2015-10-03 01:17:17.035437+00:00 heroku fwd="209.132.183.105" connection=OK',
            '2015-10-03 02:35:45.047899+00:00 heroku fwd="::1/128" connection=FAILED',
            '2015-10-03 03:35:46.049123+00:00 heroku fwd="127.0.0.1" connection=FAILED',
            '2015-10-04 04:00:01.049123+00:00 heroku fwd="::1/128" connection=FAILED',
            '2015-10-04 05:02:59.049123+00:00 heroku fwd="127.0.0.1" connection=FAILED',
        ]

        self.assertEqual(result,expected)

    def test_timestamps_02(self):
        '''
        Test print of a lines with timestamp
        '''
        test_args = ['--timestamps', 'tests/test.log']
        args = self.parser.parse_args(test_args)
        result = target.parse_log(args, test_args)

        expected = [
            '2015-10-02 17:16:15.833793+00:00 heroku fwd="12.34.56.78" connection=OK',
            '2015-10-02 17:16:24.270610+00:00 heroku fwd="11.22.33.44" connection=OK',
            '2015-10-02 18:16:15.842297+00:00 heroku fwd="684D:1111:222:3333:4444:5555:6:77" connection=OK',
            '2015-10-02 18:16:24.271826+00:00 heroku fwd="2607:f0d0:1002:51::4" connection=OK',
            '2015-10-02 21:16:16.486789+00:00 heroku fwd="192.168.1.15" connection=FAILED',
            '2015-10-02 22:16:24.047899+00:00 heroku fwd="129.42.38.10" connection=OK',
            '2015-10-02 23:17:17.035437+00:00 heroku fwd="52.6.158.18" connection=FAILED',
            '2015-10-03 00:16:24.047899+00:00 heroku fwd="2001:db8:85a3:8d3:1319:8a2e:370:7348" connection=OK',
            '2015-10-03 01:17:17.035437+00:00 heroku fwd="209.132.183.105" connection=OK',
            '2015-10-03 02:35:45.047899+00:00 heroku fwd="::1/128" connection=FAILED',
            '2015-10-03 03:35:46.049123+00:00 heroku fwd="127.0.0.1" connection=FAILED',
            '2015-10-04 04:00:01.049123+00:00 heroku fwd="::1/128" connection=FAILED',
            '2015-10-04 05:02:59.049123+00:00 heroku fwd="127.0.0.1" connection=FAILED',
        ]

        self.assertEqual(result,expected)

    def test_ipv4_01(self):
        '''
        Test print of a lines with IPv4 addresses
        '''
        test_args = ['-i', 'tests/test.log']
        args = self.parser.parse_args(test_args)
        result = target.parse_log(args, test_args)

        expected = [
            '2015-10-02 17:16:15.833793+00:00 heroku fwd="\x1b[1;33;44m12.34.56.78\x1b[m" connection=OK',
            '2015-10-02 17:16:24.270610+00:00 heroku fwd="\x1b[1;33;44m11.22.33.44\x1b[m" connection=OK',
            '2015-10-02 21:16:16.486789+00:00 heroku fwd="\x1b[1;33;44m192.168.1.15\x1b[m" connection=FAILED',
            '2015-10-02 22:16:24.047899+00:00 heroku fwd="\x1b[1;33;44m129.42.38.10\x1b[m" connection=OK',
            '2015-10-02 23:17:17.035437+00:00 heroku fwd="\x1b[1;33;44m52.6.158.18\x1b[m" connection=FAILED',
            '2015-10-03 01:17:17.035437+00:00 heroku fwd="\x1b[1;33;44m209.132.183.105\x1b[m" connection=OK',
            '2015-10-03 03:35:46.049123+00:00 heroku fwd="\x1b[1;33;44m127.0.0.1\x1b[m" connection=FAILED',
            '2015-10-04 05:02:59.049123+00:00 heroku fwd="\x1b[1;33;44m127.0.0.1\x1b[m" connection=FAILED',
        ]

        self.assertEqual(result,expected)

    def test_ipv4_02(self):
        '''
        Test print of a lines with IPv4 addresses
        '''
        test_args = ['--ipv4', 'tests/test.log']
        args = self.parser.parse_args(test_args)
        result = target.parse_log(args, test_args)

        expected = [
            '2015-10-02 17:16:15.833793+00:00 heroku fwd="\x1b[1;33;44m12.34.56.78\x1b[m" connection=OK',
            '2015-10-02 17:16:24.270610+00:00 heroku fwd="\x1b[1;33;44m11.22.33.44\x1b[m" connection=OK',
            '2015-10-02 21:16:16.486789+00:00 heroku fwd="\x1b[1;33;44m192.168.1.15\x1b[m" connection=FAILED',
            '2015-10-02 22:16:24.047899+00:00 heroku fwd="\x1b[1;33;44m129.42.38.10\x1b[m" connection=OK',
            '2015-10-02 23:17:17.035437+00:00 heroku fwd="\x1b[1;33;44m52.6.158.18\x1b[m" connection=FAILED',
            '2015-10-03 01:17:17.035437+00:00 heroku fwd="\x1b[1;33;44m209.132.183.105\x1b[m" connection=OK',
            '2015-10-03 03:35:46.049123+00:00 heroku fwd="\x1b[1;33;44m127.0.0.1\x1b[m" connection=FAILED',
            '2015-10-04 05:02:59.049123+00:00 heroku fwd="\x1b[1;33;44m127.0.0.1\x1b[m" connection=FAILED',
        ]

        self.assertEqual(result,expected)

    def test_ipv6_01(self):
        '''
        Test print of a lines with IPv6 addresses
        '''
        test_args = ['-I', 'tests/test.log']
        args = self.parser.parse_args(test_args)
        result = target.parse_log(args, test_args)

        expected = [
            '2015-10-02 18:16:15.842297+00:00 heroku fwd="\x1b[1;33;44m684D:1111:222:3333:4444:5555:6:77\x1b[m" connection=OK',
            '2015-10-02 18:16:24.271826+00:00 heroku fwd="\x1b[1;33;44m2607:f0d0:1002:51::4\x1b[m" connection=OK',
            '2015-10-03 00:16:24.047899+00:00 heroku fwd="\x1b[1;33;44m2001:db8:85a3:8d3:1319:8a2e:370:7348\x1b[m" connection=OK',
        ]

        self.assertEqual(result,expected)


    def test_ipv6_02(self):
        '''
        Test print of a lines with IPv6 addresses
        '''
        test_args = ['--ipv6', 'tests/test.log']
        args = self.parser.parse_args(test_args)
        result = target.parse_log(args, test_args)

        expected = [
            '2015-10-02 18:16:15.842297+00:00 heroku fwd="\x1b[1;33;44m684D:1111:222:3333:4444:5555:6:77\x1b[m" connection=OK',
            '2015-10-02 18:16:24.271826+00:00 heroku fwd="\x1b[1;33;44m2607:f0d0:1002:51::4\x1b[m" connection=OK',
            '2015-10-03 00:16:24.047899+00:00 heroku fwd="\x1b[1;33;44m2001:db8:85a3:8d3:1319:8a2e:370:7348\x1b[m" connection=OK',
        ]

        self.assertEqual(result,expected)

    def test_intesection_01(self):
        '''
        Test print of a lines with multiple arguments
        '''
        test_args = ['--ipv4', '--last', '50', 'tests/test.log']
        args = self.parser.parse_args(test_args)
        result = target.parse_log(args, test_args)

        expected = [
            '2015-10-02 17:16:15.833793+00:00 heroku fwd="\x1b[1;33;44m12.34.56.78\x1b[m" connection=OK',
            '2015-10-02 17:16:24.270610+00:00 heroku fwd="\x1b[1;33;44m11.22.33.44\x1b[m" connection=OK',
            '2015-10-02 21:16:16.486789+00:00 heroku fwd="\x1b[1;33;44m192.168.1.15\x1b[m" connection=FAILED',
            '2015-10-02 22:16:24.047899+00:00 heroku fwd="\x1b[1;33;44m129.42.38.10\x1b[m" connection=OK',
            '2015-10-02 23:17:17.035437+00:00 heroku fwd="\x1b[1;33;44m52.6.158.18\x1b[m" connection=FAILED',
            '2015-10-03 01:17:17.035437+00:00 heroku fwd="\x1b[1;33;44m209.132.183.105\x1b[m" connection=OK',
            '2015-10-03 03:35:46.049123+00:00 heroku fwd="\x1b[1;33;44m127.0.0.1\x1b[m" connection=FAILED',
            '2015-10-04 05:02:59.049123+00:00 heroku fwd="\x1b[1;33;44m127.0.0.1\x1b[m" connection=FAILED',
        ]

        self.assertEqual(result,expected)

    def test_intesection_02(self):
        '''
        Test print of a lines with multiple arguments
        '''
        test_args = ['--ipv4', '--last', '2', 'tests/test.log']
        args = self.parser.parse_args(test_args)
        result = target.parse_log(args, test_args)

        expected = [
            '2015-10-03 03:35:46.049123+00:00 heroku fwd="\x1b[1;33;44m127.0.0.1\x1b[m" connection=FAILED',
            '2015-10-04 05:02:59.049123+00:00 heroku fwd="\x1b[1;33;44m127.0.0.1\x1b[m" connection=FAILED',
        ]

        self.assertEqual(result,expected)

    def test_intesection_03(self):
        '''
        Test print of a lines with multiple arguments
        '''
        test_args = ['-f5', '-I', 'tests/test.log']
        args = self.parser.parse_args(test_args)
        result = target.parse_log(args, test_args)

        expected = [
            '2015-10-02 18:16:15.842297+00:00 heroku fwd="\x1b[1;33;44m684D:1111:222:3333:4444:5555:6:77\x1b[m" connection=OK',
            '2015-10-02 18:16:24.271826+00:00 heroku fwd="\x1b[1;33;44m2607:f0d0:1002:51::4\x1b[m" connection=OK',
        ]

        self.assertEqual(result,expected)

if __name__ == '__main__':
    unittest.main()
