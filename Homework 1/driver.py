import time
from collections import deque
from queue import PriorityQueue
import sys
import resource


class Node():
    def __init__(self,board,parent,dir,depth,cost,priority=None):
        self.board = board
        self.parent = parent
        self.dir=dir
        self.depth=depth
        self.cost=cost
        self.priority=priority

    def __lt__(self,board2):
        return self.board < board2.board
       

class N_puzzle():
    def __init__(self,init_node):
        self.init_node = init_node
        self.goal_state = [0,1,2,3,4,5,6,7,8]
        self.nodes_expanded = 0
        self.max_node_depth = 0

    def get_children(self,board,direction):
        index = board.board.index(0)
        if direction == 0:
           
            if (index>=0 and index<=2):
                return None
            else:
                new_board = board.board[:]
                new_board[index],new_board[index-3] = new_board[index-3],new_board[index]
                Up_node = Node(new_board,board,direction,board.depth+1,board.cost+1)
                return Up_node

        if direction == 1:
            if (index>=6 and index<=8):
                return None
            else:
                new_board = board.board[:]
                new_board[index],new_board[index+3] = new_board[index+3],new_board[index]
                Down_node = Node(new_board,board,direction,board.depth+1,board.cost+1)

                return Down_node
        if direction == 2:
            if index % 3 == 0:
                return None
            else:
                new_board = board.board[:]

                new_board[index],new_board[index-1] = new_board[index-1],new_board[index]
                Left_node = Node(new_board,board,direction,board.depth+1,board.cost+1)

                return Left_node

        if direction == 3:
            if index % 3 == 2:
                return None
            else:
                new_board = board.board[:]
                new_board[index],new_board[index+1] = new_board[index+1],new_board[index]
                Right_node = Node(new_board,board,direction,board.depth+1,board.cost+1)
                return Right_node

    def get_path(self,node):
        final_path = list()
        traversal = node
        while(traversal.dir!=None):
            if traversal.dir ==0:
                final_path.append("Up")
            if traversal.dir==1:
                final_path.append("Down")
            if traversal.dir==2:
                final_path.append("Left")
            if traversal.dir==3:
                final_path.append("Right")
            traversal=traversal.parent
        final_path.reverse()
        return final_path

    #Queue ops, enqueue(put to back,), dequeue(remove from front)
    def bfs(self):
        #frontier = deque([self.init_node])
        frontier = list([self.init_node])
        frontier_members = set(tuple(self.init_node.board))
        visited = set()

        while frontier:
            current = frontier.pop(0)
            visited.add(tuple(current.board))
            if current.board == self.goal_state:
                path = self.get_path(current)
                return path, current.depth,current.cost,self.nodes_expanded,self.max_node_depth
            
            #import pdb; pdb.set_trace()
            self.nodes_expanded+=1
            children = [self.get_children(current,direction) for direction in range(0,4)]

            
            for child in children:
                if child:   
                    if child.depth > self.max_node_depth:
                        self.max_node_depth= child.depth
                    if (tuple(child.board) not in visited):
                        frontier.append(child)
                        visited.add(tuple(child.board))
                        
    
    #Stack ops, push(put to back,), pop (remove from back)
    def dfs(self):
        frontier =list([self.init_node])
        frontier_members = set(tuple(self.init_node.board))
        visited = set()

        while frontier:
            current = frontier.pop()
            visited.add(tuple(current.board))

            if current.board == self.goal_state:
                path = self.get_path(current)
                return path, current.depth,current.cost,self.nodes_expanded,self.max_node_depth

            self.nodes_expanded+=1
            children = [self.get_children(current,direction) for direction in range(0,4)]
            children.reverse()

            for child in children:
                if child:   
                    if child.depth > self.max_node_depth:
                        self.max_node_depth= child.depth
                    if(tuple(child.board) not in visited):
                        frontier.append(child)
                        visited.add(tuple(child.board))

    def manhattan_dist(self,node):
        score = 0
        for i in range(1,len(node.board)):
            current, desired = node.board.index(i), self.goal_state.index(i)
            
            row_dist = int(abs(current-desired)/3)
            col_dist = abs(current-desired) % 3 
            score += row_dist+col_dist
        return score

    #priority queue
    def ast(self):
        frontier = PriorityQueue()
        frontier_membership = set()
        visited = set()
        frontier.put((self.init_node.depth,0,self.init_node))
        frontier_membership.add(tuple(self.init_node.board))
        while frontier.qsize() >0:
            f,g,current = frontier.get()
            
            if current.board == self.goal_state:
                path = self.get_path(current)
                return path, current.depth,current.cost,self.nodes_expanded,self.max_node_depth

            self.nodes_expanded+=1
            children = [self.get_children(current,direction) for direction in range(0,4)]

            for child in children:
                if child:
                    if child.depth > self.max_node_depth:
                        self.max_node_depth = child.depth
                    h_score = self.manhattan_dist(child)
                    decider=g+child.dir
                    if(tuple(child.board) not in visited)):     
                        
                        if tuple(child.board) in frontier_membership:
                            decider+=child.cost
                        entry = (h_score+child.cost,decider,child)
                        tentry =(h_score+child.cost,child.dir,child.board)
                        frontier.put(entry)
                        frontier_membership.add(tuple(child.board))
                        visited.add(tuple(child.board))
                   
                            #TODO - get the score, add the node to the PQ
                    elif(tuple(child.board) in visited and tuple(child.board) in frontier_membership):
                        decider+=h_score
                        print(decider)
                        entry = (h_score+child.cost,decider,child)
                        frontier.put(entry)
                        visited.add(tuple(child.board))
                        print("ah shit, this already exists")

#converts the input string into a list for computation
def convert_to_list(input):
    state = input.split(",")
    state = [int(x) for x in state]
    return state

def write_to_file(path,expanded,cost,depth,max_depth,runtime,max_ram):
    file = open("output.txt","w")
    file.write("path_to_goal: "+ str(path)+"\n")
    file.write("nodes_expanded"+str(expanded)+"\n")
    file.write("cost: "+str(cost)+"\n")
    file.write("depth:"+str(depth)+"\n")
    file.write("max_search_depth: "+str(max_depth)+"\n")
    file.write("running time: "+ runtime+"\n")
    file.write("max_ram_usage: "+max_ram+"\n")
    file.close()


junk, method, input_state = sys.argv

input_list = convert_to_list(input_state)


start = Node(input_list,None,None,0,0)

Puzzle = N_puzzle(start)
if method == 'bfs':
    start_time = time.time()
    path,depth,cost,expanded,max_depth = Puzzle.bfs()
    end_time=time.time()
    runtime = "{0:.8f}".format(end_time-start_time)
    max_ram = "{0:.8f}".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)
    write_to_file(path,depth,cost,expanded,max_depth,runtime,max_ram)

if method == 'dfs':
    start_time = time.time()
    path,depth,cost,expanded,max_depth = Puzzle.dfs()
    end_time=time.time()
    runtime = "{0:.8f}".format(end_time-start_time)
    max_ram = "{0:.8f}".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)
    write_to_file(path,depth,cost,expanded,max_depth,runtime,max_ram)
if method == 'ast':
    start_time = time.time()
    path,depth,cost,expanded,max_depth = Puzzle.bfs()
    end_time=time.time()
    runtime = "{0:.8f}".format(end_time-start_time)
    max_ram = "{0:.8f}".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000)
    write_to_file(path,depth,cost,expanded,max_depth,runtime,max_ram)