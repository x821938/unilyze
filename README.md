# Unilyze: Get detailed unicode information

This module helps you getting very detailed unicode information about characters.
It's simple to use, and presents data from unicode.org in a very easy readable and usable way.

First we import the `Unilyze` lib:
```
>> from unilyze import Unichar
>> from pprint import pprint
```
Now we can create an Unichar instance and use it:
```
>> uc = Unichar()
>> info = uc.info("ö")
>> pprint(info)

{'ASCII_Hex_Digit': False,
 'Age': 'V1_1',
 'Alphabetic': True,
 'Bidi_Class': 'Left_To_Right',
 'Bidi_Control': False,
 'Bidi_Mirrored': False,
 'Bidi_Mirroring_Glyph': '',
 'Bidi_Paired_Bracket': '',
 'Bidi_Paired_Bracket_Type': 'None',
 'Block': 'Latin_1_Supplement',
 'Canonical_Combining_Class': 'Not_Reordered',
 'Case_Folding': [],
 'Case_Ignorable': False,
 'Cased': True,
 'Changes_When_Casefolded': False,
 'Changes_When_Casemapped': True,
 'Changes_When_Lowercased': False,
 'Changes_When_NFKC_Casefolded': False,
 'Changes_When_Titlecased': True,
 'Changes_When_Uppercased': True,
 'Composition_Exclusion': False,
 'Dash': False,
 'Decomposition_Mapping': ['o', '̈'],
 'Decomposition_Type': 'Canonical',
 'Default_Ignorable_Code_Point': False,
 'Deprecated': False,
 'Diacritic': False,
 'East_Asian_Width': 'Neutral',
 'Emoji': False,
 'Emoji_Component': False,
 'Emoji_Modifier': False,
 'Emoji_Modifier_Base': False,
 'Emoji_Presentation': False,
 'Expands_On_NFC': False,
 'Expands_On_NFD': True,
 'Expands_On_NFKC': False,
 'Expands_On_NFKD': True,
 'Extended_Pictographic': False,
 'Extender': False,
 'FC_NFKC_Closure': [],
 'Full_Composition_Exclusion': False,
 'General_Category': 'Lowercase_Letter',
 'Grapheme_Base': True,
 'Grapheme_Cluster_Break': 'Other',
 'Grapheme_Extend': False,
 'Grapheme_Link': False,
 'Hangul_Syllable_Type': 'Not_Applicable',
 'Hex_Digit': False,
 'Hyphen': False,
 'IDS_Binary_Operator': False,
 'IDS_Trinary_Operator': False,
 'ID_Continue': True,
 'ID_Start': True,
 'ISO_Comment': '',
 'Ideographic': False,
 'Indic_Positional_Category': 'NA',
 'Indic_Syllabic_Category': 'Other',
 'Jamo_Short_Name': '',
 'Join_Control': False,
 'Joining_Group': 'No_Joining_Group',
 'Joining_Type': 'Non_Joining',
 'Line_Break': 'Alphabetic',
 'Logical_Order_Exception': False,
 'Lowercase': True,
 'Lowercase_Mapping': [],
 'Math': False,
 'NFC_Quick_Check': 'Yes',
 'NFD_Quick_Check': False,
 'NFKC_Casefold': [],
 'NFKC_Quick_Check': 'Yes',
 'NFKD_Quick_Check': False,
 'Name': 'LATIN SMALL LETTER O WITH DIAERESIS',
 'Noncharacter_Code_Point': False,
 'Numeric_Type': 'None',
 'Numeric_Value': 'NaN',
 'Other_Alphabetic': False,
 'Other_Default_Ignorable_Code_Point': False,
 'Other_Grapheme_Extend': False,
 'Other_ID_Continue': False,
 'Other_ID_Start': False,
 'Other_Lowercase': False,
 'Other_Math': False,
 'Other_Uppercase': False,
 'Pattern_Syntax': False,
 'Pattern_White_Space': False,
 'Prepended_Concatenation_Mark': False,
 'Quotation_Mark': False,
 'Radical': False,
 'Regional_Indicator': False,
 'Script': 'Latin',
 'Script_Extensions': ['Latin'],
 'Sentence_Break': 'Lower',
 'Sentence_Terminal': False,
 'Simple_Case_Folding': '',
 'Simple_Lowercase_Mapping': '',
 'Simple_Titlecase_Mapping': 'Ö',
 'Simple_Uppercase_Mapping': 'Ö',
 'Soft_Dotted': False,
 'Terminal_Punctuation': False,
 'Titlecase_Mapping': ['Ö'],
 'Unicode_1_Name': 'LATIN SMALL LETTER O DIAERESIS',
 'Unified_Ideograph': False,
 'Uppercase': False,
 'Uppercase_Mapping': ['Ö'],
 'Variation_Selector': False,
 'Vertical_Orientation': 'Rotated',
 'White_Space': False,
 'Word_Break': 'ALetter',
 'XID_Continue': True,
 'XID_Start': True}
```
You can also get the raw-data like this:
```
raw_info = uc.raw_info("ö")
```
All the data is bases on Unicode version 13 definition files from www.unicode.org 
You should only create one instance of Unichar, because it loads 60Mb of data into memory. It not only uses a lot of memory, it also takes some time (a second or so)

Have fun

/ Alex Skov Jensen