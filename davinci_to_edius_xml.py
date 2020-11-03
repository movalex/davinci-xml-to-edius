from tkinter import filedialog, Tk
from urllib.request import urlparse
import os, sys
import subprocess
import xml.etree.ElementTree as ET

tk_root = Tk()
tk_root.withdraw()

INIT_DIR = r"\\capture2\Capture2\shared\DAVINCI_Render"
# INIT_DIR = os.path.realpath('.')


def open_file():
    """put your .xml file in the same network folder where your rendered files are"""
    xml_in = filedialog.askopenfilename(
        initialdir=INIT_DIR, filetypes=(("XML", "*.xml"), ("All Files", "*.*"))
    )
    try:
        tree = ET.parse(xml_in)
    except FileNotFoundError:
        sys.exit()
    root_folder = get_root_folder(xml_in)
    return xml_in, tree, root_folder


def get_root_folder(file):
    parsed_path = urlparse(os.path.split(file)[0])
    return parsed_path.netloc


def parse_path(fpath, folder):
    parsed = urlparse(fpath)
    parsed = parsed._replace(netloc=folder)  # set correct hostname
    return parsed.geturl()


def pretty_xml(elem, level=0):
    indent = "\n" + level * "    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for elem in elem:
            pretty_xml(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
    elif level and (not elem.tail or not elem.tail.strip()):
        elem.tail = indent


def add_tag(field, tag, search, root):
    field_dom = ET.Element(field)
    field_dom.text = tag
    # for tag in tree.findall(search):  # add fielddominance to the end of the xml file
    for tag in root.iter(search):  # add field dominance to each media file entry
        tag.append(field_dom)


def main():
    xml_in, tree, folder = open_file()
    root = tree.getroot()
    output_file = "{}_to-EDIUS.xml".format(os.path.splitext(xml_in)[0])
    output_folder = os.path.split(xml_in)[0]
    for tag in root.iter("pathurl"):
        new_tag = parse_path(tag.text, folder)
        tag.text = new_tag

    # add_tag('fielddominance', 'upper', 'samplecharacteristics', root)
    # add_tag('fielddominance', 'upper', './sequence/media/video/format/samplecharacteristics', tree)
    # pretty_xml(root)

    with open(output_file, "wb") as out:
        out.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n')
        tree.write(out, encoding="utf-8")
    if os.name == "nt":
        subprocess.Popen("explorer /open, {}".format(os.path.normpath(output_folder)))


if __name__ == "__main__":
    main()