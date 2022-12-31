#Implement DFS, BFS, prim's algorithm, kruskal
#Group - Blades
#sources:https://buildmedia.readthedocs.org/media/pdf/pyvis/latest/pyvis.pdf
#https://anderfernandez.com/en/blog/how-to-create-api-python/#:~:text=To%20create%20an%20API%20in%20Python%20with%20Flask%2C%20we%20have,app%20%3D%20Flask()%20%40app.
#https://pyvis.readthedocs.io/en/latest/documentation.html
#https://www.w3schools.com/python/python_try_except.asp
import numpy as np
import collections
import random as rnd
import sys
from pyvis.network import Network
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#make sure you have python installed
#Do pip install fastapi, pip install uvicorn, pip install numpy, pip install pyvis, pip install react, pip install typescript, npm install

#To run server cd into backend and in terminal uvicorn main:app --reload (uvicorn main:app if its your first time)
#Once on the server, Make sure your URL contains the stuff after http://127.0.0.1:8000/algoFinal

#  allNodes[2].color = "#451235" TO CHANGE THE COLOR OF A NODE IN HTML FILE (Under DrawGraph() function)

app = FastAPI()
app.add_middleware( #unsafe CORS policy, but needed for testing
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['*'])

@app.get("/algoFinal")
def makeGraph(numOfVert = int, numOfEdges = int, startingVertex = int, random = str, 
directed = str, weighted = str, edgeListFormat = str, actualAlgo = str, weightedEdgeListFormat = str):
#Connect url = http://127.0.0.1:8000/algoFinal?numOfVert=6&numOfEdges=4&startingVertex=2&random=False&directed=True&weighted=True&edgeListFormat=0+1+2+3+3+4+5+6+7+8&actualAlgo=bfs&weightedEdgeListFormat=1+2+3+2+4+5+1+2+2+9+8+6+7+3+5
    jsonObject = {}
    if (directed == "True"): #Check if graph should be directed or not
                graph = Network(directed = True, height = "100%", width = "100%", notebook = True)
    elif(directed == "False"):
        graph = Network(directed = False, height = "100%", width = "100%", notebook = True)

    if(random == "True"): #create a random graph
        intNumOfEdges = int(numOfEdges)
        intNumOfVert = int(numOfVert)
        CRED = '\033[91m' #To make the errors in console pop out
        CEND = '\033[0m'
        if directed == "directed" and (intNumOfEdges > (intNumOfVert * (intNumOfVert-1))):
            print(CRED + "A directed graph can have at most N(N-1) edges." + CEND)
            return -1
        elif (directed != "directed" and (intNumOfEdges > (intNumOfVert * (intNumOfVert-1))//2 )):
            print(CRED + "A undirected graph can have at most N(N-1)/2 edges. (N = number of Vertices)" + CEND)
            return -1
        nodes = []
        if (weighted == "False"): #Create a non weighted random graph
            for i in range(0,intNumOfVert): #the nodes will be 0,1,2 all the way to num of nodes
                nodes.append(i)
                graph.add_node(i, label = str(i),shape = "dot", size = 15)
            for i in range(0,intNumOfEdges): #each time this loop runs, we add one edge... run it num of edges times
                randNum1 = rnd.randint(0,intNumOfVert-1) #minus one because numOfVert = 6 means 0 - 5
                randNum2 = rnd.randint(0,intNumOfVert-1)
                if (randNum1 == randNum2 and intNumOfVert > 10): #try to make sure there arent any loops ( node1 goes to node1)
                    randNum2 = rnd.randint(0,intNumOfVert-1) #low chance there will be loops
                graph.add_edge(nodes[randNum1],nodes[randNum2])
        else: #create a random weighted graph
            for i in range(0, intNumOfVert):
                nodes.append(i)
                graph.add_node(i, label = str(i),shape = "dot", size = 15)
            for i in range(0, intNumOfEdges):
                randNum1 = rnd.randint(0,intNumOfVert-1) #minus one because numOfVert = 6 means 0 - 5
                randNum2 = rnd.randint(0,intNumOfVert-1)
                randNum3 = rnd.randint(0,intNumOfVert)

                if (randNum1 == randNum2 and intNumOfVert > 10): #try to make sure there arent any loops ( node1 goes to node1)
                    randNum2 = rnd.randint(0,intNumOfVert-1) #low chance there will be loops
                graph.add_edge(nodes[randNum1],nodes[randNum2], label = str(randNum3))
    
    else:
        allNodes = []
        if (weighted == "False"):
            for letter in edgeListFormat.split(" "):
                allNodes.append(int(letter))
        else:
            counter = 0
            for letter in weightedEdgeListFormat.split(" "):
                if counter != 2: #The nodes are everything but the weights
                    allNodes.append(int(letter))
                    counter+=1
                else:
                    counter = 0

        
        allNodes = set(allNodes) #get rid of duplicate nodes
        allNodes = list(allNodes) #go back to list format 
        allEdges = []
        if (weighted == "False"):
            for letter in edgeListFormat.split(" "):
                allEdges.append(int(letter))
            for node in allNodes:
                graph.add_node(int(node),label = str(node),shape = "dot", size = 15)
            for i in range(0,len(allEdges),2):
                try:
                    graph.add_edge(allEdges[i],allEdges[i+1])
                except:
                    CRED = '\033[91m'
                    CEND = '\033[0m'
                    print(CRED + "Input to Edge list format went wrong. (A node probably leads to nothing)" + CEND)

        else:
            for letter in weightedEdgeListFormat.split(" "):
                allEdges.append(int(letter))
            for node in allNodes:
                graph.add_node(int(node),label = str(node),shape = "dot", size = 15)
            for i in range(0,len(allEdges),3):
                try:
                    graph.add_edge(allEdges[i],allEdges[i+1], label = str(allEdges[i+2]))
                except:
                    CRED = '\033[91m'
                    CEND = '\033[0m'
                    print(CRED + "Input to Weighted Edge list format went wrong. (A node probably leads to nothing)" + CEND)

    returnPath = []
    dijkstrString = ""
    if (actualAlgo == "bfs"): #check which algo to sue
        returnPath = bfs(int(startingVertex), graph)
    elif (actualAlgo == "dfs"):
        returnPath = dfs([],int(startingVertex),graph,[])
    elif (actualAlgo == "pfs"): #check which algo to sue
        returnPath = pfs(int(startingVertex), graph)
    elif (actualAlgo == "dijk"):
        dist,color = dijkstra(int(startingVertex),graph)
        for i in range(len(dist)):
            if dist[i] == float("inf"):
                dist[i] = str("-1 (Unreachable)")
            dijkstrString = dijkstrString + f"The distance from {startingVertex} to {i} is {dist[i]} "
        returnPath = color
        
    graph.force_atlas_2based(overlap= 1) #ensure no overlap happens
    graph.show("example.html")
    #https://stackoverflow.com/questions/10507230/insert-line-at-middle-of-file-with-python
    
    
#write the button into the html file
    index = 52
    if actualAlgo == "dijk":
        new_string = f"<button id='viz-graph-btn'>Visualize</button> <p id='algo'>Path of {actualAlgo}: {dijkstrString}</p>"
    else:
        new_string = f"<button id='viz-graph-btn'>Visualize</button> <p id='algo'>Path of {actualAlgo}: {returnPath}</p>"
      
    with open("example.html", "r") as fd:
        contents = fd.readlines()
    
    contents.insert(index, new_string)
    
    with open("example.html", "w") as fd:
        contents = "".join(contents)
        fd.write(contents)
    
     #write the count
    index = 66
    new_string = f"var colorCount = 0;var pathToColor = {returnPath};"
      
    with open("example.html", "r") as fd:
        contents = fd.readlines()
    
    contents.insert(index, new_string)
    
    with open("example.html", "w") as fd:
        contents = "".join(contents)
        fd.write(contents)
    
    
    #write the button press
    index = 80
    new_string = "var algoText = document.getElementById('algo'); algoText.style.display = 'none';var button = document.getElementById('viz-graph-btn');" + "button.addEventListener('click', function(){" + "algoText.style.display = 'block'; colorCount++;" +  "drawGraph();});"
      
    with open("example.html", "r") as fd:
        contents = fd.readlines()
    
    contents.insert(index, new_string)
    
    with open("example.html", "w") as fd:
        contents = "".join(contents)
        fd.write(contents)
        
    #write the javascript code to color the graph
    
    index = 101
    new_string = "if (colorCount != 0){" + " for(let i = 0; i < pathToColor.length; i++){" + " allNodes[pathToColor[i]].color = '#FF0000'}" + "console.log(allNodes)}"
      
    with open("example.html", "r") as fd:
        contents = fd.readlines()
    
    contents.insert(index, new_string)
    
    with open("example.html", "w") as fd:
        contents = "".join(contents)
        fd.write(contents)
         
    
    htmlCode = open("example.html", "r").read()
    jsonObject["dijkstrString"] = dijkstrString 
    jsonObject["htmlCode"] = htmlCode 
    jsonObject["algoPathToColor"] = returnPath
    print(json.dumps(jsonObject))
    return json.dumps(jsonObject) #convert dictionary to Json Object for easier frontend
#Description of function for now 
#input: takes in the starting node inside of the graph and entire graph object with all edges. (node = starting node in the graph) (graph = dictonary of all edges in graph)
#output: will return the shortest path from the start node in retArr (return array)

def dfs(visited, node, graph, retArr):
    if node not in visited:   #checks to see if the current node is in the graph dictonary of edges
        retArr.append(node) #adds the current node to the pathway of the dfs (at the start of the function the starting node will be added first then it will be replaced by neighboring nodes through recursive calls)
        visited.append(node) #adds the current node to the visited array (at the start of the function the starting node will be added first then it will be replaced by neighboring nodes through recursive calls)
        for neighbor in graph.neighbors(graph.get_node(node)["id"]):    #if the current node was in the graph dictonary then it will look for all the neighboring nodes in the graph dictonray 
            dfs(visited, neighbor, graph, retArr)  #if the neighboring node hasn't been visited by the search then a recurive call will be occur and the same process will continue until all neighboring nodes are visited

    #once a neighboring node is found it is then check to see if that node has been visisted by the search before
    return retArr

def bfs(start, graph):
    levelByLevel = []
    mainQueue = []
    seen = []
    mainQueue.append(start) # add the starting node to the queue
    seen.append(start) # we have seen the starting node
    while mainQueue:
        node = mainQueue.pop(0)
        curArray = []
        for neighbor in graph.neighbors(graph.get_node(node)["id"]):
            if neighbor not in seen:
                curArray.append(neighbor)
                seen.append(neighbor)
                mainQueue.append(neighbor)   
        levelByLevel.append(curArray)
        curArray = []
    dictMain = {}
    for i in range(len(seen)):
        dictMain[seen[i]] = levelByLevel[i]

    return seen

#http://www.gitta.info/Accessibiliti/en/html/Dijkstra_learningObject1.html
def dijkstra(start, graph):
    dist = [float("inf")] * len(graph.get_nodes())
    prev = [None] * len(graph.get_nodes())
    edges = graph.get_edges()
    weights = {}
    colorArr = []
    for i in range(len(edges)): #get the weights for each edge
        if (graph.directed == False): #if not directed it goes both ways
            weights[str(edges[i]["from"]) + " to " + str(edges[i]["to"])] = int(edges[i]["label"])
            weights[str(edges[i]["to"]) + " to " + str(edges[i]["from"])] = int(edges[i]["label"])
        else:
            weights[str(edges[i]["from"]) + " to " + str(edges[i]["to"])] = int(edges[i]["label"])
    

    dist[start] = 0
    Q = list(graph.get_nodes())
    u = None
    while Q:
        temp = float("inf")
        for x in Q: #find the node that has the least distance
            if dist[x] < temp:
                temp = dist[x]
                u = x
        try: 
            Q.remove(u)
            colorArr.append(u)
        except:
            return dist,colorArr
        for neighbor in graph.neighbors(graph.get_node(u)["id"]): #for each neighbor of u
            alt = dist[u] + weights[f"{u} to {neighbor}"] #find the weight from u to neighbor
            if alt  < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = u
                
    return dist,colorArr



def pfs(start, graph, end):  #prim's algo, bird in hand, don't understand
    mainQueue = [] 
    seen = []
    min = 100000000000000
    a = 0
    b = 0
    mainQueue.append(start) # add the starting node to the queue
    seen.append(start) # we have seen the starting node

    for i in range(len(graph)):
        if seen[i]:   #checks to see if the current node is in the graph dictonary of edges
            for j in range(len(graph)):
                neighbour = graph[i][j] 
                if neighbour and not seen[i]:        
                    if min > neighbour:
                       min = neighbour
                       a = i
                       b = j


"""                
def kfs(start, graph):
    mainQueue = [] 
    seen = []
    
    min = 100000000000000
    a = 0
    b = 0
    mainQueue.append(start) # add the starting node to the queue
    seen.append(start) # we have seen the starting node
    
    for i in range(len(graph)):
        mainQueue.append(i)
        seen.append(0)
        
    while a < (len(graph)- 1):
"""            
