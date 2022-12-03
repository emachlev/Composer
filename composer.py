import os.path
import pickle
import random
import music21

GENE_SIZE = 6

MELODY_SIZE = 8

CHROMOSOME_SIZE = GENE_SIZE * MELODY_SIZE

POPULATION_SIZE = 500

CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.001

GENES = {
    '000000': '3A',
    '000001': '3A#',
    '000010': '3B',
    '000011': '3C',
    '000100': '3C#',
    '000101': '3D',
    '000110': '3D#',
    '000111': '3E',
    '001000': '3F',
    '001001': '3F#',
    '001010': '3G',
    '001011': '3G#',
    '001100': '4A',
    '001101': '4A#',
    '001110': '4B',
    '001111': '4C',
    '010000': '4C#',
    '010001': '4D',
    '010010': '4D#',
    '010011': '4E',
    '010100': '4F',
    '010101': '4F#',
    '010110': '4G',
    '010111': '4G#',
    '011000': '5A',
    '011001': '5A#',
    '011010': '5B',
    '011011': '5C',
    '011100': '5C#',
    '011101': '5D',
    '011110': '5D#',
    '011111': '5E',
    '100000': 'R1',
    '100001': 'R2',
    '100010': 'R4',
    '100011': 'R8',
    '100100': 'R16',
    '100101': '5F',
    '100110': '5F#',
    '100111': '5G',
    '101000': '5G#',
    '101001': '5A#',
    '101010': '5B',
    '101011': '5C',
    '101100': '5C#',
    '101101': '5D',
    '101110': '5D#',
    '101111': '5E',
    '110000': '5F',
    '110001': '5F#',
    '110010': '5G',
    '110011': '5G#',
    '110100': '6A',
    '110101': '6A#',
    '110110': '6B',
    '110111': '6C',
    '111000': '6C#',
    '111001': '6D',
    '111010': '6D#',
    '111011': '6E',
    '111100': '6F',
    '111101': '6F#',
    '111110': '6G',
    '111111': '6G#',
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
    while exp and exp[0].startswith('R'):
        del exp[0]
    while exp and exp[-1].startswith('R'):
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
        if note == "R1":
            melody.append(music21.note.Rest(type="quarter"))  # These rests are way to long so we treat them as short ones
        elif note == "R2":
            melody.append(music21.note.Rest(type="eighth"))   # These rests are way to long so we treat them as short ones
        elif note == "R4":
            melody.append(music21.note.Rest(type="quarter"))
        elif note == "R8":
            melody.append(music21.note.Rest(type="eighth"))
        elif note == "R16":
            melody.append(music21.note.Rest(type="16th"))
        # Otherwise, append an audio note to the stream
        else:
            melody.append(music21.note.Note(note))

    return melody


def rate(population, fitnesses):
    for i in range(POPULATION_SIZE):
        melody = get_melody_from_expression(decode_chromo(population[i]))
        # Use the music21 library to analyze the melody's key and mode
        analysis = melody.analyze('key')

        # Compute the melody's score based on its rhythm, harmony, and other factors
        score = 0

        # Rhythm
        score += melody.duration.quarterLength / 32  # Bonus points for longer melodies
        num_rests = 0  # Count the number of rest notes in the melody
        for note in melody.getElementsByClass(music21.note.Note):
            if note.isRest:
                num_rests += 1  # Increment the rest count
            else:
                if note.duration.type in ['16th', '32nd', '64th']:
                    score += 0.05  # Bonus points for using fast notes
                if note.tie:
                    score += 0.1  # Bonus points for using ties
        for chord in melody.getElementsByClass(music21.chord.Chord):
            if len(chord.pitches) > 3:
                score += 0.1  # Bonus points for using complex chords
        if num_rests > 0:
            score += 0.1  # Bonus points for using rest notes
        if num_rests / len(melody.notes) > 0.5:
            score -= 0.1  # Penalty for using too many rest notes

        # Harmony
        for chord in melody.getElementsByClass(music21.chord.Chord):
            if chord.isConsonant():
                score += 0.1  # Bonus points for using consonant chords
            if chord.isMajorTriad():
                score += 0.05  # Bonus points for using major chords
        for i in range(1, len(melody.getElementsByClass(music21.chord.Chord))):
            if melody.getElementsByClass(music21.chord.Chord)[i].semitonesFromChord(
                    melody.getElementsByClass(music21.chord.Chord)[i - 1]
            ) in [2, 4, 7]:
                score += 0.1  # Bonus points for using common chord progressions

        # Motifs and patterns
        transposed = melody.transpose('p5')  # Transpose the melody up a perfect fifth
        if transposed.analyze('key').tonic.name == analysis.tonic.name:
            score += 0.2  # Bonus points for using a repeating pattern

        fitnesses[i] = score


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
    if os.path.isfile('population') and os.path.isfile('fitnesses'):
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
        min_key = min(fitnesses, key=fitnesses.get)
        max_key = max(fitnesses, key=fitnesses.get)
        print("Gen. {}: Best chromosome is {} ({}) with a fitness of {}".format(generation, population[max_key], decode_chromo(population[max_key]),
                                                                           fitnesses[max_key]))
        print("Gen. {}: Worst chromosome is {} ({}) with a fitness of {}".format(generation, population[min_key], decode_chromo(population[min_key]),
                                                                            fitnesses[min_key]))
        get_melody_from_expression(decode_chromo(population[max_key])).show("midi")
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
