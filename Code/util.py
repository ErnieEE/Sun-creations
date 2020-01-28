import os
import sys
import zipfile

def convert2csv(filename):
	print('convert2csv ', filename)
	#result = subprocess.call(["C:\Program Files\LibreOffice\program\soffice", "--headless", "--convert-to", "csv", "--infilter=CSV:44,34,76,1,,,true", filename])
	#command = '"C:\Program Files\LibreOffice\program\soffice",  "--convert-to", "csv", "--infilter=CSV:44,34,76,1,,,true", '+ filename
	#print(command)
	result = subprocess.call(["C:\Program Files\LibreOffice\program\soffice",  "--convert-to", "csv", "--infilter=CSV:44,34,76,1,,,true", filename])
	print('convert2csv ', result)

def convert2ods(filename):	
	print('convert2ods ', filename)
	result = subprocess.call(["C:\Program Files\LibreOffice\program\soffice", "--headless", "--convert-to", "ods", "--infilter=CSV:44,34,76,1,,,true", filename])
	print('convert2ods ', result)
	

def convert2ods(filename):  
    print('convert2ods ', filename)
    result = subprocess.call(["C:\Program Files\LibreOffice\program\soffice", "--headless", "--convert-to", "ods", "--infilter=CSV:44,34,76,1,,,true", filename])
    print('convert2ods ', result)
  
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def zipdir(path, name):
    zf = zipfile.ZipFile(name, "w")
    for dirname, subdirs, files in os.walk(path):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()

def printhi(x):    
    print('hi',x)
    print(sys.version_info[0])
    print(sys.version_info)
    
zipdir("dist", "dist\724.zip")