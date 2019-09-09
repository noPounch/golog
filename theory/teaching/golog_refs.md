# Programming and Math concepts for golog
This is a brief primer to the programming concepts employed in developing __golog__. This is by no means complete, there are concepts not included here, as well as references that you will need to find on your own. This is meant to be a minimal introduction to what is needed to help __develop golog__. As with all independent projects, the responsibility to learn and get help is on you. Use [me](nchrein@terpmail.umd.edu) and each other as resources.
```
key:
[no asterisk] - not that important, but may need
[*]- important, but may not need right away
[**]-fundimental to understanding/using golog
```
#### General Programming concepts and tools that will be very helpfull:
- basic [terminal](https://medium.com/@manujarvinen/learning-some-basic-terminal-commands-d478e7b8ffe4) / [command prompt](https://www.cs.princeton.edu/courses/archive/spr05/cos126/cmd-prompt.html) usage*
- [virtual environments](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html#managing-envs) (I use [miniconda](https://docs.conda.io/en/latest/miniconda.html) and  ```cd $CONDA_PREFIX``` to get to my golog directory fast)
- [git init/clone/push/pull/branch](https://guides.github.com/introduction/git-handbook/) from command line** (you will need to git pull from [golog](https://github.com/nopounch/golog) to update)
- [pip installing](https://datatofish.com/install-package-python-using-pip/) *
- [python3](https://www.python.org/downloads/release/python-374/)  and an IDE (I prefer [atom](https://riptutorial.com/atom-editor/example/31152/running-a--hello--world---program-in-python-using-atom-from-scratch))

A lot of the tutorials are done in command prompt or terminal, but not both, they have the same keywords

Example of how I begin programming from the command line with the above set up:
```
conda activate golog
cd $CONDA_PREFIX/root
git pull
atom .
```


## Python concepts used throughout the program:
There are tons of python tutorials [1](https://www.programiz.com/python-programming/tutorial)[2](https://www.guru99.com/python-tutorials.html)[3](https://www.w3schools.com/python/) [4](https://www.tutorialspoint.com/python/index.htm)[5](https://www.python-course.eu/python3_course.php) out there, find one and make sure you understand the concepts below:
- Classes & objects*************************************************************
  - attributes**
- data types*
  - lists and tuples*
  - dictionaries** (see functions)
  - python functions** (not to be confused with set theory functions or lambda functions)
    - [args and kwargs](https://www.digitalocean.com/community/tutorials/how-to-use-args-and-kwargs-in-python-3) and star operators**
- importing and modules**
- iterators and for loops**
- simple recursion*
- lambda functions
- [list comprehension](https://www.digitalocean.com/community/tutorials/understanding-list-comprehensions-in-python-3)* (see set theory image)
- \_\_magic__ functions
  - specifically \_\_init__** (see Classes)

(FYI things like which IDE you choose, and which python3 version you pick shouldn't really matter)
I prefer [atom](https://riptutorial.com/atom-editor/example/31152/running-a--hello--world---program-in-python-using-atom-from-scratch) and you should always just install the latest [python3](https://www.python.org/downloads/release/python-374/)

And, by the way, the best way to learn python is to embark on a project (such as golog) and google the concepts along the way, on top of this, you can always ask [me](nchrein@terpmail.umd.edu) about how something works :smiley: :mortar_board:

###  To understand hcat:
- set theory* ([munkres](https://anujitspenjoymath.files.wordpress.com/2018/05/topology-munkres.pdf) chapter 1.1, 1.2 is still great imo)
   - functions*
  - domain and codomain
  - image of a function
- [mathematical graphs](http://math.tut.fi/~ruohonen/GTE_kalvosarja.pdf)** (or if you're intrepid, [categories](https://d-nb.info/955028914/04))
  - graph maps** (or if you're intrepid, functors)


### To understand golog:
#### math:
- [directed acyclic graph](https://en.wikipedia.org/wiki/Directed_acyclic_graph) (see mathematical graphs)
- [scene graph](https://www.cs.utexas.edu/users/fussell/courses/cs354/lectures/lecture13.pdf)** [panda3D scene graph](https://www.cs.utexas.edu/users/fussell/courses/cs354/lectures/lecture13.pdf)
- 3D real space* (Your calc textbook actually)
   - vector valued functions* (parametric equations in space)
  - Orientations in space*


#### programming (with respect to [Panda3D](https://www.panda3d.org/) )    ([Tutorial book](https://grimfang-studio.org/data/books/book1/Panda3D%20Book%201.pdf) )
- nodepaths** (see [scene graph](https://www.panda3d.org/manual/?title=The_Scene_Graph#NodePaths))
  - collision nodes
- [ShowBase](https://www.panda3d.org/manual/?title=Starting_Panda3D)*
  - [Task Manager](https://www.panda3d.org/manual/?title=Tasks)*
  - [event handling with messenger](https://www.panda3d.org/manual/?title=Event_Handlers)*

The Panda3D manual is pretty bad. Definitely make use of the [forums](https://discourse.panda3d.org/), the [discord group](https://discordapp.com/invite/UyepRMm) and [me](nchrein@terpmail.umd.edu)


### To understand how golog saves things:
- paths in your OS** (see section on terminal/command prompt)
- [pickling](https://www.geeksforgeeks.org/understanding-python-pickling-example/) * (relies on a knowledge of objects)
- database*
- graph database** (golog is a __*simplicial database*__)


### other, vaguely related things that may be useful for *using* golog:
 [latex](https://www.latex-project.org/get/) (also mac users do need [mactex](http://www.tug.org/mactex/), windows users use [miktex](https://miktex.org/)... its annoying I know)
 - by the way, any one interested in academic work will eventually use latex.
