from myopen.subsystems import *

from .asyncio_base_command import *
from myopen.asyncio_connection import *

__all__ = ['CmdDiagAid']


class CmdDiagAid(BaseCommand):
    def start(self):
        self.log(self.params)
        return self.end()
