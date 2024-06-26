from plano import *
from plano.github import *
from transom.planocommands import *

import collections
import commands
import resources

@command
def generate():
    commands.generate()
    resources.generate()

@command
def clean():
    remove(find(".", "__pycache__"))
