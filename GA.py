import numpy as np
from numpy import pi
import csv
from numpy.random import randint
from numpy.random import rand
import matplotlib.pyplot as plt
import os

# define the total iterations
n_iter = 100

# define the population size
n_pop = 100

# crossover rate
r_cross = 0.9

#number of genes in chromosome
num_genes = 35

# mutation rate
r_mut = 10.0 / num_genes * n_pop

#defining checkpoints and constant robot distance
checkpoint1 = 0 + 100j
checkpoint2 = 100 + 100j

r_dist = 5

#variables for graphing
x_gene_coords = []
y_gene_coords = []


# Opening location file so we can write the checkpoints' locations to the file
file=open("location.txt", "w")

# objective function
# Return fitness based on how close the chromosome's path is to the hooking pattern
# Hooking pattern comes from trying to get to point B from point A, while also orienting towards point C
def objective(x):
    x_comp = 0
    y_comp = 0
    x_sublist = []
    y_sublist = []
    tht0 = 90   #initial orientation
    for gene in x:
        x_sublist.append(x_comp)
        y_sublist.append(y_comp)
        
        x_comp = x_comp + r_dist * np.cos(((gene*15)-(90-tht0))*pi/180) 
        y_comp = y_comp + r_dist * np.sin(((gene*15)-(90-tht0))*pi/180)

        tht0 = (gene*15)-(90-tht0)

        x_sublist.append(x_comp)
        y_sublist.append(y_comp)
        
        #Testing 
        #print()
        #print("x_comp: {}, y_comp: {}, x_sublist: {}, y_sublist: {}".format(x_comp, y_comp, x_sublist, y_sublist))

    x_gene_coords.append(x_sublist)
    y_gene_coords.append(y_sublist)
   
    chrom_coords = [complex(x_comp,y_comp)]
    print(chrom_coords)
    print(len(chrom_coords))

    dist2checkpoint = (np.sqrt((np.real(checkpoint1) 
                        - np.real(chrom_coords))**2 
                        + (np.imag(checkpoint1) 
                        - np.imag(chrom_coords))**2))
    
    dist2checkpoint2 = (np.sqrt((np.real(checkpoint2) 
                        - np.real(chrom_coords))**2 
                        + (np.imag(checkpoint2) 
                        - np.imag(chrom_coords))**2))
    
    distcheckpoint1to2 = (np.sqrt((np.real(checkpoint1) 
                        - np.real(checkpoint2))**2 
                        + (np.imag(checkpoint1) 
                        - np.imag(checkpoint2))**2))
    
    a = dist2checkpoint
    b = distcheckpoint1to2
    c = dist2checkpoint2
    
    angle2nextcheckpoint = np.arccos((a**2 + b**2 - c**2) / (2 * a * b))*(180/pi)
    
    idealangle = abs(90 - (tht0 + angle2nextcheckpoint))
        
    distval = dist2checkpoint/100
    angleval = idealangle / 360
    
    fitness = (distval + angleval) / 2
    
    return fitness

# tournament selection
def selection(pop, scores, k=3):
	# first random selection
	selection_ix = randint(len(pop))
	for ix in randint(0, len(pop), k-1):
		# check if better (e.g. perform a tournament)
		if scores[ix] < scores[selection_ix]:
			selection_ix = ix
	return pop[selection_ix]

# crossover two parents to create two children
def crossover(p1, p2, r_cross):
	# children are copies of parents by default
	c1, c2 = p1.copy(), p2.copy()
	# check for recombination
	if rand() < r_cross:
		# select crossover point that is not on the end of the string
		pt = randint(1, len(p1)-2)
		# perform crossover
		c1 = p1[:pt] + p2[pt:]
		c2 = p2[:pt] + p1[pt:]
	return [c1, c2]

# mutation operator
def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        #check for mutation
        if rand() < r_mut:
            #mutation is random number 0-12
            bitstring[i] = randint(0,13)
   
# genetic algorithm
def genetic_algorithm(objective, n_iter, n_pop, r_cross, r_mut):

	# Check if already have text file 
   #if not os.path.isfile("pop.csv"):
		# Create text file if it doesn't exist
	#	with open("pop.csv", w) as f:
		    # Write initial population of 100 random chromosomes 
		    
    
	# initial population of random genes
    with open('pop.csv') as f:
        reader = csv.reader(f)
        pop = [list(map(int, row)) for row in reader]
    
    
    with open('best.csv') as f:
        reader = csv.reader(f)
        best = list(map(int, f.readline().split(',')))
        best_eval = float(f.readline())
            
    # clear the array used for graphing of these initial coords
    x_gene_coords.clear()
    y_gene_coords.clear()
    
    # enumerate generations
    for gen in range(n_iter):
        
        # evaluate all candidates in the population
        scores = [objective(d) for d in pop]

		# check for new best solution
        for i in range(n_pop):
            #minimizes
            if scores[i] < best_eval:
                best, best_eval = pop[i], scores[i]
                
                #display graph of path robot took                
                
                #comment next line out to plot the progression of best chromosomes
                #or it leave in to plot only the best chromosome
                plt.clf()
             
                plt.title("Best Chromosome")
                plot_variable_x = x_gene_coords[gen*n_pop+i]
                plot_variable_y = y_gene_coords[gen*n_pop+i]
                plt.plot(plot_variable_x , plot_variable_y, linestyle = ':', color = "black")
                plot_variable_x = 0
                plot_variable_y = 0
                print(gen, pop[i], scores[i])
        
        #select parents
        selected = [selection(pop, scores) for _ in range(n_pop)]
		# create the next generation
        children = list()
        for i in range(0, n_pop, 2):
			# get selected parents in pairs
            p1, p2 = selected[i], selected[i+1]
			# crossover and mutation
            for c in crossover(p1, p2, r_cross):
				# mutation
                mutation(c, r_mut)
				# store for next generation
                children.append(c)
		# replace population
        pop = children
        
        #rewrite the csv file with the current generation
        with open('pop.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(pop)
    
    return [best, best_eval]

#Previously in 'waiting room'
pop = [randint(0,13,35).tolist() for _ in range(100)]
best = [0]*35

# write the data to a file
with open('pop.csv', 'w', newline='') as pop_file:
    writer = csv.writer(pop_file)
    writer.writerows(pop)
    
with open('best.csv', 'w', newline='') as best_file:
    writer = csv.writer(best_file)
    writer.writerow(best)
    writer.writerow([1])




# perform the genetic algorithm search
best, score = genetic_algorithm(objective, n_iter, n_pop, r_cross, r_mut)

# if there is no better chromsome the score must be converted to be rewritten
# into the csv file
if isinstance(score, float):
    score = [score]

with open('best.csv', 'w', newline='') as best_file:
    writer = csv.writer(best_file)
    writer.writerow(best)
    writer.writerow(score)
    #writer.writerow("")

print(best, '=', score[0])

plt.xlim(-60,110)
plt.ylim(-10,110)

#plt.xlim(0, 300)
#plt.ylim(0, 200)

#plt.plot(100,50, color = "red", marker = "*")
#plt.plot(100,150, color = "red", marker = "*")
#plt.plot(200,50, color = "red", marker = "*")
#plt.plot(200,150, color = "red", marker = "*")

plt.plot(0,0, color = "red", marker = "*")
plt.plot(0,100, color = "red", marker = "*")
plt.plot(100,100, color = "red", marker = "*")
plt.plot(100,0, color = "red", marker = "*")

# Writing coordinates of checkpoints to location text file
#file.write("(0, 0)")
#file.write(", ")
#file.write("(0, 100)")
#file.write(", ")
#file.write("(100, 100)")
#file.write(", ")
#file.write("(100, 0)\n")
#file.close()


plt.show()

