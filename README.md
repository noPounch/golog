# golog (graphical ontological log)
WIP graphical manipulator for ontological logs

golog is a graphics program using panda3d as the graphics engine, this is certainly subject to change.

Essentially, there are only 2 things you can do:
* create simplecies (see [simplicial set](https://en.wikipedia.org/wiki/Simplicial_set))
* open a simplex's math data

Each simplex has associated to it an (arbitrary) piece of math_data, the role of an ontology is to organize data as objects, relationships and relationships between relationships etc.

## The currently handled math_data:
* Arbitrary files* (as long as your computer has a program to open said file)
* other gologs

*files which depend on other files are NOT currently handled (this will change with file ontologies)

## breif tutorial
* install pre-requisites from requirements.txt (using pip)(this is just a list idk setuptools)
* python run.py
* choose to load a .golog file, or name your golog and choose a folder location for all the save files golog will create (I recommend using an empty folder)
Once at the main golog window refer to the following controls:

## Controls
* right click:  create a 0-simplex
* left click: select a simplex, if 2 0-simplecies are selected, this will create a 1-simplex between them
* mouse over: Preview simplex's math_data
* space: open math_data (or ontologically expand if math_data is a golog)
* u: change a simplex's meta data (its label, and math_data)
* s: save

## OS / Path-independence
* golog is made to work on arbitrary operating systems starting from an arbitrary path
* The only thing that matters is the file integrity of the folder the main golog is saved in
* To preserve this, selected files are copied into this directory while golog is running
* *thus files which depend on other files are NOT currently handled (this will change with file ontologies)
* If you wish to move a .golog, you must move the WHOLE FOLDER (just zip it)



## Disclaimer
# !--- USE AT YOUR OWN RISK ---!
This Is a very loosely tested program that executes files on your computer.

If you wish to know more contact me through github or at nopounch@gmail.com
