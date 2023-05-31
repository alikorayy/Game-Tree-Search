class Game:
    def __init__(self, grid):
        self.grid = grid
        self.state = [['']*(len(grid[0])-1) for _ in range(len(grid)-1)]
        self.is_pointmarked = [['-' if cell == 0 else False for cell in row] for row in grid]
        self.player = 0
        self.scores = [0, 0]

    def is_valid_move(self, x, y):
        return 0 <= x < len(self.state) and 0 <= y < len(self.state[0]) and self.state[x][y] == ''

    def make_move(self, x, y):
        if not self.is_valid_move(x, y):
            return False
        self.state[x][y] = self.player
        self.update_scores(x, y)
        self.player = 1 - self.player
        return True

    def update_scores(self, x, y):

      cell_neighbors = [(x,y),(x+1,y),(x,y+1),(x+1,y+1)]
      point_scores = 0
      for positions in cell_neighbors:
        neighbors_sum = 0
        if self.grid[positions[0]][positions[1]] != 0 and self.is_pointmarked[positions[0]][positions[1]] == False:
          # check left upper neighbor
          if (positions[0] > 0 and positions[1] > 0):
            if(self.state[positions[0]-1][positions[1]-1] != ''):
              neighbors_sum +=self.state[positions[0]-1][positions[1]-1]

          # check right upper neighbor
          if ((positions[0] > 0) and  (positions[1] < len(self.grid[0]) - 1)):
            if(self.state[positions[0]-1][positions[1]] != ''):
                neighbors_sum += 1-self.state[positions[0]-1][positions[1]]
            
          #check left bottom neighbor
          if ((positions[0] < len(self.grid) - 1) and (positions[1] > 0)):
            if(self.state[positions[0]][positions[1]-1] != ''):
              neighbors_sum += 1-self.state[positions[0]][positions[1]-1]
            
          #check right bottom neighbor
          if ((positions[0] < len(self.grid) - 1) and (positions[1] < len(self.grid[0])-1)):
            if(self.state[positions[0]][positions[1]] != ''):
              neighbors_sum +=self.state[positions[0]][positions[1]]
            
          #sum the neighbors and check whether it is equal to value in the matrix
          if neighbors_sum == self.grid[positions[0]][positions[1]] :
            point_scores += neighbors_sum
            self.is_pointmarked[positions[0]][positions[1]] = True
            
      
      self.scores[self.player] += point_scores
      self.scores[1-self.player] -= point_scores


    def evaluate(self):
        # Evaluate the board state and return the score
        if self.player == 0:
          end_scores = self.scores[0] - self.scores[1]
        elif self.player == 1:
          end_scores = self.scores[0] - self.scores[1]
        return end_scores


    def game_over(self):
        # This function checks whether the game has end or not
        is_over = True
        for i in range(len(self.state)):
          for k in range(len(self.state[0])):
            if self.state[i][k] == '':
              is_over = False
              break
        return is_over

    def alpha_beta(self, alpha, beta, maximizing_player,depth):
      if self.game_over() or depth == 0:
          return self.evaluate()
      if maximizing_player:
          max_eval = float('-inf')
          for x in range(len(self.state)):
              for y in range(len(self.state[0])):
                  if self.is_valid_move(x, y):
                      # Copy the old scores and pointmarks
                      old_scores = self.scores.copy()
                      old_is_pointmarked = [row.copy() for row in self.is_pointmarked]

                      self.make_move(x, y)
                      eval = self.alpha_beta(alpha, beta, False,depth-1)
                      #Restore the old scores
                      self.state[x][y] = ''
                      self.scores = old_scores
                      self.is_pointmarked = old_is_pointmarked
                      self.player = 1 - self.player
                      #Alpha-Beta Pruning
                      max_eval = max(max_eval, eval)
                      alpha = max(alpha, eval)
                      if beta <= alpha:
                          break
          return max_eval
      else:
          min_eval = float('inf')
          for x in range(len(self.state)):
              for y in range(len(self.state[0])):
                  if self.is_valid_move(x, y):
                      # Copy the old scores and pointmarks
                      old_scores = self.scores.copy()
                      old_is_pointmarked = [row.copy() for row in self.is_pointmarked]

                      self.make_move(x, y)
                      eval = self.alpha_beta(alpha, beta, True,depth-1)
                       #Restore the old scores
                      self.state[x][y] = ''
                      self.scores = old_scores
                      self.is_pointmarked = old_is_pointmarked
                      self.player = 1 - self.player
                      #Alpha-Beta Pruning
                      min_eval = min(min_eval, eval)
                      beta = min(beta, eval)
                      if beta <= alpha:
                          break
          return min_eval

def main():
    # Initialize the game with a grid
    
    '''
    grid = [[0, 1, 0],
            [1, 2, 1],
            [0, 1, 0]]
    
    
    
    grid = [
    [0, 1, 1, 2, 0],
    [2, 0, 1, 0, 1],
    [1, 0, 2, 1, 1],
    [2, 1, 1, 1, 0],
    [0, 0, 1, 0, 0]   
    ] 
    
    '''
    grid = [[1, 0,  1],
            [0, 2, 0],
            [0, 0,  1]]
       
    
    game = Game(grid)
    # Game loop
    while game.game_over() == False:
        print(f"Player {game.player + 1}'s turn")
        if game.player == 0:  # Human player's Turn
            x = int(input("Please enter a valid x cordinate of your move: "))
            y = int(input("Please enter a valid y cordinate of your move: "))
            while not game.make_move(x, y):
                print("Invalid move. Try again.")
                x = int(input("Please enter a valid x cordinate of your move: "))
                y = int(input("Please enter a valid y cordinate of your move: "))
            #game.player = 0
        else:  #The AI Player's Turn
            best_score = float('inf')
            best_move = None
            for x in range(len(game.state)):
                for y in range(len(game.state[0])):
                    # Copy the old scores and pointmarks
                    old_scores_main = game.scores.copy()
                    old_is_pointmarked_main = [row.copy() for row in game.is_pointmarked]
                    if game.make_move(x, y):
                        score = game.alpha_beta(float('-inf'), float('inf'), True,3)
                        game.state[x][y] = ''
                        game.scores = old_scores_main
                        game.is_pointmarked = old_is_pointmarked_main
                        game.player = 1 - game.player
                        if score < best_score:
                            best_score = score
                            best_move = (x, y)
             #Decide best move
            game.make_move(*best_move)
            print("AI Made move at: ",best_move)
        #game.player = 1 - game.player  # Switch to the next player
        print("Current scores: ",game.scores)

    # Game over
    print(f"The Game is over. Final scores are: ",game.scores)
    if game.scores[0] > game.scores[1]:
       print("You Win")
    elif game.scores[0] < game.scores[1]:
       print("You loose")
    elif game.scores[0] == game.scores[1]:
       print("The game is tie")

if __name__ == "__main__":
    main()
