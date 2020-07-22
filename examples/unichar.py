from unilyze import Unichar
from pprint import pprint

uc = Unichar()

raw_info = uc.ucd_info_raw("J")
pprint(raw_info, compact=True)
print()

info = uc.ucd_info("J")
pprint(info)
