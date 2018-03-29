#!/usr/bin/python

import os 
import tarfile
import threading, zipfile
     
     
class  AsyncZip(threading.Thread):
    
def  __init__ (self, infile, outfile):
        threading.Thread. __init__ (self)        
        self.infile  =  infile
        self.outfile  =  outfile
def  run(self):
        state  =   ' w ' 
        if  os.path.isfile(self.outfile)  ==  True:
        state  =   ' a ' 
        f  =  zipfile.ZipFile(self.outfile, state, zipfile.ZIP_DEFLATED)
        f.write(self.infile)
        f.close()
         print   ' Finished background zip of:  ' , self.infile
        
def  zipDir(src,dst):
    
    initPath  =  os.getcwd()
    
    tempDST  =   os.path.join(os.getcwd(),dst)
    tempSRC  =   os.path.join(os.getcwd(),src)
    os.chdir( tempSRC )
    files  =  os.listdir(os.curdir)
    tar  =  tarfile.open( " temp.tar " , " w " )
     for  file  in  files:
        tar.add(file)#www.iplaypython.com

    tar.close()
    background  =  AsyncZip( " temp.tar " ,dst)
    background.start()
    background.join()     #  Wait for the background task to finish 
         
    os.chdir( initPath )
    print  os.getcwd()
 # test ok 
 if   __name__   ==   ' __main__ ' :
    
zipDir( " D:\\AutoUpdate\\DataDist\\viruswall\\Data\\KSVW-VirusDB\\ " , 
" d:\\AutoUpdate\\DataDist\\viruswall\\Data\\update\\KSVW-VirusDB.tgz " )
