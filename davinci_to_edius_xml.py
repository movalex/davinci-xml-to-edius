import os, sys
import subprocess
from tkinter import filedialog, Tk
import xml.etree.ElementTree as ET
from urllib.request import urlparse


tk_root = Tk()
tk_root.withdraw()

INIT_DIR = r"\\capture2\Capture2"
# INIT_DIR = '.'

def open_file():
    xml_in = filedialog.askopenfilename(initialdir=INIT_DIR, 
            filetypes=(("XML", "*.xml"), ("All Files", "*.*")))
    try:
        tree = ET.parse(xml_in)
        root = tree.getroot()
    except FileNotFoundError:
        sys.exit()
    root_folder = get_root_folder(xml_in)
    return xml_in, tree, root_folder


def get_root_folder(file):
    ss = urlparse(os.path.split(file)[0])
    return ss.netloc


def parse_path(fpath, folder):
    parsed = urlparse(fpath)
    parsed = parsed._replace(netloc=folder) #set correct hostname
    return parsed.geturl()


def main():
    xml_in, tree, folder = open_file()
    root = tree.getroot()
    output_file = '{}_to-EDIUS.xml'.format(os.path.splitext(xml_in)[0])
    output_folder = os.path.split(xml_in)[0]
    for tag in root.iter('pathurl'):
        new_tag = parse_path(tag.text, folder)
        tag.text = new_tag    

    with open(output_file, 'wb') as out:
        out.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n')
        tree.write(out, encoding='utf-8')

    if os.name == 'nt':
        subprocess.Popen('explorer /open, {}'.format(os.path.normpath(output_folder)))


if __name__ == '__main__':
    main()







    
#field_dom = ET.Element('fielddominance')
#field_dom.text = 'upper'
#''' can use `for tag in root.iter('samplecharacteristics'):` for entire text'''
#for tag in tree.findall('./sequence/media/video/format/samplecharacteristics'):
#    tag.append(field_dom)



#def pretty_xml(elem, level=0):
#    i = "\n" + level*"    "
#    if len(elem):
#        if not elem.text or not elem.text.strip():
#            elem.text = i + "    "
#        if not elem.tail or not elem.tail.strip():
#            elem.tail = i
#        for elem in elem:
#            pretty_xml(elem, level+1)
#        if not elem.tail or not elem.tail.strip():
#            elem.tail = i
#    elif level and (not elem.tail or not elem.tail.strip()):
#        elem.tail = i

#pretty_xml(root)

#with open(output_file, 'wb') as out:
#    out.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n')
#    tree.write(out, encoding='utf-8')

