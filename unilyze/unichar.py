import re
import json
from os import path
from pkg_resources import resource_string

# Location of files used for unicode lookups
CHAR_DB_FILE = "db/unicode_db.json"
PROPERTY_FILE = "db/property_names.json"
PROPERTY_VALUES_FILE = "db/property_values.json"


class Unichar:
    """A class to get unicode information from characters.
    All information is based on UCD-xml data from www.unicode.org
    Field reference at https://www.unicode.org/reports/tr42/
    """

    def __init__(self):
        """Loads the json database files into memory
        """
        self.__char_db = self.__load_json(CHAR_DB_FILE)
        self.__properties = self.__load_json(PROPERTY_FILE)
        self.__property_values = self.__load_json(PROPERTY_VALUES_FILE)
        self.__uc_single_ref = ["bmg", "bpb", "suc", "slc", "stc", "scf", "EqUIdeo"]  # codepoint references
        self.__uc_multi_ref = ["FC_NFKC", "uc", "lc", "tc", "cf", "dm", "NFKC_CF"]  # codepoint references

    def __load_json(self, filename):
        """Reads a json file from disk. It's expected to be UTF-8

        Args:
            filename (str): Filename of the file to read

        Returns:
            dict|list: The object that the json file contains
        """
        # Get datafile-content from file relative to package install dir
        raw_data = resource_string("unilyze", filename).decode("utf-8")
        return json.loads(raw_data)

    def __codepoint_reference(self, property, property_value):
        """Some of the unicode characters refers to others. Eg upper, lower versions of a codepoint.
        This method converts the XML value-format of Eg "0101 004A" into real unicode characters like "āJ"

        Args:
            property (str): The property (Eg: lc, uc - meaning lowercase and uppercase resp.)
            property_value ([type]): Eg "0101 004A" from the xml property value.

        Returns:
            (bool, str|list): First value is True if the provided UCD property is member of "self._uc_ref".
                              This means that we have done a character lookup. Otherwise first value is False.

                              Second value is the converted codepoints:
                                1) string with one unicode char if property is found in self.__uc_single_ref
                                2) list of unicode chars if property is found in self.__uc_multi_ref
        """
        if property in self.__uc_single_ref:  # Codepoint have single reference
            codepoint_hex = re.findall(r"[0-9A-F]+", property_value)
            codepoint = chr(int(codepoint_hex[0], 16)) if codepoint_hex else ""
            return True, codepoint  # Return it as a string with one unicode character

        if property in self.__uc_multi_ref:  # Codepoint have multiple references?
            codepoints_hex = re.findall(r"[0-9A-F]+", property_value)
            codepoints = []
            for codepoint_hex in codepoints_hex:
                codepoints.append(chr(int(codepoint_hex, 16)))
            return True, codepoints  # Return a list of unicode characters

        return False, None  # property does not have references

    def __property_value_lookup(self, property, property_value):
        """Takes the raw VALUE of a provided UCD property and refines it:
        "Y"/"N" is converted into True/False
        Codepoint references like "004A" is converted into "J"

        Args:
            property (str): An UCD property. EG: age, uc, lc
            property_value (str): Value of the UCD property. Eg: "1.1", "Y", "N", "004A"

        Returns:
            str|bool: The converted value. EG: "V1_1", True, False, "J"
        """
        if property == "scx":  # Special case - scx is a list of sc
            return self.__scx_lookup(property_value)

        # If there is a codepoint reference in the UCD value, we return the converted reference (unicode str)
        found, codepoint_ref = self.__codepoint_reference(property, property_value)
        if found:
            return codepoint_ref

        # Get lookup table for an UCD property. Eg lookuptable for Eg "age" would be {"1.1": "V1_1",.....}
        p_lookup = self.__property_values.get(property)
        if p_lookup:
            pv_lookup = p_lookup.get(property_value)  # Look up UCD value in our lookuptable.
            if pv_lookup:
                if "NFC_QC" not in property and "NFKC_QC" not in property:  # These has Y/N/M and cant be bool
                    if pv_lookup == "Yes":
                        return True
                    if pv_lookup == "No":
                        return False
                return pv_lookup
            else:  # Property is not in lookup table, just return it as-is.
                return property_value
        else:  # Value not in lookup table, just return it as-is.
            return property_value

    def __scx_lookup(self, property_value):
        """UCD property scx is a list of sc. This generates a python list with each scx scripts

        Args:
            property_value (str): The property value of the scx tag: Eg: "Latn Lana"

        Returns:
            list: A list of scripts. EG: ["Latin", "Tai_Tham"]
        """
        scx = []
        scripts = property_value.split(" ")
        p_lookup = self.__property_values.get("sc")  # scx uses same lookup table as sc
        for script in scripts:
            pv_lookup = p_lookup.get(script)
            scx.append(pv_lookup)
        return scx

    def raw_info(self, char):
        """Gets info of a single unicode character. This is the lowlevel method that returns
        compact information very close to that found in the original XML from unicode.org
        For more readable resule use "full_charinfo"-method

        Args:
            char (str): A single character the should be looked up. Eg: "ä"

        Returns:
            dict: All the properties of the character
                  Eg: {"bc":"ON", "ea": "A", "lb":"OP", .........}
                  returns None, if the character is not found in the database
        """
        if len(char) != 1:
            raise ValueError("Only one unicode character is considered valid. No more, no less.")

        char_info = self.__char_db["chars"].get(char)

        if char_info:
            group = char_info.get("group")
            group_info = self.__char_db["groups"][group]

            merged_info = {**group_info, **char_info}  # Tags from char takes precedence over the group tags.
            merged_info.pop("group")  # Users dont need to see the group, Its for us to internally join data
            return merged_info
        else:
            return None

    def info(self, char):
        """Get raw info of a character and creates a new dict in human readable format.
        Both keys and values (UCD properties and UCD property values) are looked up and translated.

        Args:
            char (str): Single character to be looked up

        Returns:
            dict: A full dict with over 100 keys describing the character. All in readable format.
        """
        full_info = {}
        info = self.raw_info(char)  # Get raw info of char
        if info:
            for k, v in info.items():
                looked_up_v = self.__property_value_lookup(k, v)  # convert the UCD property value to readable
                looked_up_name = self.__properties.get(k)  # Lookup the UCD property name
                if looked_up_name:
                    full_info[looked_up_name] = looked_up_v
                else:
                    full_info[k] = looked_up_v
        return full_info
