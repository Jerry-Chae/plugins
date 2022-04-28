"""
====================================
 :mod:`argoslabs.python.dynamic`
====================================
.. moduleauthor:: Jerry Chae <mcchae@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
ARGOS LABS plugin module for running python script with requirements.txt
"""
#
# Authors
# ===========
# * Jerry Chae
#
# Change Log
# --------
#
#  * [2022/02/05]
#     - add --python-exe
#  * [2021/07/01]
#     - ASJ의 pywinauto 모듈이 안되는 문제 때문에 exec(py_script, locals(), locals()) 로 수정
#  * [2021/03/30]
#     - starting

################################################################################
import os
import sys
# import pip
import types
import tempfile
import traceback
import subprocess
from tempfile import gettempdir
from alabs.common.util.vvargs import ModuleContext, func_log, \
    ArgsError, ArgsExit, get_icon_path


###############################################################################
def _pip_install(pip_cmd, stdout):
    if sys.platform == 'win32':
        import pathlib
        executable = str(pathlib.PureWindowsPath(sys.executable))
    else:
        executable = sys.executable
    cmd = [
        executable,
        '-m',
        'pip',
    ]
    cmd.extend(pip_cmd)
    po = subprocess.Popen(cmd, stdout=stdout)
    po.wait()
    return po.returncode


################################################################################
def pip_install(reqtxt, encoding='utf-8'):
    org_stdout = sys.stdout
    try:
        stdout_f = os.path.join(gettempdir(), 'requirements.out')
        with open(stdout_f, 'w', encoding=encoding) as stdout:
            sys.stdout = stdout
            cmd = ['install', '-r', reqtxt]
            # r = pip.main(cmd)
            r = _pip_install(cmd, stdout)
            if r != 0:
                raise RuntimeError(f'pip install with "{reqtxt}" failure!')
            return r
    finally:
        sys.stdout = org_stdout


################################################################################
def exec_script(pys, py_exe=sys.executable, encoding='utf-8'):
    pyf = os.path.join(tempfile._get_default_tempdir(),
                       next(tempfile._get_candidate_names()) + '.py')
    try:
        with open(pyf, 'w', encoding=encoding) as ofp:
            ofp.write(pys)
        cmd = [
            py_exe,
            pyf
        ]
        po = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        po.wait()
        sys.stdout.write(po.stdout.read().decode())
        sys.stderr.write(po.stderr.read().decode())
        return po.returncode
    finally:
        if os.path.exists(pyf):
            os.remove(pyf)

################################################################################
@func_log
def do_dynamic_script(mcxt, argspec):
    mcxt.logger.info('>>>starting...')
    try:
        if not (argspec.script and os.path.exists(argspec.script)):
            raise IOError(f'Cannot read python script file "{argspec.script}"')
        if argspec.reqtxt and argspec.python_exe:
            raise IOError(f'Cannot install "{argspec.reqtxt}" because specific '
                          f'"{argspec.python_exe}" need to install for that environment')
        if argspec.reqtxt and os.path.exists(argspec.reqtxt):
            pip_install(argspec.reqtxt, encoding=argspec.encoding)
        with open(argspec.script, encoding=argspec.encoding) as ifp:
            py_script = ifp.read()
        params = {}
        if argspec.params:
            for pl in argspec.params:
                k, v = pl.split('::=', maxsplit=1)
                params[k] = v
        if params:
            py_script = py_script.format(**params)
        if argspec.python_exe:
            if not os.path.exists(argspec.python_exe):
                raise IOError(f'Cannot find Python exe from "{argspec.python_exe}"')
            return exec_script(py_script, py_exe=argspec.python_exe, encoding=argspec.encoding)
        try:
            # exec(py_script, globals(), locals())
            exec(py_script, locals(), locals())
            globals().update(locals())
        except NameError:
            return exec_script(py_script, encoding=argspec.encoding)
        return 0
    except Exception as e:
        _exc_info = sys.exc_info()
        _out = traceback.format_exception(*_exc_info)
        del _exc_info
        msg = '%s\n' % ''.join(_out)
        mcxt.logger.error(msg)
        msg = 'Error: %s' % str(e)
        mcxt.logger.error(msg)
        sys.stderr.write(msg)
        return 99
    finally:
        mcxt.logger.info('>>>end...')


################################################################################
def _main(*args):
    """
    Build user argument and options and call plugin job function
    :param args: user arguments
    :return: return value from plugin job function
    """
    try:
        with ModuleContext(
            owner='ARGOS-LABS',
            group='9',  # Utility Tools
            version='1.0',
            platform=['windows', 'darwin', 'linux'],
            output_type='text',
            display_name='Dynamic Python',
            icon_path=get_icon_path(__file__),
            description='Execute dynamic python script with 3-rd party modules',
        ) as mcxt:
            # ##################################### for app dependent parameters
            mcxt.add_argument('script',
                              display_name='Python Script',
                              input_method='fileread',
                              help='Python script to execute')
            # ##################################### for app dependent options
            mcxt.add_argument('--reqtxt',
                              display_name='Req Text',
                              input_method='fileread',
                              help='Depenent Python module description file usually "requirements.txt"')
            mcxt.add_argument('--params',
                              display_name='Parameters',
                              action='append',
                              help='Parameters for script, key::=value format')
            mcxt.add_argument('--encoding',
                              display_name='Encoding', default='utf-8',
                              help='Encoding for script and requirements file, default is [[utf-8]]')
            mcxt.add_argument('--python-exe',
                              display_name='Python Exe',
                              input_method='fileread',
                              help='Specify Python executable.')
            argspec = mcxt.parse_args(args)
            return do_dynamic_script(mcxt, argspec)
    except Exception as e:
        sys.stderr.write(f'Error: {str(e)}')
        return 98


################################################################################
def main(*args):
    try:
        return _main(*args)
    except ArgsError as err:
        sys.stderr.write('Error: %s\nPlease -h to print help\n' % str(err))
    except ArgsExit as _:
        pass
