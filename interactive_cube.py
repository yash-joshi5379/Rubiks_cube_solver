from vpython import *
import numpy as np
from solve_cube import start_state, moves_list
import sys
import time

colour_to_vector = {
    "W" : vector(1,1,1),
    "B" : vector(0,0,1),
    "Y" : vector(1,1,0),
    "R" : vector(1,0,0),
    "O" : vector(1,0.5,0),
    "G" : vector(0,1,0)
}

face_to_orientation = {
    "front" : [0, vector(0,0,0)],
    "left" : [np.pi/2, vector(0,1,0)],
    "right" : [np.pi/2, vector(0,1,0)],
    "back" : [0, vector(0,0,0)],
    "up" : [np.pi/2, vector(1,0,0)],
    "down" : [np.pi/2, vector(1,0,0)]
}

class Rubiks_Cube_3D():  # Create class for interactive rubix cube

    def __init__(self):  # Instantiate class
        self.running = True  # Boolean describes whether the program is running or not
        self.tiles = []  # Declare list of tiles
        self.rotation_speed = 0.01  # Set rotation speed
        self.positions = {  # Declare empty dictionary into which tiles will be added
            "front": [],
            "left": [],
            "right": [],
            "back": [],
            "up": [],
            "down": []}
        self.rotate = [None,0,0]
        self.moves = []
        self.velocity = 100

        tile_pos = [[vector(-1, 1, 1.5), vector(0, 1, 1.5), vector(1, 1, 1.5),  # front face positions
                     vector(-1, 0, 1.5), vector(0, 0, 1.5), vector(1, 0, 1.5),
                     vector(-1, -1, 1.5), vector(0, -1, 1.5), vector(1, -1, 1.5)],

                    [vector(-1.5, 1, -1), vector(-1.5, 1, 0), vector(-1.5, 1, 1),  # left face positions
                     vector(-1.5, 0, -1), vector(-1.5, 0, 0), vector(-1.5, 0, 1),
                     vector(-1.5, -1, -1), vector(-1.5, -1, 0), vector(-1.5, -1, 1)],

                    [vector(1.5, 1, 1), vector(1.5, 1, 0), vector(1.5, 1, -1),  # right face positions
                     vector(1.5, 0, 1), vector(1.5, 0, 0), vector(1.5, 0, -1),
                     vector(1.5, -1, 1), vector(1.5, -1, 0), vector(1.5, -1, -1)],

                    [vector(1, 1, -1.5), vector(0, 1, -1.5), vector(-1, 1, -1.5),  # back face positions
                     vector(1, 0, -1.5), vector(0, 0, -1.5), vector(-1, 0, -1.5),
                     vector(1, -1, -1.5), vector(0, -1, -1.5), vector(-1, -1, -1.5)],

                    [vector(-1, 1.5, -1), vector(0, 1.5, -1), vector(1, 1.5, -1),  # top face positions
                     vector(-1, 1.5, 0), vector(0, 1.5, 0), vector(1, 1.5, 0),
                     vector(-1, 1.5, 1), vector(0, 1.5, 1), vector(1, 1.5, 1)],

                    [vector(-1, -1.5, 1), vector(0, -1.5, 1), vector(1, -1.5, 1),  # bottom face positions
                     vector(-1, -1.5, 0), vector(0, -1.5, 0), vector(1, -1.5, 0),
                     vector(-1, -1.5, -1), vector(0, -1.5, -1), vector(1, -1.5, -1)]]

        for face_index, facelets_list in enumerate(tile_pos):  # Iterates through each facelet and keeps track of its index
            face = list(start_state.keys())[face_index]  # Converts the face index to a face name
            #print(face)  # Outputs the face name, for troubleshooting
            #print(facelets_list)  # Outputs the positions list for the face
            facelet_index = 0  # Set a counter to zero
            for position_vector in facelets_list:  # For each facelet,
                facelet_colour = start_state[face][facelet_index]  # Find the facelet's colour
                #print(facelet_colour)  # Outputs the colour, for troubleshooting
                facelet_colour_vector = colour_to_vector[facelet_colour]
                tile = box(pos = position_vector, size = vector(0.98,0.98,0.1), color = facelet_colour_vector)
                # Creates a coloured 0.98x0.98x0.1 box at the position vector
                tile.rotate(angle=face_to_orientation[face][0], axis=face_to_orientation[face][1])
                # Gives the tile its orientation depending on the face
                self.tiles.append(tile)  # Adds the tile to the 3D cube
                self.positions[face].append(tile)
                facelet_index += 1  # Increment counter

    def reset_positions(self):  # Method to reassign tiles to faces after a rotation
        self.positions = {'front': [], 'right': [], 'back': [], 'left': [], 'up': [], 'down': []}  # Redefine positions dictionary
        for tile in self.tiles:  # For each facelet,
            #print(tile.pos.x)
            if tile.pos.z > 0.4:  # Depending on the facelet's vector position, assign it a face
                self.positions['front'].append(tile)
            if tile.pos.x > 0.4:
                self.positions['right'].append(tile)
            if tile.pos.z < -0.4:
                self.positions['back'].append(tile)
            if tile.pos.x < -0.4:
                self.positions['left'].append(tile)
            if tile.pos.y > 0.4:
                self.positions['up'].append(tile)
            if tile.pos.y < -0.4:
                self.positions['down'].append(tile)
        for key in self.positions.keys():
            self.positions[key] = set(self.positions[key])  # Creates a set of tiles which can now be iterated through

    # def spin(self):
    #     time.sleep(1)
    #     self.rotate[1] = 0
    #     self.rotate[2] = np.pi * 2
    #     pieces = self.tiles
    #     direction = self.rotation_speed
    #     for tile in pieces:
    #         tile.rotate(angle=direction, axis=vector(0,1,0), origin=vector(0,0,0))
    #     self.rotate[1] += self.rotation_speed


    def animation(self):  # Method to animate rotations
        if self.rotate[0] == "F" or self.rotate[0] == "F'":  # If move is F or F',
            pieces = self.positions['front']  # Creates a set of tiles in the front face
            if self.rotate[0] == "F":
                direction = -self.rotation_speed  # clockwise if F
            else:
                direction = self.rotation_speed  # anticlockwise if F'
            for tile in pieces:  # For each tile,
                tile.rotate(angle= direction, axis=vector(0, 0, 1), origin=vector(0,0,0))
                # Rotate along the z axis with the rotation speed
            self.rotate[1] += self.rotation_speed  # Increment the amount of rotation reached

        if self.rotate[0] == "B" or self.rotate[0] == "B'":  # If move is B or B',
            pieces = self.positions['back']  # Creates a set of tiles in the back face
            if self.rotate[0] == "B":
                direction = self.rotation_speed  # clockwise if B
            else:
                direction = -self.rotation_speed  # anticlockwise if B'
            for tile in pieces:  # For each tile,
                tile.rotate(angle= direction, axis=vector(0, 0, 1), origin=vector(0,0,0))
                # Rotate along the z axis with the rotation speed
            self.rotate[1] += self.rotation_speed  # Increment the amount of rotation reached

        if self.rotate[0] == "L" or self.rotate[0] == "L'":  # If move is L or L',
            pieces = self.positions['left']  # Creates a set of tiles in the left face
            if self.rotate[0] == "L":
                direction = self.rotation_speed  # clockwise if L
            else:
                direction = -self.rotation_speed  # anticlockwise if L'
            for tile in pieces:  # For each tile,
                tile.rotate(angle= direction, axis=vector(1, 0, 0), origin=vector(0,0,0))
                # Rotate along the x axis with the rotation speed
            self.rotate[1] += self.rotation_speed  # Increment the amount of rotation reached

        if self.rotate[0] == "R" or self.rotate[0] == "R'":  # If move is R or R',
            pieces = self.positions['right']  # Creates a set of tiles in the right face
            if self.rotate[0] == "R":
                direction = -self.rotation_speed  # clockwise if R
            else:
                direction = self.rotation_speed  # anticlockwise if R'
            for tile in pieces:  # For each tile,
                tile.rotate(angle= direction, axis=vector(1, 0, 0), origin=vector(0,0,0))
                # Rotate along the x axis with the rotation speed
            self.rotate[1] += self.rotation_speed  # Increment the amount of rotation reached

        if self.rotate[0] == "U" or self.rotate[0] == "U'":  # If move is U or U',
            pieces = self.positions['up']  # Creates a set of tiles in the up face
            if self.rotate[0] == "U":
                direction = -self.rotation_speed  # clockwise if U
            else:
                direction = self.rotation_speed  # anticlockwise if U'
            for tile in pieces:  # For each tile,
                tile.rotate(angle= direction, axis=vector(0, 1, 0), origin=vector(0,0,0))
                # Rotate along the y axis with the rotation speed
            self.rotate[1] += self.rotation_speed  # Increment the amount of rotation reached

        if self.rotate[0] == "D" or self.rotate[0] == "D'":  # If move is D or D',
            pieces = self.positions['down']  # Creates a set of tiles in the down face
            if self.rotate[0] == "D":
                direction = self.rotation_speed  # clockwise if D
            else:
                direction = -self.rotation_speed  # anticlockwise if D'
            for tile in pieces:  # For each tile,
                tile.rotate(angle= direction, axis=vector(0, 1, 0), origin=vector(0,0,0))
                # Rotate along the y axis with the rotation speed
            self.rotate[1] += self.rotation_speed  # Increment the amount of rotation reached

        if self.rotate[0] == "S":  # If move is S
            pieces = self.tiles  # Creates a set of tiles of the full cube
            direction = self.rotation_speed  # Sets the direction to clockwise
            for tile in pieces:  # For each tile,
                tile.rotate(angle=direction, axis=vector(0, 1, 0), origin=vector(0, 0, 0))
                #Rotate along the y axis with the rotation speed
            self.rotate[1] += self.rotation_speed  # Increment the amount of rotation reached


        if (self.rotate[1] + self.rotation_speed > self.rotate[2]) and (self.rotate[1] - self.rotation_speed < self.rotate[2]):
            # If the angle of rotation is reached,
            self.rotate = [None, 0, 0]  # Reset the rotation list
            self.reset_positions()  # Reassign tiles after rotation

    def front_cw(self):  # Rotates front clockwise
        if self.rotate[0] == None:  # If previous rotation is complete,
            self.rotate = ["F", 0, np.pi/2]  # Rotate front face by 90 degrees

    def front_acw(self):  # Rotates front anticlockwise
        if self.rotate[0] == None:  # If previous rotation is complete,
            self.rotate = ["F'", 0, np.pi/2]  # Rotate front face by 90 degrees

    def back_cw(self):  # Rotates back clockwise
        if self.rotate[0] == None:  # If previous rotation is complete,
            self.rotate = ["B", 0, np.pi/2]  # Rotate back face by 90 degrees

    def back_acw(self):  # Rotates back anticlockwise
        if self.rotate[0] == None:  # If previous rotation is complete,
            self.rotate = ["B'", 0, np.pi/2]  # Rotate back face by 90 degrees

    def left_cw(self):  # Rotates left clockwise
        if self.rotate[0] == None:  # If previous rotation is complete,
            self.rotate = ["L", 0, np.pi/2]  # Rotate left face by 90 degrees

    def left_acw(self):  # Rotates left anticlockwise
        if self.rotate[0] == None:  # If previous rotation is complete,
            self.rotate = ["L'", 0, np.pi/2]  # Rotate left face by 90 degrees

    def right_cw(self):  # Rotates right clockwise
        if self.rotate[0] == None:  # If previous rotation is complete,
            self.rotate = ["R", 0, np.pi/2]  # Rotate right face by 90 degrees

    def right_acw(self):  # Rotates right anticlockwise
        if self.rotate[0] == None:  # If previous rotation is complete,
            self.rotate = ["R'", 0, np.pi/2]  # Rotate right face by 90 degrees

    def up_cw(self):  # Rotates up clockwise
        if self.rotate[0] == None:  # If previous rotation is complete,
            self.rotate = ["U", 0, np.pi/2]  # Rotate up face by 90 degrees

    def up_acw(self):  # Rotates up anticlockwise
        if self.rotate[0] == None:  # If previous rotation is complete,
            self.rotate = ["U'", 0, np.pi/2]  # Rotate up face by 90 degrees

    def down_cw(self):  # Rotates down clockwise
        if self.rotate[0] == None:  # If previous rotation is complete,
            self.rotate = ["D", 0, np.pi/2]  # Rotate down face by 90 degrees

    def down_acw(self):  # Rotates down anticlockwise
        if self.rotate[0] == None:  # If previous rotation is complete,
            self.rotate = ["D'", 0, np.pi/2]  # Rotate down face by 90 degrees

    def spin(self):  # Spins cube once solved
        self.velocity = 300  # Increase the speed of rotation
        time.sleep(0.5)  # Gives the program time to update
        if self.rotate[0] == None:  # If all previous rotations are done,
            self.rotate = ["S", 0, np.pi * 6]  # Spin cube 3 times

    def solve(self):  # Method to execute a list of moves
        for move in moves_list:  # For each move,
            move_lst = list(move)  # Convert the move to a list
            if move_lst[-1] == "2":  # If the move contains a 2,
                letter = str(move_lst[0])  # Get the letter of the move
                self.moves.append(letter)  # Add it to the list of moves twice
                self.moves.append(letter)
            else:  # If it does not contain a 2,
                self.moves.append(move)  # Add the move to the list of moves
        self.moves.append("S")  # Ensures cube is spun at end
        #print(self.moves)  # Output the list of single moves
        self.timer_and_num_moves()  # Calls the timer function to start the timer

    def timer_and_num_moves(self):  # Method to measure the solving time
        print("Timer started")  # Lets the user know the time has started
        start = time.time()  # Returns the current time
        total_secs = 0  # Set count to zero
        while len(self.moves) != 0:  # While the cube is not yet solved,
            time.sleep(1)  # Add a second delay
            total_secs = round(time.time()-start)  # Calculate the current time difference since the timer began
        print("The solving process took", total_secs, "seconds")  # Outputs the total time taken
        print("The number of moves required to solve this cube was", len(moves_list))  # Outputs the number of moves used

    def move(self):  # Method to take a move and execute it
        if self.rotate[0] == None and len(self.moves) > 0:  # If the moves list is not empty yet,
            next_move = self.moves[0]  # Find the first move in the list
            if next_move == "F":  # Depending on the move, execute the corresponding rotation
                self.front_cw()
            elif next_move == "F'":
                self.front_acw()
            elif next_move == "B":
                self.back_cw()
            elif next_move == "B'":
                self.back_acw()
            elif next_move == "L":
                self.left_cw()
            elif next_move == "L'":
                self.left_acw()
            elif next_move == "R":
                self.right_cw()
            elif next_move == "R'":
                self.right_acw()
            elif next_move == "U":
                self.up_cw()
            elif next_move == "U'":
                self.up_acw()
            elif next_move == "D":
                self.down_cw()
            elif next_move == "D'":
                self.down_acw()
            elif next_move == "S":
                self.spin()
            self.moves.pop(0)

    def slow_speed(self):
        self.velocity = 50  # Half of regular speed
        print("Speed set to slow")  # Lets user know the speed is set to slow

    def medium_speed(self):
        self.velocity = 100  # Regular speed
        print("Speed set to medium")  # Lets user know the speed is set to medium

    def fast_speed(self):
        self.velocity = 200  # Double of regular speed
        print("Speed set to fast")  # Lets user know the speed is set to fast

    def quit_program(self):
        print("Program ended")  # Tells the user the program has ended
        sys.exit()  # Ends the program

    def control(self):
        button(bind=self.solve, text="Solve")  # Creates button to solve cube
        button(bind=self.slow_speed, text="Slow Speed")  # Creates button to set speed to slow
        button(bind=self.medium_speed, text="Medium Speed")  # Creates button to set speed to medium
        button(bind=self.fast_speed, text="Fast Speed")  # Creates button to set speed to fast
        button(bind=self.quit_program, text="Quit program")  # Creates button to exit program

    def update(self):
        rate(self.velocity)  # Updates cube depending on the speed
        self.animation()
        self.move()

    def start(self):
        self.reset_positions()
        self.control()  # Create buttons
        while self.running:  # While the program is running,
            self.update()  # Update the cube
