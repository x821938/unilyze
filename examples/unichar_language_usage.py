from unilyze import Unichar
from pprint import pprint

uc = Unichar()
info = uc.lng_usage("å")
pprint(info)
print()

info = uc.lng_usage_raw("å")
pprint(info, compact=True)
print()

print(uc.lng_name_lookup("zu"))

