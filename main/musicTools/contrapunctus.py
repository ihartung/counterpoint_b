from random import random


def getOffset(name):
    flatmap = {'Db':'C#','Eb':'D#','Gb':'F#','Ab':'G#','Bb':'A#'}
    if 'b' in name:
        name = flatmap['name']
    result = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    return result.index(name)


class Contrapunctus:

    perfect = [1,5,8]
    consonants = [1,3,5,6,8]

    def __init__(self, key):
        self.center = key.split()[0]
        offset = getOffset(self.center)
        if 'major' in key:
            tmp = [2,2,1,2,2,2,1]
            self.scale = tmp[self.offset:] + tmp[:self.offset]
        else:
            tmp = [2,1,2,2,1,2,2]
            self.scale = tmp[self.offset:] + tmp[:self.offset]


    def intervalUp(root, interval, slight=0):
        pivot = root % 12
        if pivot==11:
            pivot = 0
        else:
            pivot = pivot + 1
        steps = self.scale[pivot:]
        if len(steps) < interval:
            steps = steps + self.scale
        return sum(steps[:interval-2]) + slight

    def intervalDown(root, interval, slight=0):
        pivot = root % 12
        if pivot==0:
            pivot = 11
        else:
            pivot = pivot - 1
        steps = self.scale[:pivot]
        if len(steps) < interval:
            steps = self.scale + steps
        return sum(steps[(interval-1) * -1:]) + slight

    def generate(melody, vertical=1):
        cp = []
        offset = vertical * 12
        ri = random() % 3

        # previous tells us whether the previous chord was perfect or imperfect
        # true if perfect, false otherwise
        previous = True

        # Beginning chord

        if vertical > 0:
            cp.push(intervalUp(melody[0], perfect[ri]))
        else:
            cp.push(intervalDown(melody[0], perfect[ri]))


        # Middle run
        i=1
        for note in melody[1:-3]:
            ri = random() % 3

            if previous:
                # We can move in oblique and contrary motion
                if random() % 2:
                    # oblique
                else:
                    # contrary

            else:
                # We can move in direct, oblique, and contrary motion
                j = random() % 3
                if j == 2:
                    # direct, the present chord must not be perfect
                elif j == 1:
                    # oblique
                else:
                    # contrary

            if vertical > 0:
                cp.push(intervalUp(note, a))
            else:
                cp.push(intervalDown(note, b))

        i += 1

        # Last two chords

        ri = random() % 3

        if vertical > 0:
            cp.push(intervalUp(melody[-2], 6, 1))
            cp.push(intervalUp(melody[-1], perfect[ri]))
        else:
            cp.push(intervalDown(melody[-2], 3, -1))
            cp.push(intervalDown(melody[-1], perfect[ri]))
