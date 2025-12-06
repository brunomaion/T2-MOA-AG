#include <conio.h>
#include <stdlib.h>
#include <ctime>
#include <iostream>
#include <vector>
#include <iomanip>
#include <fstream>
#include "AGBin.h"
#include "Singleton.h"
#include "Utils.h"

using namespace std;

int main(){
int i, j, NExec, TPop, NGenes, Ngse, NIElite;
float TC, TM;
vector<TDefGene> Ct;
clock_t STime, ETime, ExecTime;
fstream FOut;
Singleton *S = S->Instance();
Genetico *G;

	FOut.open ("OutPut.txt", fstream::out | fstream::app);
   cout << setiosflags(ios::fixed) << setprecision(8);

	//Entrando com os parâmetros do Algoritmo Genético
	cout << "Numero de execucoes: ";
	cin >> NExec;
	cout << endl;
	cout << "Numero de individuos na populacao inicial: ";
	cin >> TPop;
	cout << "Numero de genes no cromossomo: ";
	cin >> NGenes;
	cout << endl;
	Ct.resize(NGenes);

	for (i = 0; i < NGenes; ++i){
		cout << "  Tamanho do gene " << i + 1 << ": ";
		cin >> Ct[i].Tam;
		cout << endl;
	}

	cout << "Numero de individuos na elite: ";
	cin >> NIElite;
	cout << "Taxa de cruzamento: ";
	cin >> TC;
	cout << "Taxa de mutacao: ";
	cin >> TM;
	cout << "Numero de geracoes sem evolucao: ";
	cin >> Ngse;

	//Gravando log --> Header de cada lote de execuções
	FOut << "Numero de execucoes:\t" << NExec << endl;
	FOut << "Tamanho da populacao inicial:\t" << TPop << endl;
	FOut << "Numero de genes:\t" << NGenes << endl;

	for (i = 0; i < NGenes; ++i){
		FOut << "\tTamanho do gene " << i + 1 << ": \t" << Ct[i].Tam << endl;
	}

	FOut << "Tamanho da elite:\t" << NIElite << endl;
	FOut << "Taxa de cruzamento:\t" << TC << endl;
	FOut << "Taxa de mutacao:\t" << TM << endl;
	FOut << "Numero de geracoes sem evolucao:\t" << Ngse << endl << endl;

	for (i = 0; i < NExec; ++i){
		//Inicializando o algoritmo Genético
		STime = clock();
		G =  new Genetico(TPop, NGenes, Ct, NIElite, TC, TM, Ngse);
		G->CreatePop(); //Criando a população inicial
		G->EvalPop(); //Avaliando a população inicial

		while (G->Parada < G->NumGerEst){
			G->EvolPop();
			G->EvalPop();
		}

		ETime = clock();
		ExecTime = ETime - STime;

		//Gravando log --> Melhor solução
		FOut << "Solucao:\t" << i << endl;

		for (j = 0; j < NGenes; ++j){
			FOut << "\tGene:\t" << j << endl;
			FOut << "\t\tAlelos:\t" << G->GBest.Cromo[j].Alelos << endl;
			FOut << "\t\tValor :\t" << G->GBest.Cromo[j].Valor << endl;
		}

		FOut << "\tFitness:\t" << G->GBest.Fitness << endl;
		FOut << "\tNumero de geracoes:\t" << G->NumGer << endl;
		FOut << "\tTempo:\t" << ExecTime << endl << endl;
		free(G);
	}

	FOut.close();
	cout << endl << endl << "Pressione <Enter> para encerrar!";
	getche();
}
