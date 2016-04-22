__title__ = 'oam'
from .version import __version__
__author__ = 'Paul Healy'
__license__ = 'GPL-2'
__copyright__ = 'Copyright 2016, Paul Healy under GPL-2'

#from oam.eventparser import EventParser
from oam.registry import Registry

from oam.cmd import cli
from oam.dumpenv import dumpenv
from oam.listcmds import listcmds
from oam.listopts import listopts
from oam.version import version, get_version
from oam.watch import watch

from oam.changed import Changed, changed
from oam.checkconfig import CheckConfig, checkconfig
from oam.createlxc import CreateLxc, createlxc
from oam.direct import Direct, direct
from oam.emergelog import EmergeLog, emergelog
from oam.fabremote import FabRemote, fabremote
from oam.daylog import DayLog, daylog, lastday
from oam.expire import OAMExpire, expire
from oam.genlop import Genlop, genlop
from oam.go import gocmd
from oam.news import News, checknews, countnewnews
from oam.obsolete import obsolete
from oam.pkg import Pkg, pkgsizes
from oam.pretend import Pretend, pretend

from oam.events import Events, events

#__all__ = ['dumpenv']
