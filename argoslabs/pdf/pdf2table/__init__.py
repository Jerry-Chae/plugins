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


################################################################################
@func_log
def pdf2doc(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    if argspec.table:
        pdffile = argspec.table
    else:
        pdffile = argspec.text
    try:
        out_extension = os.path.splitext(argspec.output)[1]
        with pdfplumber.open(pdffile) as pdf, open(argspec.output, 'w',
                                                   encoding=argspec.encoding,
                                                   newline="") as out:
            if out_extension == '.csv':
                r_csv = csv.reader(out)
                t_csv = csv.writer(out)
            else:
                text = str()
            pages = pdf.pages
            if argspec.text:    # text로 pdf 파일을 열었으면 이부분이 끝
                if argspec.page:    # page 선택할 수 있는 기능 추가
                    text = pages[argspec.page-1].extract_text()
                else:
                    for i, page in enumerate(pages):
                        text += page.extract_text()

                out.write(text)
            else:
                count = 0   # pdf파일에 table값이 있는지 없는지 체크하는 함수

                if argspec.page:    # page 지정할경우 table index 값도 지정해야함
                    tables = pages[argspec.page-1].extract_tables(table_settings=
                                                                  {"vertical_strategy": argspec.vertical,
                                                                   "horizontal_strategy": argspec.horizontal,
                                                                   })
                    if tables:
                        count += 1
                    if argspec.table_index == 0:    # table_index값이 0인경우 테이블 모두를 가져옴(default)
                        for table in tables:
                            if out_extension == '.csv':
                                t_csv.writerows(table)
                            else:
                                for r_table in table:
                                    out.write(','.join(i if i else '' for i in r_table) + '\n')
                    else:
                        if out_extension == '.csv':
                            t_csv.writerows(tables[argspec.table_index-1])
                            count += 1
                        else:
                            for r_table in tables[argspec.table_index-1]:
                                out.write(','.join(i if i else '' for i in r_table) + '\n')

                else:
                    for page in pages:
                        tables = page.extract_tables(table_settings=
                                                     {"vertical_strategy": argspec.vertical,
                                                      "horizontal_strategy": argspec.horizontal,
                                                      })
                        for table in tables:
                            if out_extension == '.csv':
                                t_csv.writerows(table)
                                # t_csv.writerow('\n'*2)
                                count += 1
                            else:
                                for r_table in table:
                                    out.write(','.join(i if i else '' for i in r_table) + '\n')
                                    count += 1
                                # out.write('\n'*4)
                if count == 0:
                    msg = ('The table is not included in "%s"' % os.path.basename(argspec.table))
                    raise TableError(msg)
            pdf.close()
            out.close()

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
        pdf.close()
        out.close()
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
        mcxt.add_argument('--vertical',
                          display_name='Vertical strategy', default="lines",
                          choices=["lines", "lines_strict", "text", "explicit"],
                          input_group='Table option',
                          help='for more information refer to the help page')
        mcxt.add_argument('--horizontal',
                          display_name='Horizontal strategy', default="lines",
                          choices=["lines", "lines_strict", "text", "explicit"],
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
