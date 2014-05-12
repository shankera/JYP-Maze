import random
import sys

#A container for the connections and coordinates of each part of the maze.
class MazePiece:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.shortest_path = float("infinity")
        #Empty lists will denote a wall, and non-empty lists will denote 
        #a corridor.     
        self.connections = []
    #def __str__(self):
       # return "%d, %d" % (self.x, self.y)
    def __str__(self):
        return str(len(self.connections))

#print the number of connections for each MazePiece
def print_maze_connections(m):
    for i in range(len(m[0])):
        for x in m:
            if len(x[i].connections):
                print(x[i], end = " ")
            else:
                print("W", end = " ")
        print()
    print()

#return a list of coordinates along which the shortest path through maze m lies.
def shortest_path(m, start, target):
    #BFS
    visited = [start]
    fronteir = start.connections[:]
    for i in fronteir:
        i.shortest_path = 1
            
    start.shortest_path = 0
    curr = start
    
    #tell all the pieces what their shortest path is
    while curr != target and fronteir != []:
        visited.append(curr)
        curr = fronteir.pop(0)
        for i in curr.connections:
            if (curr.shortest_path+1 < i.shortest_path):
                i.shortest_path = curr.shortest_path+1
            if (i not in visited and i not in fronteir):
                fronteir.append(i)
    
    #follow and record the path from the target back to the start
    path = [(target.x,target.y)]
    curr = target
    while curr != start:
        for i in curr.connections:
            if (i.shortest_path == curr.shortest_path-1):
                curr = i
        path.append((curr.x,curr.y))
    return path
            
        

#print the properly formatted maze, optionally with the shortest path through it
def print_maze(m,w,h):
    start = m[0][h//4]
    
    #fill display grid with walls to start
    display = []
    for x in range(len(m)*2+1):
        row = []
        for y in range(len(m[0])*2+1):
        #    row.append("W")
            if(x < 1/3*w):
                row.append("black wall")
            elif(x > 1/3*w and x < 2/3*w):
                row.append("grey wall")
            elif(x < w):
                row.append("white wall")
        display.append(row)
       
    connections = wall_table(len(m),len(m[0]))
    
    l = [start] 
    seen = [start]
    while l:
        #draw paths at corners
        current = l.pop(0)
        seen.append(current)
        display[current.x*2+1][current.y*2+1] = ""
        #draw path between corners
        for i in current.connections:
            if i not in seen:
                display[current.x*2 + i.x-current.x + 1][current.y*2 + i.y-current.y + 1] = ""
                l.append(i)


    #print the display grid 
    #for i in range(len(display[0])):
    #        for x in display:
    #            print(x[i], end = " ")
    #        print("")
        
    return display
        
#return the direct neighbours of piece
def get_neighbours(table, piece):
    l = []
    if piece.x >= 1:
        l.append(table[piece.x-1][piece.y])
    if piece.y >= 1:
        l.append(table[piece.x][piece.y-1])
    if piece.x < len(table)-1:
        l.append(table[piece.x+1][piece.y])
    if piece.y < len(table[0])-1:
        l.append(table[piece.x][piece.y+1])
    return l
        
#make a table filled with MazePieces
def wall_table(width, height):
    t = []
    for x in range(width):
        row = []
        for y in range(height):
            row.append(MazePiece(x,y))
        t.append(row)
    return t
            
            
def make_maze(width, height):

    #find the size that the maze matrix needs to be since it doesn't contain
    #walls, but connections.
    width = width//2
    height = height//2
    
    
    #m will hold the maze pieces
    m = wall_table(width, height)
    
    #set the starting point and the walls around it
    maze_list = [m[0][height//2]]
    wall_list = get_neighbours(m,m[0][height//2])

    while wall_list:
        current = wall_list[random.randint(0,len(wall_list)-1)]
        
        #get a random neighbour that is in the maze
        n = []
        for i in get_neighbours(m,current):
            if i in maze_list:
                n.append(i)
                
        #if we found one then make a connection between the it and current
        #and add current's neighbours to the wall_list
        if n != []:
            n = n[random.randint(0, len(n)-1)]
        
            n.connections.append(current)
            current.connections.append(n)
            maze_list.append(current)
            
            for i in get_neighbours(m, current):
                if i not in maze_list and i not in wall_list:
                    wall_list.append(i)
                
        wall_list.remove(current)

    return m
    
if __name__ == "__main__":
    
    #w = 70
    #h = 70
    w = int(input("Please enter a width: "))
    h = int(input("Please enter a height: "))
    
    m = make_maze(w,h)
    #print_maze_connections(m)
    print_maze(m,w,h)