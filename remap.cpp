// this file is used to copy and paste from one flie to another for formatting
#include<iostream>
#include<sstream>
#include<fstream>
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

}


int main(void)
{
    countwords();
}