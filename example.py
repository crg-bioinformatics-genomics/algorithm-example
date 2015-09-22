#!/usr/bin/env python
import argparse
import yaml
import os
import subprocess
import shutil, errno
import sys

# we want to be agnostic to where the script is ran
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
WORKER_PATH = os.path.realpath(os.curdir)

# Function to copy the output directory content
def copyfolder(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise
        
# read the task definition yaml file
with open(os.path.join(SCRIPT_PATH, "example.yaml"), "r") as task_f:
    task_definition = yaml.load(task_f)

parser = argparse.ArgumentParser(
   description='Launches example algorithm with properly parset parameters')

parser.add_argument(
   '-output_dir', type=str, nargs=1,
   help='Directory where the output is going to be stored')

# accept form fields
for item in task_definition['form_fields']:
   nargs = 1 if item['required'] else "?"
   parser.add_argument(
       '-FORM%s'%item['name'], type=str, default="none", nargs=nargs,
       help='Form argument: %s' % item)

# this parse_args stops if any unexpected arguments is passed
args = parser.parse_args()

OUTPUT_PATH = os.path.join(WORKER_PATH, args.output_dir[0])
random_number = (""" "{}" """.format(args.output_dir[0])).split("/")[3]

TMP_PATH = SCRIPT_PATH+"/tmp/"+random_number
if os.path.exists(TMP_PATH) == True:
    shutil.rmtree(TMP_PATH)
copyfolder(SCRIPT_PATH+"/template", TMP_PATH)

import re
import StringIO
from Bio import SeqIO
Ppat = re.compile('>.*?\n[ARNDCQEGHILKMFPSTWYV]+', re.IGNORECASE)
if Ppat.match(args.FORMprotein_seq[0]) == None:
	args.FORMprotein_seq[0] = ">input_protein\n"+args.FORMprotein_seq[0]
protSeq = []
for record in SeqIO.parse(StringIO.StringIO(args.FORMprotein_seq[0]), "fasta"):
	protSeq.append(record)

#protFile = os.path.join(OUTPUT_PATH.replace("output/", ""),"protein.fasta")
protFile = TMP_PATH+"/prot.fa"
output_handle = open(protFile, "w")
SeqIO.write(protSeq, output_handle, "fasta")
output_handle.close()

os.chdir(SCRIPT_PATH)

args.FORMtitle = "".join([t.replace(' ', '_') for t in args.FORMtitle])

command = """ bash example.sh "{}" "{}" "{}" """.format(protFile,args.FORMfeature[0],random_number)

p = subprocess.Popen(command, cwd=SCRIPT_PATH, shell=True)
p.communicate()

# import IPython
# IPython.embed()

if p.returncode == 0:
	TMP_PATH = SCRIPT_PATH+ "/tmp/"+ random_number+"/outputs/"
    
	dirList=os.listdir(TMP_PATH)
	for file in dirList:
		shutil.copyfile(TMP_PATH+file, OUTPUT_PATH+file)
	
	from django.template import Template
	from django.template import Context
	from django.conf import settings
	from django.template import Template
	
	settings.configure(TEMPLATE_DIRS=(os.path.join(SCRIPT_PATH,'./')), DEBUG=True, TEMPLATE_DEBUG=True)
	
	# read the template file into a variable
	with open(os.path.join(SCRIPT_PATH, "index.example.html"), "r") as template_file:
	   template_string = "".join(template_file.readlines())
	
	import datetime
	
	# create template from the string
	t = Template(template_string)
	
	# context contains variables to be replaced
	c = Context(
	   {
		   "title": args.FORMtitle,
		   "randoms" : random_number,
		   "feature" : args.FORMfeature[0],
		   "generated" : str(datetime.datetime.now()),
	   }
	)
	
	# and this bit outputs it all into index.html
	with open(os.path.join(OUTPUT_PATH, "index.html"), "w") as output: 
	   output.write(t.render(c))
	   
else:
	sys.exit("The execution of the C code  failed.")
