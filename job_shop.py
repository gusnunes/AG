import random
import copy

def read_file(file_name):
    f = open(file_name, "r")
    n_jobs, n_machines = [int(valor) for valor in f.readline().split()]

    operations = []

    for i in range(1, n_jobs+1):
        line = f.readline().split()

        for j in range(0, n_machines*2, 2):
            operations.append( (i, int(line[j]), int(line[j+1])) )

    f.close()
    return n_jobs, n_machines, operations

def evaluate_makespan(individual,n_jobs,n_machines):
    # each machine has a start and end time
    machine_time = [0 for _ in range(n_machines)]

    # more recent end time of the job
    job_time = [0 for _ in range(n_jobs)]

    for operation in individual:
        job,machine,time = operation

        max_time = max(machine_time[machine],job_time[job-1])

        machine_time[machine] = max_time + time
        job_time[job-1] = machine_time[machine]
    
    # job that has the max time to complete
    makespan = max(job_time)
    return makespan

def update_population(population,n_jobs,n_machines,n_individuals):
    idx_value = []
    
    for idx,individual in enumerate(population):
        makespan = evaluate_makespan(individual,n_jobs,n_machines)
        idx_value.append((idx,makespan))
      
    # take the n biggest makespan
    sorted_values = sorted(idx_value, key=lambda x: x[1])
    individuals_idx = sorted_values[-n_individuals:]

    # sort the idx of individuals
    individuals_idx = sorted(individuals_idx, key=lambda x: x[0])

    # remove the worsts individuals from population
    shift = 0
    for i,_ in individuals_idx:
        population.pop(i-shift)
        shift += 1

def best_individual(population,n_jobs,n_machines):
    min_makespan = float("inf")
    
    for idx,individual in enumerate(population):
        makespan = evaluate_makespan(individual,n_jobs,n_machines)
        
        if makespan < min_makespan:
            min_makespan = makespan
            idx_best = idx
    
    return idx_best,min_makespan

def tournament(population,tournament_size,n_jobs,n_machines):
    population_size = len(population) - 1
    min_makespan = float("inf")
    
    # individual has the min makespan
    for _ in range(tournament_size):
        idx_random = random.randint(0,population_size)
        makespan = evaluate_makespan(population[idx_random],n_jobs,n_machines)

        if makespan < min_makespan:
            min_makespan = makespan
            idx_winner = idx_random
    
    return idx_winner

def create_offspring(mask,parents):
    offspring = []

    for value in mask:
        while True:
            x = parents[value].pop(0)
            if x not in offspring:
                offspring.append(x)
                break
    
    return offspring

def crossover(parents):
    mask_size = len(parents[0])
    m1 = [random.randint(0,1) for _ in range(mask_size)]
    m2 = [1 if value == 0 else 0 for value in m1]

    # masks list
    m = [m1,m2]

    offsprings = []
    for idx in range(2):
        os = create_offspring(m[idx],copy.deepcopy(parents))
        offsprings.append(os)
    
    return offsprings

def mutation(population,idx_individual,pm):
    individual_size = len(population[idx_individual])
    
    # many times the individual is mutating
    mutation_times = round(pm * individual_size)

    for _ in range(mutation_times):
        operation = random.choice(population[idx_individual])
        job = operation[0]
        idx_operation = population[idx_individual].index(operation)
        
        # check the left border
        left_border = -1
        for op in range(idx_operation):
            if job == population[idx_individual][op][0]:
                left_border = op

        # check the right border
        for op in range(idx_operation+1, individual_size):
            if job == population[idx_individual][op][0]:
                right_border = op
                break
        else:
            right_border = individual_size

        new_index = random.randint(left_border+1, right_border-1)
        population[idx_individual].insert(new_index, population[idx_individual].pop(idx_operation))

def execute(population,n_jobs,n_machines):
    # probability crossover
    pc =  0.8
    population_size = len(population)
    proportion_population = round(pc * population_size)
    
    # select individuasl by tournament
    tournament_size = 5
    
    # probability mutation
    pm = 0.2

    parents = []
    for _ in range(proportion_population):
        
        # choose two parents by tournament
        for _ in range(2):
            idx_individual = tournament(population,tournament_size,n_jobs,n_machines)
            
            p = population[idx_individual]
            parents.append(copy.deepcopy(p))

            # remove parent from population
            # population.pop(idx_individual)
        
        # creates two offsprings by crossover 
        offsprings = crossover(parents)
        population.extend(offsprings)

        # mutation in the last two individuals
        for i in range(1,3):
            mutation(population,-i,pm)
    
    update_population(population,n_jobs,n_machines,proportion_population*2)
        
# represents a solution to the problem
def create_individual(n_jobs,n_machines,operations):
    sequences = []   # operations sequences of the jobs
    start = 0
    stop = n_machines
    
    for _ in range(n_jobs):
        sequences.append(operations[start:stop])
        
        start = stop
        stop += n_machines 

    individual = []
    for _ in range(n_jobs*n_machines):
        first_operations = [(sequence[0],idx) for idx,sequence in enumerate(sequences) if len(sequence)>0]
        operation = random.choice(first_operations)
        
        idx = operation[1]
        sequences[idx].remove(operation[0])
        
        individual.append(operation[0])
    
    return individual

def create_population(n_jobs,n_machines,operations,population_size):
    population = []
    for _ in range(population_size):
        individual = create_individual(n_jobs, n_machines, operations)
        population.append(individual)
    
    return population
      
def main():
    file = "ft06.txt"
    n_jobs, n_machines, operations = read_file(file)

    solutions = []
    for _ in range(10):

        population_size = 50
        population = create_population(n_jobs,n_machines,operations,population_size)

        generations = 100
        for _ in range(generations):
            execute(population,n_jobs,n_machines)
        
        idx,makespan = best_individual(population,n_jobs,n_machines)

        solutions.append(makespan)
    
    print(min(solutions))
    # print(population[idx])
    
main()