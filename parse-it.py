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
    >>> parse_folder_name('/parse-projects-xml-python/test/folders/LAMETRO_impexp_lametro_CPV_ARCADIA')
    {'Project': 'LAMETRO', 'Node': 'ARCADIA'}
    '''
    tmp = folderName.split("_")[0]
    projectName = os.path.basename(tmp)
    if projectName.startswith('TW'):
        projectName_noTW = projectName.split('TW')[1]
    else:
        projectName_noTW = projectName

    nodeName = folderName.split('CPV_')[1]

    parsed = {}
    parsed['Project'] = projectName
    parsed['ProjectNoTW'] = projectName_noTW
    parsed['Node'] = nodeName

    return parsed

def get_dirs(directory):
    exclusionFolders = ['Assemblies', 'CPV_Base_Files', 'CPVImpExp', 'wintail', 'imp_exp_upd']
    exclusionSet = set(exclusionFolders)

    dirs = [d for d in os.listdir(directory) if os.path.isdir( os.path.join(directory,d))]

    mydirs = [d for d in dirs if (d not in exclusionSet)]
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

def process_file(xml_file, parsed, args):
    tree = xml.ElementTree(file=xml_file)
    root = tree.getroot()
    appSettings = root.find('appSettings')

    directory = os.path.dirname(xml_file)
    log_file = "EX-CPV_{}.log".format(parsed['Node'])
    abs_log_file_name = os.path.join(directory, log_file)

    log = xml.Element("add", {"key":"UseFixedLogName", "value":"True"})
    log2 = xml.Element("add", {"key":"FixedLogName", "value":abs_log_file_name})

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
            print('\nXML File: {}\n'.format(xml_file))
            xml.dump(log)
            xml.dump(log2)
    else:
        print('\nSkipping: {}\n'.format(xml_file))

def choose_xml(abs_path_d):
    xml_list = [f for f in os.listdir(abs_path_d) if f.endswith('.xml')]
    xml_file = ''
    while True:
        for number, filename in enumerate(xml_list):
            print(number, filename)

        try:
            P1 = int(input("\nSelect the xml file: "))
        except ValueError:
            print('\nPlease enter an integer')
            continue

        if P1 < 0 or P1 >= len(xml_list):
            print('\nPlease enter an integer listed')
            continue
        else:
            xml_file = os.path.join(abs_path_d, xml_list[P1])
            break

    return xml_file

def get_xml_name(abs_path_d, parsed):
    xml_orig = 'CPV_{}_batchCPVimpexp.xml'.format(parsed['Project'].lower())
    xml_file = os.path.join(abs_path_d, xml_orig)

    alt_xml_orig = 'CPV_{}_BatchCPVImpExp.xml'.format(parsed['Project'].lower())
    alt_xml_file = os.path.join(abs_path_d, alt_xml_orig)

    alt2_xml_orig = 'CPV_{}_BatchCPVImpExp.xml'.format(parsed['Project'])
    alt2_xml_file = os.path.join(abs_path_d, alt2_xml_orig)

    if os.path.isfile(xml_file):
        return xml_file
    elif(os.path.isfile(alt_xml_file)):
        return alt_xml_file
    elif(os.path.isfile(alt2_xml_file)):
        return alt2_xml_file
    else:
        print()
        print("Unable to auto-detect the xml file")
        print("Choose from the xmls present in {}\n".format(os.path.basename(abs_path_d)))
        choosen_xml = choose_xml(abs_path_d)
        return choosen_xml

def process_folder(args, directory):
    abs_path = os.path.abspath(args.folder)
    abs_path_d = os.path.join(abs_path, directory)
    print(abs_path_d)
    parsed = parse_folder_name(abs_path_d)
    print('Project: {}'.format(parsed['Project']))
    print('ProjectNoTW: {}'.format(parsed['ProjectNoTW']))
    print('Node: {}'.format(parsed['Node']))

    xml_file = get_xml_name(abs_path_d, parsed)

    if xml_file:
        process_file(xml_file, parsed, args)
    else:
        print('\nFAIL:: {} doesnt exist\n'.format(xml_file))

    print('#'*30 + '\n')


def main(args):
    abs_path = os.path.abspath(args.folder)

    dirs = get_dirs(abs_path)
    failed_dirs = []
    for d in dirs:
        try:
            process_folder(args, d)
        except:
            print('Couldnt process the folder {}'.format(d))
            failed_dirs.append(d)
    with open('failed_dirs.txt', 'w') as f:
        for d in failed_dirs:
            abs_path_d = os.path.join(abs_path, d)
            f.write('{}\n'.format(abs_path_d))

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
    parser.add_argument("-e", "--edit", action="store_true", default=False,
        help="edit existing FixedLogName entries")
    args = parser.parse_args()

    if(args.test):
        import doctest
        doctest.testmod()
    else:
        main(args)
