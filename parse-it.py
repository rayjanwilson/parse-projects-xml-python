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
    >>> parse_folder_name('/home/wilsonrm/dev/git/parse-projects-xml-python/test/folders/LAMETRO_impexp_lametro_CPV_ARCADIA')
    {'Project': 'LAMETRO', 'Node': 'ARCADIA'}
    '''
    tmp = folderName.split("_")[0]
    projectName = os.path.basename(tmp)

    nodeName = folderName.split('CPV_')[1]

    parsed = {}
    parsed['Project'] = projectName
    parsed['Node'] = nodeName

    return parsed

def get_dirs(directory):
    exclusionFolders = ['Assemblies', 'CPV_Base_Files', 'CPVImpExp']
    exclusionSet = set(exclusionFolders)

    dirs = [d for d in os.listdir(directory)]

    mydirs = [d for d in dirs if d not in exclusionSet]
    return mydirs

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def process_folder(args, directory):
    abs_path = os.path.abspath(args.folder)
    abs_path_d = os.path.join(abs_path, directory)
    print(abs_path_d)
    parsed = parse_folder_name(abs_path_d)
    print('Project: {}'.format(parsed['Project']))
    print('Node: {}'.format(parsed['Node']))

    xml_orig = 'CPV_{}_batchCPVimpexp.xml'.format(parsed['Project'].lower())
    xml_file = os.path.join(abs_path_d, xml_orig)

    if os.path.isfile(xml_file):
        tree = xml.ElementTree(file=xml_file)
        root = tree.getroot()
        appSettings = root.find('appSettings')

        log = xml.Element("add", {"key":"UseFixedLogName", "value":"True"})
        val = "E:\\CPV\\{}_impexp_{}_CPV_ACTON\\EX-CPV_ACTON.log".format(parsed['Project'].upper(), parsed['Project'].lower())
        log2 = xml.Element("add", {"key":"FixedLogName", "value":val})

        should_we_append = True

        # check to see if the attribute is already there for some reason
        for child in appSettings:
            if child.attrib == log.attrib:
                should_we_append = False

        if should_we_append:
            appSettings.append(log)
            appSettings.append(log2)
            tree = xml.ElementTree(root)
            indent(root)
            if(args.write):
                print('\nUpdating: {}\n'.format(xml_file))
                tree.write(xml_file, xml_declaration=True)
            else:
                print()
                xml.dump(log)
                xml.dump(log2)
        else:
            print('\nSkipping: {}\n'.format(xml_file))
    else:
        print('\nFAIL:: {} doesnt exist\n'.format(xml_file))

    print('#'*30 + '\n')

def print_to_screen(directory):
    parsed = parse_folder_name(directory)
    print('Project: {}'.format(parsed['Project']))
    print('Node: {}'.format(parsed['Node']))

    print()

def main(args):
    abs_path = os.path.abspath(args.folder)

    dirs = get_dirs(abs_path)
    for d in dirs:
        process_folder(args, d)


if __name__ == '__main__':
    import argparse
    import os
    import xml.etree.ElementTree as xml

    from xml.dom import minidom

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f","--folder", default='E:\\CPV',
        help="the folder containing all projects and nodes")
    group.add_argument("-t","--test", action="store_true", default=False,
        help="run the doc tests")
    parser.add_argument("-w", "--write", action="store_true", default=False,
        help="find the xml and write the new lines to it")
    args = parser.parse_args()

    if(args.test):
        import doctest
        doctest.testmod()
    else:
        main(args)
