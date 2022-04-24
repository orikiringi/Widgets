import os
import shutil
import threading
import time

inputdir="/home/oriki/Desktop/MNParser/Data"
targetfd="/home/oriki/Desktop/MNParser/ImportNotMain/DataCarsh/JS-safefil-sample"
cal=0
tarcount=1

def walkFile(file):
    count=0
    for root, dirs, files in os.walk(file):
        for filein in files:
            filename=os.path.join(root, filein)
            #print(filename)
            if filename.split("/")[-1].split(".")[-1] == "js" or filename.split("/")[-1].split(".")[-1] == "HPOscript":
                count+=1
    return count

print("Total of documents counted.....")
allfiles=walkFile(inputdir)
print("Total of documents : %s" % allfiles)

def copyfile():
    for root, dirs, files in os.walk(inputdir):
        for filein in files:
            """ filename=os.path.join(root, filein)
            if filename.split("/")[-1].split(".")[-1] == "js":
                print("Process Copy %3d%% [%d/%d] : %s" % (cal,tarcount,allfiles,filename))
                shutil.copy(filename,targetfd) """
            if filein.split(".")[-1] == "js" or filein.split(".")[-1] == "HPOscript":
                mvpath=os.path.join(root, filein)
                if os.path.exists(mvpath):
                    print("Process Copy %3d%% [%d/%d] : %s" % (cal,tarcount,allfiles,mvpath))
                    shutil.copy(mvpath,targetfd)
                    #os.rename(targetfd+filein,targetfd+filein.split(".")[0])
    print("Process Copy %3d%% [%d/%d] : %s" % (len(os.listdir(targetfd))/allfiles*100,len(os.listdir(targetfd)),allfiles,os.path.join(root, filein)))

def copytotal():
    global cal,tarcount
    tarcount=cal=0
    while (len(os.listdir(targetfd)) != allfiles):
        tarcount=len(os.listdir(targetfd))+2
        cal=tarcount/allfiles*100

def nothread():
    global tarcount
    for root, dirs, files in os.walk(inputdir):
        for filein in files:
            if filein.split(".")[-1] == "js" or filein.split(".")[-1] == "HPOscript":
                mvpath=os.path.join(root, filein)
                if os.path.exists(mvpath):
                    print("Process Copy %3d%% [%d/%d] : %s" % (tarcount/allfiles*100,tarcount,allfiles,mvpath))
                    shutil.copy(mvpath,targetfd)
                    os.rename(targetfd+filein,targetfd+filein.split(".")[0])
                    tarcount+=1
    tarcount=1

if __name__=="__main__":
    if allfiles < 1000:
        timestamps=time.time()
        nothread()
        timestampe=time.time()
    else:
        if not os.path.exists(inputdir):
            print("[Error] : Not exists Meta folder.")
            exit()
        if not os.path.exists(targetfd):
            os.mkdir(targetfd)
        timestamps=time.time()
        thread2copy=threading.Thread(target=copyfile,name="t2copy")
        thread2cont=threading.Thread(target=copytotal,name="t2cont")
        thread2copy.start()
        thread2cont.start()
        thread2copy.join()
        thread2cont.join()
        timestampe=time.time()
    total=timestampe-timestamps
    print("Process Total Time : %dday, %dhour, %dmin, %dsec." % (int(total/86400),int((total-int(total/86400)*86400)/3600),int((total-int(total/86400)*86400-int((total-int(total/86400)*86400)/3600)*3600)/60),total-int(total/86400)*86400-int((total-int(total/86400)*86400)/3600)*3600-int((total-int(total/86400)*86400-int((total-int(total/86400)*86400)/3600)*3600)/60)*60))
