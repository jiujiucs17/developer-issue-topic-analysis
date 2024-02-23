# initial results from the co-occurrence network
## important cluster cores in the network
version           91  
pytorch           54  
error             53  
cc                50  
conda             49  
cuda              36  
cpu               36  
model             35  
file              33  
code              32  
line              30  
gpu               29  
vulnerability     27  


## important surronding pairs around the clusters

word: version  
(('version', 'python'), 14411)  
(('version', 'collect'), 12937)  
(('version', 'cuda'), 12758)  
(('version', 'pytorch'), 10868)  
(('version', 'cmake'), 10676)  

word: pytorch  
(('pytorch', 'version'), 10868)  
(('pytorch', 'used'), 10610)  
(('pytorch', 'build'), 9119)  
(('pytorch', 'conda'), 7974)  
(('pytorch', 'o'), 5621)  

word: error  
(('error', 'reference'), 4063)  
(('error', 'code'), 2700)  
(('error', 'message'), 2325)  
(('error', 'undefined'), 2219)  
(('error', 'nvlink'), 1998)  

word: cc  
(('cc', 'ezyang'), 6434)  
(('cc', 'version'), 2818)  
(('cc', 'gchanan'), 2655)  
(('cc', 'mruberry'), 2303)  
(('cc', 'mrshenli'), 2017)  

word: conda  
(('conda', 'pypi_0'), 10798)  
(('conda', 'pytorch'), 7974)  
(('conda', 'mkl'), 7060)  
(('conda', 'pypi'), 5904)  
(('conda', 'pip3'), 3856)  

word: cuda  
(('cuda', 'version'), 12758)  
(('cuda', 'build'), 9896)  
(('cuda', 'available'), 9795)  
(('cuda', 'runtime'), 7640)  
(('cuda', 'false'), 5273)  

word: cpu  
(('cpu', 'mhz'), 2960)  
(('cpu', 'numa'), 2324)  
(('cpu', 'architecture'), 1932)  
(('cpu', 'on-line'), 1917)  
(('cpu', 'x86_64'), 1893)  

word: model  
(('model', 'gpu'), 10381)  
(('model', 'configuration'), 6898)  
(('model', 'version'), 2816)  
(('model', 'cuda'), 2123)  
(('model', 'name'), 1586)  

word: file  
(('file', 'line'), 10237)  
(('file', 'entity'), 5001)  
(('file', 'code'), 2023)  
(('file', 'found'), 1640)  
(('file', 'call'), 1407)  

word: code  
(('code', 'error'), 2700)  
(('code', 'file'), 2023)  
(('code', 'following'), 1318)  
(('code', 'example'), 1232)  
(('code', 'run'), 1188)  

word: line  
(('line', 'description'), 11240)  
(('line', 'file'), 10237)  
(('line', 'first'), 5712)  
(('line', 'entity'), 5004)  
(('line', 'blank'), 3775)  

word: gpu  
(('gpu', 'model'), 10381)  
(('gpu', 'configuration'), 10117)  
(('gpu', 'nvidia'), 4518)  
(('gpu', 'version'), 4392)  
(('gpu', 'geforce'), 3969)  

word: vulnerability  
(('vulnerability', 'affected'), 6638)  
(('vulnerability', 'spectre'), 1563)  
(('vulnerability', 'srbds'), 1502)  
(('vulnerability', 'meltdown'), 1366)  
(('vulnerability', 'l1tf'), 1315)   

## notes
 We found that a lot of word pairs are not actual topics, They are just some format information that people would include in their questions to give context for the person who are reading their post. Therefore, they are not really Reflecting the interest of the author. So We want to remove them from the pairs list and expose more that actually important in the text of the post text. The methodology we used to determine which pairs need to be removed is by looking at the sample issue from all of those pairs.  
   
 Another alternative is to re-cleaning the dataset delete the part with following informtion:  
 as the issue submission page of pytorch is guided by a structured form, therefore it's safe for us to assume that almost all versioning information will be attached at the end of the initial comment. with a header "Versions". similar thing is true for "Error logs". the only difference is that "Error logs" is usually placed in from of "Versions" (these are the format using new github issue template function). For ealier issues, it should follow a template with two sections "code example", "System Info" at the end of issue. Code examples should include a minimal example to repro the bug. Error messages and stack traces, and system info should contain a standard message generated from a given command. They are not directly related to the description of issues, but their structured output provide significan noise in our data like shown above. Therefore we are trying to eliminate this noise by ignoring those sections with regular expression. In practice we also include following keywords as title of sections, because they were part of the older version of issues template:
 "system information", "system info", "environment"

 ** comment: the following line is not being used because the new issue structure is a relatively new thing and we will lost most of our isseus by filtering with this.  
 besides we also will select only relevant issues by using key word selection: 🐛 Bug Report...   
 **

 we didn't put time constrain on the issues, therefore we are able to retrieve issues from the beginning of pytorch project went open source. This measure could help us identify the most consistent factor within the issues posts through out the lifecycle of pytorch. also, increase the size of our corpus could potentially increase the usefullness of the results obtained from co-occurrence network, as it reveals the topic significancy based on the number of times word pairs occure in different comments.
 the drawback would be that we are not able to reflect the gradule change of pytorch in our results. However this problem could be resolved by recover the architecture of pytorch in different period, which this work would provide direction to. 

after this we already can start looking at the samples, as a representative sample is within the acceptable size (60-70 comments) and some insights are already revealed: 

1. people don't know how the error are produced, it  might be helpful to provide the context of the error production and the meaning of different errors in different code context. and among the different errors, the TypeError is one of the most asked about one. We all have encountered senarios in which the error stack refers deeply inside the library/pakcage. we want to provide a view for dataflow and data manipulation. meaning how the data is passed and tranformed within the process. By this we are able to findout the exact point of problem occurrence. 

possible criteria: recovery data dependecies, and control sequences
possible technique: 1. ART



pairs and statistics:
    1. (error, code): 61 bug report for requesting fix. 4 asking how to solve error. 1 requesting feature.
    2. (error, following): 3 asking how to install; 9 asking how to solve error (1 TypeError, 2 AttributeError); 53 bug reports for requesting fix 
    3. (error, get): 1 asking how to install; 14 asking how to solve error (2 TypeError, 5 AttributeError); 49 bug reports
    4. (error, message): 3 asking how to install; 10 asking how to solve error; 53 bug reports
    5. (error, reference): 1 asking how to install; 63 asking how to solve error; 2 bug reports

one formate pair was removed: (error, code) ** not implemented due to uncertainty of effectiveness, need to be further confirmed and thought about **



## limitation:
the comments comtain a lot of bug discriptions, which are a little bit less useful for us. However, it's also not make sense for us to delete all comments contain bug discription because this is a big part of the issues' functionalities.


## the selection of tools:

by performing the snowballing of two literatures, going through all papers that are citing them in the hope of finding a newer technique that is closer related to our research question (dataflow architecture recovery)

several freqently encountered topics:
- reflection modeling: 1. need to see what is the specific technique used in recovering the implemented technique; 2. need to see what do the connectors in the models contain, do they contain information related to dataflow?

detecting abstract datatypes and state encapsulation:
- identify abstract data types (ADT) and abstract state encapsulations (ASE, also called abstract objects) in source code. This approach, named similarity clustering, groups together functions, types, and variables into ADT and ASE candidates according to the proportion of features they share
- is also a type of clustering technique
- perhaps would like to select a newest one among the sililar topic papers, and compare with other types of techniques.


## big picture of the architecture view:

on the basis of a class/function diagram, in diagram, loops connecing different class/functions would indicate the dataflow, the dataflow loops 
1. have start-points which are the argument of user called functions 
2. and end-points which are the returned value of the called functions. in the middle of the loops, 
3. the dataflow line would show how data is transformed at each node (input and output format, data assertions, ideally with explaination of the format/assertion, and the function)
4. it also shows the in-memory status of the dataflow (indicating at each stage if new memory is assigned or shallow copying is happening, etc)

remaining questions: 
    1. the scope of included functions/classes
        a) torch.nn(20k+ LOC): too complex, maybe too much work for manual recovery
        b) torch.nn.functional(4624 LOC): there's no classes defined in the file, potentially introduce difficulty for constructing class diagram.
        c) torch.autograd(7340 LOC): moderate difficulty for manual recovery, the problem is that most classes and functions are not likely to be frequently accessed by end-user programmers, which means that they are likely to be part of the bigger loops. However, this could be defended by 1. loops are always composed by numerous smaller loops. 2. the torch.autograd is the third most mentioned module name. and second mentioned second level module name. some classes/functions are interface between python and C (inherit _C.**)

        the next step would be using the automated tools to fisrt generate class/function diagrams. possible tool: Pyreverse based on Pylint
    2. how to define the "data" being tracked in the loop, as data would be contantly transformed in the loop. 
        one possible definition: the variable and the variable (partially) directly generated from it.
        another definition: the in-memory data object that created (partially) with in-memory data object that's already in the dataflow loop.
    3. how does memory management work in python:
        a) count the reference number
        b) delete unreferenced in-memory data object immediately
    4. create an indicative diagram 

    5. risk: there are some 


** nest network could be the solution for the later automate-creation of a network.


investigation and trials/errors shows that exsiting tools (pyan3, pycallgraph, cprofil+gprof2dot, pycallgraph2) don't fit the purpose of creating a static callgraph that shows all calling/datapassing relationships within the package.

experiences:
pyan3: unmaintained with bugs, after fixing the most obvious bug, it's still not compatible with torch. potentially because it's outdated and not support some newer python features the torch used.

pycallgraph: no longer maintained and with it's error that stops itself from being installed in an newer python env (3.9+), tried both pip and conda, getting the same result

cprofile+gprof2dot: only generate the actual run code, not able to provide all relationships within the package. However, this could be useful in the development of automated dataflow error exposure tool.

pycallgraph2: similarly, not able to create a static callgraph that shows all the relationships, it can only provide the runned functions and monitors it's process.


today we realized the difference between "module" and "(sub)package". modules would be .py files, while (sub)packages have to be folders that contain a __init__.py even though this file could be empty after certain version of python.

we have created a file structure network, next step would be adding edges representing importing as a approximate of the call graph. currently we loaded the importing sentences for all modules into an excel file with the help of package: "ast" and "pkgutil". The problem is that the information provided by these two packages are not sufficient enough to identify the modules of some imported functions and classes, the next step would be manually check those information and adding edges to the network, forming some loops





# the creation of a prototype architecture representation of PyTorch

## clustering of the network (call graph)