import os
import sys
import glob
import subprocess
import ntpath 
path1=os.path.dirname(os.path.abspath(__file__))
print (path1)  
for subdir,dirs,files in os.walk(path1):
     
     for file in files: 
       if not os.path.exists("temp"):
          new_dir=os.mkdir("temp")  
          
       base= os.path.basename(file)
       if file.endswith(".xz"):
          base=base[:-3]
          print(subdir)	
          cmd ="xz -dc "+subdir+"/"+file+" > "+path1+"/temp/"+base
          subprocess.call(cmd, shell= True) 
       elif file.endswith(".bz2"):
          base=base[:-4]
          print(subdir)	
          cmd1 ="bzip2 -cdk "+subdir+"/"+file+" > "+path1+"/temp/"+base
          subprocess.call(cmd1, shell= True)
       elif file.endswith(".gr"):
          base=base[:-3]
          cmd1 =subdir+"/"+file+" > "+path1+"/temp/"+base
          subprocess.call(cmd1, shell= True)		
       else:
          continue       
         
for root,dirs,files in os.walk("./temp"):
  for file in files:
     if file.endswith(".gr"): 
           base= os.path.basename(file)
           base=base[:-3]
           for r in range (1,6): 
              cmd1= path1+"/BFS.py -c "+str(2)+" -r "+str(2^r)+" "+"./temp/"+file+" >./temp/"+base+"_"+str(r)+".gr"  
              subprocess.call(cmd1,shell=True)    
            



 	
      
       
      
 




























