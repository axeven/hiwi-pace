import os
import sys
import glob
import subprocess
import ntpath 
import shutil


"Getting the path of the file"
path1=os.path.dirname(os.path.abspath(__file__))
print (path1)  

##"Traversing through all  the directories and sub-directories"
for subdir,dirs,files in os.walk(path1):
     
     for file in files: 
       ##"Taking the base name"
       base= os.path.basename(file) 

       ##".gr files needed to be extracted from the zipped .xz files  and creating the directory in the task3_output folder "
     
       if file.endswith(".xz"):
          base=base[:-3]         
          subfolder=subdir[len(path1):len(subdir)] 
          index_begin= subfolder.find("task3_input/")+len("task3_input/")
          index_end= subfolder.find("/",index_begin)
          if index_end==-1:
            index_end=len(subfolder)
          else:
            index_end=index_end
          if not os.path.exists(path1+"/task3_output/"+subfolder[index_begin:index_end]):
                  os.mkdir(path1+"/task3_output/"+subfolder[index_begin:index_end])
          else:
              index_end=index_end
         	
          cmd ="xz -dc "+subdir+"/"+file+" > "+path1+"/task3_output/"+subfolder[index_begin:index_end]+"/"+base
          subprocess.call(cmd, shell= True) 

       ##".gr files needed to be extracted from the zipped .bz2 files  and creating the directory in the task3_output folder "   

       elif file.endswith(".bz2"):
          base=base[:-4]
          subfolder=subdir[len(path1):len(subdir)]	
          index_begin= subfolder.find("task3_input/")+len("task3_input/")
          index_end= subfolder.find("/",index_begin)
          if index_end==-1:
            index_end=len(subfolder)
          else:
            index_end=index_end
          if not os.path.exists(path1+"/task3_output/"+subfolder[index_begin:index_end]):
                  os.mkdir(path1+"/task3_output/"+subfolder[index_begin:index_end])  
          else:
                  index_end=index_end         	
          cmd1 ="bzip2 -cdk "+subdir+"/"+file+" > "+path1+"/task3_output/"+subfolder[index_begin:index_end]+"/"+base
          subprocess.call(cmd1, shell= True)

       elif file.endswith(".gr"):
          base=base[:-3]
          subfolder=subdir[len(path1):len(subdir)]	
          index_begin= subfolder.find("task3_input/")+len("task3_input/")
          index_end= subfolder.find("/",index_begin)
          if index_end==-1:
            index_end=len(subfolder)
          else:
            index_end=index_end
          ##"Creating directory same name as input file"
          if not os.path.exists(path1+"/task3_output/"+subfolder[index_begin:index_end]):
                  os.mkdir(path1+"/task3_output/"+subfolder[index_begin:index_end]) 
  
          else:
                  index_end=index_end    
          if not subdir.find("task3_input/")==-1:   	
            copy1= "cp"+" "+subdir+"/"+file+" "+path1+"/task3_output/"+subfolder[index_begin:index_end]	
            subprocess.call(copy1, shell= True)	
       else:
          continue       


##"Implementing BFS.py over all the .gr files "        
for subdir,dirs,files in os.walk(path1+"/task3_output"):
  for file in files:
     if file.endswith(".gr"): 
           base= os.path.basename(file)
           base=base[:-3]
           for r in range (1,6): 
              cmd1= path1+"/BFS.py -c  -r "+str(2**r)+" "+subdir+"/"+file+" >"+subdir+"/"+base+"_"+str(r)+".gr"  
              subprocess.call(cmd1,shell=True)    
            



 	
      
       
      
 




























