import json
import os
import urllib3
import time
from shutil import copyfile,rmtree
import threading

def readCommit(http,owner,repos,shaListPath):
    page=1
    while(True):
        url='https://api.github.com/repos/'+owner+'/'+repos+'/commits?per_page=100'
        result=getSHA1(http,url + '&page=' + str(page),shaListPath)
        page += 1
        print('page number is '+str(page))
        if(result==-1):
            return 1

def getSHA1(http,url,shaListPath):
    #os.popen('touch '+shaListPath+'/Sha')
    file=open(shaListPath+'/Sha','a+',encoding='utf8')
    #os.popen('touch ' + shaListPath + '/shaWithMessage')
    file2 = open(shaListPath+'/shaWithMessage', 'a+',encoding='utf8')
    if(True):
        #time.sleep(2)
        r = http.request('GET', url)
    
        data = json.loads(r.data)
        if(len(data)==0):
            return -1
        for commit in data:
            #print(commit)
            message=commit['commit']['message'].lower()
            keywords=['close','fix','resolve']
            is_bug=False
            for keyword in keywords:
                if((keyword in message) and (('bug' in message) or ('issue' in message))):
                    is_bug=True
                    break
            if(is_bug==True):
                sha=commit['sha']
                print('sha is '+sha)
                print('message is '+message)
                file.writelines(sha+'#True\n')
                file2.writelines(sha+'\n')
                file2.writelines(message+'\n')
            else:
                sha=commit['sha']
                file.writelines(sha+'\n')
                #time.sleep(30)
        file.close()
        file2.close()
     
        return 1
    else:
        print('there is an errora')
        file.close()
        file2.close()
       



def getDiff(projectPath,shaListPath,storePath):
    print('?????')
    file=open(shaListPath+'/Sha',encoding='utf8')
    shaList=file.readlines()
    file.close()
    os.chdir(projectPath)
    for i in range(len(shaList)):
        sha=shaList[i]
        
        if(len(sha.split('#'))>1):
            
            
            sha=sha.split('#')[0]
            os.chdir(projectPath)
            command=os.popen('git show '+sha)

            try:
                output=command.read()
            except:
                pass
            
            lines=output.split('\n')
            start=False
            currentfile=''
            filelist=[]
            isC=False
            containCode = False
            commitComment = True
            for line in lines:
                #print(line)
                if(line.startswith('diff --git')):
                    start=False
                if(start == False):
                    if(line.startswith('--') or line.startswith('++')):
                        suffix=(line.split('/')[-1]).split('.')[-1]
                        if((suffix=='c') or (suffix=='cpp') or (suffix=='h')):
                            isC=True
                            tmp= projectPath+line[5:]
                            if(tmp!=currentfile):
                                added=False
                                currentfile=tmp
                    if(line.startswith('@@')):
                        line=line.split('@@')[-1]
                        start=True
                #if(start and isC and containCode and (not commitComment) and (not added)):
                if(start and isC and (not added)):
                    filelist.append(currentfile)
                    added=True
            print(filelist) 
            os.chdir(projectPath)
            #time.sleep(1)

            
            if(len(filelist)>0):
                file4=open(shaListPath+'/changedfilelist','a+',encoding='utf8')
                file4.write(sha+'\n')
                file4.write(str(filelist)+'\n')
                file4.close()
                #x=input('input sth')
                x=os.popen('This is BEFORE  git reset --hard '+sha).read()
                print(x)
                print('This is BEFORE  git reset --hard '+sha)
                for file in filelist:
                    name=file.split('/')[-1]
                    aftername=storePath + '/' + sha +'#'+name+ '_after.c'
                    try:
                        copyfile(file,aftername)
                    except:
                        print("error file "+aftername)
                print('This is AFTER  git reset --hard '+shaList[i+1].split('#')[0])
                #x=input('input sth')
                os.chdir(projectPath)
                #time.sleep(1)
		
                x=os.popen('git reset --hard '+shaList[i+1].split('#')[0]).read()
                print(x)
                for file in filelist:
                    name=file.split('/')[-1]
                    beforename=storePath + '/' + sha +'#'+name+ '_before.c'
                    try:
                        copyfile(file,beforename)
                        print('gcc -E '+file+' -o '+beforename)    
                    except:
                        print('error file '+beforename)                              




















'''
        sha = sha[:-2]
        before = open(storePath + '/' + sha + '_before.c', 'w')
        after = open(storePath + '/' + sha + '_after.c', 'w')
        diff = open(storePath + '/' + sha + '_diff.c', 'w')
        containCode = False
        commitComment = True
        start=False
        isC=False
        try:

            command=os.popen('git show '+sha)
            output=command.read()
            lines=output.split('\n')
            for line in lines:
                if(line.startswith('diff --git')):
                    start=False
                if(start == False):
                    if(line.startswith('--') or line.startswith('++')):
                        suffix=(line.split('/')[-1]).split('.')[-1]
                        if((suffix=='c') or (suffix=='cpp') or (suffix=='h')):
                            isC=True
                    if(line.startswith('@@')):
                        line=line.split('@@')[-1]
                        start=True
                if(start):
                    if(line.startswith('@@')):
                        line="\n\n\n ##??Mark of a New File#  \n\n\n\n"+line.split('@@')[-1]
                    if((';' in line) and ('//' not in line)):   #Does the lines contain any code?
                        containCode=True
                    diff.writelines(line+'\n')
                    if(len(line)==0):
                        before.writelines('\n')
                        after.writelines('\n')
                    elif(line[0]=='-' and (not line.startswith('---'))):
                        if('//' not in line):                #Is only comment changed?
                            commitComment=False
                        before.writelines(' '+line[1:]+'\n')
                    elif(line[0]=='+' and (not line.startswith('+++'))):
                        if('//' not in line):
                            commitComment=False
                        after.writelines(' '+line[1:]+'\n')
                    else:
                        before.writelines(line + '\n')
                        after.writelines(line + '\n')
            if((not containCode) or commitComment or (not isC)):
                raise Exception()
            before.close()
            after.close()
            diff.close()
        except:
            before.close()
            after.close()
            diff.close()
            os.remove(storePath + '/' + sha + '_before.c')
            os.remove(storePath + '/' + sha + '_after.c')
            os.remove(storePath + '/' + sha + '_diff.c')
            continue
'''



def all(link):
    url = 'https://github.com/' + link
    DIC='/home/ubuntu/MLDATA/'
    struct=url.split('/')
    owner=struct[3]
    repos=struct[4]
    headers={'Authorization':'token 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',
             'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'}
    http = urllib3.PoolManager(headers=headers)
    projectPath = DIC+'repos/'+repos
    print('mkdir -p'+projectPath)
    os.popen('mkdir -p '+projectPath)
    shaListPath =DIC+'sha/'+repos
    os.popen('mkdir -p ' + shaListPath)
    storePath = DIC+'diff/'+repos
    os.popen('mkdir -p ' + storePath)
    os.popen('git clone '+url+' '+projectPath).read()

    #readCommit(http,owner,repos,shaListPath)
    getDiff(projectPath,shaListPath,storePath)
    #rmtree(projectPath)
    #generateDict(shaListPath)

if(__name__=='__main__'):
    x=input('filename')
    list=open('/home/ubuntu/MLDATA/'+x)
    lines=list.readlines()
    count=0
    lines=['2,openssl/openssl,2']
    for line in lines:
        name=line.split(',')[1]
        print('Current repos is '+name+'\n')
        all(name)


