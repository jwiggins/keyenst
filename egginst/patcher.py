from contextlib import closing
from os.path import abspath, exists, join
import sys
import tarfile
import tempfile

from main import EggInst
import scripts
import object_code

if sys.platform == 'darwin':
    scripts.executable = '../MacOS/python'

prefix = abspath(sys.prefix)

tmp_dir = tempfile.mkdtemp()


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

def patch_is_valid(patch_path):
    """
    Check the file to see if it is a valid patch file.
    """
    try:
        with closing(tarfile.open(patch_path, "r:*")) as tf:
            # Check for the info.txt file
            tinfo = tf.getmember('info.txt')
    except:
        # All exceptions imply an invalid patch file
        return False
    
    return True


def main():
    t = tarfile.open(sys.argv[1], 'r:*')
    t.extractall(path=tmp_dir)
    t.close()

    platform_dir = join(tmp_dir, sys.platform)
    for line in open(join(platform_dir, 'dists.txt')):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        insert_egg(join(platform_dir, line))

    print 'Done.'


if __name__ == '__main__':
    main()
