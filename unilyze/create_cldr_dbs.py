import re
import json
from zipfile import ZipFile
import xml.etree.ElementTree as ET
from io import BytesIO
import urllib.request


def raw_url_xml(url, dir_search, file_search):
    """An iterator that yields many xml-files from inside a single zip-file in the provided url.

    Args:
        url (str): URL of the zip-file
        dir_search (str): A directory name to search for
        file_search (str): A file name to search for.

    Yields:
        xml.etree.ElementTree: An XML tree element for further parsing
    """
    url = urllib.request.urlopen(url)

    with ZipFile(BytesIO(url.read())) as zf:
        for name in zf.namelist():
            if dir_search in name and file_search in name:
                raw_xml = zf.read(name).decode("utf-8")
                yield ET.fromstring(raw_xml,)


def exemplar_unescape(text):
    """ In the original xml's the exemplar-fileds are escaped.
    This method removes the escaping and returns a cleaned exemplar string
    Info about escaping: https://www.unicode.org/reports/tr35/tr35-59/tr35.html#Unicode_Sets

    Args:
        text (str): Raw exemplar string from XML. EG: "a b c \\- \\["

    Returns:
        str: A clean exemplar string without escape characters. EG: "a b c - ["
    """
    esc_chars = ["-", "[", "]", ":", "&", "$", "\\", "^", "{", "}"]

    for esc_char in esc_chars:
        text = text.replace("\\" + esc_char, esc_char)

    text = re.sub(r"\{([^\s]+)\}", "\\1", text)  # Multichar's are in format "{xx}"

    return text


def exemplar_unicodes_convert(text):
    """Convert \u1234 strings inside the exemplar text to real unicode characters

    Args:
        text (str): Raw exemplar string. Eg: "a b c \\u0041"

    Returns:
        [type]: Converted exemplar string: Eg: "a b c A"
    """
    uni_chars = re.findall(r"\\u([0-9A-F]+)", text)
    for uni_char in uni_chars:
        text = text.replace("\\u" + uni_char, chr(int(uni_char, 16)))
    return text


def get_xml_tag_attrib(xmltree, tagname, attribute):
    """Gets a tag with a certain attribute from an XML-tree

    Args:
        xmltree (xml.etree.ElementTree): XML-tree to search through
        tagname (str): An XML tag
        attribute (str): An XML attribute

    Returns:
        str: The content of the attribute
    """
    tag = ""
    tag_search = xmltree.find(tagname)
    if tag_search is not None:
        tag = tag_search.attrib.get(attribute)
    return tag


def get_xml_tag_dict(xml_tree, tag, attribute):
    """Searches an XML tree for a tag. Under this tag it get all elements and returns them as a dict
    with "attribute" as the key, and the text for the element as the value

    Args:
        xml_tree (xml.etree.ElementTree): XML-tree to search through
        tag (str): An XML tag
        attribute (str): An XML attribute

    Returns:
        dict: Key,Value = tag attribute content, element text. Eg: {"da": "danish"...}
    """
    tag_dict = {}
    tags = xml_tree.find(tag)
    for tag in tags:
        tag_value = tag.text
        tag_key = tag.attrib.get(attribute)
        tag_dict[tag_key] = tag_value
    return tag_dict


def get_exemplar_char(url):
    """Builds a complete database of exemplars. It's ordered by Language->Group->Characters

    Args:
        url (str): URL of the zip-file that contains all xml-language definitions

    Returns:
        dict: Eg: {"da": {"Numbers": "[0 1 2]", "Auxilary":". ,"}, "en"... }
    """
    exemplar_char = {}
    for xmltree in raw_url_xml(url, "main", ".xml"):
        language = get_xml_tag_attrib(xmltree, "identity/language", "type")
        territory = get_xml_tag_attrib(xmltree, "identity/territory", "type")
        exemplar = get_language_exemplar_char(xmltree)
        lang_terr = language + "_" + territory if language and territory else language

        exemplar_char[lang_terr] = exemplar
    return exemplar_char


def get_language_exemplar_char(xmltree):
    """Gets the exemplar from one country

    Args:
        xmltree (xml.etree.ElementTree): The XML tree for a certain language

    Returns:
        dict: Eg: {"Numbers": "[0 1 2]", "Auxilary":". ,"}
    """
    exemplars = {}

    for x in xmltree.iter("exemplarCharacters"):
        exemplar_name = x.attrib.get("type", "main")
        exemplar_raw = x.text[1:-1]
        exemplar_unicode = exemplar_unicodes_convert(exemplar_raw)
        exemplar = exemplar_unescape(exemplar_unicode)

        exemplars[exemplar_name] = exemplar.split(" ")
    return exemplars


def get_char_exemplar(expemplar_char):
    """Builds a complete database of exemplars. It's ordered by Character->Group->Language

    Args:
        expemplar_char (dict): Takes the format generated in method "get_exemplar_char"

    Returns:
        dict: Eg: {"a": {"lower": ["da", "en"]}, "b"...}
    """
    exemplars = {}
    for lang_terr, groups in expemplar_char.items():
        for group in groups:
            for char in exemplar_char[lang_terr][group]:
                exemplars.setdefault(char, {})
                exemplars[char].setdefault(group, [])
                exemplars[char][group].append(lang_terr)
    return exemplars


def get_lang_terr(url):
    """Creates a database of languages and territories, based on "common/main/en.xml".

    Args:
        url (str): UTL of the zipfile that contains language definitions

    Returns:
        dict: Final database dict : {"language": {"da": "Danish"...}, "territory": {"DK": "Denmark"...}}
    """
    xml_tree = next(raw_url_xml(url, "main", "en.xml"))
    language = get_xml_tag_dict(xml_tree, "localeDisplayNames/languages", "type")
    territory = get_xml_tag_dict(xml_tree, "localeDisplayNames/territories", "type")
    return {"language": language, "territory": territory}


def save_json(filename, data):
    """Save a json file to disk

    Args:
        filename (str): Filename of the destination file
        data (dict|list): An object to be written to disk
    """
    with open(filename, mode="w", encoding="utf-8") as fp:
        json.dump(data, fp)


if __name__ == "__main__":
    """Creates all the ready CLDR-json that this entire module needs.
    All the files are stored in the db-folder.
    This is done before distribution af the package
    """
    exemplar_char = get_exemplar_char("http://unicode.org/Public/cldr/37/core.zip")
    save_json("unilyze/db/cldr_exemplar_char.json", exemplar_char)

    char_exemplar = get_char_exemplar(exemplar_char)
    save_json("unilyze/db/cldr_char_exemplar.json", char_exemplar)

    lang_terr = get_lang_terr("http://unicode.org/Public/cldr/37/core.zip")
    save_json("unilyze/db/cldr_language_territory.json", lang_terr)
