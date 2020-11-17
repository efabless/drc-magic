# Copyright 2020 Efabless Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import argparse
import subprocess
from pathlib import Path


def gds_drc_check(design_name,pdk, target_type, output_directory='/usr/local/bin/drc_checks'):
    path=Path( str(os.getenv('TARGET_DIR'))+"/"+design_name+".gds")
    if not os.path.exists(path):
        return False,"GDS not found"
    run_drc_check_cmd = "sh /usr/local/bin/run_drc_checks.sh {design_name} {pdk} {target_type} {output_directory}".format(
        design_name=design_name,
        pdk=pdk,
        target_type=target_type,
        output_directory=output_directory
    )

    print("Running DRC Checks...")

    process = subprocess.Popen(run_drc_check_cmd.split(), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        while True:
            output = process.stdout.readline()
            if not output:
                break
            if output:
                print("\r"+str(output.strip())[2:-1])
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode(sys.getfilesystemencoding())
        return False, str(error_msg)

    drcFileOpener = open(output_directory + '/' + design_name + '.magic.drc')
    if drcFileOpener.mode == 'r':
        drcContent = drcFileOpener.read()
    drcFileOpener.close()

    splitLine = '----------------------------------------'

    # design name
    # violation message
    # list of violations
    # Total Count:
    if drcContent is None:
        return False, "No DRC report generated..."
    else:
        drcSections = drcContent.split(splitLine)
        if (len(drcSections) == 2):
            return True, "0 DRC Violations"
        else:
            vioDict = dict()
            for i in range(1, len(drcSections) - 1, 2):
                vioDict[drcSections[i]] = len(drcSections[i + 1].split("\n"))
            cnt = 0
            for key in vioDict:
                val = vioDict[key]
                cnt += val
                print("Violation Message \"" + str(key.strip()) + " \"found " + str(val) + " Times.")
            return False, "Total # of DRC violations is " + str(cnt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Runs a magic drc check on a given GDSII.')

    parser.add_argument('--design_name', '-d', required=True,
                        help='Design Name')
    parser.add_argument('--pdk', '-p', default='sky130A',
                    help='PDK used. Default = sky130A')
    parser.add_argument('--target_type', '-tt', default='gds',
                    help='Target type: gds, mag, def. Default = gds')
    parser.add_argument('--output_directory', '-o', required=False,
                        help='Output Directory. Default = $TARGET_DIR/drc_checks')

    args = parser.parse_args()
    design_name = args.design_name
    pdk = args.pdk
    target_type = args.target_type
    if args.output_directory is None:
        output_directory = str(os.getenv('TARGET_DIR'))+ '/drc_checks'
    else:
        output_directory = args.output_directory

    _, txt=gds_drc_check(design_name, pdk, target_type, output_directory)
    print(txt)
