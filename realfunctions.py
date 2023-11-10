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


def bin_to_vector(cad, dimension=20):  # Converts the large bit-string into the vector of real values
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

        for e in vector:
            sum += pow(e, 2)

        return sum

    def optimal_solution(self, function, size=50):
        if function == self.f1:
            return int(size / 2)
        elif function == self.f2:
            return size - 2
        elif function == self.f3:
            return pow(2, int(size / 2)) - 1
        elif function == self.f4:
            return pow(2, size) - 1
        elif function == self.f5:
            return size

        return None

    # Ahora la cadena binaria es la resulta de concatenar todos los valores binarios del vector de numeros reales
    # Cualquier numero desde el 9 al 15 en BCD lo tomaremos como 9
