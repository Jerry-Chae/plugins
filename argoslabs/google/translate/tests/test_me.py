#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.google.translate.tests.test_me`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2021/04/07]
#     - 그룹에 "1-AI Solutions" 넣음
#  * [2020/12/04]
#     - Google API changed so new module using google_trans_new
#  * [2020/04/29]
#     - add --file, --encoding options
#  * [2020/03/05]
#     - just change group display name
#     - remove engine parameter
#     - move argoslabs.ai.translate => argoslabs.google.translate
#  * [2019/04/25]
#     - add arguments' display_name
#  * [2019/04/10]
#     - some en-us lang does not working
#  * [2019/03/08]
#     - starting

################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.google.translate import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def test0000_init(self):
        self.assertTrue(True)

    # ==========================================================================
    def test0100_empty_parameter(self):
        try:
            _ = main()
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0110_unknown_engine(self):
        try:
            _ = main('unknown', 'hello world?')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0120_missing_msg(self):
        try:
            _ = main('google')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0200_hello_detect(self):
        out_f = 'out.txt'
        err_f = 'err.txt'
        try:
            r = main('こんにちは世界？私はTTSです?', '--detect',
                     '--outfile', out_f,
                     '--errfile', err_f)
            self.assertTrue(r == 0)
            with open(out_f) as ifp:
                out = ifp.read()
                print(out)
                # self.assertTrue(out == 'lang, confidence\nja, 1.0\n')
                self.assertTrue(out == 'lang, confidence\nja, N/A\n')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_hello_jp2en(self):
        out_f = 'out.txt'
        err_f = 'err.txt'
        try:
            r = main('こんにちは世界？私はTTSです?',
                     '--dest', 'English',
                     '--outfile', out_f,
                     '--errfile', err_f)
            self.assertTrue(r == 0)
            with open(out_f, encoding='utf8') as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out in ('Hello World? Am i TTS? ',
                                        'Hello World? Is it TTS? '))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0220_hello_jp2ko(self):
        out_f = 'out.txt'
        err_f = 'err.txt'
        try:
            r = main('こんにちは世界？私はTTSです?',
                     '--dest', 'Korean',
                     '--outfile', out_f,
                     '--errfile', err_f)
            self.assertTrue(r == 0)
            with open(out_f, encoding='utf8') as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out == '안녕하세요 세계 ? 나는 TTS 입니다 ? ')
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0230_hello_jp2cn(self):
        out_f = 'out.txt'
        err_f = 'err.txt'
        try:
            r = main('こんにちは世界？私はTTSです?',
                     '--dest', 'Chinese (Mandarin/China)',
                     '--outfile', out_f,
                     '--errfile', err_f)
            self.assertTrue(r == 0)
            with open(out_f, encoding='utf8') as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out in ('你好，世界？ 我是TTS吗？ ',
                                        '你好世界？ 是tts吗？ '))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0240_hello_jp2cn_file(self):
        msg_f = 'msg.txt'
        out_f = 'out.txt'
        err_f = 'err.txt'
        with open(msg_f, 'w', encoding='utf-8') as ofp:
            ofp.write('こんにちは世界？\n私はTTSです?\n')
        try:
            r = main('', '--file', msg_f,
                     '--dest', 'Chinese (Mandarin/China)',
                     '--outfile', out_f,
                     '--errfile', err_f)
            self.assertTrue(r == 0)
            with open(out_f, encoding='utf8') as ifp:
                out = ifp.read()
                # print(out)
                self.assertTrue(out in ('你好，世界？ 我是TTS吗？ ',
                                        '你好世界？  是tts吗？ '))
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
