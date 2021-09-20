import random

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
    machine_time = [[0,0] for _ in range(n_machines)]

    # more recent end time of the job
    end_time = [0 for _ in range(n_jobs)]

    for operation in individual:
        job,machine,time = operation

        max_time = max(machine_time[machine-1][1],end_time[job-1])

        machine_time[machine-1][0] = max_time
        machine_time[machine-1][1] = machine_time[machine-1][0] + time

        end_time[job-1] = machine_time[machine-1][1]

        # print(job, end_time[job-1])
    
    # job that has the max time to complete
    makespan = max(end_time)
    return makespan

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

def mutation(population):
    # select a individual
    # for now, to test, there is only a individual
    individual = population[0]

    individual_size = len(individual)

    operation = random.choice(individual)
    job = operation[0]
    idx = individual.index(operation)
    
    # check the left border
    left_border = -1
    for op in range(idx):
        if job == individual[op][0]:
            left_border = op

    # check the right border
    for op in range(idx+1, individual_size):
        if job == individual[op][0]:
            right_border = op
            break
    else:
        right_border = individual_size

    new_index = random.randint(left_border+1, right_border-1)
    individual.insert(new_index, individual.pop(idx))

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
    file = "exemplo.txt"
    n_jobs, n_machines, operations = read_file(file)

    population_size = 3
    population = create_population(n_jobs,n_machines,operations,population_size)

    """teste = [(2,1,43),(1,1,29),(1,2,78),(3,2,91),(2,3,90),(3,1,85),(2,2,28),(1,3,9),(3,3,74)]
    population = [teste]"""

    tournament_size = 2
    idx = tournament(population,tournament_size,n_jobs,n_machines)
    print("Idx do vencedor:",idx)
    
    """idx,makespan = best_individual(population,n_jobs,n_machines)
    print(makespan)
    print(population[idx])"""
    
main()