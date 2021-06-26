#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.crypt.base64`
====================================
.. moduleauthor:: Venkatesh Vanjre <vvanjre@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""

################################################################################
import os
import sys
import base64
from alabs.common.util.vvargs import ArgsError
from unittest import TestCase
# noinspection PyProtectedMember
from argoslabs.crypt.base64 import _main as main


################################################################################
class TU(TestCase):
    """
    TestCase for argoslabs.crypt.base64
    """
    # ==========================================================================
    isFirst = True

    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_success_string_encode(self):
        outfile = 'stdout.txt'
        try:
            r = main('Encode',
                     '--stringinput', 'test text',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == 'dGVzdCB0ZXh0')

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_success_string_decode(self):
        outfile = 'stdout.txt'
        try:
            r = main('Decode',
                     '--stringinput', 'dGVzdCB0ZXh0',
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == 'test text')

        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0120_success_file_encode(self):
        outfile = 'stdout.txt'
        infile = 'infile.txt'
        with open(infile, 'w') as ofp:
            ofp.write('test text')
        try:
            r = main('Encode',
                     '--fileinput', infile,
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == 'dGVzdCB0ZXh0')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0130_success_file_decode(self):
        outfile = 'stdout.txt'
        infile = 'infile.txt'
        with open(infile, 'w') as ofp:
            ofp.write('dGVzdCB0ZXh0')
        try:
            r = main('Decode',
                     '--fileinput', infile,
                     '--outfile', outfile)
            self.assertTrue(r == 0)
            with open(outfile) as ifp:
                rs = ifp.read()
                print(rs)
            self.assertTrue(rs == 'test text')
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
