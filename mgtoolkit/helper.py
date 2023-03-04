from library import *
from random import *
from datetime import datetime
import time
def helper(numNodes, numEdges):
    generating_set = set()
    for i in range(1,numNodes+1):
        generating_set.add(i)
        mg = Metagraph(generating_set)
    
    # create random edges
    edges = []
    for _ in range(numEdges):
        invertex_set = set()
        numOfInvertex = randint(1,numNodes//2)
        for _ in range(numOfInvertex):
            node = randint(1,numNodes)
            invertex_set.add(node)
        outvertex_set = set()
        numOfOutvertex = randint(1,numNodes//2)
        for _ in range(1):
            node = randint(1,numNodes)
            outvertex_set.add(node)
        edge = Edge(invertex_set, outvertex_set)
        edges.append(edge)
    mg.add_edges_from(edges)
    return mg

start_time = datetime.now()
start = start_time.strftime("%H:%M:%S")
print('start: ', start)
mg = helper(30,20)

source = {1,2}
target = {8}

find_time = datetime.now()
find = find_time.strftime("%H:%M:%S")
print('get all metapaths: ', find)
metapaths = mg.get_all_metapaths_from(source, target)
# display results
if metapaths:
    for metapath in metapaths:
        print(repr(metapath))
else:
    print('there is no metapath')

end_time = datetime.now()
end = end_time.strftime("%H:%M:%S")
print('end: ', end)
print(end_time-start_time)