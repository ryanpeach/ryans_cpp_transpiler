// REF: https://www.tutorialspoint.com/cplusplus/cpp_pointers.htm
#include <iostream>

int foo(const int& asdf) {
   return asdf;
}

int main () {
   const int var1 = 5;
   int var2 = foo(5);        // actual variable declaration.
   int* ip;                  // pointer variable

   ip = &var2;               // store address of var in pointer variable

   std::cout << "Value of var variable: ";
   std::cout << var1 << std::endl;

   // print the address stored in ip pointer variable
   std::cout << "Address stored in ip variable: ";
   std::cout << ip << std::endl;

   // access the value at the address available in pointer
   std::cout << "Value of *ip variable: ";
   std::cout << *ip << std::endl;

   return 0;
}
