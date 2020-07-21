from unilyze import Unichar
from pprint import pprint

uc = Unichar()

info = uc.info("ö")
pprint(info)

raw_info = uc.raw_info("ö")
pprint(raw_info)
