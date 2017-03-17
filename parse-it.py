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

def parse_folder_name(folderName):
    '''
    >>> parse_folder_name('LAMETRO_impexp_lametro_CPV_ARCADIA')
    {'Project': 'LAMETRO', 'Node': 'ARCADIA', 'FirstLine': '<add key="UseFixedLogName" value="True" />', 'SecondLine': '<add key="FixedLogName" value="E:\\\\CPV\\\\LAMETRO_impexp_lametro_CPV_ACTON\\\\EX-CPV_ACTON.log" />'}
    '''

    tmp = folderName.split("_")[0]
    projectName = os.path.basename(tmp)

    projectNameUpper = projectName.upper()
    projectNameLower = projectName.lower()

    nodeName = folderName.split('CPV_')[1]

    firstLine = "<add key=\"UseFixedLogName\" value=\"True\" />"
    secondLine = "<add key=\"FixedLogName\" value=\"E:\\CPV\\{}_impexp_{}_CPV_ACTON\\EX-CPV_ACTON.log\" />".format(projectNameUpper,projectNameLower)

    parsed = {}
    parsed['Project'] = projectName
    parsed['Node'] = nodeName
    parsed['FirstLine'] = firstLine
    parsed['SecondLine'] = secondLine

    return parsed

def get_dirs(directory):
    exclusionFolders = ['Assemblies', 'CPV_Base_Files', 'CPVImpExp']
    exclusionSet = set(exclusionFolders)

    dirs = [d for d in os.listdir(directory)]

    mydirs = [d for d in dirs if d not in exclusionSet]
    return mydirs

def pretty_print(parsed):
    print('#'*60)
    print()
    print('Project:\t{}'.format(parsed['Project']))
    print('Node:\t\t{}'.format(parsed['Node']))
    print()
    print(parsed['FirstLine'])
    print(parsed['SecondLine'])
    print()

def main(directory):
    dirs = get_dirs(directory)
    for d in dirs:
        parsed_folder = parse_folder_name(d)
        pretty_print(parsed_folder)




if __name__ == '__main__':
    import argparse
    import os
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f","--folder", default='C:\\CPV',
        help="the folder containing all projects and nodes")
    group.add_argument("-t","--test", action="store_true", default=False,
        help="run the doc tests")
    args = parser.parse_args()

    if(args.test):
        import doctest
        doctest.testmod()
    else:
        main(args.folder)
