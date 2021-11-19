import csv
import sys


def main():

    file=open('/Users/zhipengzhang/dataset-small.csv')
    aimed_file=open('/Users/zhipengzhang/simpleset.csv','w')
    csvwriter=csv.writer(aimed_file,delimiter='@')
    csvwriter = csv.writer(aimed_file)
    csv_format=csv.reader(file,delimiter='@')
    csv.field_size_limit(sys.maxsize)
    begin=False
    x = 0
    for record in csv_format:
        if(begin):
            id = record[0]
            buggy_code = record[1].splitlines(keepends=False)
            patched_code = record[2].splitlines(keepends=False)
            index = eval(record[3])  #begin location list
            removed = eval(record[4])
            added=eval(record[5])

            if(isinstance(index,list)):
                for bug_index in range(len(index)):
                    before=index[bug_index]
                    after=before+removed[bug_index]
                    before-=5
                    after+=5
                    if(before<0):
                        before=0
                    if(after>=len(buggy_code)):
                        after=len(buggy_code)-1
                    print('Bug Location ',index[bug_index],' Bug End ',index[bug_index]+removed[bug_index],' scope ',[before,after])
            elif(isinstance(index,int)):
                before=index-5
                if(before<0):
                    before=0
                strbefore=''
                for line in buggy_code[before:index]:
                    strbefore+=line+'\n'
                strbug=''
                for line in buggy_code[index:index+removed]:
                    strbug+=line+'\n'
                print(strbug)
                strpatch=''
                for line in patched_code[index:index+added]:
                    strpatch+=line+'\n'
                print(strbug+'\n\n\n\n\n\n')
                if(strbug!=''):
                    csvwriter.writerow([id,strbefore,strbug,strpatch])

                print(x)
                x+=1

        else:
            begin=True
            csvwriter.writerow(['id','before','buggy_code','patched_code'])
    aimed_file.close()
    file.close()



if __name__=='__main__':
    main()
