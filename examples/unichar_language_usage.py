from unilyze import Unichar
from pprint import pprint

uc = Unichar()

# Get a list of languages where a character is used
info = uc.lng_usage("å")
pprint(info)
print()

# Get the same list, but with short language names like "en_GB"
info = uc.lng_usage_short("å")
pprint(info, compact=True)
print()

# Look up a short name
print(uc.lng_name_lookup("zu"))
print()

# Check if a character is used in a specific language:
used = uc.in_lng("å", "da")
print(used)
