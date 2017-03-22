# README #

This README would normally document whatever steps are necessary to get your application up and running.
### CS335A Project 

* Source Language - C
* Intermediate Language - Python
* Assembly - x86/mips

### Milestone 1

## [Grammar link](http://www.quut.com/c/ANSI-C-grammar-y.html)
## How to run 
```sh
$ cd src
$ make 
$ cd ..
```
There are 5 code files name
* code1.c
* code2.c
* code3.c
* code4.c
* code5.c
```sh
$ ./bin/parser.sh ./test/code1.c
```
The parse tree is generated in the "test" folder.
```sh
$ cd test
```

After the execution go to the src directory and run.
```sh
$ make clean
```

### Members
* Kshitiz Suman 14333
* Rishabh Bhardwaj 14548

## Milestone 2
### How to run

Write the code in test folder of the Milestone 2 directory.Suppose that the code file name is code1.c. Then use
```sh
$ cd src
$ python parser.py ../test/code1.c 
```

*The output dump is generated in dump.txt in src folder.
*The symboltables are generated in the src folder with the names as their symboltablenumber.csv
*For ex: 1.csv 2.csv etc.