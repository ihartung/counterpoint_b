from random import randint

class Contrapunctus:

    perfect = [1,5,8]
    consonants = [1,3,5,6,8]

    def __init__(self, key):
        self.center = key.split()[0]
        self.offset = self.getOffset(self.center)
        if 'major' in key:
            tmp = [2,2,1,2,2,2,1]
            self.scale = tmp[self.offset:] + tmp[:self.offset]
        else:
            tmp = [2,1,2,2,1,2,2]
            self.scale = tmp[self.offset:] + tmp[:self.offset]

    def getOffset(self, name):
        flatmap = {'Db':'C#','Eb':'D#','Gb':'F#','Ab':'G#','Bb':'A#'}
        if 'b' in name:
            name = flatmap[name]
        result = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        return result.index(name)

    def intervalUp(self, root, interval, half=0):
        print(type(interval))
        print(interval)
        print(root)
        print(half)
        pivot = root % 12
        if pivot==11:
            pivot = 0
        else:
            pivot = pivot + 1
        steps = self.scale[pivot:]
        if len(steps) < interval:
            steps = steps + self.scale
        return sum(steps[:interval-1]) + half + root

    def intervalDown(self, root, interval, half=0):
        pivot = root % 12
        if pivot==0:
            pivot = 11
        else:
            pivot = pivot - 1
        steps = self.scale[:pivot]
        if len(steps) < interval:
            steps = self.scale + steps
        return sum(steps[(interval-1) * -1:]) + half + root

    def findInterval(self, x, y):
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

    def oblique(self, pi, pcf, pcp, ccf):
        if pcf == ccf:
            # counterpoint
            intervals = list(filter(lambda x:x!=pi, self.consonants))
            ri = randint(0, len(intervals)-1)
            return intervals[ri]
        else:
            # if the melody moves, then the cp must stay the same
            return 0


    def contrary(self, pi, pcf, pcp, ccf):
        if ccf == pcf:
            return self.oblique(pi, pcf, pcp, ccf)
        if ccf > pcf:
            fil = lambda x:x<pi
        else:
            fil = lambda x:x>pi
        intervals = list(filter(fil, self.consonants))
        if len(intervals):
            ri = randint(0, len(intervals)-1)
            return intervals[ri]
        else:
            if pi in self.perfect:
                return self.oblique(pi, pcf, pcp, ccf)
            else:
                if randint(0,1):
                    return pi 
                else:
                    return self.oblique(pi, pcf, pcp, ccf)


    def isOblique(self, pcf, pcp, ccf, ccp):
        if pcf == ccf and pcp != ccp:
            return True
        elif pcp == ccp and pcf != ccf:
            return True
        else:
            return False

    def isContrary(self, pcf, pcp, ccf, ccp):
        if pcf > ccf and pcp < ccp:
            return True
        elif pcp > ccp and pcf < ccf:
            return True
        else:
            return False

    def isDirect(self, pcf, pcp, ccf, ccp):
        if pcf > ccf and pcp > ccp:
            return True
        elif pcp < ccp and pcf < ccf:
            return True
        else:
            return False


    def generate(self, melody, vertical=1):
        cp = []
        offset = vertical * 12
        ri = randint(0,2)

        # previous records the previous interval, slightly abused here
        previous = self.perfect[ri]

        # Beginning chord

        if vertical > 0:
            interval=self.intervalUp
        else:
            interval=self.intervalDown

        cp.append(interval(melody[0], previous))

        # Middle run
        i=1
        for note in melody[1:-2]:
            ri = randint(0,2)

            if previous in self.perfect:
                # We can move in oblique and contrary motion
                if randint(0,1):

                    # oblique
                    present = self.oblique(previous, melody[i-1], cp[i-1], melody[i])
                    if not present:
                        cp.append(cp[-1])
                        previous = self.findInterval(melody[i], cp[i])
                        i += 1
                        continue
                else:
                    # contrary
                    present = self.contrary(previous, melody[i-1], cp[i-1], melody[i])


            else:
                # We can move in direct, oblique, and contrary motion
                j = randint(0,2)
                if j == 2:
                    # direct 
                    present = previous
                elif j == 1:
                    # oblique
                    present = self.oblique(previous, melody[i-1], cp[i-1], melody[i])
                    if not present:
                        cp.append(cp[-1])
                        previous = self.findInterval(melody[i], cp[i])
                        i += 1
                        continue
                else:
                    present = self.contrary(previous, melody[i-1], cp[i-1], melody[i])
                    # contrary

            cp.append(interval(note, present))

            previous=present

            i += 1

        # Last two chords
        if vertical > 0:
            cp.append(interval(melody[-2], 6, 1))
        else:
            cp.append(interval(melody[-2], 3, -1))

        ri = randint(0,2)

        cp.append(interval(melody[-1], self.perfect[ri]))
        return cp



    # Check whether a melody (cf) and a counter melody (cp) obey the rules
    # vertical indicates whether the counter melody is in the upper or lower voice--positive for
    # upper, negative for lower.

    def isValid(self, cf, cp, vertical):
        if findInterval(cf[0], cp[0]) not in self.perfect:
            return False

        if len(cf) != len(cp):
            return False

        i=1
        for note in cf[1:-3]:
            # check acceptable intervals and transitions
            tmp = findInterval(note, cp[i])
            if tmp not in self.consonants:
                return False

            if isDirect(cf[i-1], cp[i-1], note, cp[i]):
                if tmp in self.perfect:
                    return False
            elif not isOblique(cf[i-1], cp[i-1], note, cp[i]) and \
                    not isContrary(cf[i-1], cp[i-1], note, cp[i]):
                        return False
            i += 1

        if vertical > 0 and cp[-2] != interval(cf[-2], 6, 1):
            return False
        elif cp[-2] != interval(cf[-2], 3, -1):
            return False

        if findInterval(cf[-1], cp[-1]) not in self.perfect:
            return False
        return True
