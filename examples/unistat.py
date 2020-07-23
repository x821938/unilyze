from unilyze import Unistat
from pprint import pprint

# Create an Unistat instance and add some text for analysis
us = Unistat()
us.add_text("This is a small test! 123")

# Print the detailed statistics of UCD properties of the text. Eg: the usage of lower, upper etc.
unistat = us.unistat()
pprint(unistat, compact=True, width=150)
print()

# Print the occurrences of single characters in the text
charstat = us.charstat()
print(charstat)
