# Unicode character usage
```
from unilyze.unichar import Unichar
from pprint import pprint

uc = Unichar()
info = uc.lng_usage("å")
pprint(info)
```
**Output:**
```
{'auxiliary': ['Afrikaans',
               'Asturian',
               'Breton',
               'Catalan',
               'Czech',
               'Welsh',
               'German',
               'Lower Sorbian',
               'Ewe',
               'English',
               'English : South Africa',
               'Spanish',
               'Estonian',
               'Basque',
               'French',
               'French : Canada',
               'Friulian',
               'Irish',
               'Scottish Gaelic',
               'Galician',
               'Swiss German',
               'Upper Sorbian',
               'Hungarian',
               'Indonesian',
               'Italian',
               'Kabuverdianu',
               'Kurdish',
               'Luxembourgish',
               'Dutch',
               'Polish',
               'Portuguese',
               'Quechua',
               'Romansh',
               'Romanian',
               'Northern Sami',
               'Slovak',
               'Slovenian',
               'Inari Sami',
               'Serbian',
               'Tongan',
               'Turkish',
               'Walser',
               'Zulu'],
 'main': ['Danish',
          'Finnish',
          'Javanese',
          'Kalaallisut',
          'Colognian',
          'Norwegian Bokmål',
          'Low German',
          'Norwegian Nynorsk',
          'Swedish']}
```
# Unicode character usage RAW
```
info = uc.lng_usage_raw("å")
pprint(info, compact=True)
```
**Output:**
```
{'auxiliary': ['af', 'ast', 'br', 'ca', 'cs', 'cy', 'de', 'dsb', 'ee', 'en',
               'en_ZA', 'es', 'et', 'eu', 'fr', 'fr_CA', 'fur', 'ga', 'gd',
               'gl', 'gsw', 'hsb', 'hu', 'id', 'it', 'kea', 'ku', 'lb', 'nl',
               'pl', 'pt', 'qu', 'rm', 'ro', 'se', 'sk', 'sl', 'smn', 'sr',
               'to', 'tr', 'wae', 'zu'],
 'main': ['da', 'fi', 'jv', 'kl', 'ksh', 'nb', 'nds', 'nn', 'sv']}
```