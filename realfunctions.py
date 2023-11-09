class ObjFunction:

    def f1(self, cad):
        # F1: Counts the number of isolated "1" in the string
        # Max: 25

        cont = 0
        prev = '0'
        act = '0'

        for next in cad:
            if prev == '0' and act == '1' and next == '0':  # ...010...
                cont = cont + 1

            prev = act
            act = next

        # check the last one
        if prev == '0' and act == '1':
            cont = cont + 1

        return cont

    def f2(self, cad):
        # F2: Number of "0" between "1":  10*1
        # Max: 48

        sum = 0
        cont = 0
        between = False

        for c in cad:
            if not between and c == '1':  # we've found the begining
                between = True
            elif between and c == '0':  # Count 0's (doesn't mean they're between 1's)
                cont = cont + 1
            elif between and c == '1':  # 0's were definetly between 1's
                sum = sum + cont
                cont = 0

        return sum

    def f3(self, cad):
        # F3: Decimal value of the first half minus decimal value of the second half
        # Max: 33.554.431

        subStr1 = cad[0:25]
        subStr2 = cad[25:50]

        return int(subStr1, 2) - int(subStr2, 2)

    def f4(self, cad):
        # F4: Decimal value of the reverse bit string
        # Max: 1125899906842623

        rev = cad[::-1]

        return int(rev, 2)

    def f5(self, cad):
        # F5: How far is the first "1" from the left (10 if there's no "1")
        # Max: 50

        found = False
        i = 0
        while i < len(cad) and not found:
            c = cad[i]
            if c == '1':
                found = True
            i = i + 1

        if not found:
            return i
        else:
            return i - 1

    def optimal_solution(self, function, size=50):
        if function == self.f1:
            return int(size/2)
        elif function == self.f2:
            return size - 2
        elif function == self.f3:
            return pow(2, int(size/2)) - 1
        elif function == self.f4:
            return pow(2, size) - 1
        elif function == self.f5:
            return size

        return None

