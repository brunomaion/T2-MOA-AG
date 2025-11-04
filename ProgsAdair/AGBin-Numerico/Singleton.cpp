#include <ctime>
#include "Singleton.h"

using namespace std;

Singleton* Singleton::_instance = 0;

Singleton:: Singleton(){
   Rnd = new TRandomMersenne(time(0));
}

Singleton* Singleton::Instance(){
   if (_instance == 0) _instance= new Singleton;
   return _instance;
}
