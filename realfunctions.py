import math
import random


def bcd_to_real(cad):  # Convert the bit-string into the real number that represents (4 decimal digits)
    # cad = cad.replace(' ', '')
    if ((len(cad) - 1) % 4) != 0:
        raise ValueError("Invalid decimal representation")

    # Obtain the sing
    sign = -1 if cad[0] == '1' else 1

    # Obtain digits
    digits = ""
    for i in range(1, len(cad), 4):
        num = int(cad[i:i + 4], 2)
        if num > 9:
            num = 9
        digits += str(num)

    # Separate decimals
    intDigits = digits[0:-4]
    decDigits = digits[-4:]

    realNum = sign * (int(intDigits) + int(decDigits) / 10000)

    return realNum


def bin_to_vector(cad, dimension=10):  # Converts the large bit-string into the vector of real values
    # cad = cad.replace(' ', '')
    length = len(cad)
    size = length // dimension
    vector = []

    for i in range(0, length, size):
        bcd = cad[i:i + size]
        vector.append(bcd_to_real(bcd))

    return vector


def real_to_bcd(real, int_digits=1):  # Converts a real number into it's binary representation
    bcd = '1' if real < 0 else '0'  # places the sign
    num = int(abs(real * 10000))  # removes decimal digits

    cad = str(num)
    while len(cad) < (
            int_digits + 4):  # Adjust the size of the bit string to the number of integer digits that should be represented at least
        cad = '0' + cad

    for d in cad:
        aux = bin(int(d))[2:]
        while len(aux) < 4:
            aux = '0' + aux
        bcd += aux

    return bcd


class ObjFunction:

    def sphere(self, cad):
        if len(cad) != 210:
            raise ValueError("Invalid input! 10 dimension problem was expected")

        vector = bin_to_vector(cad, 10)
        sum = 0
        cad = ""

        for e in vector:
            if e < -5.12 or e > 5.12:   # If the value is out of the boundaries: random one is generated
                e = random.uniform(-5.12, 5.12)

            cad += real_to_bcd(e, 1)
            sum += pow(e, 2)

        return 1 / (1 + sum), cad  # Inverse. Cause we wanna found the minimum

    def schwefel(self, cad):
        if len(cad) != 290:
            raise ValueError("Invalid input! 10 dimension problem was expected")

        vector = bin_to_vector(cad, 10)

        v1 = 4189.829   # Already multiplied for d=10
        sum = 0
        cad = ""

        for e in vector:
            if e < -500 or e > 500:
                e = random.uniform(-500, 500)

            cad += real_to_bcd(e, 3)

            sum += e * math.sin(pow(abs(e), 0.5))

        result = v1 - sum

        return 1 / (1 + result), cad  # Inverse. Cause we wanna found the minimum


    def rastrigin(self, cad):
        if len(cad) != 210:
            raise ValueError("Invalid input! 10 dimension problem was expected")

        vector = bin_to_vector(cad, 10)

        v1 = 100    # 10 * d
        sum = 0
        cad = ""

        for e in vector:
            if e < -5.12 or e > 5.12:   # If the value is out of the boundaries: random one is generated
                e = random.uniform(-5.12, 5.12)

            cad += real_to_bcd(e, 1)

            sum += pow(e, 2) - 10 * math.cos(2 * math.pi * e)

        result = v1 + sum

        return 1 / (1 + result), cad  # Inverse. Cause we wanna found the minimum


    def optimal_solution(self, function, size=50):
        if function == self.sphere:
            return 1
        if function == self.schwefel:
            return 1
        if function == self.rastrigin:
            return 1

        return None


