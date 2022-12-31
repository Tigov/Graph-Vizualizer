# Graph-Vizualizer
A user creates a graph. The user then inputs an algorithm (BFS,DFS or Dijkstras) to visualize and the program will show that algorithm on the graph and show a return path of 
the algorithm.
This project was worked on by a team of 4. My contribution was the entire backend folder. I was in charge of the connection between the client side and server side. 
I created a backend API that would be fetched by the front end. This would retrieve the specifics of the graphs that the front end wanted and create was is needed 
which is then returned as a JSON object. It would also run the algorithm on said graph, save its path and save the path that needs coloring.
I also worked on the creation of the graphs depending on what info was given to the server side from the client side. The graphs are made using the Pyvis library. The API was 
made using the Fast API library. I also worked on BFS, DFS and Dijkstras algorithm and translated them to work with pyvis graphs. 


An example output: 
