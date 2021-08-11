#!/usr/bin/env python
# coding=utf8
"""
====================================
 :mod:`argoslabs.data.pdf2txt`
====================================
.. moduleauthor:: Kyobong An <akb0930e@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS PDF Conversion(pdf -> txt) plugin
"""
# Authors
# ===========
#
# * Kyobong An
#
# --------
#
#  * [2021/08/11]
#   TEXT를 사용할때 None타입 에러가 발생해서 try Except 사용해서 에러해결
#  * [2021/07/28]
#   기능추가 separator, code 수정
#  * [2021/07/28]
#     - starting

################################################################################
import os
import sys
import csv
import pdfplumber

from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


################################################################################
class TableError(Exception):
    pass


class Pdf2table(object):
    def __init__(self, argspec, pdffile):
        self.pdffile = pdffile
        self.pdf = pdfplumber.open(self.pdffile)
        self.page = argspec.page
        self.t_index = argspec.table_index
        self.vertical = argspec.vertical
        self.horizontal = argspec.horizontal
        self.encoding = argspec.encoding
        self.outfile = self.outfile(argspec.output, self.encoding)
        self.out_extension = os.path.splitext(argspec.output)[1]
        if self.out_extension == '.csv':
            self.output = csv.writer(self.outfile)  # csv형태로 내보낼때 사용
        else:
            self.output = str()     # Txet open 할때
        self.pages = self.pdf.pages
        self.tables = None
        self.sep = argspec.separator
        self.count = 0  # 페이지의 테이블이 있는지 없는지 체크하는 함수

    @staticmethod
    def outfile(outfile, encoding):
        out = open(outfile, 'w', encoding=encoding, newline="")
        return out

    def get_text(self):
        if self.page:  # page 선택할 수 있는 기능 추가
            self.output = self.pages[self.page - 1].extract_text()
        else:
            for page in self.pages:
                # self.output += page.extract_text()
                try:
                    self.output += page.extract_text()
                except:
                    ...
        self.outfile.write(self.output)
        self.count = 1

    def get_table(self, page=None):
        if self.page:
            self.tables = self.pages[self.page - 1].extract_tables(table_settings={"vertical_strategy": self.vertical,
                                                                                   "horizontal_strategy": self.horizontal,
                                                                                   })
            if self.tables:
                self.count += 1
        else:   # 페이지가 없는 경우 각각의 페이지에서 테이블을 가져오기위해서 page를 매개변수로 가져와 사용함
            self.tables = page.extract_tables(table_settings={"vertical_strategy": self.vertical,
                                                              "horizontal_strategy": self.horizontal,
                                                              })
            if self.tables:
                self.count += 1

    def get_outfile(self):
        if self.out_extension == '.csv':
            if self.t_index == 0:
                for table in self.tables:
                    self.output.writerows(table)
            else:
                self.output.writerows(self.tables[self.t_index - 1])
        else:
            if self.t_index == 0:
                for table in self.tables:
                    for r_table in table:
                        self.outfile.write(self.sep.join(i if i else '' for i in r_table) + '\n')
            else:
                for r_table in self.tables[self.t_index - 1]:
                    self.outfile.write(self.sep.join(i if i else '' for i in r_table) + '\n')

    def close(self):
        self.pdf.close()
        self.pdf = None
        self.outfile.close()
        self.outfile = None
        self.output = None


################################################################################
@func_log
def pdf2doc(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    if argspec.table:
        pdffile = argspec.table
    else:
        pdffile = argspec.text
    try:
        p2t = Pdf2table(argspec, pdffile)
        if argspec.text:    # text로 PDF파일을 열었을때
            p2t.get_text()
        else:   # Table을 찾을때
            if p2t.page:
                p2t.get_table()     # 페이지가 있을 때는 매개변수를 사용안함
                p2t.get_outfile()
            else:
                for page in p2t.pages:
                    p2t.get_table(page)     # 각각의 페이지에서 테이블을 담아와야함.
                    p2t.get_outfile()
        if p2t.count == 0:  # 페이지의 함수가 없는 경우 초기에 지정했던 0이 나옴
            msg = ('The table is not included in "%s"' % os.path.basename(pdffile))
            raise TableError(msg)

        p2t.close()

        print(os.path.abspath(argspec.output), end='')
        return 0
    except TableError as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 9
    finally:
        sys.stdout.flush()
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    with ModuleContext(
            owner='ARGOS-LABS',
            group='2',
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='PDF2Table',
            icon_path=get_icon_path(__file__),
            description='Converting from pdf file to text file',
    ) as mcxt:
        # ##################################### for app dependent options
        # ----------------------------------------------------------------------
        mcxt.add_argument('--table',
                          display_name='Table', show_default=True,
                          input_method='fileread',
                          input_group='radio=PDF File;default',
                          help='Select a pdf file for table')
        mcxt.add_argument('--text',
                          display_name='Text', show_default=True,
                          input_method='fileread',
                          input_group='radio=PDF File',
                          help='Select a pdf file for text')
        mcxt.add_argument('--output', display_name='Output Filepath', show_default=True,
                          input_method='filewrite',
                          help='Specify an absolute file path to save the output')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--page',
                          display_name='Page', type=int,
                          input_group='Table and Text option',
                          help='PDF page')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--table-index',
                          display_name='Table index', type=int, default=0,
                          input_group='Table option',
                          help='table index')
        mcxt.add_argument('--separator',
                          display_name='Separator', default=',',
                          input_group='Table option',
                          help='please enter a separator which will be inserted between words in exported .txt file')
        mcxt.add_argument('--vertical',
                          display_name='Vertical strategy', default="lines",
                          choices=["lines", "lines_strict", "text"],
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--horizontal',
                          display_name='Horizontal strategy', default="lines",
                          choices=["lines", "lines_strict", "text"],
                          input_group='Table option',
                          help='for more information refer to the help page')
        # ----------------------------------------------------------------------
        mcxt.add_argument('--encoding',
                          display_name='Encoding', default='utf-8',
                          help='Encoding for OutPut file')
        argspec = mcxt.parse_args(args)
        return pdf2doc(mcxt, argspec)
        # ##################################### for app dependent parameters


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
