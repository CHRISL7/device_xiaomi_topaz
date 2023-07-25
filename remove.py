#!/usr/bin/env python3

import os
import sys
import getopt

QCOM_COMMON_PATH = 'device/qcom/common'
TARGET_FILE = 'proprietary-files.txt'

def remove_lines_from_file(lines, file_path):
    removed_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            for i, target_line in enumerate(lines):
                if line in target_line:
                    lines[i] = ''
                    if line.startswith('-'):
                        removed_lines.append(line[1:])
                    else:
                        removed_lines.append(line)
                    break
    return removed_lines

def main(argv):
    components = []
    dry_run = False

    try:
        opts, args = getopt.getopt(argv, "c:d")
    except getopt.GetoptError:
        print("Invalid option: Use -c to specify the component(s) and -d for a dry run.")
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-c':
            components.append(arg)
        elif opt == '-d':
            dry_run = True

    if not components:
        print("Component(s) not specified. Use -c to specify the component(s).")
        sys.exit(1)

    current_dir = os.getcwd()
    target_file_path = os.path.join(current_dir, TARGET_FILE)

    removed_lines = []
    for division in ('system', 'vendor'):
        for component in components:
            component_file_path = os.path.join(current_dir, QCOM_COMMON_PATH, division, component, TARGET_FILE)
            if not os.path.isfile(component_file_path):
                continue

            with open(target_file_path, 'r') as target_file:
                lines = target_file.readlines()

            removed_lines += remove_lines_from_file(lines, component_file_path)

            if not dry_run:
                with open(target_file_path, 'w') as target_file:
                    target_file.write(''.join(lines))

    if removed_lines:
        print(f"The following lines {'would be removed from' if dry_run else 'were removed from'} the file '{target_file_path}':")
        for line in removed_lines:
            print(f"\033[31m- {line}\033[0m")
    else:
        print(f"No lines were removed from the file '{target_file_path}'.")

if __name__ == '__main__':
    main(sys.argv[1:])
