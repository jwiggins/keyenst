import sys
from subprocess import Popen, PIPE
from os.path import abspath, dirname, join


log_path = abspath(join(sys.prefix, 'patcher.log'))


def main():
    import egginst

    cmd = [sys.executable,
           join(dirname(egginst.__file__), 'patcher.py')] + sys.argv[1:]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    tmp = p.communicate()

    fo = open(log_path, 'w')
    fo.write('STDOUT:\n' + tmp[0] + '\n\n')
    fo.write('STDERR:\n' + tmp[1] + '\n\n')
    fo.close()


if __name__ == '__main__':
    main()
