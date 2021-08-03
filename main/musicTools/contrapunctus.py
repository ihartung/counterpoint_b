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

    def findInterval(x, y)
        if x > y:
            tmp = x
            x = y
            y = tmp
        pivot = x % 12
        steps = self.scale[pivot+1:]
        count = 1
        while 1:
            for step in steps:
                if x == y:
                    return count
                if x > y:
                    return count - .5
                x += step
                count += 1
            steps = self.scale


    # the next two functions will return an appropriate interval
    # pi = previous interval
    # pcf = previous cantus firmus note
    # pcp = previous counterpoint note
    # ccf = current cantus firmus note

    def oblique(pi, pcf, pcp, ccf):
        if pcf == ccf:
            # counterpoint
            intervals = filter(lambda x:x!=pi, consonants)
            ri = random() % len(intervals)
            return intervals[ri]
        else:
            # if the melody moves, then the cp must stay the same
            return 0


    def contrary(pi, pcf, pcp, ccf):
        if ccf == pcf:
            return oblique(pi, pcf, pcp, ccf)
        if ccf > pcf:
            fil = lambda x:x<pi
        elif ccf < pcf:
            fil = lambda x:x>pi
       intervals = filter(fil, consonants)
       if len(intervals):
           ri = random() % len(intervals)
           return intervals[ri]
       else:
           if pi in perfect:
               return oblique()
           else:
               if random() % 2:
                   return direct(pi, pcf, pcp, ccf)
               else:
                   return oblique(pi, pcf, pcp, ccf)


    def generate(melody, vertical=1):
        cp = []
        offset = vertical * 12
        ri = random() % 3

        # previous records the previous interval, slightly abused here
        previous = perfect[ri]

        # Beginning chord

        if vertical > 0:
            interval=intervalUp
        else:
            interval=intervalDown


        cp.push(interval(melody[0], previous))


        # Middle run
        i=1
        for note in melody[1:-3]:
            ri = random() % 3

            if previous in perfect:
                # We can move in oblique and contrary motion
                if random() % 2:
                    # oblique
                    present = oblique(previous, melody[i-1], cp[i-1], melody[i])
                    if not present:
                        cp.push(cp[-1])
                        previous = findInterval()
                        i += 1
                        continue
                else:
                    # contrary
                    present = contrary(previous, melody[i-1], cp[i-1], melody[i])


            else:
                # We can move in direct, oblique, and contrary motion
                j = random() % 3
                if j == 2:
                    # direct 
                    present = previous
                elif j == 1:
                    # oblique
                    present = oblique(previous, melody[i-1], cp[i-1], melody[i])
                    if not present:
                        cp.push(cp[-1])
                        previous = findInterval()
                        i += 1
                        continue
                else:
                    present = contrary(previous, melody[i-1], cp[i-1], melody[i])
                    # contrary

            cp.push(interval(note, present))

            previous= present

            i += 1

        # Last two chords

        ri = random() % 3

        if vertical > 0:
            cp.push(interval(melody[-2], 6, 1))
        else:
            cp.push(interval(melody[-2], 3, -1))

        cp.push(interval(melody[-1], perfect[ri]))
