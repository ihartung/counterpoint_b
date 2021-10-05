from random import randint

class Contrapunctus:

    perfect = [1,5,8]
    consonants = [1,3,5,6,8]
    imperfects = [3,6]

    def __init__(self, key):
        self.center = key.split()[0]
        self.vertical = 1
        self.root = self.getMidi(self.center)
        if 'major' in key:
            tmp = [2,2,1,2,2,2,1]
        else:
            tmp = [2,1,2,2,1,2,2]
        self.scale = tmp[self.root:] + tmp[:self.root]
        self.setNaturals();

    def setNaturals(self):
        self.naturals = [self.root]
        x = self.root
        for interval in self.scale[:-1]:
            x = x + interval
            if x >= 12:
                x = x % 12
            self.naturals.append(x)
        self.naturals.sort()

    def getMidi(self, name):
        flatmap = {'Db':'C#','Eb':'D#','Gb':'F#','Ab':'G#','Bb':'A#'}
        if 'b' in name:
            name = flatmap[name]
        result = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
        return result.index(name)

    def getOffset(self, midi):
        if midi in self.naturals:
            return self.naturals.index(midi)
        for x in range(len(self.naturals)):
            if self.naturals[x] > midi:
                if self.vertical == 1:
                    return x-1
                else:
                    return x+1
        return 6

    def intervalUp(self, root, interval, half=0):
        if interval == 1:
            return root
        pivot = self.getOffset(root % 12)
        steps = self.scale[pivot:]
        while len(steps) < interval:
            steps = steps + self.scale
        return sum(steps[:interval-1]) + half + root

    def intervalDown(self, root, interval, half=0):
        if interval == 1:
            return root
        pivot = self.getOffset(root % 12)
        steps = self.scale[pivot-1::-1]
        while len(steps) < interval:
            steps = steps + self.scale[::-1]
        return root - sum(steps[:(interval-1)]) - half

    def findInterval(self, x, y):
        if x > y:
            tmp = x
            x = y
            y = tmp
        pivot = self.getOffset(x % 12)
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


    # the next three functions will return an appropriate interval
    # pi = previous interval
    # pcf = previous cantus firmus note
    # pcp = previous counterpoint note
    # ccf = current cantus firmus note

    def directAbove(self, pi, pcf, pcp, ccf):
        if pcf == ccf:
            return self.oblique(pi, pcf, pcp, ccf)
        if ccf > pcf:
            gap = pi - self.findInterval(ccf,pcf)
            fil = lambda x:x>gap
            y = 1
        else:
            gap = pi + self.findInterval(ccf,pcf)
            fil = lambda x:x<gap
            y=-1
        intervals = list(filter(fil, self.imperfects))
        if len(intervals):
            ri = randint(0, len(intervals)-1)
            return intervals[ri]
        if y == -1:
            if randint(0,1):
                ci = self.quickOblique(ccf, pcp)
                if ci:
                    return ci
                else:
                    return self.contrary(pi, pcf, pcp, ccf)
            else:
                return self.contrary(pi, pcf, pcp, ccf)
        big_intervals = self.imperfects
        while 1:
            big_intervals = list(map(lambda x: x+8, big_intervals))
            intervals = list(filter(fil, big_intervals))
            if len(intervals):
                ri = randint(0, len(intervals)-1)
                return intervals[ri]


    def directBelow(self, pi, pcf, pcp, ccf):
        if pcf == ccf:
            return self.oblique(pi, pcf, pcp, ccf)
        if ccf > pcf:
            gap = pi + self.findInterval(pcf,ccf)
            fil = lambda x:x<gap
            y = 1
        else:
            gap = pi - self.findInterval(pcf,ccf)
            fil = lambda x:x>gap
            y=-1
        intervals = list(filter(fil, self.imperfects))
        if len(intervals):
            ri = randint(0, len(intervals)-1)
            return intervals[ri]
        if y == 1:
            if randint(0,1):
                ci = self.quickOblique(ccf, pcp)
                if ci:
                    return ci
                else:
                    return self.contrary(pi, pcf, pcp, ccf)
            else:
                return self.contrary(pi, pcf, pcp, ccf)
        big_intervals = self.imperfects
        while 1:
            big_intervals = list(map(lambda x: x+8, big_intervals))
            intervals = list(filter(fil, big_intervals))
            if len(intervals):
                ri = randint(0, len(intervals)-1)
                return intervals[ri]


    def quickOblique(self, ccf, pcp):
        ci = self.findInterval(ccf, pcp)
        if ci in self.consonants:
            return ci
        return 0;


    def oblique(self, pi, pcf, pcp, ccf):
        if pcf == ccf:
            intervals = list(filter(lambda x:x!=pi, self.consonants))
            ri = randint(0, len(intervals)-1)
            return intervals[ri]
        else:
            # if the melody moves, then the cp must stay the same
            ci = self.quickOblique(ccf, pcp)
            if ci:
                return ci
            else:
                if randint(0, 1):
                    return self.contrary(pi, pcf, pcp, ccf)
                else:
                    # this will not cause an infinite loop with oblique
                    # because the melody has moved
                    return self.direct(pi, pcf, pcp, ccf)


    def contraryAbove(self, pi, pcf, pcp, ccf):
        if pcf == ccf:
            return self.oblique(pi, pcf, pcp, ccf)
        if ccf > pcf:
            gap = pi - self.findInterval(ccf,pcf)
            fil = lambda x:x<gap
            y = 1
        else:
            gap = pi + self.findInterval(pcf,ccf)
            fil = lambda x:x>gap
            y=-1
        intervals = list(filter(fil, self.consonants))
        if len(intervals):
            ri = randint(0, len(intervals)-1)
            return intervals[ri]
        if y == 1:
            if randint(0,1):
                ci = self.quickOblique(ccf, pcp)
                if ci:
                    return ci
                else:
                    return self.direct(pi, pcf, pcp, ccf)
            else:
                return self.direct(pi, pcf, pcp, ccf)
        big_intervals = self.consonants
        while 1:
            big_intervals = list(map(lambda x: x+8, big_intervals))
            intervals = list(filter(fil, big_intervals))
            if len(intervals):
                ri = randint(0, len(intervals)-1)
                return intervals[ri]

    def contraryBelow(self, pi, pcf, pcp, ccf):
        if pcf == ccf:
            return self.oblique(pi, pcf, pcp, ccf)
        if ccf > pcf:
            gap = pi + self.findInterval(ccf,pcf)
            fil = lambda x:x>gap
            y = 1
        else:
            gap = pi - self.findInterval(ccf,pcf)
            fil = lambda x:x<gap
            y=-1
        intervals = list(filter(fil, self.consonants))
        if len(intervals):
            ri = randint(0, len(intervals)-1)
            return intervals[ri]
        if y==-1:
            if randint(0,1):
                ci = self.quickOblique(ccf, pcp)
                if ci in self.consonants:
                    return ci
                else:
                    return self.direct(pi, pcf, pcp, ccf)
            else:
                return self.direct(pi, pcf, pcp, ccf)
        big_intervals = self.consonants
        while 1:
            big_intervals = list(map(lambda x: x+8, big_intervals))
            intervals = list(filter(fil, big_intervals))
            if len(intervals):
                ri = randint(0, len(intervals)-1)
                return intervals[ri]




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
            self.direct=self.directAbove
            self.contrary=self.contraryAbove
        else:
            interval=self.intervalDown
            self.direct=self.directBelow
            self.contrary=self.contraryBelow

        self.vertical = vertical

        cp.append(interval(melody[0], previous))

        # Middle run
        i=1
        for note in melody[1:-2]:
            j = randint(0,2)
            if j == 2:
                present = self.direct(previous, melody[i-1], cp[i-1], melody[i])
            elif j == 1:
                present = self.oblique(previous, melody[i-1], cp[i-1], melody[i])
            else:
                present = self.contrary(previous, melody[i-1], cp[i-1], melody[i])

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
        if self.findInterval(cf[0], cp[0]) not in self.perfect:
            return False

        if len(cf) != len(cp):
            return False

        i=1
        for note in cf[1:-3]:
            # check acceptable intervals and transitions
            tmp = self.findInterval(note, cp[i])
            if tmp not in self.consonants:
                return False

            if self.isDirect(cf[i-1], cp[i-1], note, cp[i]):
                if tmp in self.perfect:
                    return False
            elif not self.isOblique(cf[i-1], cp[i-1], note, cp[i]) and \
                    not self.isContrary(cf[i-1], cp[i-1], note, cp[i]):
                        return False
            i += 1

        if vertical > 0 and cp[-2] != self.intervalUp(cf[-2], 6, 1):
            return False
        elif cp[-2] != self.intervalDown(cf[-2], 3, -1):
            return False

        if self.findInterval(cf[-1], cp[-1]) not in self.perfect:
            return False
        return True
