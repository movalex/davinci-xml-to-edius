import os, sys
import subprocess
from tkinter import filedialog, Tk
import xml.etree.ElementTree as ET
from urllib.request import urlparse

tk_root = Tk()
tk_root.withdraw()

init_dir = r"\\capture2\Capture2"
#init_dir = '.'

xml_in = filedialog.askopenfilename(initialdir=init_dir, 
        filetypes=(("XML", "*.xml"), ("All Files", "*.*")))
output_folder = os.path.split(xml_in)[0]

try:
    tree = ET.parse(xml_in)
except FileNotFoundError:
    sys.exit()

root = tree.getroot()


def parse_path(fpath):
    parsed = urlparse(fpath)
    i = parsed.path.index("/", 1)
    fix_path = parsed.path[1:i]
    parsed = parsed._replace(netloc=fix_path)
    return parsed.geturl()

for tag in root.iter('pathurl'):
    new_tag = parse_path(tag.text)
    tag.text = new_tag

output_file = '{}_to-EDIUS.xml'.format(os.path.splitext(xml_in)[0])

field_dom = ET.Element('fielddominance')
field_dom.text = 'upper'

#for tag in root.iter('samplecharacteristics'):
for tag in tree.findall('./sequence/media/video/format/samplecharacteristics'):
    tag.append(field_dom)


def pretty_xml(elem, level=0):
    i = "\n" + level*"    "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            pretty_xml(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    elif level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i

pretty_xml(root)

with open(output_file, 'wb') as out:
    out.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n')
    tree.write(out, encoding='utf-8')

if os.name == 'nt':
    subprocess.Popen('explorer /open, {}'.format(os.path.normpath(output_folder)))
