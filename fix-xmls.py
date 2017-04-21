#!/usr/bin/env python3

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
    parsed['Folder'] = folderName

    return parsed

def get_dirs(directory):
    exclusionFolders = ['Assemblies', 'CPV_Base_Files', 'CPVImpExp', 'wintail', 'imp_exp_upd']
    exclusionSet = set(exclusionFolders)

    dirs = [d for d in os.listdir(directory) if os.path.isdir( os.path.join(directory,d))]

    mydirs = [d for d in dirs if (d not in exclusionSet)]
    return mydirs

def get_files(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile( os.path.join(directory,f) )]
    return files

def process_file(xml_file, parsed, args):
    with fileinput.input(xml_file, inplace=True) as f:
        for line in f:
            if('key="FixedLogName"' in line):
                m = re.search(r'value\=\"(\S+)[\\\/](\S+\.log)\"', line)
                oldFolder = m.group(1)
                log = m.group(2)
                newlog = os.sep.join([parsed['Folder'], log])
                newvalue = ''.join(['value="',newlog,'"'])
                newLineFolder = re.sub(r'value\=\"\S+\.log\"', newvalue, line)
                print(newLineFolder.rstrip())
            else:
                print(line.rstrip())

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

def match_xml(files):
    xml_file = ''
    for f in files:
        result = re.match(r'(CPV_\w+_BatchCPVImpExp\.xml)', f, flags=re.IGNORECASE)
        if(result):
            xml_file = result.group(1)
    print('auto selected:')
    print(xml_file)
    return xml_file

def get_xml_name(abs_path_d, parsed):
    files = get_files(abs_path_d)
    print('Files:')
    print(files)

    xml_file = os.path.join(abs_path_d, match_xml(files))
    # xml_orig = 'CPV_{}_batchCPVimpexp.xml'.format(parsed['Project'].lower())
    # xml_file = os.path.join(abs_path_d, xml_orig)
    #
    # alt_xml_orig = 'CPV_{}_BatchCPVImpExp.xml'.format(parsed['Project'].lower())
    # alt_xml_file = os.path.join(abs_path_d, alt_xml_orig)
    #
    # alt2_xml_orig = 'CPV_{}_BatchCPVImpExp.xml'.format(parsed['Project'])
    # alt2_xml_file = os.path.join(abs_path_d, alt2_xml_orig)

    if os.path.isfile(xml_file):
        return xml_file
    else:
        print()
        print("Unable to auto-detect the xml file")
        print("Choose from the xmls present in {}\n".format(os.path.basename(abs_path_d)))
        choosen_xml = choose_xml(abs_path_d)
        return choosen_xml

def process_folder(args, directory):
    abs_path = os.path.abspath(args.folder)
    abs_path_d = os.path.join(abs_path, directory)

    parsed = parse_folder_name(abs_path_d)
    print('Project:\t{}'.format(parsed['Project']))
    print('ProjectNoTW:\t{}'.format(parsed['ProjectNoTW']))
    print('Node:\t\t{}'.format(parsed['Node']))
    print('Folder:\t\t{}\n'.format(parsed['Folder']))

    xml_file = get_xml_name(abs_path_d, parsed)
    print('Selected XML File:\n{}\n'.format(xml_file))

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
        except Exception as e:
            print('Couldnt process the folder {}'.format(d))
            print(e)
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
    import re
    import fileinput

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f","--folder", default='E:\\CPV',
        help="the folder containing all projects and nodes")

    args = parser.parse_args()

    main(args)
