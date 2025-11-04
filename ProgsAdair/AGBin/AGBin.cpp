#include <iostream>
#include <cmath>
#include "Randomc.h"
#include "AGBin.h"
#include "Utils.h"
#include "Singleton.h"

using namespace std;

//----------------------------------------------------------------------------------------------
// Rotina para mutar aleatoriamente os alelos de um Gene. Recebe como parâmetro a taxa de
// mutação
//----------------------------------------------------------------------------------------------
void Gene::Mutate(const float &TxMut){
int i;
Singleton *S = S->Instance();

   //Mutação aplicada em um alelo de cada gene
   if (S->Rnd->Random() < TxMut){
      i = S->Rnd->IRandom(0, Alelos.size());
      if (Alelos[i] == '0') Alelos[i] = '1';
      else Alelos[i] = '0';
   }
}

//----------------------------------------------------------------------------------------------
// Rotina para efetuar o crossover em um ponto entre genes. Recebe como parâmetros a taxa de
// crossover e o cromossomo com o qual o cromossomo corrente deverá compartilhar bits
//----------------------------------------------------------------------------------------------
void Gene::Crossover(const float &TxCruz, const Gene &Gene2){
int i, PCorte;
string Tmp1, Tmp2;
Singleton *S = S->Instance();

   if (S->Rnd->Random() < TxCruz){
		PCorte = S->Rnd->IRandom(0, Tamanho - 1);

		for (i = PCorte; i < Tamanho; ++i){
			Alelos[i] = Gene2.Alelos[i];
		}
	}
}

//----------------------------------------------------------------------------------------------
// Calcula o equivalente decimal do gene e seu valor escalonado
//----------------------------------------------------------------------------------------------
void Gene::Eval(){
int i;
	Valor = 0;
	for (i = 0; i < Tamanho; ++i){
      if (Alelos[i] == '1') ++Valor;
	}
}

//----------------------------------------------------------------------------------------------
// Destrutor do Gene - Zera as propriedades do Gene
//----------------------------------------------------------------------------------------------
Gene::~Gene(){
	Tamanho = 0;
	Alelos = "";
}

//----------------------------------------------------------------------------------------------
// Construtor do Gene - Um Gene é uma string de 0's e 1's que codificam um valor qualquer
//----------------------------------------------------------------------------------------------
Gene::Gene(const int &Tam){
int i;
Singleton *S = S->Instance();

	Tamanho = Tam;
	Alelos.resize(Tam);

	for (i = 0; i < Tam; ++i){
		if (S->Rnd->IRandom(1, 100) <= 90) Alelos[i] = '0';
		else Alelos[i] = '1';
	}
};

//----------------------------------------------------------------------------------------------
// Efetua o crossover do cromossomo realizando o crossover dos genes
//----------------------------------------------------------------------------------------------
void Cromossomo::Mutate(const float &TxMut){
int i;

   for (i = 0; i < NumGenes; ++i){
		Cromo[i].Mutate(TxMut);
	}
}

//----------------------------------------------------------------------------------------------
// Efetua o crossover do cromossomo realizando o crossover dos genes
//----------------------------------------------------------------------------------------------
void Cromossomo::Crossover(const float &TxCruz, const Cromossomo &Crom){
int i;

   for (i = 0; i < NumGenes; ++i){
		Cromo[i].Crossover(TxCruz, Crom.Cromo[i]);
	}
}

//----------------------------------------------------------------------------------------------
// Cálculo do Fitness do Cromossomo
//----------------------------------------------------------------------------------------------
void Cromossomo::Eval(){
int i;

   Fitness = 0;
   for (i = 0; i < NumGenes; ++i){
      Cromo[i].Eval();
      Fitness += Cromo[i].Valor;
   }
}

//----------------------------------------------------------------------------------------------
// Destrutor do Cromossomo. Desaloca todos os genes criados.
//----------------------------------------------------------------------------------------------
Cromossomo::~Cromossomo(){
	Cromo.resize(0);
}

//----------------------------------------------------------------------------------------------
// Construtor do Cromossomo. Com os parâmetros dos genes setados em Ctrl cria o cromossomo.
//----------------------------------------------------------------------------------------------
Cromossomo::Cromossomo(const int &NGenes, const vector<TDefGene> &Ctrl){
int i;

	NumGenes = NGenes;
	Cromo.resize(NumGenes);
	for (i = 0; i < NumGenes; ++i) Cromo[i] = Gene(Ctrl[i].Tam);
};

//----------------------------------------------------------------------------------------------
// Realiza a seleção de indivíduos da população para aplicar os operadores genéticos
//----------------------------------------------------------------------------------------------
int Genetico::Selecao(const double &SumFit){
float Aleat, Parcela;
int i;
Singleton *S = S->Instance();

   Aleat = S->Rnd->Random() * SumFit;
	Parcela = 0;
	i = -1;

	do {
      ++i;
      Parcela += (Populacao[i].Fitness + FatorTrans);
   }while ((Parcela < Aleat) && (i < (TamPop - 1)));

	return(i);
}

//----------------------------------------------------------------------------------------------
// Realiza a evolução da população atual. Aplicando os operadores genéticos.
//----------------------------------------------------------------------------------------------
void Genetico::EvolPop(){
double SumFit;
int i, TamNPop, CSel1, CSel2;
vector<Cromossomo> NPopulacao;
Singleton *S = S->Instance();

   //Inicializa vetor da nova população
   NPopulacao.resize(TamPop);
	//Copia os elementos da elite
	for (i = 0; i < TamElite; ++i) NPopulacao[i] = Populacao[i];
	TamNPop = TamElite;
	//Calcula o somatório do Fitness - Processo de seleção
	SumFit = 0;

	for (i = 0; i < TamPop; ++i){
		//A adição do fator de translação elimina o problema decorrente de fitness negativo
		SumFit += (Populacao[i].Fitness + FatorTrans);
	}

	//Cruza elementos da população atual até completar a nova população
	while (TamNPop < TamPop){
	   //Seleciona dois indivíduos distintos da população para realizar o cruzamento
		do{
			CSel1 = Selecao(SumFit);
			CSel2 = Selecao(SumFit);
		}while (CSel1 == CSel2);

		//Cruza o indivíduo CSel1 com CSel2
		NPopulacao[TamNPop] = Populacao[CSel1];
		NPopulacao[TamNPop].Crossover(TxCruz, Populacao[CSel2]);
		++TamNPop;

		//Se ainda couber mais um indivíduo na nova população
		if (TamNPop < TamPop){
			NPopulacao[TamNPop] = Populacao[CSel2];
			//Cruza o indivíduo CSel2 com CSel1
			NPopulacao[TamNPop].Crossover(TxCruz, Populacao[CSel1]);
			++TamNPop;
		}
	}

	//Realiza a mutação da nova população
	for (i = TamElite; i < TamPop; ++i) NPopulacao[i].Mutate(TxMut);

	//Copiando a nova população
	for (i = 0; i < TamPop; ++i) Populacao[i] = NPopulacao[i];
}
//----------------------------------------------------------------------------------------------
// Faz a avaliação da população atual, identificando o melhor indivíduo
//----------------------------------------------------------------------------------------------
void Genetico::EvalPop(){
int i;

	++NumGer;
   ++Parada;
   for (i = 0; i < TamPop; ++i) Populacao[i].Eval();
	QuickSort(Populacao, 0, TamPop - 1);

	FatorTrans = 0;
	if (Populacao[TamPop - 1].Fitness < 0) FatorTrans = abs(Populacao[TamPop - 1].Fitness);

	if (Populacao[0].Fitness > GBest.Fitness){
		GBest = Populacao[0];
		Parada = 0;
	}
}
//----------------------------------------------------------------------------------------------
// Cria a população inicial de indivíduos
//----------------------------------------------------------------------------------------------
void Genetico::CreatePop(){
int i;

	Populacao.resize(TamPop);
	for (i = 0; i < TamPop; ++i){
		Populacao[i] = Cromossomo(NumGenes, DefCromo);
	}
};
//----------------------------------------------------------------------------------------------
// Construtor do Algoritmo Genético. Prepara variáveis de controle.
//----------------------------------------------------------------------------------------------
Genetico::Genetico(const int &TPop, const int &NGenes, const vector<TDefGene> &Ct,
						 const int &NIElite, const float &TxC, const float &TxM, const int &Ngse){

   TamPop = TPop;
	NumGenes = NGenes;
	DefCromo = Ct;
	TamElite = NIElite;
	TxCruz = TxC/100.0;
	TxMut = TxM/100.0;
	NumGerEst = Ngse;
	GBest.Fitness = -1e100;
	Parada = 0;
	NumGer = 0;
}
