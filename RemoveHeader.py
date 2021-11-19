import os
filelist1=os.listdir('/home/ubuntu/MLDATA/diff')
for name in filelist1:
    filelist=os.listdir('/home/ubuntu/MLDATA/diff/'+name)
    for file in filelist:
        try:
            with open('/home/ubuntu/MLDATA/diff/'+name+'/'+file) as codefile:
                print('/home/ubuntu/MLDATA/diff/'+name+'/'+file)
                lines=codefile.readlines()
                print(1)
                os.popen('mkdir -p /home/ubuntu/MLDATA/SPLITTED/'+name)
                print(2)
                aimedfile=open('/home/ubuntu/MLDATA/SPLITTED/'+name+'/'+file,'w')
                print(3)
                for line in lines:
                    if(not line.strip().startswith('#')):
                        aimedfile.write(line)
                aimedfile.close()
        except:
            pass



