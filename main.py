import random

from realfunctions import ObjFunction, bin_to_vector

f = ObjFunction()
# Generation of first generation of 50 solutions with their quality value
def first_gen(function, length=50, population=50):
    solutions = dict()  # Solutions are stored with their quality value

    while len(solutions) < population:  # If a solution is repeated it is discarded
        s = ""
        for j in range(length):
            s += str(random.randint(0, 1))

        solutions[s] = None

    solutions = evaluate(solutions, function)
    return solutions, best_found(solutions)


# Evaluation with quality function
def evaluate(solutions, function):
    new = dict()
    for s in solutions.keys():
        if solutions[s] is None:  # Just evaluates the new ones
            value, new_s = function(s)
            new[new_s] = value
        else:
            new[s] = solutions[s]

    return new


# Move best 20% of the population into the next generation
def next_gen(solutions, perc=20):
    values = sorted(solutions.values(), reverse=True)  # List of values from the highest
    size = int(len(values) * perc / 100)  # Size of survivors set

    nextgen = dict()

    for val in values[0:size]:

        key = None
        for k, v in solutions.items():  # Take the first key that has this value
            if v == val:
                key = k
                break

        nextgen[key] = val  # Add key-value to the new set of solutions
        solutions.pop(key)  # Removes key-value from original

    return nextgen


# Roulette selection: selects 2 mutually different parents from the set of solutions
def roulette(solutions):
    pa1 = None
    pa2 = None
    total = sum(solutions.values())

    rnum = random.uniform(0, total)

    i = 0
    for k in solutions.keys():
        i += solutions[k]
        if i >= rnum:
            pa1 = k
            break

    while True:  # Avoid the problem of choosing the same parents

        rnum = random.uniform(0, total)

        i = 0
        for k in solutions.keys():
            i += solutions[k]
            if i >= rnum:
                pa2 = k
                break

        if pa1 != pa2:  # Check that the parents are different
            break

    return pa1, pa2


# One-point crossover of two parents -> two childrens
def crossover(pa1, pa2):
    point = random.randint(0, len(pa1))

    new1 = pa1[0:point] + pa2[point:len(pa2)]
    new2 = pa2[0:point] + pa1[point:len(pa1)]

    return new1, new2


# Mutate each bit of children vectors with a probability of 1%
def mutate(s, prob=1):
    new = ""

    for bit in s:
        if random.randint(0, 100) < prob:
            bit = str(1 - int(bit))  # Switch the bit

        new += bit

    return new


# Complete the generation with all the necessary children
def complete_generation(solutions, function, prob=1):
    # At the begining solutions have just 10 vectors
    new_set = solutions.copy()  # Original cannot be modified for roulette selection

    for i in range(20):
        while True:
            pa1, pa2 = roulette(solutions)
            ch1, ch2 = crossover(pa1, pa2)
            ch1 = mutate(ch1, prob)
            ch2 = mutate(ch2, prob)

            """# Adjust bit-strings before evaluation tu ensure validity
            ch1 = f.adjust_solution(ch1, function)
            ch2 = f.adjust_solution(ch2, function)"""

            # This 'if' makes the children to be generated again if they are repeated
            if ch1 not in new_set and ch2 not in new_set and ch1 != ch2:
                new_set[ch1] = None
                new_set[ch2] = None
                break

    new_set = evaluate(new_set, function)

    return new_set, best_found(new_set)


# Find the best-found solution
def best_found(solutions):
    val = sorted(solutions.values(), reverse=True)[0]  # Highest value

    key = None
    for k, v in solutions.items():  # Take the first key that has this value
        if v == val:
            key = k
            break

    return key, val


# Genetic Algorithm
def genetic_algorithm(function, optimal, generations=1000, length=50, population=50, probability=1):
    best_solutions = []
    solutions, best = first_gen(function, length, population)

    # Store the best solution from first generation
    key, value = best
    best_solutions.append(value)
    if value == optimal:  # If the best-found solution is optimal the execution ends
        return (key, value), best_solutions

    for i in range(generations):
        solutions = next_gen(solutions)
        solutions, best = complete_generation(solutions, function, probability)

        # Store the best solution from current generation
        key, value = best
        #print(bin_to_vector(key),value)
        best_solutions.append(value)
        if value >= optimal:  # If the best-found solution is optimal the execution ends
            return (key, value), best_solutions

    return best_found(solutions), best_solutions


if __name__ == '__main__':

    function = f.schwefel

    # length = 210 / 290 / 210
    best, history = genetic_algorithm(function, f.optimal_solution(function), 1000, 290, 20, 2)
    # History keeps the best solution from every generation
    print(best)
    cad, quality = best
    print(bin_to_vector(cad))
    print("Ejecuciones: ", len(history))
