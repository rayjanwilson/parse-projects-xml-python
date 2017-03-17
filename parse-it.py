#!/usr/bin/env python3

# Open the CPV_ProjectName_BatchCPVImpExp.xml file with Notepad and make the following changes and additions:
#
# b.      Add these two lines, editing the logfile path and name in the second line for current job.
#
# ʼ/span><add key="UseFixedLogName" value="True" />
# ʼ/span><add key="FixedLogName" value="E:\CPV\TWLASOUTH_impexp_lasouth_CPV_ACTON\EX-CPV_ACTON.log" />
#
#
# Projectname in the file name for the .xml file is specific to the project
# in this case above– TWLASOUTH is the top level project folder and lasouth is the sob project folder – so that line is specific to project.

def main(fileName):
    # fileName = "CPV_ProjectName_BatchCPVImpExp.xml"
    print('file name: \t{}'.format(fileName))
    projectName = fileName.split("_")[1]
    print('project name: \t{}'.format(projectName))
    projectNameUpper = projectName.upper()
    projectNameLower = projectName.lower()

    firstLine = "ʼ/span><add key=\"UseFixedLogName\" value=\"True\" />"
    secondLine = "ʼ/span><add key=\"FixedLogName\" value=\"E:\\CPV\\TW{}_impexp_{}_CPV_ACTON\\EX-CPV_ACTON.log\" />".format(projectNameUpper,projectNameLower)
    print()
    print(firstLine)
    print(secondLine)
    print()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("fileName", help="the file name you want to parse")
    args = parser.parse_args()

    main(args.fileName)
