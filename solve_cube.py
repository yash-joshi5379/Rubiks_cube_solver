from get_input_net import start_state
from cube_object import Cube
import kociemba

# start_state = {'front': ['W', 'W', 'G', 'R', 'W', 'O', 'W', 'O', 'O'],  # Used for testing
#                'left': ['R', 'G', 'O', 'W', 'O', 'G', 'O', 'R', 'O'],
#                'right': ['Y', 'Y', 'G', 'Y', 'R', 'G', 'G', 'R', 'R'],
#                'back': ['R', 'W', 'B', 'O', 'Y', 'B', 'W', 'W', 'B'],
#                'up': ['Y', 'O', 'W', 'Y', 'B', 'B', 'B', 'G', 'R'],
#                'down': ['G', 'B', 'Y', 'B', 'G', 'Y', 'Y', 'R', 'B']
# }

colour_to_face = {  # Converts a colour to its correct face
            'W'  : 'F',
            'B'  : 'U',
            'Y'   : 'B',
            'R'    : 'R',
            'O' : 'L',
            'G' : 'D'
}

colour_count = {"W": 0, "B": 0, "Y": 0, "R": 0, "O": 0, "G": 0}  # Dictionary to count number of occurrences of each letter

for x in start_state:  # For each face in the start state,
    for colour in start_state[x]:  # For each colour on that face,
        colour_count[colour] += 1  # Increment that colour's count

print(colour_count)  # Count should be 9 for all colours if valid

valid_state = True  # Set a flag to true
for colour in colour_count:  # For each colour of the cube,
    if colour_count[colour] != 9:  # If the colour does not occur 9 times,
        valid_state = False  # Then set the flag to false
        break

#print(valid_state)  # Outputs if the cube state is valid or not

if valid_state == False:  # If invalid cube state,
    print("Invalid Cube State")  # Output message to user
    exit()  # End program

elif valid_state == True:  # If valid cube state,
    start_state_string = ""  # Create an empty string
    for x in ["up", "right", "front", "down", "left", "back"]:  # For each face of the cube,
        for j in start_state[x]:  # For each facelet on a face,
            start_state_string += colour_to_face[j]  # Add the face letter to the string

    if start_state_string == "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB":  # If the start string matches the solved state,
        print("Cube is already solved")  # Output message to user
        exit()  # End program
    else:  # If the cube is not solved,
        moves_to_solve = kociemba.solve(start_state_string)  # Generating the solving algorithm
        print(moves_to_solve)  # Prints the solving algorithm
        moves_list = moves_to_solve.split()  # Converts the output string to a list

        c = Cube()  # Creating a test Cube

        c.face_front.top_row = start_state["front"][0:3]  # Front = White
        c.face_front.middle_row = start_state["front"][3:6]
        c.face_front.bottom_row = start_state["front"][6:9]

        c.face_left.top_row = start_state["left"][0:3]  # Left = Orange
        c.face_left.middle_row = start_state["left"][3:6]
        c.face_left.bottom_row = start_state["left"][6:9]

        c.face_right.top_row = start_state["right"][0:3]  # Right = Red
        c.face_right.middle_row = start_state["right"][3:6]
        c.face_right.bottom_row = start_state["right"][6:9]

        c.face_top.top_row = start_state["up"][0:3]  # Top = Blue
        c.face_top.middle_row = start_state["up"][3:6]
        c.face_top.bottom_row = start_state["up"][6:9]

        c.face_bottom.top_row = start_state["down"][0:3]  # Bottom = Green
        c.face_bottom.middle_row = start_state["down"][3:6]
        c.face_bottom.bottom_row = start_state["down"][6:9]

        c.face_back.top_row = start_state["back"][0:3]  # Back = Yellow
        c.face_back.middle_row = start_state["back"][3:6]
        c.face_back.bottom_row = start_state["back"][6:9]

        #print("Start State:")
        #print(c)

        for next_move in moves_to_solve.split():
            # time.sleep(10)  # Wait 10 secs before outputting the next cube state
            #print("After", next_move, ": ")  # Describe the rotation
            if next_move == "U":  # Adapt the cube object corresponding to the rotation
                c.rotate_top_clockwise()
            elif next_move == "U'":
                c.rotate_top_anti_clockwise()
            elif next_move == "D":
                c.rotate_bottom_clockwise()
            elif next_move == "D'":
                c.rotate_bottom_anti_clockwise()
            elif next_move == "F":
                c.rotate_front_clockwise()
            elif next_move == "F'":
                c.rotate_front_anti_clockwise()
            elif next_move == "B":
                c.rotate_back_clockwise()
            elif next_move == "B'":
                c.rotate_back_anti_clockwise()
            elif next_move == "L":
                c.rotate_left_clockwise()
            elif next_move == "L'":
                c.rotate_left_anti_clockwise()
            elif next_move == "R":
                c.rotate_right_clockwise()
            elif next_move == "R'":
                c.rotate_right_anti_clockwise()
            elif next_move == "U2":
                c.rotate_top_clockwise()
                c.rotate_top_clockwise()
            elif next_move == "D2":
                c.rotate_bottom_clockwise()
                c.rotate_bottom_clockwise()
            elif next_move == "F2":
                c.rotate_front_clockwise()
                c.rotate_front_clockwise()
            elif next_move == "B2":
                c.rotate_back_clockwise()
                c.rotate_back_clockwise()
            elif next_move == "L2":
                c.rotate_left_clockwise()
                c.rotate_left_clockwise()
            elif next_move == "R2":
                c.rotate_right_clockwise()
                c.rotate_right_clockwise()
            #print(c)  # Output the cube after each rotation

        #print("Solved!")  # Confirms the solving process is complete









