"""
====================================
 :mod:`argoslabs.ibm.visualrecog`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module sample
"""
# Authors
# ===========
#
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2019/08/11]
#     - finish
#  * [2019/08/10]
#     - starting

################################################################################
import os
import sys
import csv
from ibm_watson import VisualRecognitionV3, ApiException
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path

################################################################################
@func_log
def do_vr(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if not argspec.apikey:
            raise IOError('Invalid API key' % argspec.apikey)
        if not os.path.exists(argspec.image):
            raise IOError('Cannot Open image file "%s"' % argspec.image)

        svc = VisualRecognitionV3(
            '2018-03-19',
            url='https://gateway.watsonplatform.net/visual-recognition/api',
            iam_apikey=argspec.apikey)
        h = ('class', 'score', 'type_hierarchy')
        with open(argspec.image, 'rb') as ifp:
            # noinspection PyTypeChecker
            response = svc.classify(ifp, threshold=str(argspec.threshold))
            if response.status_code // 10 != 20:
                raise RuntimeError('API response code is not 20? but "%s"'
                                   % response.status_code)
            # jds = json.dumps(response.result, indent=1)
            # print(jds)
            rj = response.result
            c = csv.writer(sys.stdout, lineterminator='\n')
            rjcl = rj.get('images')
            if not (rjcl and isinstance(rjcl, list)):
                raise ValueError('Invalid Result "%s"' % rj)
            rjcl = rjcl[0].get('classifiers')
            if not (rjcl and isinstance(rjcl, list)):
                raise ValueError('Invalid Result "%s"' % rj)
            rjcl = rjcl[0].get('classes')
            if not (rjcl and isinstance(rjcl, list)):
                raise ValueError('Invalid Result "%s"' % rj)
            if rjcl:
                c.writerow(h)
            for r in rjcl:
                row = []
                for hitem in h:
                    v = None
                    if hitem in r:
                        v = r[hitem]
                    row.append(v)
                c.writerow(row)
        return 0
    except Exception as err:
        msg = str(err)
        mcxt.logger.error(msg)
        sys.stderr.write('%s%s' % (msg, os.linesep))
        return 1
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    with ModuleContext(
        owner='ARGOS-LABS',
        group='ibm',
        version='1.0',
        platform=['windows', 'darwin', 'linux'],
        output_type='text',
        display_name='Visual Recognition',
        icon_path=get_icon_path(__file__),
        description='IBM Watson Visual Recognition. Refer {{https://developer.ibm.com/articles/introduction-watson-visual-recognition/}}',
    ) as mcxt:
        # ######################################## for app dependent options
        mcxt.add_argument('--threshold',
                          display_name='Score Threshold', type=float,
                          min_value=0.0, max_value=1.0,
                          default=0.0,
                          help='Suppress score value is below than this threshold. Default is [[0.0]], and 0.0~1.0')
        # ##################################### for app dependent parameters
        mcxt.add_argument('apikey',
                          display_name='API key', input_method='password',
                          help='Calendar for region')
        mcxt.add_argument('image',
                          display_name='Image file', input_method='fileread',
                          help='Image file to recognize')
        argspec = mcxt.parse_args(args)
        return do_vr(mcxt, argspec)


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
