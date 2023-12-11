import yachalk
import argparse
import sys
import exvenvded
print("Josiauhtools")
print(yachalk.chalk.red_bright("Unstabler ") + "0.0.3")
parser = argparse.ArgumentParser()
parser.add_argument("tool", help="The tool to use. If specified, the help will be dynamic.")

if (sys.argv[1] == "exvenvded"):
    parser.add_argument("subtool", help="The subtool to use.")

args = parser.parse_args()