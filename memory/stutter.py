#!/usr/bin/env python
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: 2016 IBM
# Author:Praveen K Pandey <praveen@linux.vnet.ibm.com>
#


import os

from avocado import Test
from avocado import main
from avocado.utils import process, archive, memory, build
from avocado.utils.software_manager import SoftwareManager


class Stutter(Test):

    """
    stutter benchmark

    :avocado: tags=memory,privileged
    """

    def setUp(self):
        '''
        Build Stutter Test
        Source:
        https://github.com/gaowanlong/stutter/archive/master.zip
        '''

        # Check for basic utilities
        smm = SoftwareManager()
        if not smm.check_installed("gcc") and not smm.install("gcc"):
            self.error('Gcc is needed for the test to be run')

        locations = ["https://github.com/gaowanlong/stutter/archive/"
                     "master.zip"]
        tarball = self.fetch_asset("stutter.zip", locations=locations,
                                   expire='7d')
        archive.extract(tarball, self.srcdir)
        self.sourcedir = os.path.join(self.srcdir, 'stutter-master')

        mem_byte = str(memory.memtotal())
        print mem_byte
        self._memory = self.params.get('memory', default=mem_byte)
        self._iteration = self.params.get('iteration', default='10')
        self._logdir = self.params.get('logdir', default='/var/tmp/logdir')
        self._rundir = self.params.get('rundir', default='/tmp')

        process.run('mkdir -p  %s' % self._logdir)

        # export env variable, used by test script
        os.environ['MEMTOTAL_BYTES'] = self._memory
        os.environ['ITERATIONS'] = self._iteration
        os.environ['LOGDIR_RESULTS'] = self._logdir
        os.environ['TESTDISK_DIR'] = self._rundir

        build.make(self.sourcedir)

    def test(self):

        os.chdir(self.sourcedir)
        if process.system('./run.sh', shell=True, ignore_status=True) != 0:
            self.fail("Test failed")


if __name__ == "__main__":
    main()
