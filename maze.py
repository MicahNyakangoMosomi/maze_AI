import sys
# Node class represents a state in the search tree
class Node():
  def __init__(self, state, parent, action):
    self.state = state  # Current position in the maze
    self.parent = parent  # Parent node (previous position)
    self.action = action  # Action taken to reach this state

# StackFrontier implements a stack (LIFO) data structure for depth-first search
class StackFrontier():
  def __init__(self):
    self.frontier = []
  
  def add(self, node):
    self.frontier.append(node)  # Add node to the frontier
  
  def contains_state(self, state):
    return any(node.state == state for node in self.frontier)  # Check if state is in frontier
  
  def empty(self):
    return len(self.frontier) == 0  # Check if frontier is empty
  
  def remove(self):
    if self.empty():
      raise Exception("Empty Frontier")  # Raise error if no nodes left to explore
    else:
      node = self.frontier[-1]  # Remove last node (LIFO behavior)
      self.frontier = self.frontier[:-1]
      return node

# QueueFrontier implements a queue (FIFO) data structure for breadth-first search
class QueueFrontier(StackFrontier):
  def remove(self):
    if self.empty():
      raise Exception("Empty Frontier")
    else:
      node = self.frontier[0]  # Remove first node (FIFO behavior)
      self.frontier = self.frontier[1:]
      return node
    
# Maze class handles maze structure and solving process
class Maze():
  
  def __init__(self, filename):
    # Read file and set height and width of the maze
    with open(filename) as f:
      contents = f.read()
      
    # Validate start and goal points
    if contents.count("A") != 1:
      raise Exception("Maze must have exactly one start point")
    if contents.count("B") != 1:
      raise Exception("Maze must have exactly one goal")
    
    # Determine maze dimensions
    contents = contents.splitlines()
    self.height = len(contents)
    self.width = max(len(line) for line in contents)
    
    # Keep track of walls and start/goal positions
    self.walls = []
    for i in range(self.height):
      row = []
      for j in range(self.width):
        try:
          if contents[i][j] == "A":
            self.start = (i, j)  # Mark start position
            row.append(False)
          elif contents[i][j] == "B":
            self.goal = (i, j)  # Mark goal position
            row.append(False)
          elif contents[i][j] == " ":
            row.append(False)  # Open path
          else:
            row.append(True)  # Wall
        except IndexError:
          row.append(False)
      self.walls.append(row)
    
    self.solution = None  # Solution path
    
  # Print the maze with solution path if available
  def print(self):
    solution = self.solution[1] if self.solution is not None else None
    print()
    for i, row in enumerate(self.walls):
      for j, col in enumerate(row):
        if col:
          print("♦", end="")  # Wall
        elif (i, j) == self.start:
          print("A", end="")  # Start point
        elif (i, j) == self.goal:
          print("B", end="")  # Goal point
        elif solution is not None and (i, j) in solution:
          print("*", end="")  # Solution path
        else:
          print(" ", end="")  # Open path
      print()
    print()
    
  # Get valid neighbors of a given state
  def neighbors(self, state):
    row, col = state
    
    # All possible movement actions
    candidates = [
      ("up", (row - 1, col)),
      ("down", (row + 1, col)),
      ("left", (row, col - 1)),
      ("right", (row, col + 1))
    ]
    
    # Ensure actions are valid (inside maze and not walls)
    result = []
    for action, (r, c) in candidates:
      try:
        if not self.walls[r][c]:
          result.append((action, (r, c)))
      except IndexError:
        continue  # Skip invalid moves
    return result
    
  # Solve the maze using depth-first search
  def solve(self):
    """Finds a solution to the maze, if one exists."""
    
    # Keep track of the number of states explored
    self.num_explored = 0
    
    # Initialize frontier with the start position
    start = Node(state=self.start, parent=None, action=None)
    frontier = StackFrontier()
    frontier.add(start)
    
    # Initialize an empty explored set
    self.explored = set()
    
    # Keep looping until a solution is found
    while True:
      
      # If nothing left in frontier, no solution exists
      if frontier.empty():
        raise Exception("No solution")
      
      # Choose a node from the frontier
      node = frontier.remove()
      self.num_explored += 1
      
      # If node is the goal, solution found
      if node.state == self.goal:
        actions = []
        cells = []
        
        # Follow parent nodes to reconstruct the solution path
        while node.parent is not None:
          actions.append(node.action)
          cells.append(node.state)
          node = node.parent
        
        actions.reverse()
        cells.reverse()
        self.solution = (actions, cells)  # Store solution path
        return
      
      # Mark node as explored
      self.explored.add(node.state)
      
      # Add valid neighbors to the frontier
      for action, state in self.neighbors(node.state):
        if not frontier.contains_state(state) and state not in self.explored:
          child = Node(state=state, parent=node, action=action)
          frontier.add(child)
