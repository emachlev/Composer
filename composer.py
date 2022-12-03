import os.path
import pickle
import random
import music21

GENE_SIZE = 5

MELODY_SIZE = 8

CHROMOSOME_SIZE = GENE_SIZE * MELODY_SIZE

POPULATION_SIZE = 500

CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.001

GENES = {
    '00000': '3A',
    '00001': '3A#',
    '00010': '3B',
    '00011': '3C',
    '00100': '3C#',
    '00101': '3D',
    '00110': '3D#',
    '00111': '3E',
    '01000': '3F',
    '01001': '3F#',
    '01010': '3G',
    '01011': '3G#',
    '01100': '4A',
    '01101': '4A#',
    '01110': '4B',
    '01111': '4C',
    '10000': '4C#',
    '10001': '4D',
    '10010': '4D#',
    '10011': '4E',
    '10100': '4F',
    '10101': '4F#',
    '10110': '4G',
    '10111': '4G#',
    '11000': '5A',
    '11001': '5A#',
    '11010': '5B',
    '11011': '5C',
    '11100': '5C#',
    '11101': '5D',
    '11110': '5D#',
    '11111': '5E',
    # '100000': '5F',
    # '100001': '5F#',
    # '100010': '5G',
    # '100011': '5G#',
    # '100100': 'R',  # Rest
}

REPETITION_RATE = 0.4


def get_random_chromo():
    chromo = ""
    exp = get_melody_from_expression(decode_chromo(chromo))
    while not (exp and len(exp) > 3):
        chromo = ""
        prev = ""
        for _ in range(CHROMOSOME_SIZE):
            if prev and random.uniform(0, 1) <= REPETITION_RATE:
                char = prev
            else:
                char = str(random.randint(0, 1))
            chromo += char
            prev = char
        exp = get_melody_from_expression(decode_chromo(chromo))
    return chromo


def validate_expression(exp):
    while exp and exp[0] == 'R':
        del exp[0]
    while exp and exp[-1] == 'R':
        del exp[-1]
    return exp


def decode_chromo(chromo):
    ret = []
    if len(chromo) % GENE_SIZE != 0:
        return False
    for chunk in [str(chromo[i:i + GENE_SIZE]) for i in range(0, len(chromo), GENE_SIZE)]:
        if chunk in GENES:
            ret.append(GENES[chunk])
    return validate_expression(ret) if ret else False


def get_melody_from_expression(exp):
    # Create an empty music21 stream
    melody = music21.stream.Stream()
    if not exp:
        return melody

    # Iterate over the notes in the expression
    for note in exp:
        # If the note is a rest, append a rest to the stream
        if note == 'R':
            melody.append(music21.note.Rest())
        # Otherwise, append an audio note to the stream
        else:
            melody.append(music21.note.Note(note))

    return melody


def rate(population, fitnesses):
    for i in range(POPULATION_SIZE):
        melody = get_melody_from_expression(decode_chromo(population[i]))


def select_two(fitnesses):
    return random.choices(population=list(fitnesses.keys()), weights=fitnesses.values(), k=2)


def crossover(population, chosen):
    if random.uniform(0, 1) <= CROSSOVER_RATE:
        chromo_1 = population[chosen[0]]
        chromo_2 = population[chosen[1]]
        point = int(random.randint(0, CHROMOSOME_SIZE) / 2)
        from_1 = chromo_1[point:]
        from_2 = chromo_1[point:]
        population[chosen[0]] = chromo_1[:point] + from_2
        population[chosen[1]] = chromo_2[:point] + from_1


def mutate(population, chosen):
    chromo_1 = list(population[chosen[0]])
    chromo_2 = list(population[chosen[1]])
    for i, char in enumerate(chromo_1):
        if random.uniform(0, 1) <= MUTATION_RATE:
            chromo_1[i] = '1' if char == 0 else '0'
    for i, char in enumerate(chromo_2):
        if random.uniform(0, 1) <= MUTATION_RATE:
            chromo_2[i] = '1' if char == 0 else '0'
    population[chosen[0]] = ''.join(chromo_1)
    population[chosen[1]] = ''.join(chromo_2)


def main():
    population = []
    fitnesses = {}
    if os.path.isfile('population') and os.path.isfile('fitnesses') and False:
        with open('population', 'rb') as pop_file:
            population = pickle.load(pop_file)
        with open('fitnesses', 'rb') as fit_file:
            fitnesses = pickle.load(fit_file)
    else:
        population = [get_random_chromo() for _ in range(POPULATION_SIZE)]
    generation = 1
    while True:
        with open('population', 'wb') as pop_file:
            pickle.dump(population, pop_file)
        with open('fitnesses', 'wb') as fit_file:
            pickle.dump(fitnesses, fit_file)
        rate(population, fitnesses)
        max_key = max(fitnesses, key=fitnesses.get)
        print("Gen. {}: Best chromosome is {} with a fitness of {}".format(generation, population[max_key], fitnesses[max_key]))
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            selected = select_two(fitnesses)
            crossover(population, selected)
            mutate(population, selected)
            new_population.append(population[selected[0]])
            new_population.append(population[selected[1]])
        population = new_population
        generation += 1


if __name__ == '__main__':
    main()
