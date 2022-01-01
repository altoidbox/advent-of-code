
# 1
z = int(input()) + 6
# 2
z *= 26 
z += (int(input()) + 2)
# 3
z *= 26 
z += (int(input()) + 13)
# 4
w = int(input())
x = ((z % 26) - 6)
z //= 26
if w != x:
    z *= 26
    z += w + 8


# 1 - 1
w, x, y, z = 0, 0, 0, 0
w = int(input())
x = z # x = 0; x += z
# x %= 26
# z //= 1
x = 12  # x += 12
x = w != 12  # x = x == w; x = x == 0
y = 25  # y = 0; y += 25
y = y * x
y += 1
z = z * y
y = w + 6  # y *= 0; y += w; y += 6
y *= x
z += y

# 2 - 19
w = int(input())  # inp w
x = z % 26 + 10 # mul x 0; add x z; mod x 26; div z 1; add x 10
if (w != x):  # eql x w; eql x 0
    z *= 26  # mul y 0; add y 25; mul y x; add y 1; mul z y
    z += (w + 2) * x  # mul y 0; add y w; add y 2; mul y x; add z y

# 3 - 37
w = int(input())  # inp w
x = z % 26 + 10  # mul x 0; add x z; mod x 26; div z 1; add x 10
if (w != x):  # eql x w; eql x 0
    z *= 26  # mul y 0; add y 25; mul y x; add y 1; mul z y
    z += (w + 13)  # mul y 0; add y w; add y 13; mul y x; add z y

# 4 - 55
w = int(input())  # inp w
x = z % 26 - 6  # mul x 0; add x z; mod x 26; add x -6
z //= 26  # div z 26
x = (w != x)  # eql x w; eql x 0
y = 25 * x + 1 # mul y 0; add y 25; mul y x; add y 1
z *= y  # mul z y
z += (w + 8) * x  # mul y 0; add y w; add y 8; mul y x; add z y
# ->
w = int(input())
x = (z % 26) - 6
z //= 26
if w != x:
    z *= 26
    z += w + 8

# 5 - 73
w = int(input())  # inp w
x = z % 26 + 11  # mul x 0; add x z; mod x 26; add x 11
x = (w != x)  # eql x w; eql x 0
y = 25 * x + 1 # mul y 0; add y 25; mul y x; add y 1
z *= y  # mul z y
z += (w + 13) * x  # mul y 0; add y w; add y 13; mul y x; add z y
# ->
w = int(input())
if w != (z % 26) + 11:
    z *= 26
    z += w + 13

# 6 - 91
w = int(input())  # inp w
x = z % 26 - 12  # mul x 0; add x z; mod x 26; add x -12
z //= 26  # div z 26
if (w != x): # eql x w; eql x 0
    z *= 26 # mul y 0; add y 25; mul y x; add y 1; mul z y
    z += (w + 8)  # mul y 0; add y w; add y 8; mul y x; add z y

# 7 - 109
w = int(input())  # inp w
x = z % 26 + 11  # mul x 0; add x z; mod x 26; add x 11
# div z 1
if (w != x): # eql x w; eql x 0
    z *= 26 # mul y 0; add y 25; mul y x; add y 1; mul z y
    z += (w + 3)  # mul y 0; add y w; add y 3; mul y x; add z y

# 8 - 127
w = int(input())  # inp w
x = z % 26 + 12  # mul x 0; add x z; mod x 26; add x 12
# div z 1
if (w != x): # eql x w; eql x 0
    z *= 26 # mul y 0; add y 25; mul y x; add y 1; mul z y
    z += (w + 11)  # mul y 0; add y w; add y 11; mul y x; add z y

# 9 - 145
w = int(input())  # inp w
x = z % 26 + 12  # mul x 0; add x z; mod x 26; add x 12
# div z 1
if (w != x): # eql x w; eql x 0
    z *= 26 # mul y 0; add y 25; mul y x; add y 1; mul z y
    z += (w + 10)  # mul y 0; add y w; add y 10; mul y x; add z y

# 10 - 163
w = int(input())  # inp w
x = z % 26 - 2  # mul x 0; add x z; mod x 26; add x -2
z //= 26  # div z 26
if (w != x): # eql x w; eql x 0
    z *= 26 # mul y 0; add y 25; mul y x; add y 1; mul z y
    z += (w + 8)  # mul y 0; add y w; add y 8; mul y x; add z y
# 11 - 181
w = int(input())  # inp w
x = z % 26 - 5  # mul x 0; add x z; mod x 26; add x -5
z //= 26  # div z 26
if (w != x): # eql x w; eql x 0
    z *= 26 # mul y 0; add y 25; mul y x; add y 1; mul z y
    z += (w + 14)  # mul y 0; add y w; add y 14; mul y x; add z y
# 12 - 199
w = int(input())  # inp w
x = z % 26 - 4  # mul x 0; add x z; mod x 26; add x -4
z //= 26  # div z 26
if (w != x): # eql x w; eql x 0
    z *= 26 # mul y 0; add y 25; mul y x; add y 1; mul z y
    z += (w + 6)  # mul y 0; add y w; add y 6; mul y x; add z y
# 13 - 217
w = int(input())  # inp w
x = z % 26 - 4  # mul x 0; add x z; mod x 26; add x -4
z //= 26  # div z 26
if (w != x): # eql x w; eql x 0
    z *= 26 # mul y 0; add y 25; mul y x; add y 1; mul z y
    z += (w + 8)  # mul y 0; add y w; add y 8; mul y x; add z y
# 14 - 235
w = int(input())  # inp w
x = z % 26 - 12  # mul x 0; add x z; mod x 26; add x -12
z //= 26  # div z 26
if (w != x): # eql x w; eql x 0
    z *= 26 # mul y 0; add y 25; mul y x; add y 1; mul z y
    z += (w + 10)  # mul y 0; add y w; add y 2; mul y x; add z y
