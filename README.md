RoughSets library (Pandas version)
----------------------------------

The goal of the library is to provide base functions of Rough Sets Theory and give foundation to build extensions
which will provide different methods built on RoughSets Theory, like:
- pre-processing methods
- find core and reducts
- classifiers
- post-processing methods

The library doesn't use basic loops so should help to build vary fast extensions when large datasets will be used.

The library implements these main functions:
- computation of indiscernibilty relations - function: get_indiscernibility_relations

- computation of a lower and upper approximations, boundary and negative regions - all these 4 boundaries are computed by function: get_approximation_indices.  For optimization, only indices of X,y are returned by the function, so can be used for futher computations  
before slicing with X and y.  

The library has included unit tests for different datasets, subsets and concepts.  



Requirements  
------------
Python >= 3.8  
OS: Linux, Windows  


Install from PyPi server  
------------------------
pip install roughsets-base  


Build and install the library from source code  
----------------------------------------------
pip install --upgrade pip  
pip install --upgrade build  

On linux:
python3 -m build  

On Windows:  
py -m build  

pip install dist/roughsets_base-<version>-py3-none-any.whl  


Install CI and dev tools
------------------------
pip install -r requirements.dev.txt  


Unit tests
----------

File tests/test_dataset_KDD.py contains tests which use KDD99 dataset.   
By default file will be downloaded from: http://kdd.ics.uci.edu/databases/kddcup99/corrected.gz  
If You have the file on Your system You can set OS environment variable ROUGHSETS_KDD99_TEST_DATA_FOLDER  
with the path to th file.  
File tests/KDD99_compare_with_R_RoughSets.R contains R script which generate refernece data using well knwon reference library: RoughSets.  
See: https://www.rdocumentation.org/packages/RoughSets/topics/RoughSets-package (R language).
Reference datasets with results from R-RoughSets library are saved in folder tests/datasets/KDD99.  
You can disable running tests for specific dataset in file test_dataset_X.py (X - symbol of dataset), method setUp.

For checking of unit tests' results was used algorithms from well known reference library:  
https://www.rdocumentation.org/packages/RoughSets/topics/RoughSets-package


Documentation
-------------

Documentation of the library is included in folder doc and also available online: https://.... 


Re-Build sphinx documentation
--------------------------
pip install -r requirements.ci.txt  
sphinx-build -b html ./doc ./doc/_build/html  
sphinx-build -b man ./doc ./doc/_build/man  


Recommended packages
--------------------

sklearn-pandas https://github.com/scikit-learn-contrib/sklearn-pandas   
pandas ecosystem: https://pandas.pydata.org/community/ecosystem.html  


