#ifndef  UTILS_H
#define  UTILS_H

#include <string>
#include <vector>
#include "AGBin.h"

using namespace std;

double BinStrToDouble(const string &Str); //Converte uma string binária para seu equivalente numérico
void QuickSort(vector<Cromossomo> &Pop, int l, int r); //Ordena a populacao pelo Fitness crescente
#endif
