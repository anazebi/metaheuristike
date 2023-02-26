from copy import deepcopy
from functools import reduce

# tabu lista koja sadrzi "zabranjene korake" 
class TabuList(list):

    # tabu lista ce biti duljine 3
    def __init__(self, size = 3):           
        self.size = size
        super(TabuList, self).__init__()

    # dodavanje koraka u listu FIFO nacinom
    def append(self, element):
        if len(self) == self.size:          
            self.pop(0)
            return super(TabuList, self).append(element)
        return super(TabuList, self).append(element)

    # provjera sadrzi li tabu lista dani korak
    def __contains__(self, move):
        for i in range(len(self)):
            if move == self[i]:
                return True
        return False

def sort_steps(self, steps):
    return sorted(steps, key = lambda x: x.evaluate_step, reverse = True)

# klasa koja predstavlja TabuSearch algoritam
class TabuSearch(object): 

    def __init__(self, max_iteration = 2):
        
        self.iteration_counter = 0              # broj provedenih iteracija
        self.iteration_better = 0               # zadnja iteracija koja je poboljsala vrijednost ruksaka
        self.max_iteration = max_iteration      # maksimalan dozvoljeni broj uzastopnih iteracija bez poboljsanja vrijednosti ruksaka

    def __call__(self, neighborhood_function, knapsack):

        solutions = neighborhood_function(knapsack) 
        sorted_steps = self.sorted_steps(solutions)
        [sorted_steps.remove(tabu.reverse()) for tabu in knapsack.tabu_list if tabu.reverse() in sorted_steps]  
        
        best_solution = knapsack.value          # trenutna konfiguracija
        best_solution_steps = deepcopy(knapsack.steps)
        best_solution_items = deepcopy(knapsack.items_in)
        end = False

        while self.iteration_counter - self.iteration_better < self.max_iteration:   
            self.iteration_counter += 1

            if not len(sorted_steps) == 0:
                next_step = sorted_steps.pop(0)
                solution = knapsack.value + next_step.evaluate_step
                knapsack.execute_step(next_step)
                knapsack.tabu_list.append(next_step.reverse())          # u tabu listu dodajemo novi zabranjeni korak, koji bi ponistio upravo napravljeni korak (sprjecavamo vracanje u upravo odabrano stanje)
                
                if(solution > best_solution):
                    print ("Trenutna iteracija %d, trenutno rjesenje %d, bolje rjesenje pronadeno u iteraciji %d s vrijednosti %d" % (self.iteration_counter, solution, self.iteration_better, best_solution))
                    best_solution = solution
                    best_solution_steps = deepcopy(knapsack.steps)
                    best_solution_items = deepcopy(knapsack.items_in)
                    self.iteration_better = self.iteration_counter
            else:
                best_tabu = reduce(lambda x, y: x if x.evaluate_step > y.evaluate_step else y, knapsack.tabu_list) # najbolji zabranjeni korak
                if best_tabu.evaluate_step > 0:  # ako zabranjeni korak daje novo globalno optimalno rjesenje, dopustamo njegovo izvrsavanje
                    solution = knapsack.value + best_tabu.evaluate_step
                    if solution > best_solution:
                        print ("[TABU POTEZ] Trenutna iteracija %d, trenutno rjesenje %d, bolje rjesenje pronadeno u iteraciji %d s vrijednosti %d" % (self.iteration_counter, solution, self.iteration_better, best_solution))
                        best_solution = solution
                        best_solution_steps = deepcopy(knapsack.steps)
                        best_solution_items = deepcopy(knapsack.items_in)
                        self.iteration_better = self.iteration_counter
                    
                    knapsack.execute_step(best_tabu)
            
            next_solutions = neighborhood_function(knapsack) 
            sorted_steps = self.sort_steps(next_solutions)
            [sorted_steps.remove(tabu.reverse()) for tabu in knapsack.tabu_list if tabu.reverse() in sorted_steps] # micemo zabranjene poteze iz dostupnih poteza

        print ("Bolje rjesenje nadeno je u iteraciji %d s vrijednoscu %d" % (self.iteration_better, best_solution))

        knapsack.value = best_solution
        knapsack.items_in = best_solution_items
        knapsack.steps = best_solution_steps

        print ('Tabu search proveden je s maksimumom od %d iteracija i tabu listom duljine %d.' % (self.max_iteration, knapsack.tabu_list.size))
        if not end:
            print ('Tabu search je zaustavljen zbog dostizanja maksimalnog broja iteracija.')
        return False
