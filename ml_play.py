class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        self.target_lane = self.car_lane
        pass

    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |    |
        |  1 |  2 |  3 |
        |    |  5 |    |
        |  4 |  c |  6 |
        |    |    |    |
        |  7 |  8 |  9 |
        |    |    |    |       
        """
        def check_grid():
            grid = set()
            speed_ahead = 100
            if self.car_pos[0] <= 65: # left bound
                grid.add(4)
            elif self.car_pos[0] >= 565: # right bound
                grid.add(6)

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    dropDistance = (self.car_vel - car["velocity"]) * ((abs(self.car_pos[0] - car["pos"][0]) // 3) + 8 )
                    laneDif = ((car["pos"][0] // 70) - self.car_lane)
                    if dropDistance > y - 90 and dropDistance < y + 103:
                        if abs(laneDif) <= 2:
                            grid.add(laneDif)
                    if x > -45 and x <= -40 :
                        if y > -82 and y < 82:
                            grid.add(4)
                    if x < 45 and x >= 40:
                        if y > -82 and y < 82:
                            grid.add(6)
            return targeting(grid = grid)

        def targeting(grid):
            self.target_lane = self.car_lane
            for coin in scene_info["coins"]:
                print((coin[0] - self.car_pos[0]) / 3, (self.car_pos[1] - coin[1]) / 5)
                if (coin[1] < self.car_pos[1]) and ((abs(coin[0] - self.car_pos[0]) / 3) < (self.car_pos[1] - coin[1]) / 5) + 4:
                    if coin[0] // 70 < self.car_lane and (-1 not in grid) and (-2 not in grid):
                        self.target_lane = coin[0] // 70
                        print("target_set:",self.target_lane)
                        break
                    elif coin[0] // 70 > self.car_lane and (1 not in grid) and (2 not in grid):
                        self.target_lane = coin[0] // 70
                        print("target_set:",self.target_lane)
                        break
                    elif coin[0] // 70 == self.car_lane:
                        self.target_lane = self.car_lane
                        break
            if (4 in grid) and self.car_lane != 8:
                self.target_lane = self.car_lane + 1
            if (6 in grid) and self.car_lane != 0:
                self.target_lane = self.car_lane - 1
            return move(grid= grid)
            
        def move(grid): 
            # if self.player_no == 0:
            #     print(grid)
            if self.player_no == 0:
                print(self.car_lane, self.target_lane, self.car_lane > self.target_lane, self.car_lane < self.target_lane)
                if len(grid) != 0:
                    print(self.player_no , grid)
            if len(grid) == 0:
                return ["SPEED"]
            else:
                if (0 not in grid): # Check forward 
                    # Back to lane center
                    if self.car_lane > self.target_lane:
                        print("self.car_lane > self.target_lane")
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_lane < self.target_lane:
                        print("self.car_lane < self.target_lane")
                        return ["SPEED", "MOVE_RIGHT"]
                    else :
                        if self.car_pos[0] < self.lanes[self.target_lane]:
                            print("self.car_pos[0] < self.lanes[self.target_lane]")
                            return ["SPEED", "MOVE_RIGHT"]
                        if self.car_pos[0] > self.lanes[self.target_lane]:
                            print("self.car_pos[0] > self.lanes[self.target_lane]")
                            return ["SPEED", "MOVE_LEFT"]
                        else: 
                            print("Else SPEED")
                            return ["SPEED"]
                elif (0 in grid):
                    if (4 not in grid) and (-1 not in grid): # turn left 
                        print("MOVE_LEFT")
                        return ["MOVE_LEFT"]
                    elif (6 not in grid) and (1 not in grid): # turn right
                        print("MOVE_RIGHT")
                        return ["MOVE_RIGHT"]
                    else : 
                        print("BRAKE")
                        return ["BRAKE"]
                    
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass
