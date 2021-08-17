# pathfinding-visualizer
-implements the Dijkstra's and A* pathfinding algorithms
-GUI tool to visualize how they function
-first 2 clicks place start and end nodes, rest place barriers
-h score is calculated based on manhattan distance because edges only go in 4 directions: up, right, down left. 
-implemented Dijkstra's by making some edits to the A* algorithm (f score = g score instead of f score being the sum of g and h scores, doesn't have a sense of direction thus is pretty much a brute-force approach. 
