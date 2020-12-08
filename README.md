# Roundtrip from Edius to Davinci Resolve

## Optimize FCP7 XML files from Davinci Resolve 14/16 to import footage to Edius

To make proper roundtrip from editing in EDIUS to colorgrade in Davinci Resolve, you would probably use oficial AAF roundtrip workflow. This workflow will suffice if you work with files locally on your machine. In case you have network located files on your timeline, you will get a ‘Files not found’ error when you put AAF with colorgraded files back to EDIUS. Thats why I use AAF-to-XML roundtrip which is undocumented but still possible.

For some reason the UNC paths to network-located media written by Davinci will not be located by EDIUS. This is not a Davinci Resolve issue, because this workflow works correctly in Adobe Premiere. Thats why we need to fix the XML with some magic!

Our roundtrip consists of two simple steps:

    Edit in Edius and export AAF to Davinci Resolve for color correction
    Put back color corrected clips back to Edius Timeline with XML

### from EDIUS to Davinci  

When you complete your editing, choose File >> Export Project >> AAF...
You will be prompted to select a preset. Choose Type 4:

![](https://abogomolov.s3.amazonaws.com/pictures/blog/edius_preset_AAF.jpg)

You can customize export settings according to your needs. I use `Copy Option` with margin of 1 sec:

![](https://abogomolov.s3.amazonaws.com/pictures/blog/edius_settings.PNG)

 Don't forget to check `Export between in and out` and click `Save`.

To use Quicktime HQX codec you have to install [Quicktime](https://support.apple.com/kb/DL837?locale=en_US) and Edius codecs on your Davinci Resolve Windows machine. To eliminate possible security flaws, uncheck all Quicktime components except the first and necessary one upon installation. Once you have Qucktime installed, Davinci Resolve will recognize any Canopus HQX MOV file on the timeline. If you don't like the idea of QT installation, which is understandable since Apple discontinued Windows version support, you need to export your edit with DNxHD codec. It is available as a part of Edius 8/9 Workgroup version.

Prior to importing AAF file to Resolve, place rendered clips into the Media Pool on the [MEDIA] page.   

### from Davinci to EDIUS
There you go, when you have colorgraded your edit, now you would like to put it back to Edius to do the final touches. On a deliver page choose Custom >> Render Individual Clips >> Choose Format and Codec. I use MXF OP1a with XDCAM MPEG2, which is nicely supported by EDIUS. Then choose File >> Filename uses -- Source Name >> Add a uniquie name (Prefix/Suffix). Choose render location to your desired network folder. Add to render queue and start render. After all files are done, go to Davinci Resolve EDIT page and choose File >> Export AAF/XML. Export XML to the same network folder where your renders are (this is important).

![](https://abogomolov.s3.amazonaws.com/pictures/blog/davinci_settings.png)

Well, to get things done we need to import our XML to Edius. I wrote some kind of [XML resolver](https://lowepost.com/forums/topic/565-roundtrip-resolve-fromto-edius/?do=findComment&comment=2405), which will make our rondtrip possible.
Here is it:

```
import os, sys
import subprocess
from tkinter import filedialog, Tk
import xml.etree.ElementTree as ET
from urllib.request import urlparse

tk_root = Tk()
tk_root.withdraw()

INIT_DIR = r"\\your\network\located\folder\with\xml\file\and\rendered\files"

def open_file():
    """put your .xml file in the same network folder where your rendered files are"""

    xml_in = filedialog.askopenfilename(initialdir=INIT_DIR, 
            filetypes=(("XML", "*.xml"), ("All Files", "*.*")))
    try:
        tree = ET.parse(xml_in)
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
        
    # field_dom = ET.Element('fielddominance')
    # field_dom.text = 'upper'
    # ''' can use `for tag in root.iter('samplecharacteristics'):` for entire text'''
    # for tag in tree.findall('./sequence/media/video/format/samplecharacteristics'):
    #    tag.append(field_dom)
    
    with open(output_file, 'wb') as out:
        out.write(b'<?xml version="1.0" encoding="UTF-8"?>\n\n')
        tree.write(out, encoding='utf-8')

    if os.name == 'nt':
        subprocess.Popen('explorer /open, {}'.format(os.path.normpath(output_folder)))


if __name__ == '__main__':
    main()
    
```

For xml parsing I use standard Python library `xml.etree.ElementTree`.
When the script is launched you will be prompted to choose XML file you exported on previous step. Basically all what we need is to get rid of wrong part of each filepath in XML. These network paths start with `file://localhost/`, but instead EDIUS looks for proper net location, so `localhost` has to be replaced with server name. Script will take server name from the location of your XML file, that's why you had to put XML file in the render folder. The result is a new XML file which will work flawlessly in EDIUS. The folder with new file will open automatically.

I know what you're thinking right now. If the problem was simply with wrong file path, why won't we just search and replace?
The answer is: YES, you are right. Basically it is what we do, but with XML parser instead of text editor. But look at these commented lines in main() function. You can use the script to modify and change any tag or field in your XML file. For example, you can add field dominance or any other paramerer according to [FCP XML 1.0 specifications](http://mirror.informatimago.com/next/developer.apple.com/documentation/AppleApplications/Conceptual/FinalCutPro_XML/FinalCutPro_XML.pdf). 

And besides it was fun. 

Take care and thanks for reading this!
