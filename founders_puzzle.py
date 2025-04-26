from constraint import *

# Step 1: Create the problem object
problem = Problem()

# Step 2: Define founders and houses
founders = [
    "Deepmire", "Funflame", "Hypnotums", "Imaginez",
    "Miraculo", "Rimbleby", "Septimus", "Tremenda"
]

houses = ["Gianteye", "Meramaid", "Longmous", "Vidopnir"]

# Step 3: Assign each founder to one of the 4 houses
problem.addVariables(founders, houses)

# Step 4: Add the correct founder hat info
founder_info = {
    "Deepmire": {"color": "blue", "symbol": "stars"},
    "Funflame": {"color": "red", "symbol": "swirls"},
    "Hypnotums": {"color": "red", "symbol": "stars"},
    "Imaginez": {"color": "yellow", "symbol": "moons"},
    "Miraculo": {"color": "red", "symbol": "moons"},
    "Rimbleby": {"color": "blue", "symbol": "moons"},
    "Septimus": {"color": "yellow", "symbol": "stars"},
    "Tremenda": {"color": "blue", "symbol": "swirls"},
}

# Step 5: Constraint - no more than 2 founders per house
def max_two_per_house(*assignments):
    for house in houses:
        if list(assignments).count(house) > 2:
            return False
    return True

problem.addConstraint(max_two_per_house, founders)

# Step 6: Constraint - no same hat color or symbol in a house
def no_same_color_or_symbol(*assignments):
    assignments = dict(zip(founders, assignments))
    for house in houses:
        assigned = [f for f in assignments if assignments[f] == house]
        colors = [founder_info[f]["color"] for f in assigned]
        symbols = [founder_info[f]["symbol"] for f in assigned]
        if len(colors) != len(set(colors)):
            return False
        if len(symbols) != len(set(symbols)):
            return False
    return True

problem.addConstraint(no_same_color_or_symbol, founders)

# Step 7: Clue - Funflame and Imaginez founded Gianteye and Longmous
problem.addConstraint(
    lambda f, i: f in ["Gianteye", "Longmous"] and i in ["Gianteye", "Longmous"],
    ["Funflame", "Imaginez"]
)

# Step 8: Clue - Miraculo and Rimbleby founded Longmous and Meramaid
problem.addConstraint(
    lambda m, r: m in ["Longmous", "Meramaid"] and r in ["Longmous", "Meramaid"],
    ["Miraculo", "Rimbleby"]
)

# Step 9: Clue - Septimus did not found Vidopnir
problem.addConstraint(lambda s: s != "Vidopnir", ["Septimus"])

# Step 10: Solve and print results
solutions = problem.getSolutions()
print(f"Found {len(solutions)} solution(s):\n")

for solution in solutions:
    for founder in sorted(solution):
        print(f"{founder:10} => {solution[founder]}")
    print("-" * 30)
