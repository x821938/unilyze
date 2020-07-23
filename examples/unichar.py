from unilyze import Unichar
from pprint import pprint

uc = Unichar()

# Get unicode information af a character with english attributes
info = uc.ucd_info("J")
pprint(info)

# Get RAW and not so readable unicode information of a character
raw_info = uc.ucd_info_short("J")
pprint(raw_info, compact=True)
print()
