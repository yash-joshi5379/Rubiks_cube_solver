import copy


class Face:  # Creating an object for the cube face
    def __init__(self, colour):  # Instantiating the class with the colour attribute
        self._t_row = [colour, colour, colour]  # Top row of face
        self._m_row = [colour, colour, colour]  # Middle row of face
        self._b_row = [colour, colour, colour]  # Bottom row of face
        self.rows = [  # Setting the structure of a cube face
            self._t_row,  # [top left, top edge, top right]
            self._m_row,  # [left edge, centre, right edge]
            self._b_row  # [bottom left, bottom edge, bottom right]
        ]

    @property
    def top_row(self):  # If the top row function is called,
        return self._t_row  # output the top row

    @top_row.setter
    def top_row(self, row):  # If user enters a row of facelets,
        for idx in range(3):  # For each facelet in the top row,
            self._t_row[idx] = row[idx]  # Set the user's input to the object

    @property
    def middle_row(self):
        return self._m_row

    @middle_row.setter
    def middle_row(self, row):
        for idx in range(3):
            self._m_row[idx] = row[idx]

    @property
    def bottom_row(self):
        return self._b_row

    @bottom_row.setter
    def bottom_row(self, row):
        for idx in range(3):
            self._b_row[idx] = row[idx]

    @property
    def left_col(self):  # If the left column function is called,
        return [self._t_row[0], self._m_row[0], self._b_row[0]]  # Output the left column

    @left_col.setter
    def left_col(self, row):  # If the user enters a row of facelets
        self._t_row[0] = row[0]  # User's facelet --> Top left
        self._m_row[0] = row[1]  # User's facelet --> Middle left
        self._b_row[0] = row[2]  # User's facelet --> Bottom left

    @property
    def right_col(self):
        return [self._t_row[2], self._m_row[2], self._b_row[2]]

    @right_col.setter
    def right_col(self, row):
        self._t_row[2] = row[0]
        self._m_row[2] = row[1]
        self._b_row[2] = row[2]

    def __str__(self):
        full_face = ''  # Creates an empty string
        for row in self.rows:  # For each row in a face,
            full_face += f"{row}\n"  # Add the row to the face
        return full_face  # Outputs full face

    def rotate_clockwise(self):
        old_face = copy.deepcopy(self.rows)  # Creates a copy of the original face
        for n_row in range(3):  # For each new row,
            for n_col in range(3):  # For each new column,
                self.rows[n_row][n_col] = old_face[2 - n_col][n_row]  # Move the old facelet to the new position

    def rotate_anti_clockwise(self):
        old_face = copy.deepcopy(self.rows)  # Creates a copy of the original face
        for n_row in range(3):  # For each new row,
            for n_col in range(3):  # For each new column,
                self.rows[n_row][n_col] = old_face[n_col][2 - n_row]  # Move the old facelet to the new position


# f = Face("W")  # Creating a white face
# print(f)  # Should output white face
# f.top_row = ["A", "B", "C"]  # Set top row
# f.middle_row = ["D", "E", "F"]  # Set middle row
# f.bottom_row = ["G", "H", "I"]  # Set bottom row
# print(f)  # Should output new face
# f.rotate_clockwise()  # Execute cw rotation
# print(f)  # Output face after cw rotation
# f.rotate_anti_clockwise()  # Execute acw rotation
# print(f)  # Should output face as it was before
#
# exit()  # Break point for troubleshooting


class Cube:
    """
    Layout
                    Face3
                      |
            Face1 - Face0 - Face2 - Face5
                      |
                    Face4

                       TT TT TT
                       MT MT MT
                       BT BT BT
                          |
            TL TL TL   TF TF TF   TR TR TR   TK TK TK
            ML ML ML - MF MF MF - MR MR MR - MK MK MK
            BL BL BL   BF BF BF   BR BR BR   BK BK BK
                          |
                       TB TB TB
                       MB MB MB
                       BB BB BB

        Face 0 is at the front
        Face 1 is on the left
        Face 2 is on the right
        Face 3 is on the top
        Face 4 is on the bottom
        Face 5 is at the back
    """
    face_name = ['front', 'left', 'right', 'top', 'bottom', 'back']

    def __init__(self):
        self.face_front = Face('F')
        self.face_left = Face('L')
        self.face_right = Face('R')
        self.face_top = Face('T')
        self.face_bottom = Face('B')
        self.face_back = Face('K')
        self.faces = [self.face_front, self.face_left, self.face_right, self.face_top, self.face_bottom, self.face_back]

    def __str__(self):
        left_padding = ' ' * 20  # Moves the top and bottom faces to in line with the front face
        face_top_str = left_padding + str(self.face_top).replace('\n', '\n' + left_padding).rstrip()  # Casts the top face as a string
        full_net = face_top_str + ('\n' * 2)  # Adds the top face and a break line to the main string
        for row in range(3):  # For each row,
            for face in [self.face_left, self.face_front, self.face_right, self.face_back]:  # In each face,
                if row == 0:  # If top row
                    full_net += str(face.top_row)  # Then add the face's top row
                elif row == 1:  # If middle row
                    full_net += str(face.middle_row)  # Then add the face's middle row
                elif row == 2:  # If bottom row
                    full_net += str(face.bottom_row)  # Then add the face's bottom row
                full_net += ' ' * 5
            full_net += '\n'  # Add a new line at the end of each row
        full_net += '\n'  # Add a new line after the middle section
        face_bottom_str = left_padding + str(self.face_bottom).replace('\n', '\n' + left_padding).rstrip()  # Casts the bottom face as a string
        full_net += face_bottom_str  # Adds the bottom face to the main string
        return full_net  # Outputs the 2D net

    def rotate_top_clockwise(self):  # U
        self.face_top.rotate_clockwise()  # Call the clockwise rotation function
        save = self.face_front.top_row.copy()  # Creates a copy of the original Front top row
        self.face_front.top_row = self.face_right.top_row  # Right top row --> Front top row
        self.face_right.top_row = self.face_back.top_row  # Back top row --> Right top row
        self.face_back.top_row = self.face_left.top_row  # Left top row --> Back top row
        self.face_left.top_row = save  # Original Front top row --> Left top row

    def rotate_top_anti_clockwise(self):  # U'
        self.face_top.rotate_anti_clockwise()  # Call the anticlockwise rotation function
        save = self.face_front.top_row.copy()  # Creates a copy of the original Front top row
        self.face_front.top_row = self.face_left.top_row  # Left top row --> Front top row
        self.face_left.top_row = self.face_back.top_row  # Back top row --> Left top row
        self.face_back.top_row = self.face_right.top_row  # Right top row --> Back top row
        self.face_right.top_row = self.face_front.top_row  # Front top row --> Right top row
        self.face_right.top_row = save  # Original Front Top row --> Right top row

    def rotate_bottom_clockwise(self):  # D
        self.face_bottom.rotate_clockwise()
        save = self.face_front.bottom_row.copy()
        self.face_front.bottom_row = self.face_left.bottom_row
        self.face_left.bottom_row = self.face_back.bottom_row
        self.face_back.bottom_row = self.face_right.bottom_row
        self.face_right.bottom_row = save

    def rotate_bottom_anti_clockwise(self):  # D'
        self.face_bottom.rotate_anti_clockwise()
        save = self.face_front.bottom_row.copy()
        self.face_front.bottom_row = self.face_right.bottom_row
        self.face_right.bottom_row = self.face_back.bottom_row
        self.face_back.bottom_row = self.face_left.bottom_row
        self.face_left.bottom_row = save

    def rotate_front_clockwise(self):  # F
        self.face_front.rotate_clockwise()
        save = self.face_bottom.top_row.copy()
        self.face_bottom.top_row = self.face_right.left_col[::-1]
        self.face_right.left_col = self.face_top.bottom_row
        self.face_top.bottom_row = self.face_left.right_col[::-1]
        self.face_left.right_col = save

    def rotate_front_anti_clockwise(self):  # F'
        self.face_front.rotate_anti_clockwise()
        save = self.face_bottom.top_row.copy()
        self.face_bottom.top_row = self.face_left.right_col
        self.face_left.right_col = self.face_top.bottom_row[::-1]
        self.face_top.bottom_row = self.face_right.left_col
        self.face_right.left_col = save[::-1]

    def rotate_back_clockwise(self):  # B
        self.face_back.rotate_clockwise()
        save = self.face_bottom.bottom_row.copy()
        self.face_bottom.bottom_row = self.face_left.left_col
        self.face_left.left_col = self.face_top.top_row[::-1]
        self.face_top.top_row = self.face_right.right_col
        self.face_right.right_col = save[::-1]

    def rotate_back_anti_clockwise(self):  # B'
        self.face_back.rotate_anti_clockwise()
        save = self.face_bottom.bottom_row.copy()
        self.face_bottom.bottom_row = self.face_right.right_col[::-1]
        self.face_right.right_col = self.face_top.top_row
        self.face_top.top_row = self.face_left.left_col[::-1]
        self.face_left.left_col = save

    def rotate_left_clockwise(self):  # L
        self.face_left.rotate_clockwise()
        save = self.face_bottom.left_col.copy()
        self.face_bottom.left_col = self.face_front.left_col
        self.face_front.left_col = self.face_top.left_col
        self.face_top.left_col = self.face_back.right_col[::-1]
        self.face_back.right_col = save[::-1]

    def rotate_left_anti_clockwise(self):  # L'
        self.face_left.rotate_anti_clockwise()
        save = self.face_bottom.left_col.copy()
        self.face_bottom.left_col = self.face_back.right_col[::-1]
        self.face_back.right_col = self.face_top.left_col[::-1]
        self.face_top.left_col = self.face_front.left_col
        self.face_front.left_col = save

    def rotate_right_clockwise(self):  # R
        self.face_right.rotate_clockwise()
        save = self.face_bottom.right_col.copy()
        self.face_bottom.right_col = self.face_back.left_col[::-1]
        self.face_back.left_col = self.face_top.right_col[::-1]
        self.face_top.right_col = self.face_front.right_col
        self.face_front.right_col = save

    def rotate_right_anti_clockwise(self):  # R'
        self.face_right.rotate_anti_clockwise()
        save = self.face_bottom.right_col.copy()
        self.face_bottom.right_col = self.face_front.right_col
        self.face_front.right_col = self.face_top.right_col
        self.face_top.right_col = self.face_back.left_col[::-1]
        self.face_back.left_col = save[::-1]
