import sys
from os.path import abspath, basename, exists, join

from main import EggInst
import scripts
import object_code

if sys.platform == 'darwin':
    scripts.executable = '../MacOS/python'

prefix = abspath(sys.prefix)


# Monkey patch egginst.object_code.alt_replace_func, which is an
# optional function, which is applied to the replacement string.
def mk_relative(r):
    """
    As we don't want the absolute path to the library to link to in the
    headers, but rather relative path from the executable.
    """
    res = []
    for rpath in r.split(':'):
        assert (exists(rpath)  and
                rpath.startswith(prefix + '/')), rpath
        res.append('@executable_path/..' + rpath[len(prefix):])
    assert len(res) > 0, r
    return ':'.join(res)

object_code.alt_replace_func = mk_relative


def insert_egg(egg_path):
    """
    inserts an egg into the application
    """
    print "Inserting:", egg_path
    ei = EggInst(egg_path, prefix, verbose=True, noapp=True)
    ei.install()


def untar():
    pass



def main():
    pass



if __name__ == '__main__':
    main()
