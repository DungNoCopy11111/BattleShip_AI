import random

class Ship:
    def __init__(self,size):
        self.row = random.randrange(0,9)
        self.col = random.randrange(0,9)
        self.size = size
        self.orientation =random.choice(["h","v"])
        self.indexes = self.compute_indexes()
    
    def compute_indexes(self):
        #  vị trí xuất phát
        start_index = self.row*10+self.col
        if self.orientation == "h":
            return [start_index + i for i in range(self.size)]
        elif self.orientation == "v":
            return [start_index + i*10 for i in range(self.size)] 

class Player:
    def __init__(self):
        self.ships = []
        self.search = ["U" for i in range(100)]
        self.place_ships(sizes=[5, 4, 3, 3, 2])
        
        # danh sách các chỉ số của mỗi chiến hạm [[1,2,3],[5,6,7]]
        list_of_lists = [ship.indexes for ship in self.ships]
        
        #danh sách các ô nơi chứa các chiến hamj [1,2,3,5,6,7]
        self.indexes = [index for sublist in list_of_lists for index in sublist]

    def place_ships(self, sizes):
        for size in sizes:
            placed = False
            while not placed:
                ship = Ship(size)
                # Kiểm tra xem vị trí có thể đặt hay không
                possible = True
                for i in ship.indexes:
                    if i >= 100:
                        possible = False
                        break
                    # Tìm hàng và cột mới
                    new_row = i//10
                    new_col = i%10
                    if new_row != ship.row and new_col != ship.col:
                        possible = False
                        break
                    #Các tàu không được giao nhau
                    for other_ship in self.ships:
                        if i in other_ship.indexes:
                            possible = False
                            break

                if possible:
                    self.ships.append(ship)
                    placed = True
    
    # hiển thị trạng thái của các chiến hạm
    def show_ships(self):
        indexes = ["-" if i not in self.indexes else "X" for i in range(100)]
        for row in range(10):
            print(" ".join(indexes[(row-1)*10:row*10]))
              
p = Player()
p.show_ships()

class Game: 
    def __init__(self,human1,human2):
        self.human1 = human1
        self.human2 = human2
        self.player1 = Player()
        self.player2 = Player()
        self.player1_turn = True
        self.computer_turn = True if not self.human1 else False
        self.over = False
        self.result  = None
    
    def make_move(self,i):
        player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1
        hit = False 
        if i in opponent.indexes:
            player.search[i] = "H"
            hit = True
            #CHECK if ship is sunk
            for ship in opponent.ships:
                    sunk = True
                    for i in ship.indexes:
                        if player.search[i] == "U":
                            sunk = False
                            break
                    if sunk:
                        for i in ship.indexes:
                            player.search[i] = "S"                                   
        else:
            player.search[i] = "M"
        
        
        #Check gameover
        game_over = True
        for i in opponent.indexes:
            if player.search[i] =="U":
                game_over=False
        self.over = game_over
        self.result = 1 if self.player1_turn else 2
        
        if not hit:
            self.player1_turn = not self.player1_turn
            
            if(self.human1 and not self.human2) or (not self.human1 and self.human2):
                self.computer_turn = not self.computer_turn

    def random_ai(self):
        search = self.player1.search if self.player1_turn  else self.player2.search
        unknown = [i for i,square in enumerate(search) if square =="U"]
        if len(unknown) > 0 :
            random_index = random.choice(unknown)
            self.make_move(random_index)
    
    def basic_ai(self):
        #setup
        
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i,square in enumerate(search) if square =="U"]
        hits = [i for i,square in enumerate(search) if square =="H"]
        
        unknown_with_neighboring_hits = []
        unknown_with_neighboring_hits2 = []
        for u in unknown:
            if u+1 in hits or u-1 in hits or u-10 in hits or u+10 in hits:
                unknown_with_neighboring_hits.append(u)
        if len(unknown_with_neighboring_hits) > 0:
            self.make_move(random.choice(unknown_with_neighboring_hits))
            return
            
        self.random_ai()