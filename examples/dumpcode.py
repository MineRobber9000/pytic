from pytic import TICFile
from pytic.objects import CodeBlock
import argparse

parser = argparse.ArgumentParser(description="Prints code from .tic file.")
parser.add_argument("file",help=".tic file")
args = parser.parse_args()

tf = TICFile.from_file(args.file)
code = ""
for block in tf.blocks:
	if type(block)==CodeBlock:
		code+=block.content
print(code)
