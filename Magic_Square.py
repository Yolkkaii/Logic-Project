from z3 import *
from turtle import *
#from ColabTurtlePlus.Turtle import *

#Function to find a solution for the magic square of n * n size
def find_magic_square(n):
    #Magic constant formula is n(n^2 + 1)/2
    M = n * (n**2 + 1) // 2

    #Create n×n grid of integer variables
    X = [[Int(f"x_{i}_{j}") for j in range(n)] for i in range(n)]

    s = Solver()

    #1. Each cell holds a number between 1 and n^2
    for i in range(n):
        for j in range(n):
            s.add(And(X[i][j] >= 1, X[i][j] <= n * n))

    #2. All numbers are distinct
    s.add(Distinct([X[i][j] for i in range(n) for j in range(n)]))

    #3. Each row sums to magic number M
    for i in range(n):
        s.add(Sum(X[i]) == M)

    #4. Each column sums to magic number M
    for j in range(n):
        s.add(Sum([X[i][j] for i in range(n)]) == M)

    # 5. Diagonals sum to magic number M
    s.add(Sum([X[i][i] for i in range(n)]) == M)
    s.add(Sum([X[i][n - 1 - i] for i in range(n)]) == M)

    # Solve it
    if s.check() == sat:
        m = s.model()
        grid = [[m[X[i][j]].as_long() for j in range(n)] for i in range(n)]

        print("Solution found!")
        return grid
    else:
        print("No solution found.\n")
        return None

#Function to draw magic square, if the magic square has a solution.
def draw_magic_square(n, sq):
    if sq is None:
        return
    
    M = n * (n**2 + 1) // 2

    speed(8)
    pu()

    goto(0, 30 * (n / 2) + 20)
    write(f"Sum for each row, column and diagonal = {M}", align="center", font=("Arial", 10, "normal"))

    start_x = -30 * (n / 2)
    start_y = 30 * (n / 2)

    for i, row in enumerate(sq):
        goto(start_x, start_y - (30 * i))
        for num in row:
            x, y = xcor(), ycor()
            pd()
            for _ in range(4):
                forward(30)
                right(90)
            pu()
            goto(x + 15, y - 15)
            write(num, align="center", font=("Arial", 10, "normal"))

            goto(x, y)
            forward(30)

    done()

#Get grid size input from the user
while True:
    try:
        n = int(input("Enter size of the grid (1 to 10): "))
        if 1 <= n <= 10:
            break
        print("Please enter a number between 1 and 10.")
    except ValueError:
        print("Invalid input, enter an integer between 1 and 10.")

grid = find_magic_square(n)
draw_magic_square(n, grid)
