#!/usr/bin/python

import os, sys, glob, shutil

def _form_digit(num):
	if num < 10:
		return '00' + str(num)
	elif num >= 10 and num < 100:
		return '0' + str(num)
	else: return str(num)

def touch(prefix, num, ext ):
    '''
    Create up to 100 files in a well-formated form
    Usage: import myUtil myUtil.touch('b',10,'txt')
    '''
    num = int ( num)
    for i in range( num ):
        filename = prefix + _form_digit(i) + '.' + ext
        afile = open(filename,'w')
        afile.close()

def renameTail( old, new ):
    '''
    usb.xml -> usb-ja.xml
    '''
    for f in glob.glob('*.*'):
        os.rename( old, new)
    
def renameExt( old, new ):
    '''
    In current directory, usb.xml -> usb.txt
    '''
    for fileName in glob.glob('*.' + old):
        newFileName = os.path.splitext(fileName)[0]+ '.'+ new
        os.rename(fileName, newFileName)
        print "Renamed " + fileName + " to " + newFileName 



if __name__ == '__main__':
   # try:
    #    prefix = sys.argv[1]
     #   num =  sys.argv[2]
      #  ext =  sys.argv[3]
    #except:
     #   print "Usage:",os.path.basename(sys.argv[0]), "prefix number extension"
      #  print 'Example: ', os.path.basename(sys.argv[0]),'tmp 11 txt -> create tmp000.txt to tmp011.txt' ;
       # sys.exit(1)

    #touch(prefix, num, ext)
    renameExt('txt', 'dat')
