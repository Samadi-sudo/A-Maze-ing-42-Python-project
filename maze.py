import random

height = 5
width = 5


# هدا هو الكلاس الخاص بال(union and find)
class DisjointSet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = self
        self.rank = 0
        self.walls = {"top": True, "bottom": True, "left": True, "right": True}

# هده الدالة تقوم بانشاء الخلايا او النقاط المكونة للشبكة 
def ft_cells(height, width):
    maze = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(DisjointSet(x, y))
        maze.append(row)
    return (maze)

#هده الدالة تقوم بربط كل خلية مع التي على يمينها او فوقها لانشاء جدران الشبكة  

def ft_walls(maze, width, height):
    walls = []
    for row in maze:
        for cell in row:
            x = cell.x
            y = cell.y
            if x+1 < width:
                walls.append((cell, maze[y][x+1]))
            if y+1 < height:
                walls.append((cell, maze[y+1][x]))
    return (walls)
# maze[y][x] y = row and x = column



# find


def ft_find(cell):
    if cell.parent != cell:
        cell.parent = ft_find(cell.parent)
    return (cell.parent)

# union


def ft_union(cell_a, cell_b):
    root_a = ft_find(cell_a)
    root_b = ft_find(cell_b)
    if root_a is root_b:
        return False

    if root_a.rank < root_b.rank:
        root_a.parent = root_b
    elif root_a.rank > root_b.rank:
        root_b.parent = root_a
    elif root_a.rank == root_b.rank:
        root_b.parent = root_a
        root_a.rank += 1
    return True

def remove_wall(cell_a, cell_b):
    dx = cell_b.x - cell_a.x
    dy = cell_b.y - cell_a.y

    if dx == 1:
        cell_b.walls["left"] = False
        cell_a.walls["right"] = False
    elif dx == -1:
        cell_b.walls["right"] = False
        cell_a.walls["left"] = False
    
    if dy == 1:
        cell_b.walls["top"] = False
        cell_a.walls["bottom"] = False
    elif dy == -1:
        cell_b.walls["bottom"] = False
        cell_a.walls["top"] = False


maze = ft_cells(height, width)
walls = ft_walls(maze, width, height)


random.shuffle(walls)

for cell_a, cell_b in walls:
    if ft_union(cell_a, cell_b) is True:
        remove_wall(cell_a, cell_b)




#########################################################################

def print_maze(maze):
    height = len(maze)
    width = len(maze[0])
    
    for y in range(height):
        # خطوط الجدران العلوية لكل خلية في الصف
        top_line = ""
        middle_line = ""
        bottom_line = ""
        
        for x in range(width):
            cell = maze[y][x]
            
            # السطر العلوي
            top_line += "+" + ("---" if cell.walls["top"] else "   ")
            # السطر الأوسط
            middle_line += ("|" if cell.walls["left"] else " ") + "   "
            # السطر السفلي
            bottom_line += "+" + ("---" if cell.walls["bottom"] else "   ")
        
        # بعد آخر خلية في الصف، نضيف + أو | للحدود اليمنى
        top_line += "+"
        middle_line += "|" if maze[y][-1].walls["right"] else " "
        bottom_line += "+"
        
        # طباعة الصف
        print(top_line)
        print(middle_line)
        print(bottom_line)
    
    # بعد آخر صف، تأكد من طباعة الخط السفلي الأخير
    final_bottom = ""
    for x in range(width):
        final_bottom += "+" + ("---" if maze[-1][x].walls["bottom"] else "   ")
    final_bottom += "+"
    print(final_bottom)
print_maze(maze)
# for i in walls:
#     print(f"({i[0].x},{i[0].y}),({i[1].x},{i[1].y})")
