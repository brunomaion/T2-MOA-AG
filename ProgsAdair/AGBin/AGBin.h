#ifndef  GENETICO_H
#define  GENETICO_H

#include <string>
#include <vector>
#include "Randomc.h"

using namespace std;

//----------------------------------------------------------------------------------------------
//Estrutura que define a formatação de cada gene que comporá um cromossomo
//----------------------------------------------------------------------------------------------
typedef struct St_DefGene{
	int Tam;    //Quantos bits serão usados no gene
}TDefGene;


class Gene{
public:
	string Alelos; //Cadeia de 0s e 1s que codificam um valor
	int Tamanho;   //Comprimento máximo da cadeia de Alelos
	double Valor;  //Valor associado ao gene

	Gene(){}
	Gene(const int &Tam); //Gera os alelos binários
	void Eval();
	void Crossover(const float &TxC, const Gene &Gene2);
	void Mutate(const float &TxM);
	~Gene();
};

class Cromossomo{
public:
	int NumGenes;        //Número de genes no cromossomo
   vector <Gene> Cromo; //Um cromossomo com N genes de acordo com a Estrutura
	double Fitness;      //Aptidão do cromossomo

	Cromossomo(){}
	Cromossomo(const int &NGenes, const vector<TDefGene> &Ctrl);
	~Cromossomo();
	void Eval();
	void Crossover(const float &TxC, const Cromossomo &Crom);
	void Mutate(const float &TxM);
};

class Genetico{
private:
	double FatorTrans;
public:
	int TamPop, NumGenes, NumGerEst, TamElite, NumGer, Parada;
	float TxCruz, TxMut;
	vector<TDefGene> DefCromo;
	vector<Cromossomo> Populacao;
	Cromossomo GBest;

	Genetico(const int &TPop, const int &NGenes, const vector<TDefGene> &Ct, const int &NIElite,
				const float &TxC, const float &TxM, const int &Ngse);
	~Genetico();
	void CreatePop();
   void EvalPop();
	int Selecao(const double &SumFit);
	void EvolPop();
};

#endif
