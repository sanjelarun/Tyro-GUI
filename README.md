# TYRO
_Tyro_ is a new tool for translating a sequential Python program into a semantically equivalent PySpark program.
The input sequential program generally iterates over huge datasets. 
Tyro uses techniques from classical compilers like pattern matching rules to apply transformations when the input code matches a pattern. 

Tyro utilizes the **GRA**dual **S**ynthesis for **S**tatic **P**arallelization (GRASSP) [See] (https://dl.acm.org/doi/10.1145/3062341.3062382) approach 
to convert the selected fragment from the existing code. 
The key idea behind GRASSP is to gradually increase the complexity of the target for translation.
Finally, Tyro uses user supplied test cases to determine program equivalence between the initial program and the parallel result.

To learn more about _Tyro_, please read our paper [here](https://www.proquest.com/docview/2487149689?pq-origsite=gscholar&fromopenview=true) 

If you have like our tool, please star our repo!


### Getting  Started
Tyro is built using Python so you need Python 3.X (x >= 7 ). You can download and install 
Python [Here](https://www.python.org/downloads/). 

Once you  have installed Python, you can download the codebase. The various modules are 
seperated in each indivdual package. 

To  run Tyro, you can build and run the _main.py_. Right now,  we are working on GUI version
of Tyro, which will make the whole process easy and simple. 

#### Contact
If you have any queries and suggestion, feel free contact via email: arun_sanjel1@baylor.edu, sanjelarun@gmail.com