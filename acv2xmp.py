#!/usr/bin/env python

import sys
import os
import traceback
from struct import unpack


def read_curve(acv_file):
    """
    AUTHOR
        email: vassilis@weemoapps.com
        twitter: @weemoapps
    """
    # Here we read the .acv curve file. It will help to take a look at see the link below to lean about the .acv file format specifications
    # http://www.adobe.com/devnet-apps/photoshop/fileformatashtml/PhotoshopFileFormats.htm#50577411_pgfId-1056330
    curve = []
    number_of_points_in_curve, = unpack("!h", acv_file.read(2))
    for j in range(number_of_points_in_curve):
        y, x = unpack("!hh", acv_file.read(4))
        curve.append((x, y))
    return curve


def main(curveFile, presetName):

    try:
        acv_file = open(curveFile, "rb")
        # acv_file = open(sys.argv[1], "rb")

    except Exception:
        print("Correct use: python acv2xmp.py file.acv presetName")
        os._exit(1)

    _, nr_curves = unpack("!hh", acv_file.read(4))
    curves = []
    for i in range(nr_curves):
        curves.append(read_curve(acv_file))

    # Reading an xmpFile to get most of the xmp code
    with open("data.xmp", 'r', encoding='utf-8') as f:
        output = f.readlines()

    # Adding the preset name to the xmp
    output[30] = output[30].replace("CURVESFORPYTHON", presetName)

    # Fast coding the crs Names
    tone = ["", "Red", "Green", "Blue"]

    # Cycling through the 4 Curves settings
    for i in range(4):
        output.append("   <crs:ToneCurvePV2012%s>\n    <rdf:Seq>\n" % tone[i])

        # Adding points
        for each in curves[i]:
            output.append("     <rdf:li>%s, %s</rdf:li>\n" % each)

        # Closing the curves
        output.append("    </rdf:Seq>\n   </crs:ToneCurvePV2012%s>\n" % tone[i])

    # Adding last bit of datas
    output.append("  </rdf:Description>\n")
    output.append(" </rdf:RDF>\n")
    output.append("</x:xmpmeta>\n")

    # Saving the file

    with open(presetName + ".xmp", 'w', encoding='utf-8') as f:
        f.writelines(output)


    return os.path.join(os.getcwd(), presetName + ".xmp")


if __name__ == '__main__':
    try:
        os.chdir(os.path.abspath(os.path.join(__file__, os.pardir)))

        main(*sys.argv[1:])
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)
