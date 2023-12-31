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

1. people don't know how the error are produced, it  might be helpful to provide the context of the error production and the meaning of different errors in different code context. [(error, code), ]



pairs and statistics:
    1. (error, code): 61 bug report for requesting fix. 4 asking how to solve error. 1 requesting feature.
    2. (error, following): 3 asking how to install; 9 asking how to solve error (1 TypeError, 2 AttributeError); 53 bug reports for requesting fix 
    3. (error, get): 1 asking how to install; 14 asking how to solve error (2 TypeError, 5 AttributeError); 49 bug reports
    4. (error, message): 3 asking how to install; 10 asking how to solve error; 53 bug reports
    5. (error, reference): 1 asking how to install; 63 asking how to solve error; 2 bug reports

one formate pair was removed: (error, code) ** not implemented due to uncertainty of effectiveness, need to be further confirmed and thought about **



## limitation:
the comments comtain a lot of bug discriptions, which are a little bit less useful for us. However, it's also not make sense for us to delete all comments contain bug discription because this is a big part of the issues' functionalities.
