import re
import json
from zipfile import ZipFile
import urllib.request
from io import BytesIO
import xml.etree.ElementTree as ET


def download_zip(url, filename):
    """Gets content of a file inside an online zip-file

    Args:
        url (str): URL of the zip-file
        filename (str): Filename of the compressed file

    Returns:
        str: The full content of the file. Is UTF-8 decoded
    """
    url = urllib.request.urlopen(url)

    with ZipFile(BytesIO(url.read())) as zf:
        with zf.open(filename, "r") as fp:
            data = fp.read()
        return data.decode("utf-8")


def download_text(url):
    """Gets the content of an online text-file

    Args:
        url (str): URL of the text-file

    Returns:
        str: The full content of the file. Is UTF-8 decoded
    """
    url = urllib.request.urlopen(url)
    data = url.read()
    return data.decode("utf-8")


def save_json(filename, data):
    """Save a json file to disk

    Args:
        filename (str): Filename of the destination file
        data (dict|list): An object to be written to disk
    """
    with open(filename, mode="w", encoding="utf-8") as fp:
        json.dump(data, fp)


def get_ucd_db(xmldata):
    """Creates an unicode dictionary database that is ready for the entire module.

    Args:
        xmldata (str): Raw utf-8 encoded XML data the should be processed

    Returns:
        Dict: {
                groups: {"1": {properties}, "2": {properties}},
                chars: {"A": {"group": 1, properties}, "B": {"group": 1, properties}}
               }
    """
    tree = ET.fromstring(xmldata,)

    namespace = {"ucd": "http://www.unicode.org/ns/2003/ucd/1.0"}

    chars = {}
    groups = {}

    for idx, group in enumerate(tree.findall(".//ucd:group", namespace)):  # Enumerate all group-tags in XML
        groups[str(idx)] = group.attrib  # Store attributes for the group
        for char in group.findall(".//ucd:char", namespace):  # Inside a group enumerate all unicode chars.
            if char.attrib.get("cp"):  # There are some reserved areas that doesn't have assigned unicode.
                unicode = chr(int(char.attrib.pop("cp"), 16))
                char.attrib["group"] = str(idx)  # save a reference inside each char, what group we belong to
                chars[unicode] = char.attrib

    return {"groups": groups, "chars": chars}


def get_property_names(textdata):
    """Creates a database of properties that can be found inside the UCD-XML.
    This is later used for lookup, for making data more human readable.
    All tag attributes in UCD are very short and hard to read. This is the translation table.
    Eg: gc="Po" dt="none" bc="ON" ea="A" lb="OP".... "dt" becomes "Decomposition_Type"

    Args:
        textdata (str): The content of the properties-file, that is downloaded

    Returns:
        dict: { "dm": "Decomposition_Mapping", ......}
    """
    properties = {}

    for line in textdata.split("\n"):
        s = re.search(r"(\w+)\s+;\s(\w+)", line)
        if s:
            abbr = s[1].strip()
            name = s[2].strip()
            properties[abbr] = name
    return properties


def get_property_values(textdata):
    """Creates a database of property values that can be found inside the UCD-XML
    Eg the proporty "gc" could be set to "Nl". With this function it will be translated to a more
    human readable text "Letter_Number"

    Args:
        textdata (str): The content of the property-value file, that is downloaded

    Returns:
        dict: {"gc": {"Nl": "Letter_Number", "M": "Mark"}, "ea": {.....}}
    """
    property_values = {}

    for line in textdata.split("\n"):
        s = re.search(r"^([\._\w]+)\s*;\s*([\._\w]+)\s*;\s*([\._\w]+)", line)
        if s:
            property = s[1]
            property_value = s[2]
            property_value_looked_up = s[3]

            property_values.setdefault(property, {})
            if property == "dt":  # Special case - the casing is wrong in official lookup table!
                property_values[property][property_value.lower()] = property_value_looked_up
            elif property == "ccc":  # Special case - we want 4th column instead of 3rd
                property_values[property][property_value] = re.search(r"([\._\w]+)$", line)[1]
            else:
                property_values[property][property_value] = property_value_looked_up

    return property_values


if __name__ == "__main__":
    """Creates all the ready json that this entire module needs.
    All the files are stored in the db-folder.
    This is done before distribution af the package
    """
    xmldata = download_zip(
        "https://www.unicode.org/Public/UCD/latest/ucdxml/ucd.all.grouped.zip", "ucd.all.grouped.xml"
    )
    data = get_ucd_db(xmldata)
    save_json("unilyze/db/unicode_db.json", data)

    textdata = download_text("https://www.unicode.org/Public/UCD/latest/ucd/PropertyAliases.txt")
    data = get_property_names(textdata)
    save_json("unilyze/db/property_names.json", data)

    textdata = download_text("https://www.unicode.org/Public/UCD/latest/ucd/PropertyValueAliases.txt")
    data = get_property_values(textdata)
    save_json("unilyze/db/property_values.json", data)
