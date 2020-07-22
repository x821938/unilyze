# Unilyze: Get detailed unicode information

## Unichar Class
This module helps you getting very detailed unicode information about single characters.
It's simple to use, and presents data from unicode.org in a very easy readable and usable way.

First we import the `Unilyze` lib:
```
>> from unilyze import Unichar
>> from pprint import pprint
```
Now we can create an Unichar instance and use it:
```
>> uc = Unichar()
>> info = uc.info("a")
>> pprint(info)

{'ASCII_Hex_Digit': False,
 'Age': 'V1_1',
 'Alphabetic': True ...}
```
This will make a huge dict of attributes of the character. **See [FULL OUTPUT](docs/unichar_info.md)**
You can also get the raw-data like this:
```
raw_info = uc.raw_info("J")
```
You can also find out in what languages a unicode character is used:
```
>> info = uc.lng_usage("å")
>> pprint(info)

{'main': ['Danish',
          'Finnish',
          'Javanese',
          'Kalaallisut',...
}
```
Here you will get a huge dict with countries. **See [FULL OUTPUT](docs/unichar_usage.md)**
## Unistat Class

This class is used to get statistics of strings instead of single characters. It's used for summing op
information of each single character in the string.

```
>> from unilyze.unistat import Unistat
>> from pprint import pprint

>> us = Unistat()
>> us.add_text("This is a small test! 123")

>> unistat = us.unistat()
>> pprint(unistat, compact=True)

{'ASCII_Hex_Digit': {True: {'chars': {'1', '3', 'a', '2', 'e'},
                            'total-count': 6}},
 'Age': {'V1_1': {'chars': {' ', '!', '1', '2', '3', 'T', 'a', 'e', 'h', 'i',   
                            'l', 'm', 's', 't'},
                  'total-count': 25}},.........
```
Again we get a huge output grouped on UCD properties, and a count of the characters. 
**See [FULL OUTPUT](docs/unistat_info.md)**

A simple count of each character can be done like this:
```
>> charstat = us.charstat()
>> print(charstat)

{'T': 1, 'h': 1, 'i': 2, 's': 4, ' ': 5, 'a': 2, 'm': 1, 'l': 2, 't': 2, 'e': 1, '!': 1, '1': 1, '2': 1, '3': 1}
```

## Final notes
All the data is bases on Unicode version 13 definition files from www.unicode.org 
You should only create one instance of Unichar or Unistat, because it loads 60Mb of data into memory. 
It not only uses a lot of memory, it also takes some time (a second or so)

Have fun

/ Alex Skov Jensen