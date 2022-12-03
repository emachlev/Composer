from notes import AudioNote, Melody

SHAPE_OF_YOU = Melody([
    AudioNote('5C#'),
    AudioNote('5E'),
    AudioNote('5C#'),
    AudioNote('5C#'),
    AudioNote('5E'),
    AudioNote('5C#'),
    AudioNote('5C#'),
    AudioNote('5E'),
    AudioNote('5C#'),
    AudioNote('5D#'),
    AudioNote('5C#'),
    AudioNote('4B'),
])

FADED = Melody([
    AudioNote('4F#'),
    AudioNote('4F#'),
    AudioNote('4F#'),
    AudioNote('4A#'),
    AudioNote('5D#'),
    AudioNote('5D#'),
    AudioNote('5D#'),
    AudioNote('5C#'),
    AudioNote('4A#'),
    AudioNote('4A#'),
    AudioNote('4A#'),
    AudioNote('4C#'),
    AudioNote('4F'),
    AudioNote('4F'),
    AudioNote('4F'),
    AudioNote('4D#'),
])

SOMETHING_JUST_LIKE_THIS = Melody([
    AudioNote('5D'),
    AudioNote('5F#'),
    AudioNote('5F#'),
    AudioNote('5E'),
    AudioNote('5E'),
    AudioNote('5E'),
    AudioNote('5D'),
])


if __name__ == '__main__':
    FADED.play()
