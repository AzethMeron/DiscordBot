
import nltk

# by Jakub Grzana

# function to create n-grams of given text or any list of data
# input: text - string or list of any data 
# input: n - integer, parameter for N-grams
# output: list of ngrams. Ngram is list of data, type depends on input 
def ngrams(text,n):
    return [ ngram for ngram in nltk.ngrams(text,n) ]

# function to create N-Gram Graph for given text
# input: text - string, 
# input: n - integer, parameter for N-grams
# input: f - integer, size of frame (number of edges per node)
# output: graph (implemented as list of succesors, without weights)
def Graph(text,n,f):
    ltext = [ char for char in text ]
    # Managing very short texts - because im using ngrams it is required for text to be atleast (n+1) characters long
    length = len(ltext)
    for i in range(length,n+1):
        ltext.append(' ')
    # end of short texts
    nodes = [ ngram for ngram in ngrams(ltext,n) ]
    
    graph = []
    for i in range(0,len(nodes)):
        graph.append( (nodes[i] , []) )
        for j in range(i+1, min(len(nodes),i+f+1)):
            graph[-1][1].append( nodes[j] )
    return graph            

# function to create list of edges of N-Gram graph
# input: graph - N-gram graph
# output: list of tuples (start_node,end_node)
# nodes = ngrams, exact type depends on data Graph was made on
#parsed_graphs = {} # for acceleration?
def EdgeList(graph):
    #graph_str = str(graph)
    #if graph_str in parsed_graphs:
    #    return parsed_graphs[graph_str]
    edges = []
    for (start_node,end_node_list) in graph:
        for end_node in end_node_list:
            edges.append( (start_node, end_node) )
    #parsed_graphs[graph_str] = edges
    return edges

# function insert edges into graph passed via parameter
# input: graph - N-Gram graph
# input: start_node - node from which the edges comes
# input: end_node_list - list of nodes to which start_node has edge
# edges that are already present in graph are ignored
# output: None
def GraphInsertEdges(graph, start_node, end_node_list):
    for (s_node, e_node_list) in graph:
        if(s_node == start_node):
            e_node_list = list( set( e_node_list + end_node_list) )
            return None
    graph.append( (start_node,end_node_list) )

# function to perform union of graphs
# input: a - N-Gram graph
# input: b - N-Gram graph
# output: graph, union of a and b
def GraphUnion(a,b):
    graph = a.copy()
    for (s_node, e_nodes_list) in b:
        GraphInsertEdges(graph,s_node,e_nodes_list)
    return graph

# function to compare size of graphs
# input: a - N-Gram graph
# input: b - N-Gram graph
# output: float, size-similarity of graphs, values 0...1
def GraphSizeSimilarity(a,b):
    A = EdgeList(a)
    B = EdgeList(b)
    denominator = max(len(A),len(B))
    numerator = min(len(A),len(B))
    return numerator/denominator
    
# function to check containment similarity
# input: a - N-Gram graph
# input: b - N-Gram graph
# output: float, containment-similarity of graphs, values 0...1
def GraphContainmentSimilarity(a,b):
    A = EdgeList(a)
    B = EdgeList(b) 
    denominator = min(len(A), len(B))
    B_set = set(B) # for vast performance gain
    numerator = sum( [ 1 for w in A if w in B_set ] )
    return numerator/denominator