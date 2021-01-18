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

For xml parsing I use standard Python library `xml.etree.ElementTree`.
When the script is launched you will be prompted to choose XML file you exported on previous step. Basically all what we need is to get rid of wrong part of each filepath in XML. These network paths start with `file://localhost/`, but instead EDIUS looks for proper net location, so `localhost` has to be replaced with server name. Script will take server name from the location of your XML file, that's why you had to put XML file in the render folder. The result is a new XML file which will work flawlessly in EDIUS. The folder with new file will open automatically.

I know what you're thinking right now. If the problem was simply with wrong file path, why won't we just search and replace?
The answer is: YES, you are right. Basically it is what we do, but with XML parser instead of text editor. But look at these commented lines in main() function. You can use the script to modify and change any tag or field in your XML file. For example, you can add field dominance or any other paramerer according to [FCP XML 1.0 specifications](http://mirror.informatimago.com/next/developer.apple.com/documentation/AppleApplications/Conceptual/FinalCutPro_XML/FinalCutPro_XML.pdf). 

And besides it was fun. 

Take care and thanks for reading this!
