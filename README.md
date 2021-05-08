# Ryan's CPP Transpiler

Hot Take: C++ is a terrible language.

If that statement resonates with you, you will probably love to both use and contribute to this project.

Imagine this scenario. You HATE C++. It's backwards compatibility has made it a total mess of a language
with each new version. However, you have to use C++ for your job, or your peers have stockholm syndrome
and don't want to switch to objectively better languages (tongue and cheek of course).

This project is probably for you.

We are defining a C++ transpiler that can go back and forth between C++ 14-16 and this new (unnamed) intermediary language. I have a few goals to make C++ less error prone, more readable, and to encourage best practices.

The best thing is, you don't have to tell your coworkers you are using this transpiler at all. It will be super minimalistic. Simply add `*.rcpp` and `*.rhpp` to your `.gitignore` and then you can invoke this transpiler to get code back from your peers in this format and upon invoking this transpiler prior to git commit you will receive `*.cpp` and `*.hpp` files with minimal changes to them as if you had edited the file directly yourself. No one needs to know, and thus no need to ask permission from your boss or peers to rage against their machine.

The other great thing about this language is that it is, itself, C++, just with some preprocessor statements and a good syntax checker. So if you don't care to hide the fact you are using it from your coworkers, and they can handle your weird syntax, you are good to go, and it will work with any other syntax checker, linter, code highlighter, etc.

The goals of this new language (so far) are as follows:

  - [ ]  Make `const` default by introducing a new keyword `mut`
  - [ ]  Make smart pointers default by introducing a new keyword `dumb` for "old-style" pointers.
  - [ ]  Get rid of `new`
  - [ ]  Disambiguate rvalue references and [universal references](https://isocpp.org/blog/2012/11/universal-references-in-c11-scott-meyers)
  - [ ]  Disambiguate `dumb` pointers and dereference (`deref`) which both use `*` in C++.
  - [ ]  Disambiguate references (`ref`) and address-of (`addr`) which both use `&` in C++.

The goals of this project's codebase are as follows:

  * Make conversion rules and error rules easy to implement and easy to expand on over time.
  * Make a rhobust testing framework for back and forth conversion.

I will be using my other project `py_intuitive_regex` to keep the regex in this project clean and easy to read.

Note: The point of calling a non-smart pointer `dumb` is twofold:

  * It is not a smart pointer therefore it is dumb.
  * Unless you are very smart, you are dumb for using it. (jk, but in this transpilers philosophy, dumb is like a warning to the user "don't do it!")

# Development TODO List

## In General

  - [ ]  Create a cpp header file that can be imported for all the header preprocessing.
  - [ ]  Write Utility
  - [ ]  Add regex context to converter and complainer classes to speed up processing.

## Complainers

### CPP

  - [ ]  Don't allow `use namespace std`

### RCPP

  - [ ]  Require import of the header file `#include <rcpp>`
  - [ ]  Don't allow `use namespace std`
  - [ ]  Don't allow raw `new` `*` `&`
  - [ ]  Don't allow `mut dumb(const $TYPE)`
  - [ ]  Don't allow `mut const` or `const mut`
  - [ ]  Don't allow missing `mut` or `const` from variable declarations.
  - [ ]  Don't allow missing `mut` or `const` from function parameter declarations.

## Converters

### CPP to RCPP

  - [ ]  Add the header to the code
  - [ ]  Add `mut` to any non-const variables
  - [ ]  Convert any `${NAME}\*` to `dumb($NAME)`
  - [ ]  Convert any `${NAME}&` to `ref($NAME)`
  - [ ]  Convert any `*${NAME}` to `deref($NAME)`
  - [ ]  Convert any `&${NAME}` to `addr($NAME)`
  - [ ]  Convert any `std::shared_ptr<$TYPE>` to `shared($TYPE)`
  - [ ]  Convert any `std::weak_ptr<$TYPE>` to `weak($TYPE)`
  - [ ]  Convert any `std::unique_ptr<$TYPE>` to `unique($TYPE)`
  - [ ]  Convert any `new ${ANY}` to `make_dumb($ANY)`
  - [ ]  Convert any `std::make_shared($ANY)>` to `make_shared($ANY)`
  - [ ]  Convert any `std::make_unique($TYPE)` to `make_unique($TYPE)`
  - [ ]  Convert any `${NAME}&&` to `rref($NAME)` or `univref($NAME)` appropriately based on lvalue or rvalue reference (HARD to automate)

### RCPP to CPP

  - [ ]  Remove the header from the code
  - [ ]  Convert any `dumb($NAME)` to `${NAME}\*`
  - [ ]  Convert any `ref($NAME)` to `${NAME}&`
  - [ ]  Convert any `rref($NAME)` or `univref($NAME)` to `${NAME}&&`
  - [ ]  Convert any `deref($NAME)` to `*${NAME}`
  - [ ]  Convert any `addr($NAME)` to `&${NAME}`
  - [ ]  Convert any `shared($TYPE)` to `std::shared_ptr<$TYPE>`
  - [ ]  Convert any `weak($TYPE)` to `std::weak_ptr<$TYPE>`
  - [ ]  Convert any `unique($TYPE)` to `std::unique_ptr<$TYPE>`
  - [ ]  Convert any `make_dumb($ANY)` to `new ${ANY}`
  - [ ]  Convert any `make_shared($ANY)` to `std::make_shared($ANY)>`
  - [ ]  Convert any `make_unique($TYPE)`  to `std::make_unique($TYPE)`
