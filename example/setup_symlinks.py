#!/usr/bin/env python
import os, os.path

path = os.path.dirname(os.path.abspath(__file__))

import feincms
feincms_path = os.path.dirname(feincms.__file__)
cmd = "ln -f -s %s/media/feincms %s/media/feincms" % (feincms_path, path, )
print cmd
os.system(cmd)

