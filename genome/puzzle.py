#python3

from itertools import permutations

INPUT = 25
class Face:
    def __init__(self, string):
        sides = string.replace('(','').replace(')','').split(',')
        self.top = sides[0]
        self.left = sides[1]
        self.bottom = sides[2]
        self.right = sides[3]

    def __str__(self):
        return '({0},{1},{2},{3})'.format(self.top,self.left,self.bottom,self.right)

class Board:
    def __init__(self, faces):
        self.faces = faces

    def build_board(self):
        topleft = None
        botleft = None
        topright = None
        botright = None
        top = []
        left = []
        bot = []
        right = []
        mid = []

        for face in self.faces:
            if face.top == 'black' and face.left == 'black':
                topleft = face
            elif face.bottom == 'black' and face.left == 'black':
                botleft = face
            elif face.bottom == 'black' and face.right == 'black':
               botright = face
            elif face.top == 'black' and face.right == 'black':
               topright = face
            elif face.top == 'black':
                top.append(face)
            elif face.left == 'black':
                left.append(face)
            elif face.bottom == 'black':
                bot.append(face)
            elif face.right == 'black':
                right.append(face)
            else:
                mid.append(face)

        for perm in permutations(top, 3):
            if (topleft.right == perm[0].left 
            and perm[0].right == perm[1].left
            and perm[1].right == perm[2].left
            and perm[2].right == topright.left):
                self.top_row = [topleft] + list(perm) + [topright]
                break

        for perm in permutations(left, 3):
            if (topleft.bottom == perm[0].top 
            and perm[0].bottom == perm[1].top
            and perm[1].bottom == perm[2].top
            and perm[2].bottom == botleft.top):
                self.left = [topleft] + list(perm) + [botleft]
                break

        for perm in permutations(bot, 3):
            if (botleft.right == perm[0].left 
            and perm[0].right == perm[1].left
            and perm[1].right == perm[2].left
            and perm[2].right == botright.left):
                self.bot_row = [botleft] + list(perm) + [botright]
                break

        for perm in permutations(right, 3):
            if (topright.bottom == perm[0].top 
            and perm[0].bottom == perm[1].top
            and perm[1].bottom == perm[2].top
            and perm[2].bottom == botright.top):
                self.right = [topright] + list(perm) + [botright]
                break

        for perm in permutations(mid, 9):
            if (perm[0].top == self.top_row[1].bottom
            and perm[0].left ==self.left[1].right 
            and perm[0].right == perm[1].left
            and perm[0].bottom == perm[3].top
            and perm[1].top == self.top_row[2].bottom
            and perm[1].bottom == perm[4].top
            and perm[1].right == perm[2].left
            and perm[2].top == self.top_row[3].bottom
            and perm[2].bottom == perm[5].top
            and perm[2].right == self.right[1].left
            and perm[3].left == self.left[2].right
            and perm[3].bottom == perm[6].top
            and perm[3].right == perm[4].left
            and perm[4].bottom == perm[7].top
            and perm[4].right == perm[5].left
            and perm[5].bottom == perm[8].top
            and perm[5].right == self.right[2].left
            and perm[6].left == self.left[3].right
            and perm[6].bottom == self.bot_row[1].top
            and perm[6].right == perm[7].left
            and perm[7].bottom == self.bot_row[2].top
            and perm[7].right == perm[8].left
            and perm[8].bottom == self.bot_row[3].top
            and perm[8].right == self.right[3].left

            ):
                self.umid_row = [self.left[1]] + list(perm[:3]) + [self.right[1]]
                self.mid_row = [self.left[2]] + list(perm[3:6]) + [self.right[2]]
                self.lmid_row = [self.left[3]] + list(perm[6:]) + [self.right[3]]
                # print('YES')

    def print_rows(self):
        print(';'.join(list(map(lambda x: x.__str__(), self.top_row))))
        print(';'.join(list(map(lambda x: x.__str__(), self.umid_row))))
        print(';'.join(list(map(lambda x: x.__str__(), self.mid_row))))
        print(';'.join(list(map(lambda x: x.__str__(), self.lmid_row))))
        print(';'.join(list(map(lambda x: x.__str__(), self.bot_row))))




# inface = "(black,black,blue,cyan);(black,cyan,yellow,brown);(black,brown,maroon,red);(black,red,white,red);(black,red,green,black);\
#     (blue,black,orange,yellow);(yellow,yellow,yellow,orange);(maroon,orange,brown,orange);(white,orange,maroon,blue);(green,blue,blue,black);\
#     (orange,black,maroon,cyan);(yellow,cyan,orange,maroon);(brown,maroon,orange,yellow);(maroon,yellow,white,cyan);(blue,cyan,white,black);\
#     (maroon,black,yellow,purple);(orange,purple,purple,purple);(orange,purple,maroon,cyan);(white,cyan,red,orange);(white,orange,orange,black);\
#     (yellow,black,black,brown);(purple,brown,black,blue);(maroon,blue,black,orange);(red,orange,black,orange);(orange,orange,black,black)".split(';')
faces = [] 
# for i in range(INPUT):
#      faces.append(Face(inface[i].strip()))
for _ in range(INPUT):
    faces.append(Face(input().strip()))

b = Board(faces)
b.build_board()
b.print_rows()
# for face in faces:
#     print(face)
# (yellow,black,black,blue)
# (blue,blue,black,yellow)
# (orange,yellow,black,black)
# (red,black,yellow,green)
# (orange,green,blue,blue)
# (green,blue,orange,black)
# (black,black,red,red)
# (black,red,orange,purple)
# (black,purple,green,black)
