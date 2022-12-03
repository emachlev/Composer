from abc import ABC, abstractmethod
from threading import Thread
from time import sleep

from playsound import playsound

FREQS = {
    '3A': 45,
    '3A#': 46,
    '3B': 47,
    '3C': 48,
    '3C#': 49,
    '3D': 50,
    '3D#': 51,
    '3E': 52,
    '3F': 53,
    '3F#': 54,
    '3G': 55,
    '3G#': 56,
    '4A': 57,
    '4A#': 58,
    '4B': 59,
    '4C': 60,
    '4C#': 61,
    '4D': 62,
    '4D#': 63,
    '4E': 64,
    '4F': 65,
    '4F#': 66,
    '4G': 67,
    '4G#': 68,
    '5A': 69,
    '5A#': 70,
    '5B': 71,
    '5C': 72,
    '5C#': 73,
    '5D': 74,
    '5D#': 75,
    '5E': 76,
    '5F': 77,
    '5F#': 78,
    '5G': 79,
    '5G#': 80,
}


class Note(ABC):
    @abstractmethod
    def play(self):
        pass


class AudioNote(Note):
    def __init__(self, name):
        self.name = name
        self.file = 'notes/{}.wav'.format(name)

    def play(self):
        playsound(self.file)

    def distance(self, note):
        if not isinstance(note, AudioNote):
            return False
        return FREQS[note.name] - FREQS[self.name]

    def __str__(self):
        return self.name


class ChordNote(Note):
    """
    A list of notes that are played asynchronously
    """

    def __init__(self, notes):
        self.notes = notes

    def play(self):
        threads = []
        for note in self.notes:
            thread = Thread(target=note.play)
            threads.append(thread)
            thread.start()
        for th in threads:
            th.join()

    def __str__(self):
        return str(self.notes)


class RestNote(Note):
    def __init__(self, time=0.1):
        self.time = time

    def play(self):
        sleep(self.time)

    def __str__(self):
        return "R"


class Melody(list):
    """
    A list of notes that are played in order
    """

    def play(self):
        for note in self:
            note.play()

    def distances(self):
        if len(self) < 2:
            return []
        ret = []
        for i in range(len(self) - 1):
            ret.append(self[i].distance(self[i + 1]))
        return ret

    def difference(self, melody):
        ret = 0
        for d1, d2 in zip(self.distances(), melody.distances()):
            ret += abs(int(d1)-int(d2))
        return ret

    def __str__(self):
        ret = ""
        for item in self:
            ret += str(item)
        return ret


class ParallelMelody(Melody):
    """
    A list of melodies that are played asynchronously
    """

    def play(self):
        threads = []
        for melody in self:
            thread = Thread(target=melody.play)
            threads.append(thread)
            thread.start()
        for th in threads:
            th.join()

    def __str__(self):
        ret = ""
        for melody in self:
            ret += str(melody)
        return ret


if __name__ == '__main__':
    # Play Shape of You
    m1 = Melody([
        AudioNote('5C#'),
        RestNote(),
        AudioNote('5E'),
        RestNote(),
        AudioNote('5C#'),
        AudioNote('5C#'),
        RestNote(),
        AudioNote('5E'),
        RestNote(),
        AudioNote('5C#'),
        AudioNote('5C#'),
        RestNote(),
        AudioNote('5E'),
        RestNote(),
        AudioNote('5C#'),
        AudioNote('5D#'),
        RestNote(),
        AudioNote('5C#'),
        RestNote(),
        AudioNote('4B'),
    ])

    m2 = Melody([
        AudioNote('4C#'),
        RestNote(),
        AudioNote('4C#'),
        RestNote(),
        AudioNote('4C#'),
        AudioNote('3F#'),
        RestNote(),
        AudioNote('3F#'),
        RestNote(),
        AudioNote('3F#'),
        AudioNote('3A'),
        RestNote(),
        AudioNote('3A'),
        RestNote(),
        AudioNote('3A'),
        AudioNote('3B'),
        RestNote(),
        AudioNote('3B'),
        RestNote(),
        AudioNote('3B'),
    ])

    mel = ParallelMelody([m1, m2])
    while True:
        mel.play()
