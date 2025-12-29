"""胖块"""
import random

from loop import rules
from PlatForm.Basic_Platform import Platform


class SIPHighPlatform(Platform):
    def __init__(self):
        super().__init__(height=random.randint(30, 25 + 10 * rules.Rule.stage))

