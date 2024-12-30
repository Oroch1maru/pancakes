import random
import heapq


class PancakesSolver:
    def __init__(self):
        self.count_of_pancakes = int(input("Write count of pancakes: "))
        self.start_pancakes = list(range(1, self.count_of_pancakes + 1))
        random.shuffle(self.start_pancakes)

        print(f"Starting state: {self.start_pancakes}")

        self.queue = []
        self.counter = 0
        self.explored = set()
        self.current_state = self.start_pancakes


    def is_goal(self):
        return self.current_state == sorted(self.current_state)

    def flips_pancake(self):
        successors = []
        for k in range(2, len(self.current_state) + 1):
            new_state = self.current_state[:k][::-1] + self.current_state[k:]
            successors.append((new_state, k))
        return successors

    def check_largest_pancake(self, state):
        result = 0
        for largest_pancake in range(self.count_of_pancakes, -1, -1):
            if state[largest_pancake-1] != largest_pancake:
                result = largest_pancake
                break
        return result

    def check_inversion(self,state):
        result = 0
        for i in range(0, self.count_of_pancakes - 1):
            for j in range(i+1, self.count_of_pancakes):
                if state[i] > state[j]:
                    result+=1
        return result

    def distance_to_sorted_state(self,state):
        total_distance = 0
        for i in range(self.count_of_pancakes):
            target_position = state[i] - 1
            total_distance += abs(i - target_position)
        return total_distance

    def check_pair(self,state):
        sum = 0
        for i in range(0, self.count_of_pancakes - 1):
            if state[i] - state[i + 1] != -1:
                sum += abs(state[i] - state[i + 1])
        return sum

    def reset(self):
        self.queue = []
        self.counter = 0
        self.explored = set()

    def search(self, algorithm, solution=0):
        if algorithm == 'ucs':
            heapq.heappush(self.queue, (0, self.counter, self.start_pancakes, []))
        elif algorithm == 'greedy':
            heapq.heappush(self.queue, (0, self.counter, 0,self.start_pancakes, []))
        elif algorithm == 'a_star':
            heapq.heappush(self.queue, (0,0,0,self.counter, self.start_pancakes, []))

        count_of_expanded = 0
        while self.queue:
            if algorithm == 'ucs':
                g, _, self.current_state, path = heapq.heappop(self.queue)
            elif algorithm == 'greedy':
                h, _, g, self.current_state, path = heapq.heappop(self.queue)
            else:
                f, _, g, h, self.current_state, path = heapq.heappop(self.queue)

            if tuple(self.current_state) in self.explored:
                continue
            self.explored.add(tuple(self.current_state))

            if self.is_goal():
                return (g if algorithm == 'ucs' or algorithm == 'greedy' else f), count_of_expanded, path + [self.current_state]

            for new_state, flip_cost in self.flips_pancake():
                if tuple(new_state) not in self.explored:
                    self.counter += 1
                    new_g = g + flip_cost
                    new_path = path + [self.current_state]

                    if solution == 0:
                        h = self.check_largest_pancake(new_state)
                    elif solution == 1:
                        h = self.check_inversion(new_state)
                    elif solution == 2:
                        h = self.check_pair(new_state)
                    else:
                        h = self.distance_to_sorted_state(new_state)

                    if algorithm == 'ucs':
                        heapq.heappush(self.queue, (new_g, self.counter, new_state, new_path))
                    elif algorithm == 'greedy':
                        heapq.heappush(self.queue, (h, self.counter, new_g, new_state, new_path))
                    elif algorithm == 'a_star':
                        f = new_g + h
                        heapq.heappush(self.queue, (f, self.counter, new_g, h, new_state, new_path))
            count_of_expanded += 1
        return None


solver = PancakesSolver()
print("\n==== Solution using UCS algorithm ====\n")
ucs_cost,ucs_count,ucs_path = solver.search("ucs")
if ucs_cost is not None:
    print(f"\nMinimum sorting cost: {ucs_cost}\nCount of extended nodes: {ucs_count}")
    for number in ucs_path:
        print(number)
else:
    print("Solution not found.")

solver.reset()
print("\n==== Solution using Greedy algorithm (The biggest pancake out of position) ====\n")
greedy_biggest_cost,greedy_biggest_count,greedy_biggest_path = solver.search("greedy",0)
if greedy_biggest_cost is not None:
    print(f"\nMinimum sorting cost: {greedy_biggest_cost}\nCount of extended nodes: {greedy_biggest_count}")
    for number in greedy_biggest_path:
        print(number)
else:
    print("Solution not found.")
solver.reset()

print("\n==== Solution using Greedy algorithm (Inversion Count) ====\n")
greedy_inversion_cost,greedy_inversion_count,greedy_inversion_path = solver.search("greedy",1)
if greedy_inversion_cost is not None:
    print(f"\nMinimum sorting cost: {greedy_inversion_cost}\nCount of extended nodes: {greedy_inversion_count}")
    for number in greedy_inversion_path:
        print(number)
else:
    print("Solution not found.")


solver.reset()
print("\n==== Solution using Greedy algorithm (Sequence Gap Heuristic) ====\n")
greedy_gap_cost, greedy_gap_count, greedy_gap_path = solver.search("greedy",2)
if greedy_gap_cost is not None:
    print(f"\nMinimum sorting cost: {greedy_gap_cost}\nCount of extended nodes: {greedy_gap_count}")
    for number in greedy_gap_path:
        print(number)
else:
    print("Solution not found.")


solver.reset()
print("\n==== Solution using Greedy algorithm (Distance to sorted state) ====\n")
greedy_manhattan_cost, greedy_manhattan_count, greedy_manhattan_path = solver.search("greedy",3)
if greedy_manhattan_cost is not None:
    print(f"\nMinimum sorting cost: {greedy_manhattan_cost}\nCount of extended nodes: {greedy_manhattan_count}")
    for number in greedy_manhattan_path:
        print(number)
else:
    print("Solution not found.")



solver.reset()
print("\n==== Solution using A* algorithm (The biggest pancake out of position) ====\n")
a_star_biggest_cost,a_star_biggest_count,a_star_biggest_path = solver.search("a_star",0)
if a_star_biggest_cost is not None:
    print(f"\nMinimum sorting cost: {a_star_biggest_cost}\nCount of extended nodes: {a_star_biggest_count}")
    for number in a_star_biggest_path:
        print(number)
else:
    print("Solution not found.")
solver.reset()

print("\n==== Solution using A* algorithm (Inversion Count) ====\n")
a_star_inversion_cost,a_star_inversion_count,a_star_inversion_path = solver.search("a_star",1)
if a_star_inversion_cost is not None:
    print(f"\nMinimum sorting cost: {a_star_inversion_cost}\nCount of extended nodes: {a_star_inversion_count}")
    for number in a_star_inversion_path:
        print(number)
else:
    print("Solution not found.")


solver.reset()
print("\n==== Solution using A* algorithm (Sequence Gap Heuristic) ====\n")
a_star_gap_cost, a_star_gap_count, a_star_gap_path = solver.search("a_star",2)
if a_star_gap_cost is not None:
    print(f"\nMinimum sorting cost: {a_star_gap_cost}\nCount of extended nodes: {a_star_gap_count}")
    for number in a_star_gap_path:
        print(number)
else:
    print("Solution not found.")

solver.reset()
print("\n==== Solution using A* algorithm (Distance to sorted state) ====\n")
a_star_manhattan_cost, a_star_manhattan_count, a_star_manhattan_path = solver.search("a_star",3)
if a_star_manhattan_cost is not None:
    print(f"\nMinimum sorting cost: {a_star_manhattan_cost}\nCount of extended nodes: {a_star_manhattan_count}")
    for number in a_star_manhattan_path:
        print(number)
else:
    print("Solution not found.")

results_ucs_a_star = {
    "UCS": {"cost": ucs_cost, "expanded_nodes": ucs_count},
    "A* (Biggest Pancake)": {"cost": a_star_biggest_cost, "expanded_nodes": a_star_biggest_count},
    "A* (Inversion Count)": {"cost": a_star_inversion_cost, "expanded_nodes": a_star_inversion_count},
    "A* (Sequence Gap)": {"cost": a_star_gap_cost, "expanded_nodes": a_star_gap_count},
    "A* (Distance to sorted state)": {"cost": a_star_manhattan_cost, "expanded_nodes": a_star_manhattan_count},
}

base_nodes = results_ucs_a_star["UCS"]["expanded_nodes"]
base_cost = results_ucs_a_star["UCS"]["cost"]

print("\nComparison of Algorithms UCS and A*:")
print(f"{'Algorithm':<30} {'Cost':<10} {'Expanded Nodes':<15} {'Improvement(%)':<25}")
print("-" * 85)
for algo, data in results_ucs_a_star.items():
    cost = data['cost']
    nodes = data['expanded_nodes']
    node_improvement = (1 - nodes / base_nodes) * 100 if nodes <= base_nodes else (nodes / base_nodes - 1) * -100
    print(f"{algo:<30} {cost:<10} {nodes:<15} {node_improvement:+.2f}%")

results_greedy_a_star = {
    "Biggest Pancake": {
        "Greedy": {"cost": greedy_biggest_cost, "expanded_nodes": greedy_biggest_count},
        "A*": {"cost": a_star_biggest_cost, "expanded_nodes": a_star_biggest_count},
    },
    "Inversion Count": {
        "Greedy": {"cost": greedy_inversion_cost, "expanded_nodes": greedy_inversion_count},
        "A*": {"cost": a_star_inversion_cost, "expanded_nodes": a_star_inversion_count},
    },
    "Sequence Gap": {
        "Greedy": {"cost": greedy_gap_cost, "expanded_nodes": greedy_gap_count},
        "A*": {"cost": a_star_gap_cost, "expanded_nodes": a_star_gap_count},
    },
    "Distance to sorted state": {
        "Greedy": {"cost": greedy_manhattan_cost, "expanded_nodes": greedy_manhattan_count},
        "A*": {"cost": a_star_manhattan_cost, "expanded_nodes": a_star_manhattan_count},
    },
}

print("\nComparison of Greedy and A* Algorithms for the Same Heuristic:\n")
print(f"{'Heuristic':<25} {'Algorithm':<10} {'Cost':<10} {'Expanded Nodes':<15}")
print("-" * 60)

for heuristic, data in results_greedy_a_star.items():
    greedy_data = data["Greedy"]
    astar_data = data["A*"]
    print(f"{heuristic:<25} {'Greedy':<10} {greedy_data['cost']:<10} {greedy_data['expanded_nodes']:<15}")
    print(f"{'':<25} {'A*':<10} {astar_data['cost']:<10} {astar_data['expanded_nodes']:<20}\n")
