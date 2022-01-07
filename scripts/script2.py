from biosim.landscapes import Lowland
import matplotlib.pyplot as plt
import statistics

poph = [{'species': 'Herbivore',
            'age': 5,
            'weight': 20}
            for _ in range(50)]
lo = Lowland()
params_fodder = {"f_max": 800}
lo.set_params(params_fodder)
lo.herbs_population(poph)
testlist = []

for i in range(300):
    print(lo.count_herbs())
    lo.eating_process()
    lo.animal_gives_birth()
    lo.animal_dies()
    lo.animal_gets_older()

    amount = lo.count_herbs()
    testlist.append(amount)

print(testlist)
print(statistics.mean(testlist))

#plt.rcParams['figure.figsize'] = (12, 5)
#plt.plot([i for i in range(300)], amount)
#plt.legend()

#antall = lo.count_herbs()
#print(antall)
