// this file is used to copy and paste from one flie to another for formatting
// this is verry ineffcient but i dont have a faster way of reformatting the file the way i need it
// to be.
#include<iostream>
#include<sstream>
#include<fstream>
#include<stdlib.h>
#include<time.h>
using namespace std;

void countwords()
{
    ifstream datafile;
    int count=0;
    string array[2391];
    string word;
    int index;
    datafile.open("holder.txt");
    while(!datafile.eof())
    {
        datafile>>word;
        if(index%2==0)
        {
            array[count]=word;
            count++;
        }
        index++;
    }
    datafile.close();
    int num;
    cout<< "#"<< endl;
    cout<< "file has been read"<< endl;
    cout<< "#"<< endl;
     for(int i=0;i<386; i++)
    {
        srand(time(NULL));
        num= rand() % 386+1;
        if(array[num]!="")
        {
            cout<< "editing item "<<i<< " of 368" << endl;
            array[num]="";
        }
        else
        {
            i--;
        }

    }
    cout<< "#"<< endl;
    cout<< "array editing complete"<< endl;
    cout<< "#"<< endl;
    cout<< "writing to negwords.txt"<<endl;
    ofstream outfile("negwords.txt");
    for(int i=0;i<2391;i++)
    {
        if(array[i]!="")
        {
            outfile<<array[i]<<endl;
        }
    }
}


int main(void)
{
    countwords();
}