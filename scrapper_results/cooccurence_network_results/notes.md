# initial results from the co-occurrence network
## important cluster cores in the network:
version           92  
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


## important surronding pairs around the clusters:

word: version  
(('version', 'python'), 14411)  
(('version', 'collect'), 12937)  
(('version', 'cuda'), 12758)  
(('version', 'runtime'), 12288)  
(('version', 'pytorch'), 10868)  

word: pytorch  
(('version', 'pytorch'), 10868)  
(('used', 'pytorch'), 10610)  
(('build', 'pytorch'), 9119)  
(('conda', 'pytorch'), 7974)  
(('o', 'pytorch'), 5621)  

word: error  
(('error', 'reference'), 4063)  
(('code', 'error'), 2700)  
(('message', 'error'), 2325)  
(('undefined', 'error'), 2219)  
(('nvlink', 'error'), 1998)  

word: cc  
(('cc', 'ezyang'), 6434)  
(('version', 'cc'), 2818)  
(('cc', 'gchanan'), 2655)  
(('mruberry', 'cc'), 2303)  
(('mrshenli', 'cc'), 2017)  

word: conda  
(('conda', 'pypi_0'), 10798)  
(('conda', 'pytorch'), 7974)  
(('conda', 'mkl'), 7060)  
(('pypi', 'conda'), 5904)  
(('conda', 'pip3'), 3856)  

word: cuda  
(('version', 'cuda'), 12758)  
(('build', 'cuda'), 9896)  
(('available', 'cuda'), 9795)  
(('runtime', 'cuda'), 7640)  
(('false', 'cuda'), 5273)  

word: cpu  
(('cpu', 'mhz'), 2960)  
(('cpu', 'numa'), 2324)  
(('architecture', 'cpu'), 1932)  
(('on-line', 'cpu'), 1917)  
(('x86_64', 'cpu'), 1893)  

word: model  
(('model', 'gpu'), 10381)  
(('configuration', 'model'), 6898)  
(('version', 'model'), 2816)  
(('model', 'cuda'), 2123)  
(('name', 'model'), 1586)  

word: file  
(('line', 'file'), 10237)  
(('entity', 'file'), 5001)  
(('code', 'file'), 2023)  
(('found', 'file'), 1640)  
(('call', 'file'), 1407)  

word: code  
(('code', 'error'), 2700)  
(('code', 'file'), 2023)  
(('code', 'following'), 1318)  
(('example', 'code'), 1232)  
(('run', 'code'), 1188)  

word: line  
(('line', 'description'), 11240)  
(('line', 'file'), 10237)  
(('line', 'first'), 5712)  
(('line', 'entity'), 5004)  
(('line', 'blank'), 3775)  

word: gpu  
(('model', 'gpu'), 10381)  
(('configuration', 'gpu'), 10117)  
(('nvidia', 'gpu'), 4518)  
(('version', 'gpu'), 4392)
(('geforce', 'gpu'), 3969)

word: vulnerability  
(('affected', 'vulnerability'), 6638)  
(('spectre', 'vulnerability'), 1563)  
(('vulnerability', 'srbds'), 1502)  
(('vulnerability', 'meltdown'), 1366)  
(('vulnerability', 'l1tf'), 1315)  

## notes
 We found that a lot of word pairs are not actual topics, They are just some format information that people would include in their questions to give context for the person who are reading their post. Therefore, they are not really Reflecting the interest of the author. So We want to remove them from the pairs list and expose more that actually important in the text of the post text. The methodology we used to determine which pairs need to be removed is by looking at the sample issue from all of those pairs.
