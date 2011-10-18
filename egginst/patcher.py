from __future__ import with_statement

from contextlib import closing
from os.path import abspath, exists, join
import shutil
import sys
import tarfile
import tempfile

from egginst.main import EggInst
from egginst import scripts
from egginst import object_code
from egginst.patch_ui import PatcherApp

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
    tmp_dir = tempfile.mkdtemp()

    t = tarfile.open(sys.argv[1], 'r:*')
    t.extractall(path=tmp_dir)
    t.close()

    platform_dir = join(tmp_dir, sys.platform)
    patches = []
    with open(join(platform_dir, 'dists.txt')) as fp:
        for line in fp:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            patches.append(join(platform_dir, line))
    
    # Start up a nice looking Qt GUI for feedback during the patching process
    app = PatcherApp(patches=patches,
                     patch_fn=insert_egg,
                     translation_file=sys.argv[2])
    app.exec_()

    shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == '__main__':
    main()
