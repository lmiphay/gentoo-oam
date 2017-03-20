# -*- coding: utf-8 -*-

from __future__ import print_function

import invoke

from oam.logdest import logdest

class Context(invoke.Context):

    def __init__(self, config=None):
        super(Context, self).__init__(config)

    def run(self, command, **kwargs):
        oamlog_write(command)
        print('in oaminvoke.Context run')
        kwargs['out_stream'], kwargs['err_stream'] = logdest(command)
        runner_class = self.config.get('runner', invoke.Local)
        return runner_class(context=self).run(command, **kwargs)
