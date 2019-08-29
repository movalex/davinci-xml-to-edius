from urllib.request import urlparse, url2pathname
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import os, sys
import tkinter as tk
from tkinter import filedialog
import subprocess

tk_root = tk.Tk()
tk_root.withdraw()

init_dir = r"\\capture2\Capture2"
xml_in = filedialog.askopenfilename(initialdir=init_dir, 
        filetypes=(("XML", "*.xml"), ("All Files", "*.*")))

try:
    tree = ET.parse(xml_in)
except FileNotFoundError:
    sys.exit()

root = tree.getroot()


def parse_path(fpath):
    parsed = urlparse(fpath)
    i = parsed.path.index("/", 1)
    fix_path = parsed.path[:i].replace('/','')
    parsed = parsed._replace(netloc=fix_path)
    return parsed.geturl()

for tag in root.iter('pathurl'):
    new_tag = parse_path(tag.text)
    tag.text = new_tag

xml_name, xml_ext = os.path.splitext(xml_in)
output_folder = os.path.split(xml_in)[0]
output_file = '{}_to-EDIUS{}'.format(xml_name, xml_ext)

with open(output_file, 'wb') as out:
    out.write(b'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n')
    tree.write(out, encoding='utf-8')

subprocess.Popen('explorer /open, {}'.format(os.path.normpath(output_folder)))
