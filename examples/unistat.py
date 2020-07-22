from unilyze import Unistat
from pprint import pprint

us = Unistat()
us.add_text("This is a small test! 123")

unistat = us.unistat()
pprint(unistat, compact=True, width=150)
print()

charstat = us.charstat()
print(charstat)
