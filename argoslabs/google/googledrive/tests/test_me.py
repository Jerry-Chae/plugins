#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.google.googledrive`
====================================
.. moduleauthor:: Irene Cho <irene@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module : unittest
"""
################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.google.googledrive import _main as main
from alabs.common.util.vvargs import ArgsError


################################################################################
class TU(TestCase):

    # ==========================================================================
    @classmethod
    def setUpClass(cls) -> None:
        os.chdir(os.path.dirname(__file__))

    # ==========================================================================
    def tearDown(self) -> None:
        ...

    # ==========================================================================
    def test0050_failure(self):
        try:
            _ = main('invalid')
            self.assertTrue(False)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0100_token(self):
        try:
            r = main('Recently Modified',
                     'token.pickle')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    # def test0110_credentials(self):
    #     try:
    #         r = main('File List','--credentials','credit.json' )
    #         self.assertTrue(r == 0)
    #     except ArgsError as e:
    #         sys.stderr.write('\n%s\n' % str(e))
    #         self.assertTrue(False)

    # ==========================================================================
    def test0120_download_imagefile(self):
        try:
            r = main('Download a File',
                     'token.pickle',
                     '--fileid', '1dHf8VCub6sWwhPY5g-6zYM_AJCmwazXR',
                     '--filetype', 'File in Google Drive',
                     '--filepath', 'test1.png')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0130_create_folder(self):
        try:
            r = main('Create a Folder', 'token.pickle',
                     '--foldername', 'Test_Folder1')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0140_upload_files(self):
        try:
            r = main('Upload a File', 'token.pickle',
                     '--filepath',
                     'diamond.csv')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0150_upload_files_in_folder(self):
        try:
            r = main('Upload a File', 'token.pickle',
                     '--folderid', '1wrUXoE3nClICWzKgB5Ivvb2kjlxh1mOB    '
                                   '',
                     '--filepath', 'zoom1.png')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0160_download_csvfile(self):
        try:
            r = main('Download a File', 'token.pickle',
                     '--fileid', '14WWhxCg5QUf4FbctOLp--Q9At-IHcLdO7a3mpdFQPsg',
                     '--filetype', 'G Suite Files',
                     '--filepath', 'diamond.csv', '--mimeType',
                     'application/vnd.openxmlformats-officedocument'
                     '.spreadsheetml.sheet')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0170_search(self):
        try:
            r = main('Search', 'token.pickle')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0190_sharefiles(self):
        try:
            r = main('Share File/Folder', 'token.pickle', '--usertype',
                     'anyone',
                     '--role', 'reader', '--fileid',
                     '1mrmdCCwVkXbalbhdw3ucRwXB_GLMWE33', )
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0200_missing_files_sharefiles(self):
        try:
            r = main('Share File/Folder', 'token.pickle', '--usertype', 'user',
                     '--role', 'reader', '--address',
                     'ireneeeee@argos-labs.com')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0210_missing_address_sharefiles(self):
        try:
            r = main('Share File/Folder', 'token.pickle',
                     '--usertype', 'user',
                     '--role', 'reader',
                     '--folderid', '1axUo2maEct-3KZMQ7sDSMHgFltsbjYCH')
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0220_token_pagesize(self):
        try:
            r = main('Recently Modified', 'token.pickle', '--pagesize', '11')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0230_download_png(self):
        try:
            r = main('Download a File', 'token.pickle',
                     '--fileid', '1dHf8VCub6sWwhPY5g-6zYM_AJCmwazXR',
                     '--filetype', 'File in Google Drive',
                     '--filepath', os.getcwd())
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0240_sharefiles(self):

        try:
            r = main('Share File/Folder', 'token.pickle', '--usertype', 'user',
                     '--role', 'reader', '--folderid',
                     '1QjDb8sk2pNwKJq07lJaC3OXwvyyQhJSM',
                     '--address', 'irenessssss@argos-labs.com')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0250_search(self):
        try:
            r = main('Search', 'token.pickle', '--query',
                     "mimeType='image/png' and parents in "
                     "'1SuayxSlMNF_sTVAhQT6Md23uhvGHfLkg'")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0260_search(self):
        try:
            r = main('Search', 'token.pickle', '--query',
                     "name = 'hello'")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0270_filelist_folder(self):
        try:
            r = main('Recently Modified',
                     'token.pickle', '--folderid',
                     '1jXiHNM0zNiuJOOsmQVNCzM1Dk9QBak1t', '--pagesize', '3')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0280_search_in_folder(self):
        try:
            r = main('Search', 'token.pickle', '--folderid',
                     '1SuayxSlMNF_sTVAhQT6Md23uhvGHfLkg',
                     '--query', "name != 'hello'")
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0290_filelist_pagesize(self):
        try:
            r = main('Recently Modified',
                     'token.pickle', '--pagesize', '3')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0300_search(self):
        try:
            r = main('Recently Modified', 'token.pickle')
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0310_download_gsuite_wrong_option(self):
        try:
            r = main('Download a File', 'token.pickle',
                     '--fileid', '1ZDHvls6Yg0yOUxV0SbVKWyOYsgX5PWZm96KoAg9Jc5U',
                     '--filetype', 'File in Google Drive',
                     '--filepath', os.getcwd())
            self.assertTrue(r != 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

    # ==========================================================================
    def test0320_download_gsuite(self):
        try:
            r = main('Download a File', 'token.pickle',
                     '--fileid', '1ZDHvls6Yg0yOUxV0SbVKWyOYsgX5PWZm96KoAg9Jc5U',
                     '--filetype', 'G Suite Files','--mimeType','text/plain',
                     '--filepath', os.getcwd())
            self.assertTrue(r == 0)
        except ArgsError as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(False)

