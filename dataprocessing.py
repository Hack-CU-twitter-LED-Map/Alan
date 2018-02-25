#this is the data processing file
#this file is a small workspace for the data processing fuctions fuctions
#the fuctions will be inplemented in the datagetter.py file
import re
import time
def process(raw_tweet):
    raw_tweet= re.sub(r'[^\w\s]','',raw_tweet)
    raw_tweet=raw_tweet.lower()
    return raw_tweet

def main(): 
    start_time=time.time()
    positive=0
    negative=0
    posw =[None]* 2012
    negw= [None]* 2020
    ignorew =[None]*51
    count =0
    test_string= "#IWasOnTheDanceFloorWhen re-creating that jump-and-lift scene from Dirty Dancing seemed like a fun idea. Nope, wasn't...but I did meet some rather nice paramedics"
    f=open("poswords.txt", "r")
    for l in f:
        l=l.strip()
        posw[count]=l
        count+=1
    f.close()
    count=0
    f= open("negwords.txt")
    for l in f:
        l=l.strip()
        negw[count]=l
        count+=1
    f.close()
    count=0
    f=open("ignoreWords.txt")
    for l in f:
        l=l.strip()
        ignorew[count]=l
        count+=1
    f.close()
    tweet=process(test_string)
    tweet=tweet.split()
    for i in tweet:
        if i in ignorew:
            continue
        elif i in posw:
            print("pos",i)
            positive+=1
        elif i in negw:
            print("neg",i)
            negative-=1
    print(negative)
    print(positive)
    print ("Program Excicuted in ", time.time()-start_time)
    if positive>negative:
        return 1
    if negative>positive:
        return -1
    else:
        return 0

        
     


if __name__ == "__main__":
    main()