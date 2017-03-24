#!/usr/bin/env python3

from shutil import copyfile
import os

def get_dirs(directory):
    exclusionFolders = ['Assemblies', 'CPV_Base_Files', 'CPVImpExp']
    exclusionSet = set(exclusionFolders)

    dirs = [d for d in os.listdir(directory)]

    mydirs = [d for d in dirs if d not in exclusionSet]
    return mydirs

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", default=False,
        help="prints out where the file is being copied")
    args = parser.parse_args()

    test_folder = './test/folders'
    abs_path_test_folder = os.path.abspath(test_folder)

    example_file_loc = './test/input/'
    dirs = get_dirs(abs_path_test_folder)
    for d in dirs:
        example_file_name = ''
        if 'dukenet' in d:
            example_file_name = 'CPV_dukenet_BatchCPVImpExp.xml'
        elif d.startswith('TW'):
            example_file_name = 'CPV_TWLAMETRO_BatchCPVImpExp.xml'
        elif d.startswith('scarolina'):
            example_file_name = 'CPV_twsc_BatchCPVImpExp.xml'
        else:
            example_file_name = 'CPV_lametro_batchCPVimpexp.xml'
        src = os.path.join(example_file_loc, example_file_name)
        dst = os.path.join(abs_path_test_folder, d, example_file_name)
        if(args.verbose):
            print('Copying {} to {}'.format(src, dst))
        copyfile(src, dst)
