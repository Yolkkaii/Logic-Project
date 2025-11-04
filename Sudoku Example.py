# Check reminders for details on this project
your_student_id = 68011278  # Replace this number by your student ID no.

# DO NOT CHANGE THE CODE BELOW
# x = (your_student_id % 6) + 1
# y = (3*your_student_id % 5) + 1
# if x==y:
#   y = 6

# print("You can choose to solve either Problem", x, "or Problem", y, "only.")

# -- Result: Only Problem 1 or Problem 5 can be chosen.

# Problem 1: N Queens
# Problem 5: Magic Square

#Given SAT Solver Code
### An implementation of a simplified DPLL algorithm

## Some helper functions
# Get the complement of literal 'lit'
def comp(lit):
  if lit[0]!='~':
    return '~' + lit
  else:
    return lit[1:]

# Check whether 'clause' contains complementary literals or Top
def tautology(clause):
    for lit in clause:
        if comp(lit) in clause:
            return True
    return False

# Resolve each clause in cnf with lit
def resolve(cnf, lit):
  # Remove every clause containing lit
  new_cnf = [c for c in cnf if lit not in c]
  # Remove the complement of lit from each clause
  comp_lit = comp(lit)
  new_cnf = [[l for l in c if l != comp_lit] for c in new_cnf]
  return new_cnf

## Check whether cnf is satisfiability using DPLL
def sat(cnf):
  # Remove tautologies
  cnf = [c for c in cnf if not tautology(c)]
  result = dpll(cnf)
  return result

# Apply the simplified DPLL algorithm
def dpll(cnf):
    # Empty set of clauses is obviously satisfiable.
    if len(cnf) == 0:
        return {}

    # If cnf contains an empty clause, it is unsatisfiable.
    if [] in cnf:
        return None

    # Find a unit clause in the clause set
    uc = next((c for c in cnf if len(c)==1), None)
    if uc is not None:
      # In case there is a unit clause:
      # Perform unit propagation
      lit = uc[0]
      cnf_lit = resolve(cnf, lit)
      result = dpll(cnf_lit)
    else:
      # In case there is no unit clause:
      # Select the first literal in the first clause
      lit = cnf[0][0]
      # Try resolving with lit
      cnf_lit = resolve(cnf, lit)
      result = dpll(cnf_lit)
      if result is None:
          # Try resolving with the complement of lit
          lit = comp(lit)
          cnf_lit = resolve(cnf, lit)
          result = dpll(cnf_lit)

    # Update the truth assignment and return
    if result is None:
      return None
    else:
      if lit[0]=='~':
        result[comp(lit)] = False
      else:
        result[lit] = True
      return result


#Sudoku Solver - Example

from turtle import *

#  -----------
# |11|12|13|14|
#  -----------
# |21|22|23|24|
#  -----------
# |31|32|33|34|
#  -----------
# |41|42|43|44|
#  -----------
# Propositional atom pijk means cell (i,j) contains k.
# Helper functions for creating literals
def p(i,j,k):
    return 'p'+str(i)+str(j)+str(k)
def np(i,j,k):
    return '~p'+str(i)+str(j)+str(k)

# S will be used to store the list of the clauses to be constructed
S = []

# Generate clauses for each condition of 2x2 sudoku game
# 1. Each cell contains a single number, 1-4.
for i in range(1,5):
    for j in range(1,5):
        # Cell (i,j) contains at least one of the numbers 1-4
        S.append([p(i,j,k) for k in range(1,5)])
        # Cell (i,j) may not contain two numbers
        for c in range(1,4):
            for d in range(c+1,5):
                S.append([np(i,j,c),np(i,j,d)])

# 2. Each row contains all numbers 1-4.
for i in range(1,5):
    for k in range(1,5):
        # Row i must contain number k
        S.append([p(i,j,k) for j in range(1,5)])

# 3. Each column contains all numbers 1-4.
for j in range(1,5):
    for k in range(1,5):
        # Column j must contain number k
        S.append([p(i,j,k) for i in range(1,5)])

# 4. Each block contains all numbers 1-4.
for b in range(0,4):
    for k in range(1,5):
        # Block b must contain number k
        S.append([p(2*(b//2)+c//2+1, 2*(b%2)+c%2+1,k) for c in range(0,4)])

# 5. Initial numbers
S.append([p(1,2,4)])
S.append([p(2,4,3)])
S.append([p(4,1,2)])
S.append([p(4,3,1)])

# Check for satisfiability
result = sat(S)

if result is None:
    print('No solution')
else:
    # Draw sudoku board with the solution
    speed(13)
    for i in range(1,5):
        for j in range(1,5):
            penup()
            goto((j-3)*100, (3-i)*100)
            setheading(0)
            pendown()
            # Draw cell (i,j)
            for d in range(4):
                forward(100)
                right(90)
            for k in range(1,5):
                if result[p(i,j,k)]:
                    penup()
                    goto((j-3)*100+50, (3-i)*100-50)
                    write(k, align='center')
                    break
    home()
    done()