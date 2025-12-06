#ifndef  SINGLETON_H
#define  SINGLETON_H

#include "Randomc.h"

using namespace std;

class Singleton{
public:
   static Singleton* Instance();
	TRandomMersenne *Rnd;
protected:
   Singleton();
private:
   static Singleton* _instance;
};

#endif
