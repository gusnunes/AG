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

def evaluate_makespan(population):
    pass

# represents a solution to the problem
def create_chromosome(n_jobs, n_machines, operations):
    sequences = []   # operations sequences of the jobs
    start = 0
    stop = n_machines
    
    for _ in range(n_jobs):
        sequences.append(operations[start:stop])
        
        start = stop
        stop += n_machines 

    chromosome = []
    for _ in range(n_jobs*n_machines):
        first_operations = [(sequence[0],idx) for idx,sequence in enumerate(sequences) if len(sequence)>0]
        operation = random.choice(first_operations)
        
        idx = operation[1]
        sequences[idx].remove(operation[0])
        
        chromosome.append(operation[0])
    
    return chromosome
           
def main():
    file = "exemplo.txt"
    n_jobs, n_machines, operations = read_file(file)

    population_size = 1
    population = []
    for _ in range(population_size):
        population.append(create_chromosome(n_jobs, n_machines, operations))
    
    print(population)

main()