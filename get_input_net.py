import cv2  # Import openCV
import numpy as np  # Import numpy which is required for openCV


capture = cv2.VideoCapture(0)  # Assigns the variable "capture" to the camera and assigns port 0 to the camera
cv2.namedWindow("Live Video")  # Calls the video window "Live Video"

net = np.zeros((700, 900, 3), np.uint8)  # Creates a 3D array of zeros

# Initialising HSV limits for each colour
hsv_ranges = {
    "G": [(0, 55, 0), (50, 128, 61)],
    "O": [(0, 41, 170), (15, 110, 255)],
    "R": [(0, 10, 100), (78, 74, 256)],
    "Y": [(0, 115, 151), (15, 210, 255)],
    "W": [(135, 126, 113), (255, 234, 230)],
    "B": [(85, 20, 0), (210, 80, 37)],
}

# Rubix cube notation and colour for each face
face_colour_notation = {
    "front": ["F", "white"],
    "left": ["L", "orange"],
    "right": ["R", "red"],
    "back": ["B", "yellow"],
    "up": ["U", "blue"],
    "down": ["D", "green"]
}

rgb_colours = {
    "W" : (220,220,220),
    "O" : (0,130,255),
    "R" : (0,0,255),
    "Y" : (0,255,255),
    "B" : (255,0,0),
    "G" : (1,89,1)
}

state=  {
            'front':['W','W','W','W','W','W','W','W','W'],
            'left':['W','W','W','W','O','W','W','W','W'],
            'right':['W','W','W','W','R','W','W','W','W'],
            'back':['W','W','W','W','Y','W','W','W','W'],
            'up':['W','W','W','W','B','W','W','W','W'],
            'down':['W','W','W','W','G','W','W','W','W']
}

fixed_square_positions = {
    "coords": [
        [180, 100], [300, 100], [420, 100],
        [180, 220], [300, 220], [420, 220],
        [180, 340], [300, 340], [420, 340]
    ]
}

def get_masks(frame, hsv_ranges):  # Creating a function to make a masked image for all colours
    cv2.imwrite("picture.png", frame)  # Captures the current frame
    img = cv2.imread("picture.png")  # Current frame is loaded and stored in "img"
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Converts image from RBG to HSV colour space
    for item in hsv_ranges:  # Iterates through each colour
        image_name = item + ".png"  # Creates the name of the file for that colour
        mask = cv2.inRange(hsv_img, hsv_ranges[item][0], hsv_ranges[item][1]) > 0  # Mask is applied using HSV limits
        colour = np.zeros_like(img, np.uint8)  # Slicing the colour from all other colours
        colour[mask] = img[mask]  # Creating an image where only this colour is visible
        cv2.imwrite(image_name, colour)  # The masked colour image is saved


def draw_face_real(net, x, y, index, pos):
    font = cv2.FONT_HERSHEY_SIMPLEX  # Font of letters
    face = list(face_colour_notation.keys())[index]  # Method to retrieve the current face of the dictionary
    face_letter = str(face_colour_notation[face][0])  # Gets the notation letter of the current face
    face_name = list(state.keys())[index]  # Gets the name of the face
    #print(face_name)  # For troubleshooting
    count = 0  # Counter for the facelets
    y_pos = y  # Initialise the y coordinate as a local variable
    for i in range(3):  # For each row,
        x_pos = x  # Initialise the x coordinate as a local variable
        for j in range(3):  # For each column,
            if i == 1 and j == 1:  # If it is the centre facelet,
                value = list(rgb_colours.keys())[pos]  # Convert the colours dictionary to a list
                colour = rgb_colours[value]  # Get the colour of the current face
                cv2.rectangle(net, (x_pos, y_pos), (x_pos + 50, y_pos + 50), colour, -1)  # Draws a square in that colour
            else:  # For all other facelets,
                facelet_colour = state[face_name][count]  # Get the colour of the facelet
                #print(facelet_colour)  # For troubleshooting
                colour_code = rgb_colours[str(facelet_colour)]  # Gets the rgb value of the colour
                cv2.rectangle(net, (x_pos, y_pos), (x_pos + 50, y_pos + 50), colour_code,
                          -1)  # Draws a coloured square of size 50x50
            count +=1  # Increment counter
            x_pos += 60  # New x coordinate for each column
        y_pos += 60  # New y coordinate for each row
    cv2.putText(net, face_letter, (x + 75, y + 90), font, 1, (0, 0, 0),
                cv2.LINE_4)  # Writes the letter on the centre facelet


def draw_all_faces_real(net, x_coord, y_coord):  # Draws all faces of the cube
    draw_face_real(net, x_coord, y_coord, 0, 0)
    draw_face_real(net, x_coord-200, y_coord, 1, 1)
    draw_face_real(net, x_coord+200, y_coord, 2, 2)
    draw_face_real(net, x_coord+400, y_coord, 3, 3)
    draw_face_real(net, x_coord, y_coord-200, 4, 4)
    draw_face_real(net, x_coord, y_coord+200, 5, 5)


def draw_fixed_squares(frame, fixed_square_positions, name):
    for x, y in fixed_square_positions[name]:
        cv2.rectangle(frame, (x, y), (x + 40, y + 40), (255, 255, 255), 2)


def detect_colour_limits(frame, hsv_list, fixed_square_positions):  # Creating a function to detect a colour
    for i in range(9):  # For each of the fixed squares,
        hsv_list.append(frame[fixed_square_positions["coords"][i][1] + 10][fixed_square_positions["coords"][i][0] + 10])
        # Add the hsv value to the hsv list
    #print(hsv_list)  # Outputs the hsv list, for troubleshooting
    h_count, s_count, v_count = 0, 0, 0  # Set all totals to zero
    for k in range(9):  # For each fixed square,
        h_count += hsv_list[k][0]  # Increment the h, s and v totals
        s_count += hsv_list[k][1]
        v_count += hsv_list[k][2]
    h_avg = h_count // 9  # Calculate the average h, s and v values
    s_avg = s_count // 9
    v_avg = v_count // 9
    #print(h_avg, s_avg, v_avg)  # Prints average HSV value
    lower_lim = np.array([h_avg-15, s_avg-20, v_avg-20])  # Creates a lower limit
    upper_lim = np.array([h_avg+15, s_avg+20, v_avg+20])  # Creates an upper limit
    print(lower_lim, upper_lim)  # Outputs the limits


def get_face_colours(hsv_list, hsv_ranges, letter):
    face_colours = []  # Creates an empty list into which colours will be added
    for i in range(9):  # For each facelet,
        if i == 4:  # If centre facelet,
            letter = letter.upper()  # Convert letter to uppercase
            #print(letter)
            for i in range(6):  # For each face,
                face_name = list(face_colour_notation.keys())[i]  # Find the face name
                face_letter = face_colour_notation[face_name][0]  # Find the face letter
                if letter == face_letter:  # If the face name matches the letter,
                    face_colour_letter = state[face_name][4]  # Assign the corresponding colour to that face
                    face_colours.append(face_colour_letter)  # Add the colour to the list
            continue  # Move to the next facelet
        else:
            detected = False  # Sets a flag to false
            h, s, v = hsv_list[i][0], hsv_list[i][1], hsv_list[i][2]  # Finds the h, s and v values
            #print(h, s, v)  # For troubleshooting
            facelet_hsv = np.array([h, s, v])  # Creates an HSV array
            #print(facelet_hsv)  # Outputs the HSV list of the facelet
            for j in range(6):  # For each possible colour,
                colour_name = list(hsv_ranges.keys())[j]  # Converts the dictionary to a list
                #print(colour_name)  # For troubleshooting
                is_in_range = ((hsv_ranges[colour_name][0] <= facelet_hsv) & (facelet_hsv <= hsv_ranges[colour_name][1])).all()  # Checks if the hsv values lie between the range
                if is_in_range == True:  # If the correct colour is detected,
                    #print(colour_name)  # For troubleshooting
                    face_colours.append(colour_name)  # Add the detected colour to a list
                    detected = True  # Sets the flag to true
                    break
            if detected == False:
                print(i, facelet_hsv)
        #print(detected)  # Outputs whether the facelet's colour has been detected
    #print(face_colours)
    #print("\n")  # Adds a line break
    if len(face_colours) == 9:
        return face_colours  # Only return the colour list if all colours are detected
    else:
        return -1  # Else, do not return the colour list


while True:  # Infinite loop created to display video
    hsv_list = []
    current_state = []
    return_frame, frame = capture.read()  # Captures an image from the webcam

    draw_fixed_squares(frame, fixed_square_positions, "coords")
    draw_all_faces_real(net, 250, 250)

    for i in range(9):  # For each of the fixed squares,
        hsv_list.append(frame[fixed_square_positions["coords"][i][1] + 10][fixed_square_positions["coords"][i][0] + 10])
        # Add the hsv value to the hsv list

    cv2.imshow("2D net", net)  # Displays the square to the user
    cv2.imshow("Live Video", frame)  # Displays the image with contours to the user

    k = cv2.waitKey(1)  # Assigns k to a key press

    if k == ord("p"):  # If p is pressed,
        get_masks(frame, hsv_ranges)  # then create a masked image for each colour
        detect_colour_limits(frame, hsv_list, fixed_square_positions)

    elif k==ord("u") or k==ord("d") or k==ord("l") or k==ord("r") or k==ord("f") or k==ord("b"):  # If an input letter is pressed,
        face_colours = get_face_colours(hsv_list, hsv_ranges, chr(k))  # Get the colours of that face
        if face_colours == -1:
            print("All colours not detected \n")  # Do not alter the net if all colours are not detected
        else:
            if k == ord("u"):  # Alter the state dictionary row corresponding to the input letter
                state["up"] = face_colours
            elif k == ord("d"):
                state["down"] = face_colours
            elif k == ord("l"):
                state["left"] = face_colours
            elif k == ord("r"):
                state["right"] = face_colours
            elif k == ord("f"):
                state["front"] = face_colours
            elif k == ord("b"):
                state["back"] = face_colours

    elif k == ord("q"):  # Stop condition: if q is pressed,
        break  # then the loop ends

cv2.destroyAllWindows()  # Closes the video window
capture.release()  # Releases the webcam

start_state = state  # new variable for next part of code
