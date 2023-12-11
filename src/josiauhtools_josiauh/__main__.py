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
    if (sys.argv[2] == "convert"):
        parser.add_argument("path", help="The path to work with. The default is the current directory.", default=".")

args = parser.parse_args()

if (args.tool == "exvenvded" and args.subtool == "convert"):
    exvenvded.convertToVenv(args.path)