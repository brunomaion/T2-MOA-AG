#include <string>
#include <math.h>
#include "Utils.h"
//----------------------------------------------------------------------------------------------
double BinStrToDouble(const string &Str){
int i, Size;
double Num;
	
	Num = 0;
	Size = (int)Str.length();
	
	for (i = 0; i < Size; ++i){
		if (Str[i] == '1') Num += pow(2, Size - i - 1);
	}
	
	return(Num);
}
//----------------------------------------------------------------------------------------------
int Particao(vector<Cromossomo> &Pop, int l, int r) {
int i, j;
Cromossomo Pivo, Temp;

   Pivo = Pop[l];
	i = l;
   j = r + 1;

	while (true){
		do{
         ++i;
      }while((i <= r) && (Pop[i].Fitness >= Pivo.Fitness));

		do{
         --j;
      }while(Pop[j].Fitness < Pivo.Fitness);

		if (i >= j) break;
		Temp = Pop[i];
      Pop[i] = Pop[j];
      Pop[j] = Temp;
	}

	Temp = Pop[l];
   Pop[l] = Pop[j];
   Pop[j] = Temp;
   return j;
}
//----------------------------------------------------------------------------------------------
void QuickSort(vector<Cromossomo> &Pop, int l, int r){
int j;

	if (l < r){
      j = Particao(Pop, l, r);
	   QuickSort(Pop, l, j - 1);
	   QuickSort(Pop, j + 1, r);
   }
}
//----------------------------------------------------------------------------------------------
