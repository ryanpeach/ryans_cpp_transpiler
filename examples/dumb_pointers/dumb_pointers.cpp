// REF: https://www.tutorialspoint.com/cplusplus/cpp_pointers.htm
#include <iostream>

using namespace std;

int main () {
   const int var = 20;   // actual variable declaration.
   mut dumb mut int ip;  // pointer variable 

   ip = addr var;        // store address of var in pointer variable

   cout << "Value of var variable: ";
   cout << var << endl;

   // print the address stored in ip pointer variable
   cout << "Address stored in ip variable: ";
   cout << ip << endl;

   // access the value at the address available in pointer
   cout << "Value of deref ip variable: ";
   cout << deref ip << endl;

   return 0;
}