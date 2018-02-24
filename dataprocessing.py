#this is the data processing file
#this file is a small workspace for the data processing fuctions fuctions
#the fuctions will be inplemented in the datagetter.py file
def process(raw_tweet):
    
def main(): 
    posw =[None]* 2005
    negw= [None]* 2005
    ignorew =[None]*50
    count =0
    test_string= " I like pizza of all kinds except pinnaple, I hate pinnale pizza. It is truly awful. But what I really like is ice cream. its the best."
    f=open("poswords.txt", "r")
    for l in f:
        posw[count]=l
        count+=1
    f.close()
    count=0
    f= open("negwords.txt")
    for l in f:
        negw[count]=l
        count+=1
    f.close()
    count=0
    f=open("ignoreWords.txt")
    for l in f:
        ignorew[count]=l
        count+=1
    f.close()
    print("files have been read")


if __name__ == "__main__":
    main()