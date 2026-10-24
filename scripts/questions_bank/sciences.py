"""
Module: sciences.py
Generates exactly 100 authentic questions (34 Easy, 33 Medium, 33 Hard) for:
1. Mathematics
2. Physics
3. Chemistry
4. Biology
"""
from scripts.question_helpers import make_q


# ==========================================
# 1. MATHEMATICS
# ==========================================
def get_mathematics_questions():
    qs = []
    
    # --- EASY (34) ---
    math_easy = [
        ("What is 15% of 480?", "72", ["68", "75", "80"], "15% of 480 = 0.15 * 480 = 72."),
        ("If 3x + 7 = 22, what is the value of x?", "5", ["4", "6", "7"], "3x = 22 - 7 = 15 => x = 5."),
        ("What is the Least Common Multiple (LCM) of 12 and 18?", "36", ["24", "48", "72"], "12 = 2^2 * 3, 18 = 2 * 3^2. LCM = 2^2 * 3^2 = 36."),
        ("What is the Greatest Common Divisor (GCD) of 36 and 60?", "12", ["6", "18", "24"], "Common divisors of 36 and 60 include 12, which is the highest."),
        ("What is the sum of the interior angles of a triangle?", "180 degrees", ["360 degrees", "270 degrees", "90 degrees"], "The sum of interior angles of any planar triangle is always 180 degrees."),
        ("What is the perimeter of a square with side length 8 cm?", "32 cm", ["64 cm", "16 cm", "24 cm"], "Perimeter = 4 * side = 4 * 8 = 32 cm."),
        ("A car travels 240 km in 4 hours. What is its average speed?", "60 km/h", ["50 km/h", "70 km/h", "80 km/h"], "Speed = Distance / Time = 240 / 4 = 60 km/h."),
        ("What is the square root of 625?", "25", ["15", "35", "45"], "25 * 25 = 625."),
        ("Simplify the expression: (2^3) * (2^4).", "128", ["64", "256", "32"], "2^3 * 2^4 = 2^(3+4) = 2^7 = 128."),
        ("If a shirt costs Rs 500 and is sold at a 20% discount, what is the selling price?", "Rs 400", ["Rs 420", "Rs 380", "Rs 450"], "Discount = 20% of 500 = 100. Selling price = 500 - 100 = Rs 400."),
        ("What is the value of 7! (7 factorial)?", "5040", ["720", "2520", "40320"], "7! = 7 * 6 * 5 * 4 * 3 * 2 * 1 = 5040."),
        ("What is the sum of the first 10 positive integers?", "55", ["45", "50", "60"], "Sum = n(n+1)/2 = 10 * 11 / 2 = 55."),
        ("If y = 4x - 5 and x = 3, what is y?", "7", ["6", "8", "9"], "y = 4(3) - 5 = 12 - 5 = 7."),
        ("What is the area of a rectangle with length 12 m and breadth 7 m?", "84 sq m", ["72 sq m", "96 sq m", "80 sq m"], "Area = length * breadth = 12 * 7 = 84 sq m."),
        ("Convert 0.75 into a fraction in its simplest form.", "3/4", ["7/10", "4/5", "15/20"], "0.75 = 75/100 = 3/4."),
        ("What is the reciprocal of -4/5?", "-5/4", ["5/4", "4/5", "-4/5"], "Reciprocal of a/b is b/a. Reciprocal of -4/5 is -5/4."),
        ("If the ratio of boys to girls is 3:2 and there are 30 boys, how many girls are there?", "20", ["15", "25", "18"], "3 units = 30 => 1 unit = 10. Girls = 2 units = 20."),
        ("What is the median of the numbers: 3, 7, 8, 12, 14?", "8", ["7", "10", "12"], "The numbers are sorted; the middle value is 8."),
        ("What is the mean of: 10, 20, 30, 40, 50?", "30", ["25", "35", "20"], "Mean = (10+20+30+40+50)/5 = 150/5 = 30."),
        ("What is the mode of: 4, 6, 7, 6, 9, 6, 8?", "6", ["7", "4", "8"], "6 appears three times, more than any other number."),
        ("What is the value of 5^0?", "1", ["0", "5", "Undefined"], "Any non-zero number raised to the power 0 equals 1."),
        ("What is the area of a right-angled triangle with base 6 cm and height 10 cm?", "30 sq cm", ["60 sq cm", "36 sq cm", "40 sq cm"], "Area = 0.5 * base * height = 0.5 * 6 * 10 = 30 sq cm."),
        ("Find the circumference of a circle with radius 7 cm (pi = 22/7).", "44 cm", ["88 cm", "22 cm", "154 cm"], "Circumference = 2 * pi * r = 2 * (22/7) * 7 = 44 cm."),
        ("If an angle is 35 degrees, what is its complementary angle?", "55 degrees", ["145 degrees", "65 degrees", "45 degrees"], "Complementary angles sum to 90 degrees: 90 - 35 = 55 degrees."),
        ("If an angle is 110 degrees, what is its supplementary angle?", "70 degrees", ["80 degrees", "90 degrees", "60 degrees"], "Supplementary angles sum to 180 degrees: 180 - 110 = 70 degrees."),
        ("Evaluate: |-15| - |7|.", "8", ["-8", "22", "-22"], "|-15| = 15, |7| = 7. 15 - 7 = 8."),
        ("What is the probability of flipping heads on a fair coin?", "1/2", ["1/4", "1", "0"], "A fair coin has two equally likely outcomes: Heads and Tails."),
        ("If 5 pens cost Rs 75, how much do 8 pens cost?", "Rs 120", ["Rs 110", "Rs 125", "Rs 100"], "1 pen = 75/5 = 15. 8 pens = 8 * 15 = Rs 120."),
        ("Solve for p: 2p - 8 = 10.", "9", ["8", "10", "7"], "2p = 18 => p = 9."),
        ("What is the smallest prime number?", "2", ["1", "3", "0"], "2 is the smallest prime number and the only even prime."),
        ("What is the volume of a cube with edge 4 cm?", "64 cubic cm", ["16 cubic cm", "48 cubic cm", "96 cubic cm"], "Volume = edge^3 = 4^3 = 64 cubic cm."),
        ("A circle has diameter 14 cm. What is its radius?", "7 cm", ["14 cm", "28 cm", "3.5 cm"], "Radius = Diameter / 2 = 14 / 2 = 7 cm."),
        ("If x/4 = 9, what is x?", "36", ["32", "40", "45"], "x = 9 * 4 = 36."),
        ("What is 25% written as a decimal?", "0.25", ["2.5", "0.025", "25.0"], "25% = 25/100 = 0.25.")
    ]
    for q, ca, wa, exp in math_easy:
        qs.append(make_q(q, ca, wa, "EASY", exp))

    # --- MEDIUM (33) ---
    math_med = [
        ("A sum doubles itself in 5 years at simple interest. What is the annual interest rate?", "20%", ["15%", "25%", "10%"], "SI = P => P * R * 5 / 100 = P => R = 100 / 5 = 20%."),
        ("Find the roots of the quadratic equation x^2 - 7x + 12 = 0.", "3 and 4", ["2 and 6", "-3 and -4", "1 and 12"], "(x - 3)(x - 4) = 0 => x = 3, 4."),
        ("A can complete a work in 12 days and B in 24 days. Working together, in how many days will they finish?", "8 days", ["6 days", "10 days", "9 days"], "Combined rate = 1/12 + 1/24 = 3/24 = 1/8 => 8 days."),
        ("What is the area of a circle whose circumference is 44 cm (pi = 22/7)?", "154 sq cm", ["144 sq cm", "160 sq cm", "176 sq cm"], "2*pi*r = 44 => r = 7 cm. Area = pi*r^2 = (22/7)*49 = 154 sq cm."),
        ("What is the value of log10(1000) + log10(100)?", "5", ["6", "4", "300"], "log10(1000) = 3 and log10(100) = 2. 3 + 2 = 5."),
        ("The 10th term of the arithmetic progression 2, 7, 12, 17... is:", "47", ["42", "52", "45"], "a = 2, d = 5. T10 = a + 9d = 2 + 9(5) = 47."),
        ("In how many ways can the letters of the word 'MATH' be arranged?", "24", ["12", "48", "16"], "4 distinct letters can be arranged in 4! = 24 ways."),
        ("What is the compound interest on Rs 10,000 for 2 years at 10% per annum compounded annually?", "Rs 2,100", ["Rs 2,000", "Rs 2,200", "Rs 1,900"], "Amount = 10000*(1.1)^2 = 12100. CI = 12100 - 10000 = Rs 2,100."),
        ("If sin(theta) = 3/5, what is the value of cos(theta) for an acute angle?", "4/5", ["3/4", "5/3", "1/5"], "cos^2 = 1 - sin^2 = 1 - 9/25 = 16/25 => cos(theta) = 4/5."),
        ("Find the distance between the points (1, 2) and (4, 6).", "5 units", ["6 units", "7 units", "4 units"], "Distance = sqrt((4-1)^2 + (6-2)^2) = sqrt(9 + 16) = 5."),
        ("What is the slope of the line passing through (2, 3) and (6, 11)?", "2", ["3", "4", "1/2"], "Slope m = (11 - 3)/(6 - 2) = 8/4 = 2."),
        ("A bag contains 5 red and 3 green balls. One ball is drawn. Probability it is red is:", "5/8", ["3/8", "1/2", "5/3"], "Total balls = 8. Favorable outcomes = 5. Probability = 5/8."),
        ("If a fair die is rolled, what is the probability of rolling a prime number?", "1/2", ["1/3", "2/3", "1/6"], "Prime numbers on a die: 2, 3, 5 (3 outcomes). P = 3/6 = 1/2."),
        ("Find the sum of the infinite geometric series: 1 + 1/2 + 1/4 + 1/8 + ...", "2", ["1.5", "3", "Infinite"], "Sum = a / (1 - r) = 1 / (1 - 0.5) = 2."),
        ("The average of 5 numbers is 20. If one number is excluded, average becomes 18. Excluded number is:", "28", ["26", "24", "30"], "Sum of 5 = 100. Sum of 4 = 72. Excluded = 100 - 72 = 28."),
        ("If the radius of a sphere is doubled, its volume increases by a factor of:", "8", ["4", "2", "6"], "V is proportional to r^3. (2r)^3 = 8r^3, so volume increases by 8 times."),
        ("Solve the system: x + y = 10 and x - y = 4. What is x?", "7", ["6", "8", "3"], "Adding both equations: 2x = 14 => x = 7."),
        ("What is the value of tan(45 degrees) + cot(45 degrees)?", "2", ["1", "0", "sqrt(2)"], "tan(45) = 1, cot(45) = 1. 1 + 1 = 2."),
        ("A train 150 m long crosses a pole in 15 seconds. Its speed in km/h is:", "36 km/h", ["45 km/h", "54 km/h", "30 km/h"], "Speed = 150/15 = 10 m/s. 10 * 18/5 = 36 km/h."),
        ("If a square and an equilateral triangle have the same perimeter 36 cm, what is the area of the square?", "81 sq cm", ["64 sq cm", "100 sq cm", "72 sq cm"], "Square side = 36/4 = 9 cm. Area = 9^2 = 81 sq cm."),
        ("Find the value of k if the equation x^2 - kx + 9 = 0 has equal roots.", "6 or -6", ["3 or -3", "9 or -9", "12 or -12"], "Discriminant b^2 - 4ac = 0 => k^2 - 36 = 0 => k = 6 or -6."),
        ("What is the 5th term of the geometric sequence 3, 6, 12...?", "48", ["36", "24", "96"], "a = 3, r = 2. T5 = a * r^4 = 3 * 16 = 48."),
        ("A shopkeeper marks an item 40% above cost and offers 10% discount. His profit percentage is:", "26%", ["30%", "24%", "28%"], "CP = 100 => MP = 140. SP = 140 * 0.9 = 126. Profit = 26%."),
        ("What is the length of the diagonal of a rectangle of sides 6 cm and 8 cm?", "10 cm", ["12 cm", "14 cm", "9 cm"], "d = sqrt(6^2 + 8^2) = sqrt(36 + 64) = 10 cm."),
        ("If 2^x = 32, what is the value of 3^(x - 2)?", "27", ["9", "81", "3"], "2^x = 32 => x = 5. Then 3^(5 - 2) = 3^3 = 27."),
        ("What is the remainder when 3^25 is divided by 4?", "3", ["1", "0", "2"], "3 = -1 (mod 4). (-1)^25 = -1 = 3 (mod 4)."),
        ("What is the value of cos(60 degrees)?", "1/2", ["sqrt(3)/2", "1/sqrt(2)", "1"], "Standard trigonometric value: cos(60) = 1/2."),
        ("How many subsets does a set with 5 elements have?", "32", ["25", "16", "64"], "A set with n elements has 2^n subsets: 2^5 = 32."),
        ("If a polygon has 8 sides (octagon), what is the sum of its interior angles?", "1080 degrees", ["900 degrees", "1260 degrees", "720 degrees"], "Sum = (n - 2) * 180 = 6 * 180 = 1080 degrees."),
        ("What is the acute angle between the hands of a clock at 3:30?", "75 degrees", ["90 degrees", "60 degrees", "85 degrees"], "Angle = |30*H - 5.5*M| = |30*3 - 5.5*30| = |90 - 165| = 75 degrees."),
        ("Evaluate: 10C2 (Combinations of 10 taken 2 at a time).", "45", ["90", "20", "50"], "10C2 = (10 * 9)/(2 * 1) = 45."),
        ("If x + 1/x = 4, what is x^2 + 1/x^2?", "14", ["16", "18", "12"], "(x + 1/x)^2 = x^2 + 1/x^2 + 2 => 16 - 2 = 14."),
        ("Find the midpoint of the line segment joining (3, -4) and (7, 6).", "(5, 1)", ["(4, 1)", "(5, 2)", "(2, 5)"], "Midpoint = ((3+7)/2, (-4+6)/2) = (5, 1).")
    ]
    for q, ca, wa, exp in math_med:
        qs.append(make_q(q, ca, wa, "MEDIUM", exp))

    # --- HARD (33) ---
    math_hard = [
        ("What is the derivative of f(x) = x^3 * sin(x) with respect to x?", "3x^2 sin(x) + x^3 cos(x)", ["3x^2 cos(x)", "x^3 cos(x) - 3x^2 sin(x)", "3x^2 sin(x)"], "Product rule: d/dx(uv) = u'v + uv' = 3x^2 sin(x) + x^3 cos(x)."),
        ("Evaluate the limit as x approaches 0 of sin(5x)/x.", "5", ["1", "0", "1/5"], "lim_{x->0} sin(kx)/x = k. Here k = 5."),
        ("In how many ways can 5 boys and 4 girls sit in a row such that no two girls are together?", "43,200", ["14,400", "28,800", "57,600"], "Boys seated: 5! = 120. 6 gaps for 4 girls: 6P4 = 360. 120 * 360 = 43,200."),
        ("What is the probability of rolling at least one 6 in three rolls of a fair die?", "91/216", ["1/6", "125/216", "1/2"], "P(no 6 in 3 rolls) = (5/6)^3 = 125/216. P(at least one 6) = 1 - 125/216 = 91/216."),
        ("What is the length of the tangent from (5, 0) to the circle x^2 + y^2 = 9?", "4", ["sqrt(34)", "3", "5"], "Length = sqrt(x1^2 + y1^2 - r^2) = sqrt(25 + 0 - 9) = sqrt(16) = 4."),
        ("Evaluate the definite integral of 2x dx from x = 1 to x = 4.", "15", ["16", "14", "12"], "Integral of 2x is x^2. Evaluated from 1 to 4: 4^2 - 1^2 = 16 - 1 = 15."),
        ("What is the determinant of the 2x2 matrix [[3, 5], [2, 7]]?", "11", ["21", "10", "31"], "Det = (3 * 7) - (5 * 2) = 21 - 10 = 11."),
        ("If a matrix A is of order 3x3 and |A| = 4, what is |2A|?", "32", ["8", "16", "24"], "For nxn matrix, |kA| = k^n |A|. Here 2^3 * 4 = 8 * 4 = 32."),
        ("Find the eccentricity of the ellipse x^2/25 + y^2/16 = 1.", "3/5", ["4/5", "9/25", "2/5"], "b^2 = a^2(1 - e^2) => 16 = 25(1 - e^2) => e^2 = 9/25 => e = 3/5."),
        ("Evaluate: lim_{x -> infinity} (3x^2 + 5x)/(2x^2 - 7).", "3/2", ["5/2", "0", "Infinity"], "Divide numerator and denominator by highest power x^2 => 3/2."),
        ("What is the general solution of the differential equation dy/dx = 3y?", "y = C * e^(3x)", ["y = 3x + C", "y = C * e^(-3x)", "y = C * x^3"], "dy/y = 3 dx => ln(y) = 3x + c => y = C * e^(3x)."),
        ("What is the coefficient of x^3 in the expansion of (1 + 2x)^5?", "80", ["40", "160", "20"], "Term = 5C3 * 1^2 * (2x)^3 = 10 * 8x^3 = 80x^3."),
        ("If vectors A = 2i + 3j and B = 4i - j, what is their dot product A . B?", "5", ["8", "11", "7"], "A . B = (2*4) + (3*-1) = 8 - 3 = 5."),
        ("What is the magnitude of the vector 3i - 4j + 12k?", "13", ["11", "15", "17"], "Magnitude = sqrt(3^2 + (-4)^2 + 12^2) = sqrt(9 + 16 + 144) = sqrt(169) = 13."),
        ("What is the angle between the planes 2x - y + z = 6 and x + y + 2z = 3?", "60 degrees", ["45 degrees", "90 degrees", "30 degrees"], "cos(theta) = |2(1) - 1(1) + 1(2)| / (sqrt(6)*sqrt(6)) = 3/6 = 1/2 => 60 degrees."),
        ("What is the area bounded by the curve y = x^2 and line y = 4?", "32/3", ["16/3", "8", "64/3"], "Area = 2 * int_0^2 (4 - x^2) dx = 2 * [4x - x^3/3]_0^2 = 2 * (8 - 8/3) = 32/3."),
        ("The rank of the matrix [[1, 2, 3], [2, 4, 6], [3, 6, 9]] is:", "1", ["3", "2", "0"], "Rows 2 and 3 are exact scalar multiples of Row 1. Rank = 1."),
        ("If z = 1 + i*sqrt(3), what is the modulus and argument of z?", "Modulus = 2, Argument = pi/3", ["Modulus = 2, Argument = pi/6", "Modulus = 4, Argument = pi/3", "Modulus = 1, Argument = pi/4"], "|z| = sqrt(1 + 3) = 2. arg(z) = arctan(sqrt(3)/1) = pi/3 (60 degrees)."),
        ("Find the derivative of ln(sec(x) + tan(x)).", "sec(x)", ["tan(x)", "sec(x) * tan(x)", "sec^2(x)"], "d/dx ln(sec x + tan x) = (sec x tan x + sec^2 x)/(sec x + tan x) = sec x."),
        ("What is the value of int_0^(pi/2) sin^2(x) dx?", "pi/4", ["pi/2", "1", "1/2"], "By symmetry int sin^2 = int cos^2 = (1/2) * (pi/2) = pi/4."),
        ("How many diagonals does a regular polygon with 12 sides have?", "54", ["48", "66", "72"], "Diagonals = n(n - 3)/2 = 12 * 9 / 2 = 54."),
        ("If f(x) = |x - 2|, at x = 2 the function is:", "Continuous but not differentiable", ["Differentiable and continuous", "Neither continuous nor differentiable", "Discontinuous"], "Left derivative is -1, right derivative is +1. Continuous everywhere, non-differentiable at sharp point x = 2."),
        ("Find the maximum value of f(x) = sin(x) + cos(x).", "sqrt(2)", ["2", "1", "sqrt(3)"], "Maximum value of a*sin(x) + b*cos(x) is sqrt(a^2 + b^2) = sqrt(1+1) = sqrt(2)."),
        ("A box has 4 white and 6 black balls. 2 balls drawn without replacement. Probability both are white is:", "2/15", ["4/25", "1/5", "1/10"], "P = (4/10) * (3/9) = 12/90 = 2/15."),
        ("The sum of eigenvalues of a matrix is equal to its:", "Trace", ["Determinant", "Rank", "Inverse"], "Theorem: Sum of eigenvalues = Trace (sum of main diagonal elements)."),
        ("The product of eigenvalues of a square matrix is equal to its:", "Determinant", ["Trace", "Rank", "Norm"], "Theorem: Product of eigenvalues of matrix A = det(A)."),
        ("Find the focus of the parabola y^2 = 12x.", "(3, 0)", ["(0, 3)", "(6, 0)", "(-3, 0)"], "Standard form y^2 = 4ax => 4a = 12 => a = 3. Focus is (a, 0) = (3, 0)."),
        ("What is the radius of the circle x^2 + y^2 - 4x + 6y - 12 = 0?", "5", ["4", "6", "sqrt(12)"], "Center = (2, -3). r = sqrt(g^2 + f^2 - c) = sqrt(4 + 9 - (-12)) = sqrt(25) = 5."),
        ("What is the value of i^49 where i = sqrt(-1)?", "i", ["-i", "1", "-1"], "49 = 4 * 12 + 1 => i^49 = (i^4)^12 * i = 1 * i = i."),
        ("Evaluate: int e^(2x) dx.", "(1/2) e^(2x) + C", ["2 e^(2x) + C", "e^(2x) + C", "e^x + C"], "Integral of e^(kx) dx is (1/k) e^(kx) + C."),
        ("What is the inverse of the matrix [[1, 0], [0, 1]]?", "Identity matrix [[1, 0], [0, 1]]", ["[[0, 1], [1, 0]]", "[[-1, 0], [0, -1]]", "Does not exist"], "The identity matrix is its own inverse."),
        ("If two events A and B are independent with P(A) = 0.4 and P(B) = 0.5, what is P(A union B)?", "0.7", ["0.9", "0.6", "0.2"], "P(A union B) = P(A) + P(B) - P(A)*P(B) = 0.4 + 0.5 - 0.20 = 0.70."),
        ("Find the asymptote of y = (2x + 1)/(x - 3).", "x = 3 and y = 2", ["x = 2 and y = 3", "x = -3 and y = 2", "x = 3 and y = 0"], "Vertical asymptote at denominator = 0 (x = 3). Horizontal asymptote as x -> inf is y = 2.")
    ]
    for q, ca, wa, exp in math_hard:
        qs.append(make_q(q, ca, wa, "HARD", exp))

    return qs


# ==========================================
# 2. PHYSICS
# ==========================================
def get_physics_questions():
    qs = []
    
    # --- EASY (34) ---
    phys_easy = [
        ("What is the SI unit of Force?", "Newton", ["Joule", "Pascal", "Watt"], "The SI unit of force is the Newton (N = kg*m/s^2)."),
        ("What is the approximate acceleration due to gravity near Earth's surface?", "9.8 m/s^2", ["8.9 m/s^2", "11.2 m/s^2", "6.67 m/s^2"], "Standard gravitational acceleration g on Earth is ~9.8 m/s^2."),
        ("Which of Newton's laws states that for every action there is an equal and opposite reaction?", "Third Law", ["First Law", "Second Law", "Law of Gravitation"], "Newton's Third Law states every action has an equal and opposite reaction."),
        ("What is the SI unit of electrical resistance?", "Ohm", ["Volt", "Ampere", "Coulomb"], "Electrical resistance is measured in Ohms (symbol Omega)."),
        ("What is the speed of light in vacuum?", "3 x 10^8 m/s", ["3 x 10^6 m/s", "3 x 10^10 m/s", "1.5 x 10^8 m/s"], "The speed of light c in vacuum is approximately 300,000 km/s or 3x10^8 m/s."),
        ("What instrument is used to measure electric current?", "Ammeter", ["Voltmeter", "Ohmmeter", "Galvanometer"], "An ammeter is connected in series in a circuit to measure current in Amperes."),
        ("Which of the following colors of visible light has the shortest wavelength?", "Violet", ["Red", "Green", "Yellow"], "Violet light has the shortest wavelength (~380-450 nm) and highest frequency."),
        ("The rate of change of displacement with respect to time is known as:", "Velocity", ["Acceleration", "Speed", "Momentum"], "Velocity is a vector quantity defined as displacement divided by time."),
        ("What is the SI unit of work and energy?", "Joule", ["Newton", "Watt", "Calorie"], "Work and energy have the SI unit Joule (J = N*m)."),
        ("Sound waves cannot travel through:", "Vacuum", ["Water", "Steel", "Air"], "Sound requires a material medium to propagate; it cannot travel in a vacuum."),
        ("What type of lens is thinner at the center and thicker at the edges?", "Concave lens", ["Convex lens", "Bifocal lens", "Cylindrical lens"], "A diverging or concave lens is thinner in the middle than at the edges."),
        ("What is the SI unit of frequency?", "Hertz", ["Decibel", "Second", "Meter"], "Frequency (cycles per second) is measured in Hertz (Hz)."),
        ("Which form of heat transfer does NOT require any medium?", "Radiation", ["Conduction", "Convection", "Advection"], "Radiation transfers thermal energy via electromagnetic waves through empty space."),
        ("What is the formula for kinetic energy of a mass m moving at velocity v?", "1/2 m v^2", ["m v", "m g h", "1/2 m^2 v"], "Kinetic energy is given by KE = 0.5 * m * v^2."),
        ("What is the SI unit of pressure?", "Pascal", ["Bar", "Torr", "Atmosphere"], "The SI unit of pressure is the Pascal (Pa = N/m^2)."),
        ("When ice melts into water at 0 degrees Celsius, its density:", "Increases", ["Decreases", "Remains same", "Becomes zero"], "Water has anomalous expansion; liquid water at 0°C is denser than solid ice."),
        ("Which mirror is commonly used as a rear-view mirror in automobiles?", "Convex mirror", ["Concave mirror", "Plane mirror", "Parabolic mirror"], "Convex mirrors produce diminished, erect images with a wider field of view."),
        ("The resistance of an ideal ammeter should be:", "Zero", ["Infinite", "100 Ohms", "1 Ohm"], "An ideal ammeter has zero resistance to avoid altering circuit current."),
        ("The resistance of an ideal voltmeter should be:", "Infinite", ["Zero", "100 Ohms", "10 Ohms"], "An ideal voltmeter has infinite resistance so it draws no current from the circuit."),
        ("What is the energy possessed by an object due to its position called?", "Potential energy", ["Kinetic energy", "Thermal energy", "Chemical energy"], "Gravitational potential energy depends on mass, gravity, and height (PE = mgh)."),
        ("Which physical quantity is measured in Watts?", "Power", ["Work", "Force", "Energy"], "Power is the rate of doing work, measured in Watts (1 W = 1 J/s)."),
        ("A device that converts mechanical energy into electrical energy is a:", "Generator", ["Electric motor", "Transformer", "Battery"], "An electric generator uses electromagnetic induction to produce electricity."),
        ("The bending of light as it passes from one medium to another is called:", "Refraction", ["Reflection", "Diffraction", "Dispersion"], "Refraction occurs due to the change in speed of light in different optical media."),
        ("What is the value of absolute zero temperature in Celsius?", "-273.15 degrees C", ["0 degrees C", "-100 degrees C", "-459 degrees C"], "Absolute zero (0 Kelvin) corresponds to -273.15°C."),
        ("Which fundamental force is the weakest in nature?", "Gravitational force", ["Electromagnetic force", "Weak nuclear force", "Strong nuclear force"], "Gravity is the weakest fundamental force, though it has infinite range."),
        ("What is the primary source of solar energy?", "Nuclear fusion", ["Nuclear fission", "Chemical combustion", "Gravitational collapse"], "Hydrogen nuclei fuse into helium inside the sun's core, releasing vast energy."),
        ("An object stays at rest unless acted upon by an external force. This represents:", "Inertia (Newton's 1st Law)", ["Newton's 2nd Law", "Newton's 3rd Law", "Kepler's Law"], "Newton's First Law is also known as the Law of Inertia."),
        ("What is the unit of electric charge?", "Coulomb", ["Ampere", "Volt", "Farad"], "Electric charge is measured in Coulombs (C = A * s)."),
        ("What is the relationship between frequency (f), wavelength (lambda), and speed (v)?", "v = f * lambda", ["v = f / lambda", "v = lambda / f", "v = f + lambda"], "The wave equation is speed = frequency * wavelength."),
        ("Splitting of white light into its constituent spectral colors is called:", "Dispersion", ["Diffraction", "Polarization", "Interference"], "Dispersion occurs because different wavelengths refract by different angles in a prism."),
        ("What is the unit of capacitance?", "Farad", ["Henry", "Ohm", "Tesla"], "Capacitance (ability to store charge per unit voltage) is measured in Farads (F)."),
        ("Atmospheric pressure is measured using a:", "Barometer", ["Manometer", "Hydrometer", "Thermometer"], "A mercury barometer measures atmospheric pressure."),
        ("Weight of an object on the Moon is roughly what fraction of its weight on Earth?", "1/6", ["1/2", "1/4", "1/8"], "Lunar gravity is approximately 1.62 m/s^2, about 1/6th of Earth's gravity."),
        ("In a pure resistive AC circuit, current and voltage are:", "In phase", ["90 deg out of phase", "180 deg out of phase", "45 deg out of phase"], "In an ideal resistor, voltage and current oscillate simultaneously in phase.")
    ]
    for q, ca, wa, exp in phys_easy:
        qs.append(make_q(q, ca, wa, "EASY", exp))

    # --- MEDIUM (33) ---
    phys_med = [
        ("A ball is dropped from a height of 20 m. With what speed does it hit ground? (g = 10 m/s^2)", "20 m/s", ["10 m/s", "14.1 m/s", "25 m/s"], "v^2 = u^2 + 2gh = 0 + 2(10)(20) = 400 => v = 20 m/s."),
        ("What is the kinetic energy of a 2 kg body moving at 5 m/s?", "25 Joules", ["50 Joules", "10 Joules", "20 Joules"], "KE = 0.5 * m * v^2 = 0.5 * 2 * 25 = 25 Joules."),
        ("Two resistors of 6 Ohms and 3 Ohms are connected in parallel. Equivalent resistance is:", "2 Ohms", ["9 Ohms", "4.5 Ohms", "1.5 Ohms"], "1/R = 1/6 + 1/3 = 3/6 = 1/2 => R = 2 Ohms."),
        ("What is the power dissipated in a 10 Ohm resistor carrying a current of 2 Amperes?", "40 Watts", ["20 Watts", "100 Watts", "200 Watts"], "P = I^2 * R = 2^2 * 10 = 4 * 10 = 40 Watts."),
        ("A convex lens has a focal length of 20 cm. What is its optical power in Dioptres?", "+5 D", ["+0.05 D", "+2 D", "+10 D"], "Power P = 1 / f(in meters) = 1 / 0.20 = +5 Dioptres."),
        ("If the distance between two masses is doubled, the gravitational force between them becomes:", "1/4th", ["Half", "Double", "1/8th"], "Gravitational force obeys the inverse-square law: F proportional to 1/r^2."),
        ("What is the momentum of a 1500 kg car moving at 20 m/s?", "30,000 kg m/s", ["15,000 kg m/s", "75 kg m/s", "300,000 kg m/s"], "p = m * v = 1500 * 20 = 30,000 kg m/s."),
        ("An electric heater consumes 1000 W for 2 hours. How many electrical units (kWh) are used?", "2 kWh", ["1 kWh", "2000 kWh", "0.5 kWh"], "Energy = Power * time = 1 kW * 2 h = 2 kWh (2 units)."),
        ("What is the critical angle for total internal reflection if refractive index of medium is 2?", "30 degrees", ["45 degrees", "60 degrees", "90 degrees"], "sin(C) = 1/mu = 1/2 => C = 30 degrees."),
        ("A sound wave has frequency 500 Hz and speed 340 m/s. What is its wavelength?", "0.68 m", ["1.47 m", "0.34 m", "1.70 m"], "lambda = v / f = 340 / 500 = 0.68 m."),
        ("What is the time period of a simple pendulum of length 1 m? (take g = pi^2 m/s^2)", "2 seconds", ["1 second", "4 seconds", "pi seconds"], "T = 2 * pi * sqrt(L/g) = 2 * pi * sqrt(1/pi^2) = 2 seconds."),
        ("A force of 50 N acts on an area of 2 m^2. What is the pressure produced?", "25 Pa", ["100 Pa", "50 Pa", "10 Pa"], "P = F / A = 50 / 2 = 25 Pa."),
        ("What is the work done in moving a 5 C charge through a potential difference of 12 V?", "60 Joules", ["2.4 Joules", "17 Joules", "30 Joules"], "Work W = q * V = 5 * 12 = 60 Joules."),
        ("The focal length of a spherical mirror of radius of curvature 30 cm is:", "15 cm", ["60 cm", "30 cm", "10 cm"], "f = R / 2 = 30 / 2 = 15 cm."),
        ("A car accelerates uniformly from rest to 30 m/s in 6 seconds. Its acceleration is:", "5 m/s^2", ["6 m/s^2", "180 m/s^2", "2.5 m/s^2"], "a = (v - u) / t = (30 - 0) / 6 = 5 m/s^2."),
        ("How much heat is required to raise temperature of 1 kg of water by 10 deg C? (c = 4200 J/kg K)", "42,000 J", ["4,200 J", "420 J", "420,000 J"], "Q = m * c * deltaT = 1 * 4200 * 10 = 42,000 Joules."),
        ("What is the magnetic force on a charge q moving parallel to a magnetic field B?", "Zero", ["q v B", "q v / B", "q B"], "F = q(v x B) = q v B sin(0) = 0 when moving parallel."),
        ("A transformer has 100 primary turns and 500 secondary turns. It is a:", "Step-up transformer", ["Step-down transformer", "Isolation transformer", "Auto transformer"], "Secondary turns > Primary turns increases output voltage: Step-up."),
        ("In an elastic collision between two isolated bodies, which quantities are conserved?", "Both Momentum and Kinetic Energy", ["Only Momentum", "Only Kinetic Energy", "Neither"], "Elastic collisions conserve both linear momentum and total kinetic energy."),
        ("What happens to the resistance of a pure semiconductor as temperature increases?", "Decreases", ["Increases", "Remains constant", "Becomes zero immediately"], "Semiconductors have negative temperature coefficient of resistance (NTC)."),
        ("What is the buoyant force on an object submerged in a fluid equal to?", "Weight of displaced fluid", ["Weight of the object", "Volume of the object", "Mass of the fluid"], "Archimedes Principle: Upthrust = Weight of fluid displaced."),
        ("A projectile is launched at 45 degrees. Its range is maximum because:", "sin(2 * 45) = 1 (maximum)", ["cos(45) is minimum", "Gravity is zero", "Air resistance is zero"], "R = (u^2 sin 2theta)/g. Maximum when sin(2*theta) = 1 => theta = 45 degrees."),
        ("What is the unit of magnetic flux?", "Weber", ["Tesla", "Henry", "Gauss"], "Magnetic flux is measured in Webers (Wb = T * m^2)."),
        ("What is the unit of magnetic field strength (magnetic flux density)?", "Tesla", ["Weber", "Henry", "Ampere-meter"], "Magnetic field density B is measured in Tesla (T = N/(A*m))."),
        ("Two capacitors of 4 microfarads and 6 microfarads are in parallel. Total capacitance is:", "10 microfarads", ["2.4 microfarads", "24 microfarads", "5 microfarads"], "In parallel: C_total = C1 + C2 = 4 + 6 = 10 microfarads."),
        ("Two capacitors of 6 microfarads each are connected in series. Total capacitance is:", "3 microfarads", ["12 microfarads", "6 microfarads", "1.5 microfarads"], "In series: C_total = (C1 * C2)/(C1 + C2) = 36 / 12 = 3 microfarads."),
        ("What is the escape velocity from the surface of Earth approximately?", "11.2 km/s", ["8.2 km/s", "15.4 km/s", "9.8 km/s"], "Escape velocity v_e = sqrt(2gR) is approximately 11.2 km/s."),
        ("A body of mass 5 kg rests on a rough horizontal floor (mu = 0.4). Limiting friction is (g=10):", "20 N", ["25 N", "15 N", "50 N"], "f_s = mu * N = mu * m * g = 0.4 * 5 * 10 = 20 N."),
        ("An ideal gas expands isothermally. The change in its internal energy (delta U) is:", "Zero", ["Positive", "Negative", "Equal to work done"], "In an ideal gas, internal energy depends only on temperature; T is constant => delta U = 0."),
        ("What type of wave is an electromagnetic wave?", "Transverse wave", ["Longitudinal wave", "Mechanical wave", "Stationary wave"], "Electric and magnetic field vectors oscillate perpendicular to direction of propagation."),
        ("A wire of resistance R is stretched to double its original length. Its new resistance is:", "4R", ["2R", "R/2", "R/4"], "Volume is constant. If length doubles, area halves. R' = rho*(2L)/(A/2) = 4R."),
        ("According to Lenz's law, the direction of induced current always:", "Opposes the cause producing it", ["Supports the magnetic field", "Flows clockwise always", "Has zero magnitude"], "Lenz's Law is a consequence of conservation of energy: it opposes the flux change."),
        ("What is the threshold frequency in photoelectric effect?", "Minimum frequency required to eject electrons", ["Maximum frequency of photon", "Frequency of emitter", "Frequency of anode"], "Light below threshold frequency nu_0 cannot eject photoelectrons regardless of intensity.")
    ]
    for q, ca, wa, exp in phys_med:
        qs.append(make_q(q, ca, wa, "MEDIUM", exp))

    # --- HARD (33) ---
    phys_hard = [
        ("What is the efficiency of a Carnot engine operating between 500 K and 300 K?", "40%", ["60%", "20%", "30%"], "Carnot efficiency eta = 1 - (T_cold / T_hot) = 1 - 300/500 = 2/5 = 40%."),
        ("What is the de Broglie wavelength of an electron accelerated through 100 V?", "0.123 nm", ["1.23 nm", "0.012 nm", "12.3 nm"], "lambda = 1.227 / sqrt(V) nm = 1.227 / 10 = 0.1227 nm ~ 0.123 nm."),
        ("In an RLC series circuit at resonance, the power factor is:", "1.0 (Unity)", ["0", "0.5", "0.707"], "At resonance, inductive and capacitive reactances cancel (X_L = X_C). Impedance is purely resistive, power factor = 1."),
        ("What is the moment of inertia of a uniform solid sphere of mass M and radius R about its diameter?", "2/5 M R^2", ["1/2 M R^2", "2/3 M R^2", "M R^2"], "Standard moment of inertia formula for a solid sphere is 2/5 M R^2."),
        ("What is the work function of a metal if threshold wavelength is 620 nm? (hc ~ 1240 eV nm)", "2.0 eV", ["3.1 eV", "1.5 eV", "4.0 eV"], "Work function Phi = hc / lambda_0 = 1240 / 620 = 2.0 eV."),
        ("A particle executes SHM with amplitude A. At what displacement from mean position is KE = PE?", "A / sqrt(2)", ["A / 2", "A / 4", "A * sqrt(3) / 2"], "KE = PE => 0.5 k (A^2 - x^2) = 0.5 k x^2 => A^2 = 2x^2 => x = A / sqrt(2)."),
        ("What is the velocity of sound in an ideal gas proportional to?", "sqrt(Absolute Temperature)", ["Absolute Temperature", "1 / Temperature", "Pressure directly"], "v = sqrt(gamma * R * T / M); speed is directly proportional to the square root of Kelvin temperature."),
        ("In young's double slit experiment, if slit separation is halved and screen distance doubled, fringe width:", "Becomes 4 times", ["Doubles", "Halves", "Remains same"], "Fringe width beta = (lambda * D) / d. D -> 2D, d -> d/2 => beta' = 4 * beta."),
        ("The half-life of a radioactive isotope is 10 days. What fraction remains after 30 days?", "1/8th", ["1/4th", "1/16th", "1/6th"], "Number of half-lives n = 30 / 10 = 3. Remaining fraction = (1/2)^3 = 1/8."),
        ("What is the magnetic field at the center of a circular coil of N turns, radius R carrying current I?", "mu_0 N I / (2 R)", ["mu_0 N I / R", "mu_0 N I / (4 pi R)", "2 pi mu_0 N I / R"], "B at center of circular loop = mu_0 * N * I / (2R)."),
        ("In a p-n junction diode under reverse bias, the depletion layer width:", "Increases", ["Decreases", "Remains unchanged", "Vanishes"], "Reverse bias pulls majority carriers away from the junction, widening the depletion region."),
        ("What is the relation between bulk modulus B, pressure P, and volume V?", "B = - V (dP / dV)", ["B = - P (dV / dP)", "B = dP / dV", "B = V / P"], "Bulk modulus is volumetric stress over volumetric strain: B = - dP / (dV/V) = - V (dP/dV)."),
        ("A black body radiates heat at temperature T. If T is doubled, radiant energy per second increases by:", "16 times", ["4 times", "8 times", "2 times"], "Stefan-Boltzmann Law: E is proportional to T^4. (2T)^4 = 16 * T^4."),
        ("What is the torque acting on an electric dipole p in an external electric field E?", "p x E", ["p . E", "E / p", "p * E^2"], "Vector torque tau = p x E, with magnitude p * E * sin(theta)."),
        ("A satellite orbits Earth at height h = R (Earth radius). Its orbital velocity is:", "sqrt(g R / 2)", ["sqrt(g R)", "sqrt(2 g R)", "g R / 4"], "v = sqrt(G M / r) where r = 2R. Since GM = gR^2, v = sqrt(g R^2 / 2R) = sqrt(g R / 2)."),
        ("What is the self-inductance L of a solenoid of length l, area A, and N turns?", "mu_0 N^2 A / l", ["mu_0 N A / l", "mu_0 N^2 A * l", "N A / l"], "L = mu_0 * n^2 * A * l = mu_0 * (N/l)^2 * A * l = mu_0 * N^2 * A / l."),
        ("According to Brewster's law, polarization angle theta_p satisfies:", "tan(theta_p) = mu", ["sin(theta_p) = mu", "cos(theta_p) = mu", "cot(theta_p) = mu"], "At Brewster's angle, reflected light is completely polarized and tan(theta_p) = mu."),
        ("What is the Q-factor (Quality Factor) of a series RLC resonant circuit?", "(1 / R) * sqrt(L / C)", ["R * sqrt(L / C)", "sqrt(L C) / R", "R / sqrt(L C)"], "Q = omega_0 * L / R = (1 / sqrt(LC)) * L / R = (1/R) * sqrt(L/C)."),
        ("In an adiabatic process for an ideal gas, which equation holds true?", "P * V^gamma = Constant", ["P * V = Constant", "V / T = Constant", "P / T = Constant"], "An adiabatic process with no heat transfer follows P * V^gamma = constant."),
        ("What is the energy stored in a charged capacitor of capacitance C and voltage V?", "1/2 C V^2", ["C V", "1/2 C^2 V", "2 C V^2"], "Energy stored in electric field of capacitor U = 0.5 * C * V^2."),
        ("An observer moves towards a stationary sound source with speed v_o. Observed frequency f' is:", "f * (v + v_o) / v", ["f * (v - v_o) / v", "f * v / (v + v_o)", "f * v / (v - v_o)"], "Doppler formula when observer approaches stationary source: f' = f * (v + v_o) / v."),
        ("What is the radius of the first Bohr orbit of a hydrogen atom?", "0.529 Angstroms", ["1.058 Angstroms", "0.265 Angstroms", "2.116 Angstroms"], "Bohr radius a_0 = h^2 * epsilon_0 / (pi * m * e^2) ~ 0.0529 nm = 0.529 A."),
        ("The energy of an electron in the nth orbit of a hydrogen atom is proportional to:", "1 / n^2", ["1 / n", "n^2", "n"], "En = -13.6 / n^2 eV, which varies inversely with n^2."),
        ("What is the ratio of root mean square speed to average speed of gas molecules?", "sqrt(3 pi / 8)", ["sqrt(8 / 3 pi)", "sqrt(3 / 2)", "1"], "v_rms = sqrt(3RT/M), v_avg = sqrt(8RT/pi M). Ratio = sqrt(3 / (8/pi)) = sqrt(3 pi / 8)."),
        ("A wire carries current along the z-axis. The magnetic field at point (x, y, 0) is directed:", "Tangent to circle in x-y plane", ["Along z-axis", "Radially outward", "Radially inward"], "By Right Hand Thumb rule, magnetic field lines form concentric circles around the wire in the x-y plane."),
        ("The displacement equation in a wave is y = 0.02 sin(2 pi (50t - 2x)). Wave speed is:", "25 m/s", ["50 m/s", "100 m/s", "0.02 m/s"], "omega = 2 pi * 50 = 100 pi, k = 2 pi * 2 = 4 pi. Speed v = omega / k = 100 pi / 4 pi = 25 m/s."),
        ("A body slides down a frictionless inclined plane of angle theta. Its acceleration along the incline is:", "g sin(theta)", ["g cos(theta)", "g tan(theta)", "g"], "Component of gravitational force along the incline is m g sin(theta), so a = g sin(theta)."),
        ("What is the dimension of Planck's constant (h)?", "[M L^2 T^-1]", ["[M L T^-1]", "[M L^2 T^-2]", "[M L^0 T^-1]"], "E = h * nu => h = E / nu = [M L^2 T^-2] / [T^-1] = [M L^2 T^-1]."),
        ("In an ideal step-down transformer, if voltage decreases by a factor of 4, current:", "Increases by 4 times", ["Decreases by 4 times", "Remains unchanged", "Doubles"], "Power is conserved (V_p * I_p = V_s * I_s). If voltage drops to 1/4th, current quadruples."),
        ("The terminal velocity of a small spherical ball falling through a viscous fluid is proportional to:", "r^2 (radius squared)", ["r", "r^3", "1 / r"], "Stokes' law gives terminal velocity v_t = 2 r^2 (rho - sigma) g / (9 eta)."),
        ("What is the angle between electric field lines and equipotential surfaces?", "90 degrees (Perpendicular)", ["0 degrees (Parallel)", "45 degrees", "180 degrees"], "Electric field is the negative gradient of potential, always perpendicular to equipotential surfaces."),
        ("What is the work done in moving a charge along an equipotential surface?", "Zero", ["Positive", "Negative", "Depends on charge magnitude"], "W = q * delta V. On an equipotential surface, delta V = 0, so work done is identically zero."),
        ("What phenomenon provides conclusive evidence that light is a transverse wave?", "Polarization", ["Interference", "Diffraction", "Refraction"], "Only transverse waves can be polarized; longitudinal waves (like sound) cannot undergo polarization.")
    ]
    for q, ca, wa, exp in phys_hard:
        qs.append(make_q(q, ca, wa, "HARD", exp))

    return qs


# ==========================================
# 3. CHEMISTRY
# ==========================================
def get_chemistry_questions():
    qs = []
    
    # --- EASY (34) ---
    chem_easy = [
        ("What is the chemical formula of water?", "H2O", ["CO2", "H2O2", "HO2"], "Water consists of two hydrogen atoms bonded to one oxygen atom."),
        ("What is the atomic number of Carbon?", "6", ["12", "14", "8"], "Carbon has 6 protons in its nucleus, giving it atomic number 6."),
        ("What is the pH of pure water at 25 degrees Celsius?", "7.0 (Neutral)", ["0.0", "14.0", "5.5"], "Pure water is neutral with [H+] = [OH-] = 10^-7 M, corresponding to pH 7."),
        ("Which gas is the most abundant in Earth's atmosphere?", "Nitrogen", ["Oxygen", "Carbon dioxide", "Argon"], "Nitrogen makes up approximately 78% of Earth's atmosphere by volume."),
        ("What is the chemical symbol for Gold?", "Au", ["Ag", "Fe", "Pb"], "Au comes from the Latin word 'Aurum', meaning shining dawn."),
        ("What is the chemical symbol for Silver?", "Ag", ["Au", "Si", "Sr"], "Ag comes from the Latin word 'Argentum'."),
        ("Which of the following is an alkali metal?", "Sodium (Na)", ["Calcium (Ca)", "Iron (Fe)", "Aluminum (Al)"], "Group 1 metals (Li, Na, K, Rb, Cs, Fr) are alkali metals."),
        ("What type of bond is formed by the sharing of electrons between atoms?", "Covalent bond", ["Ionic bond", "Metallic bond", "Hydrogen bond"], "A covalent bond involves the sharing of electron pairs between atoms."),
        ("Which subatomic particle has a negative electric charge?", "Electron", ["Proton", "Neutron", "Positron"], "Electrons have a negative charge of -1.6 x 10^-19 Coulombs."),
        ("What is the chemical name of common table salt?", "Sodium chloride", ["Sodium bicarbonate", "Sodium hydroxide", "Potassium chloride"], "Table salt is NaCl, sodium chloride."),
        ("What is the chemical formula of Carbon Dioxide?", "CO2", ["CO", "C2O", "CH4"], "Carbon dioxide has one carbon atom double bonded to two oxygen atoms."),
        ("Which element is present in all organic compounds?", "Carbon", ["Nitrogen", "Oxygen", "Sulfur"], "Organic chemistry is defined as the chemistry of carbon compounds."),
        ("What is the state of matter of Bromine at room temperature?", "Liquid", ["Gas", "Solid", "Plasma"], "Bromine is one of only two liquid elements at standard conditions (with Mercury)."),
        ("What is the atomic number of Hydrogen?", "1", ["2", "0", "1.008"], "Hydrogen is the first and simplest element, with atomic number 1."),
        ("Acids turn blue litmus paper into which color?", "Red", ["Blue", "Yellow", "Green"], "Acids turn blue litmus red; bases turn red litmus blue."),
        ("What is the chemical formula of Methane?", "CH4", ["C2H6", "CH3", "C2H4"], "Methane is the simplest alkane hydrocarbon, CH4."),
        ("Which gas is commonly known as laughing gas?", "Nitrous oxide (N2O)", ["Nitric oxide (NO)", "Nitrogen dioxide (NO2)", "Ammonia (NH3)"], "Nitrous oxide (N2O) is used as an anesthetic and is known as laughing gas."),
        ("What is the chemical formula of rust?", "Fe2O3 . xH2O", ["FeO", "Fe3O4", "FeCl3"], "Rust is hydrated iron(III) oxide, Fe2O3 . xH2O."),
        ("Which law states that mass is neither created nor destroyed in a chemical reaction?", "Law of Conservation of Mass", ["Law of Definite Proportions", "Avogadro's Law", "Boyle's Law"], "Lavoisier formulated the Law of Conservation of Mass."),
        ("What is the value of Avogadro's number?", "6.022 x 10^23", ["6.022 x 10^22", "3.0 x 10^8", "1.6 x 10^-19"], "Avogadro's number represents particles per mole: 6.022 x 10^23 mol^-1."),
        ("What is the chemical formula of sulfuric acid?", "H2SO4", ["HCl", "HNO3", "H2SO3"], "Sulfuric acid is H2SO4, often called the 'King of Chemicals'."),
        ("Which acid is naturally found in citrus fruits like lemons and oranges?", "Citric acid", ["Acetic acid", "Lactic acid", "Tartaric acid"], "Citrus fruits are rich in citric acid."),
        ("What is the pH range of basic (alkaline) solutions at 25 degrees C?", "Greater than 7", ["Less than 7", "Exactly 7", "Negative"], "On the pH scale, values > 7 are basic, = 7 is neutral, and < 7 are acidic."),
        ("Which gas is released when an acid reacts with an active metal?", "Hydrogen (H2)", ["Oxygen (O2)", "Carbon dioxide", "Nitrogen"], "Metal + Acid -> Salt + Hydrogen gas (pops with a lighted splint)."),
        ("What is the common name of Sodium Bicarbonate (NaHCO3)?", "Baking soda", ["Washing soda", "Caustic soda", "Bleaching powder"], "NaHCO3 is commercially known as baking soda."),
        ("Which non-metal is a good conductor of electricity?", "Graphite", ["Diamond", "Sulfur", "Phosphorus"], "Graphite has delocalized pi electrons between its hexagonal layers."),
        ("Hardness of water is caused by salts of which two metals?", "Calcium and Magnesium", ["Sodium and Potassium", "Iron and Copper", "Zinc and Lead"], "Hardness is primarily due to dissolved Ca2+ and Mg2+ bicarbonates, sulfates, and chlorides."),
        ("What is the chemical name of vitamin C?", "Ascorbic acid", ["Citric acid", "Folic acid", "Acetic acid"], "Vitamin C is chemically known as L-ascorbic acid."),
        ("Which element has the highest electronegativity on the Pauling scale?", "Fluorine (F)", ["Oxygen (O)", "Chlorine (Cl)", "Nitrogen (N)"], "Fluorine is the most electronegative element with a Pauling value of 3.98 ~ 4.0."),
        ("What is the chemical formula of Ozone?", "O3", ["O2", "O4", "O"], "Ozone is an allotrope of oxygen consisting of three oxygen atoms: O3."),
        ("The process of conversion of a solid directly into vapor is called:", "Sublimation", ["Evaporation", "Condensation", "Deposition"], "Sublimation bypasses the liquid phase (e.g., dry ice, camphor)."),
        ("What is the chemical formula of bleaching powder?", "CaOCl2", ["CaCl2", "CaCO3", "Ca(OH)2"], "Bleaching powder is calcium hypochlorite / chloride: CaOCl2."),
        ("What is the light gas filled in balloons that is lighter than air and non-flammable?", "Helium", ["Hydrogen", "Argon", "Neon"], "Helium is an inert noble gas that does not combust, making it safe for airships."),
        ("Vinegar is a dilute aqueous solution of which acid?", "Acetic acid", ["Formic acid", "Citric acid", "Hydrochloric acid"], "Vinegar is typically a 4-8% aqueous solution of acetic acid (CH3COOH).")
    ]
    for q, ca, wa, exp in chem_easy:
        qs.append(make_q(q, ca, wa, "EASY", exp))

    # --- MEDIUM (33) ---
    chem_med = [
        ("What is the hybridization of the central carbon atom in Methane (CH4)?", "sp3", ["sp2", "sp", "dsp2"], "Carbon in CH4 forms 4 single sigma bonds, adopting tetrahedral sp3 hybridization."),
        ("What is the oxidation state of Manganese in Potassium Permanganate (KMnO4)?", "+7", ["+6", "+4", "+2"], "K is +1, each O is -2 (-8 total). +1 + Mn - 8 = 0 => Mn = +7."),
        ("According to Le Chatelier's principle, increasing pressure on N2 + 3H2 <=> 2NH3 shifts equilibrium to:", "Forward (Right)", ["Backward (Left)", "No effect", "Stops reaction"], "Higher pressure favors the side with fewer gas moles (4 moles reactants -> 2 moles product)."),
        ("What is the molarity of a solution containing 40 g of NaOH in 1 liter of solution? (Molar mass NaOH = 40)", "1.0 M", ["0.5 M", "2.0 M", "0.1 M"], "Moles of NaOH = 40 / 40 = 1 mol. Molarity = 1 mol / 1 L = 1.0 M."),
        ("What is the pH of a 0.001 M HCl solution?", "3", ["1", "4", "2"], "HCl is a strong acid: [H+] = 10^-3 M. pH = -log(10^-3) = 3."),
        ("What is the bond angle in a water (H2O) molecule approximately?", "104.5 degrees", ["109.5 degrees", "120 degrees", "90 degrees"], "Two lone pairs on oxygen repel bonding pairs, reducing tetrahedral angle from 109.5 to 104.5 degrees."),
        ("Which of the following compounds exhibits optical isomerism (has a chiral carbon)?", "2-Chlorobutane", ["1-Chlorobutane", "2-Chloropropane", "Ethanol"], "Carbon-2 in 2-chlorobutane is bonded to four distinct groups: -H, -CH3, -Cl, -C2H5."),
        ("What is the conjugate base of HSO4^- (bisulfate ion)?", "SO4^2-", ["H2SO4", "SO3^2-", "H3SO4+"], "A conjugate base is formed by removing one proton (H+): HSO4^- minus H+ = SO4^2-."),
        ("Which catalyst is traditionally used in the Haber process for synthesizing ammonia?", "Finely divided Iron (Fe)", ["Platinum", "Nickel", "Vanadium pentoxide"], "Finely divided iron with molybdenum/potassium oxide promoter is used in the Haber process."),
        ("What is the catalyst used in the Contact Process for the manufacture of Sulfuric acid?", "V2O5 (Vanadium pentoxide)", ["Fe2O3", "Pt", "MnO2"], "Vanadium(V) oxide catalyzes the oxidation of SO2 to SO3 in the Contact Process."),
        ("Which rule states that electrons occupy lowest available energy orbitals first?", "Aufbau Principle", ["Hund's Rule", "Pauli Exclusion Principle", "Heisenberg Principle"], "The Aufbau principle dictates filling orbitals in order of increasing (n + l) energy."),
        ("What is the maximum number of electrons that can be accommodated in the d-subshell?", "10", ["6", "14", "2"], "The d-subshell has 5 orbitals (l = 2), each holding 2 electrons: 5 * 2 = 10."),
        ("What type of intermolecular force is responsible for the unusually high boiling point of water?", "Hydrogen bonding", ["Dipole-dipole interaction", "London dispersion forces", "Ion-dipole forces"], "Strong hydrogen bonds between hydrogen and electronegative oxygen elevate water's boiling point."),
        ("What is the IUPAC name for Acetone (CH3-CO-CH3)?", "Propan-2-one", ["Propanal", "Propanoic acid", "2-Methylpropanone"], "Acetone is a 3-carbon ketone with carbonyl at C-2: propan-2-one."),
        ("Which gas is evolved during the electrolysis of molten NaCl at the anode?", "Chlorine gas (Cl2)", ["Hydrogen gas", "Oxygen gas", "Sodium vapor"], "At the anode (oxidation): 2Cl^- -> Cl2(g) + 2e^-."),
        ("What is the geometry of Sulfur Hexafluoride (SF6) according to VSEPR theory?", "Octahedral", ["Trigonal bipyramidal", "Square planar", "Tetrahedral"], "SF6 has 6 bonding pairs and 0 lone pairs on sulfur, giving an octahedral geometry."),
        ("Which law states that at constant temperature, pressure is inversely proportional to volume?", "Boyle's Law", ["Charles's Law", "Gay-Lussac's Law", "Dalton's Law"], "Boyle's Law: P1 * V1 = P2 * V2 at constant T."),
        ("What is the half-life of a first-order reaction with rate constant k = 0.0693 min^-1?", "10 minutes", ["5 minutes", "20 minutes", "1 minute"], "t_1/2 = 0.693 / k = 0.693 / 0.0693 = 10 minutes."),
        ("What is the oxidation state of Chromium in the dichromate ion (Cr2O7^2-)?", "+6", ["+3", "+7", "+5"], "2(Cr) + 7(-2) = -2 => 2Cr - 14 = -2 => 2Cr = 12 => Cr = +6."),
        ("Which functional group characterizes alcohols?", "-OH (Hydroxyl)", ["-CHO (Aldehyde)", "-COOH (Carboxylic)", "-NH2 (Amine)"], "Alcohols possess a hydroxyl group (-OH) covalently attached to a carbon atom."),
        ("The reaction between an acid and an alcohol in the presence of an acid catalyst produces:", "An Ester", ["An Ether", "An Aldehyde", "A Ketone"], "Fischer esterification: R-COOH + R'-OH -> R-COO-R' (Ester) + H2O."),
        ("What is the empirical formula of glucose (C6H12O6)?", "CH2O", ["C6H12O6", "CHO", "C2H4O2"], "Simplest whole-number ratio of 6:12:6 is 1:2:1 => CH2O."),
        ("Which alkali metal gives a golden-yellow flame in flame test?", "Sodium", ["Potassium", "Lithium", "Calcium"], "Sodium compounds impart a characteristic bright persistent yellow flame."),
        ("Which transition metal ion is responsible for the blue color of Fehling's solution?", "Cu^2+ (Copper(II))", ["Fe^3+", "Zn^2+", "Ni^2+"], "Alkaline copper(II) tartrate complex gives Fehling's solution its deep blue color."),
        ("What is the main constituent of Liquefied Petroleum Gas (LPG)?", "Butane and Propane", ["Methane and Ethane", "Carbon monoxide", "Hydrogen"], "LPG is composed primarily of propane (C3H8) and butane (C4H10)."),
        ("Which gas has the highest rate of diffusion according to Graham's Law?", "Hydrogen (H2)", ["Helium (He)", "Oxygen (O2)", "Methane (CH4)"], "Graham's Law: Rate is inversely proportional to sqrt(Molar Mass). H2 has lowest molar mass (2 g/mol)."),
        ("What is the conjugate acid of Ammonia (NH3)?", "NH4^+ (Ammonium ion)", ["NH2^-", "HNO3", "NH4OH"], "Conjugate acid forms by adding one proton (H+) to NH3 => NH4^+."),
        ("Which noble gas does NOT have 8 valence electrons?", "Helium (He)", ["Neon (Ne)", "Argon (Ar)", "Krypton (Kr)"], "Helium has an atomic number of 2 with a stable duet 1s^2 valence configuration."),
        ("What product is formed when ethene undergoes catalytic hydrogenation?", "Ethane", ["Ethyne", "Ethanol", "Methane"], "C2H4 + H2 (with Ni/Pt catalyst) -> C2H6 (Ethane)."),
        ("Which law relates the vapor pressure of a solvent to its mole fraction in solution?", "Raoult's Law", ["Henry's Law", "Dalton's Law", "Hess's Law"], "Raoult's Law: Partial vapor pressure P_A = P_A^0 * X_A."),
        ("What is the standard reduction potential of the standard hydrogen electrode (SHE)?", "0.00 Volts", ["1.00 Volt", "-1.00 Volt", "0.50 Volt"], "By IUPAC convention, the Standard Hydrogen Electrode (SHE) is assigned exactly 0.00 V at all temperatures."),
        ("The conversion of vegetable oil into solid vegetable ghee involves which process?", "Hydrogenation", ["Dehydrogenation", "Saponification", "Esterification"], "Hydrogenation of unsaturated fats using nickel catalyst converts them into saturated fats."),
        ("Which substance is used as a coagulant in the purification of drinking water?", "Potash Alum", ["Bleaching powder", "Common salt", "Baking powder"], "Alum hydrolyzes to form gelatinous Al(OH)3 that coagulates colloidal dirt particles.")
    ]
    for q, ca, wa, exp in chem_med:
        qs.append(make_q(q, ca, wa, "MEDIUM", exp))

    # --- HARD (33) ---
    chem_hard = [
        ("What is the standard cell potential (E_cell) for the Daniell cell (Zn + Cu^2+ -> Zn^2+ + Cu)?", "1.10 V", ["0.76 V", "0.34 V", "1.50 V"], "E_cell = E_cathode - E_anode = +0.34 V - (-0.76 V) = +1.10 V."),
        ("What is the bond order of O2^+ ion according to Molecular Orbital Theory?", "2.5", ["2.0", "3.0", "1.5"], "O2 has 16 electrons (BO = 2). Removing an antibonding pi* electron gives BO = (10 - 5)/2 = 2.5."),
        ("Which nucleophilic substitution mechanism proceeds with complete inversion of configuration (Walden inversion)?", "SN2", ["SN1", "E1", "E2"], "SN2 involves backside attack in a concerted bimolecular step, causing 100% inversion of stereochemistry."),
        ("What is the Crystal Field Stabilization Energy (CFSE) for a d6 low-spin octahedral complex?", "-2.4 Delta_o + 2P", ["-0.4 Delta_o", "-1.8 Delta_o", "-2.4 Delta_o"], "In low-spin d6, all 6 electrons occupy t2g orbitals: 6 * (-0.4) = -2.4 Delta_o + 2 pairing energies."),
        ("According to the Arrhenius equation, the slope of a plot of ln(k) versus 1/T is equal to:", "-E_a / R", ["E_a / R", "-E_a", "ln(A)"], "ln(k) = ln(A) - (E_a / R) * (1/T). The slope is -E_a / R."),
        ("Which of the following molecules has a zero dipole moment due to symmetric geometry?", "BF3 (Boron trifluoride)", ["NH3", "H2O", "SO2"], "BF3 is trigonal planar (120 deg); three equal B-F dipole vectors cancel completely."),
        ("What is the IUPAC name for K4[Fe(CN)6]?", "Potassium hexacyanidoferrate(II)", ["Potassium ferrocyanide", "Potassium ferricyanide", "Potassium hexacyanidoiron(III)"], "K4 gives [Fe(CN)6]^4-. Fe oxidation state: x - 6 = -4 => Fe(II). Ending is 'ferrate(II)'."),
        ("Cannizzaro reaction is given by aldehydes that have:", "No alpha-hydrogen atoms", ["At least one alpha-hydrogen", "An aromatic ring only", "A hydroxyl group"], "Aldehydes lacking alpha-hydrogens (e.g., benzaldehyde, formaldehyde) undergo self redox in conc. alkali."),
        ("What is the pH of a buffer containing 0.1 M acetic acid and 0.1 M sodium acetate (pKa = 4.76)?", "4.76", ["5.76", "3.76", "7.00"], "Henderson-Hasselbalch: pH = pKa + log([Salt]/[Acid]) = 4.76 + log(1) = 4.76."),
        ("Which rule governs the regioselectivity of electrophilic addition of HBr to unsymmetrical alkenes?", "Markovnikov's Rule", ["Saytzeff's Rule", "Hund's Rule", "Kornblum's Rule"], "Markovnikov's rule: Hydrogen adds to the double-bonded carbon bearing greater number of hydrogens."),
        ("Which law states that total enthalpy change of a reaction is independent of the pathway taken?", "Hess's Law", ["First Law of Thermodynamics", "Kirchhoff's Law", "Henry's Law"], "Hess's Law of Constant Heat Summation is a direct consequence of enthalpy being a state function."),
        ("What is the coordination number of iron in hemoglobin?", "6", ["4", "5", "8"], "Fe(II) in heme coordinates to 4 porphyrin nitrogens, 1 proximal histidine, and 1 O2 molecule."),
        ("What is the product of the reaction between an aldehyde and a Grignard reagent, followed by hydrolysis?", "Secondary alcohol", ["Primary alcohol", "Tertiary alcohol", "Ketone"], "RCHO + R'MgX -> R-CH(OH)-R' (Secondary alcohol). (Formaldehyde yields primary, ketones yield tertiary)."),
        ("What is the unit of the rate constant (k) for a second-order reaction?", "L mol^-1 s^-1", ["s^-1", "mol L^-1 s^-1", "mol^2 L^-2 s^-1"], "Rate = k [A]^2 => (mol L^-1 s^-1) / (mol^2 L^-2) = L mol^-1 s^-1."),
        ("The phenomenon where a substance shows increased solubility when fine particles are used is governed by:", "Ostwald-Freundlich Equation", ["Nernst Equation", "Gibbs-Duhem Equation", "Langmuir Adsorption"], "Smaller particle size increases surface curvature and chemical potential, enhancing solubility."),
        ("Which transition element has anomalous electronic configuration [Ar] 3d5 4s1?", "Chromium (Cr)", ["Copper (Cu)", "Manganese (Mn)", "Iron (Fe)"], "Cr (Z=24) has half-filled 3d5 4s1 configuration due to extra stability of half-filled d-subshell."),
        ("What is the magnetic behavior of an oxygen molecule (O2) in its ground state?", "Paramagnetic", ["Diamagnetic", "Ferromagnetic", "Antiferromagnetic"], "MOT reveals two unpaired electrons in antibonding pi* orbitals, making O2 paramagnetic."),
        ("In Lucas test for distinguishing alcohols, which alcohol produces immediate turbidity at room temp?", "Tertiary alcohol", ["Secondary alcohol", "Primary alcohol", "Methanol"], "Tertiary carbocations form instantly via SN1, yielding immediate insoluble alkyl chloride turbidity."),
        ("What is the coordination number in a Face-Centered Cubic (FCC) lattice?", "12", ["8", "6", "4"], "In an FCC lattice (cubic close packing), each sphere touches 12 nearest neighbors."),
        ("What is the packing efficiency of a Body-Centered Cubic (BCC) crystal lattice?", "68%", ["74%", "52.4%", "82%"], "BCC packing efficiency is sqrt(3)*pi / 8 ~ 68.02%."),
        ("What type of defect in ionic solids lowers the overall density of the crystal?", "Schottky defect", ["Frenkel defect", "Interstitial defect", "F-center defect"], "Schottky defect involves stoichiometric missing cation-anion pairs from lattice sites, lowering density."),
        ("The change in Gibbs free energy (delta G) at equilibrium for a reversible process is:", "Zero", ["Negative", "Positive", "Infinity"], "At equilibrium, delta G = 0; the system is at minimum free energy."),
        ("Which colloidal system represents a liquid dispersed in a solid?", "Gel", ["Sol", "Emulsion", "Aerosol"], "A gel consists of liquid dispersed medium trapped within a solid continuous network (e.g., cheese, jelly)."),
        ("What is the shape of Xenon Tetrafluoride (XeF4) according to VSEPR theory?", "Square planar", ["Tetrahedral", "Octahedral", "See-saw"], "Xe has 4 bonding pairs and 2 axial lone pairs (sp3d2), giving a square planar molecular geometry."),
        ("In the extraction of aluminum by Hall-Heroult process, cryolite (Na3AlF6) is added to:", "Lower melting point and increase conductivity", ["Act as oxidizing agent", "Prevent anode corrosion", "Remove iron impurities"], "Pure Al2O3 melts at >2000°C; cryolite reduces melting point to ~950°C and increases ionic conductivity."),
        ("What is the monomer of Natural Rubber?", "Isoprene (2-methyl-1,3-butadiene)", ["Chloroprene", "Styrene", "Butadiene"], "Natural rubber is cis-1,4-polyisoprene derived from the monomer isoprene."),
        ("Which reagent is used to detect presence of peptide bonds in proteins?", "Biuret reagent", ["Fehling solution", "Tollens reagent", "Barfoed reagent"], "Biuret test gives a violet-purple coordination complex with peptide bonds in alkaline Cu2+ solution."),
        ("What is the thermodynamic criterion for spontaneity of a process at constant T and P?", "delta G < 0", ["delta H < 0", "delta S < 0", "delta G > 0"], "A process is thermodynamically spontaneous when Gibbs free energy change delta G is strictly negative."),
        ("Which carbohydrate does NOT reduce Tollens or Fehling solution?", "Sucrose", ["Glucose", "Fructose", "Maltose"], "Sucrose is a non-reducing disaccharide because both anomeric carbons are locked in glycosidic linkage."),
        ("What is the primary product of ozonolysis of 2-butene followed by Zn/H2O workup?", "Acetaldehyde (CH3CHO)", ["Formaldehyde", "Acetone", "Acetic acid"], "Cleavage of symmetrical CH3-CH=CH-CH3 yields two molecules of acetaldehyde (ethanal)."),
        ("What is the effect of a positive catalyst on the activation energy and delta H of a reaction?", "Lowers activation energy, leaves delta H unchanged", ["Lowers both", "Increases delta H", "Increases activation energy"], "A catalyst provides an alternate pathway with lower activation energy; state function delta H is unaffected."),
        ("Which lanthanoid ion is diamagnetic in its +3 oxidation state?", "Lu^3+ (Lutetium)", ["Ce^3+", "Gd^3+", "Eu^3+"], "Lu (Z=71) has [Xe] 4f14 5d1 6s2. Lu^3+ has completely filled 4f14 shell with no unpaired electrons."),
        ("What is the IUPAC name for Picric acid?", "2,4,6-Trinitrophenol", ["2,4-Dinitrophenol", "Trinitrotoluene", "3,5-Dinitrobenzoic acid"], "Nitration of phenol yields 2,4,6-trinitrophenol, commonly known as picric acid.")
    ]
    for q, ca, wa, exp in chem_hard:
        qs.append(make_q(q, ca, wa, "HARD", exp))

    return qs


# ==========================================
# 4. BIOLOGY
# ==========================================
def get_biology_questions():
    qs = []
    
    # --- EASY (34) ---
    bio_easy = [
        ("Which cell organelle is known as the 'Powerhouse of the Cell'?", "Mitochondria", ["Ribosome", "Nucleus", "Golgi apparatus"], "Mitochondria generate cellular energy in the form of ATP via aerobic respiration."),
        ("What is the primary green pigment in plants responsible for photosynthesis?", "Chlorophyll", ["Carotenoid", "Anthocyanin", "Xanthophyll"], "Chlorophyll traps light energy to drive the photosynthetic conversion of CO2 and water into glucose."),
        ("Which blood cells are responsible for carrying oxygen throughout the human body?", "Red Blood Cells (Erythrocytes)", ["White Blood Cells", "Platelets", "Lymphocytes"], "Hemoglobin inside erythrocytes binds oxygen in the lungs and releases it into tissues."),
        ("What is the normal human body temperature in Celsius?", "37 degrees C", ["35 degrees C", "39 degrees C", "98.6 degrees C"], "Normal core body temperature is approximately 37°C (98.6°F)."),
        ("Which human organ filters metabolic waste from blood to produce urine?", "Kidney", ["Liver", "Pancreas", "Spleen"], "The paired kidneys filter blood through nephrons to excrete urea, excess salts, and water."),
        ("What is the basic structural and functional unit of all living organisms?", "Cell", ["Tissue", "Organ", "Molecule"], "Cell theory states that all organisms are composed of one or more cells, the fundamental unit of life."),
        ("Which macromolecule carries the primary genetic instructions in living organisms?", "DNA (Deoxyribonucleic acid)", ["RNA", "Protein", "Lipid"], "DNA contains genetic code organized in nucleotide base sequences."),
        ("What is the process by which green plants synthesize food using sunlight?", "Photosynthesis", ["Respiration", "Transpiration", "Fermentation"], "Photosynthesis uses light, CO2, and water to produce glucose and oxygen."),
        ("How many chambers does a normal human heart possess?", "4", ["2", "3", "5"], "The human heart has 4 chambers: right and left atria, and right and left ventricles."),
        ("Which vitamin is synthesized in human skin upon exposure to sunlight?", "Vitamin D", ["Vitamin A", "Vitamin C", "Vitamin K"], "UVB radiation converts 7-dehydrocholesterol in the epidermis into cholecalciferol (Vitamin D3)."),
        ("Deficiency of which mineral leads to simple goitre (swelling of thyroid)?", "Iodine", ["Iron", "Calcium", "Phosphorus"], "Iodine is a necessary structural component of thyroid hormones thyroxine (T4) and triiodothyronine (T3)."),
        ("Which component of human blood is essential for blood clotting?", "Platelets (Thrombocytes)", ["Red Blood Cells", "Plasma", "Hemoglobin"], "Platelets adhere to damaged endothelium and initiate the coagulation cascade."),
        ("What is the largest internal organ in the human body?", "Liver", ["Brain", "Heart", "Lungs"], "The liver is the heaviest internal organ (~1.5 kg) and performs over 500 metabolic functions."),
        ("Which tissue in plants conducts water and dissolved minerals from roots to leaves?", "Xylem", ["Phloem", "Cambium", "Collenchyma"], "Xylem vessels and tracheids transport water and minerals unidirectionally upwards."),
        ("Which tissue transports organic nutrients (sugars) synthesized in leaves to other plant parts?", "Phloem", ["Xylem", "Cortex", "Epidermis"], "Phloem sieve tubes and companion cells conduct photosynthates bidirectionally."),
        ("Deficiency of Vitamin C causes which disease?", "Scurvy", ["Rickets", "Beriberi", "Night blindness"], "Scurvy causes bleeding gums, skin spots, and poor wound healing due to defective collagen synthesis."),
        ("Deficiency of Vitamin A leads to which vision disorder?", "Night blindness (Nyctalopia)", ["Color blindness", "Cataract", "Myopia"], "Vitamin A (retinol) is a precursor for rhodopsin in retinal rod cells."),
        ("Which organ in the human digestive system secretes insulin and glucagon?", "Pancreas", ["Liver", "Gallbladder", "Stomach"], "Islets of Langerhans in the pancreas secrete insulin (beta cells) and glucagon (alpha cells)."),
        ("What is the primary site of nutrient absorption in the human digestive tract?", "Small intestine", ["Stomach", "Large intestine", "Esophagus"], "The small intestine has millions of microvilli that create massive surface area for absorption."),
        ("Which kingdom of organisms includes mushrooms and yeasts?", "Fungi", ["Plantae", "Protista", "Monera"], "Fungi are eukaryotic heterotrophs with chitinous cell walls."),
        ("What is the chemical substance that speeds up biological reactions without being consumed?", "Enzyme", ["Hormone", "Vitamin", "Antibody"], "Enzymes are biocatalysts (mostly proteins) that lower activation energy of biochemical pathways."),
        ("Which gas is inhaled for cellular respiration and used to oxidize glucose?", "Oxygen", ["Carbon dioxide", "Nitrogen", "Methane"], "Oxygen serves as the terminal electron acceptor in the mitochondrial electron transport chain."),
        ("What is the universal donor blood group in the ABO system?", "O negative", ["AB positive", "A positive", "B negative"], "O negative red cells lack A, B, and Rh antigens, minimizing risk of hemolytic transfusion reactions."),
        ("What is the universal recipient blood group in the ABO system?", "AB positive", ["O negative", "A positive", "B positive"], "AB positive plasma lacks anti-A, anti-B, and anti-Rh antibodies."),
        ("The genetic makeup of an organism is known as its:", "Genotype", ["Phenotype", "Karyotype", "Allele"], "Genotype refers to the specific alleles carried; phenotype refers to observable physical traits."),
        ("Who is universally recognized as the 'Father of Genetics'?", "Gregor Mendel", ["Charles Darwin", "Louis Pasteur", "Robert Hooke"], "Mendel uncovered fundamental laws of inheritance through breeding experiments on garden peas."),
        ("Which organelle is responsible for protein synthesis in the cell?", "Ribosome", ["Lysosome", "Vacuole", "Centrosome"], "Ribosomes translate mRNA codons into polypeptide amino acid chains."),
        ("What is the enzyme found in human saliva that initiates starch digestion?", "Salivary Amylase (Ptyalin)", ["Pepsin", "Trypsin", "Lipase"], "Salivary amylase breaks dietary starch down into maltose and dextrins in the mouth."),
        ("Which insect is the vector for transmitting Malaria parasites to humans?", "Female Anopheles mosquito", ["Male Anopheles", "Aedes aegypti", "Culex mosquito"], "Female Anopheles mosquitoes transmit Plasmodium sporozoites while taking blood meals."),
        ("What is the process of cell division that produces identical somatic daughter cells?", "Mitosis", ["Meiosis", "Binary fission", "Budding"], "Mitosis produces two diploid daughter cells genetically identical to the parent cell."),
        ("What is the process of reductional cell division that produces haploid gametes?", "Meiosis", ["Mitosis", "Amitosis", "Fertilization"], "Meiosis halves chromosome number from diploid (2n) to haploid (n) in germ cells."),
        ("Which organ stores bile produced by the liver before releasing it into duodenum?", "Gallbladder", ["Pancreas", "Stomach", "Appendix"], "The gallbladder concentrates and stores bile until stimulated to contract by cholecystokinin (CCK)."),
        ("What is the tough fibrous band of connective tissue that connects muscle to bone?", "Tendon", ["Ligament", "Cartilage", "Fascia"], "Tendons connect muscle to bone; ligaments connect bone to bone."),
        ("Which hormone is commonly known as the 'Emergency' or 'Fight-or-Flight' hormone?", "Adrenaline (Epinephrine)", ["Thyroxine", "Insulin", "Estrogen"], "Adrenaline from the adrenal medulla increases heart rate, blood pressure, and blood glucose in stress.")
    ]
    for q, ca, wa, exp in bio_easy:
        qs.append(make_q(q, ca, wa, "EASY", exp))

    # --- MEDIUM (33) ---
    bio_med = [
        ("During which phase of mitosis do duplicated chromosomes align at the cell's equatorial plane?", "Metaphase", ["Prophase", "Anaphase", "Telophase"], "During metaphase, spindle fibers attach to kinetochores and align chromosomes on the metaphase plate."),
        ("What is the structural and functional filtration unit of the human kidney?", "Nephron", ["Neuron", "Glomerulus", "Alveolus"], "Each human kidney contains roughly 1 million nephrons that filter blood and form urine."),
        ("What is the phenotypic ratio in the F2 generation of a Mendelian monohybrid cross?", "3 : 1", ["9 : 3 : 3 : 1", "1 : 2 : 1", "1 : 1"], "A cross between heterozygous Tt parents yields 3 dominant phenotype : 1 recessive phenotype."),
        ("What is the genotypic ratio in the F2 generation of a Mendelian monohybrid cross?", "1 : 2 : 1", ["3 : 1", "9 : 3 : 3 : 1", "2 : 1 : 1"], "Genotypic composition is 1 TT : 2 Tt : 1 tt."),
        ("Which hormone lowers blood glucose concentration by facilitating glucose uptake into cells?", "Insulin", ["Glucagon", "Cortisol", "Thyroxine"], "Beta cells of pancreatic islets secrete insulin to lower circulating blood sugar levels."),
        ("Which hormone elevates blood glucose by stimulating glycogenolysis in the liver?", "Glucagon", ["Insulin", "Prolactin", "Calcitonin"], "Alpha cells secrete glucagon when blood glucose is low to break down stored glycogen into glucose."),
        ("In DNA, adenine pairs with thymine via how many hydrogen bonds?", "Two hydrogen bonds", ["Three hydrogen bonds", "One hydrogen bond", "Four hydrogen bonds"], "A=T base pairs share 2 hydrogen bonds; G-C base pairs share 3 hydrogen bonds."),
        ("In RNA, which pyrimidine nitrogenous base replaces Thymine?", "Uracil", ["Cytosine", "Guanine", "Adenine"], "RNA contains Uracil (U) instead of Thymine (T) found in DNA."),
        ("What is the primary site of gaseous exchange in the human respiratory system?", "Alveoli", ["Bronchi", "Trachea", "Larynx"], "Alveolar sacs with capillary networks provide massive surface area for O2/CO2 diffusion."),
        ("Which part of the human brain controls involuntary vital functions like respiration and heart rate?", "Medulla oblongata", ["Cerebrum", "Cerebellum", "Hypothalamus"], "The brainstem's medulla oblongata houses cardiovascular and respiratory control centers."),
        ("Which part of the brain is primarily responsible for motor coordination and balance?", "Cerebellum", ["Cerebrum", "Medulla", "Thalamus"], "The cerebellum integrates sensory inputs to fine-tune posture, balance, and voluntary motor movements."),
        ("What is the term for the loss of water in the form of vapor through stomata of plant leaves?", "Transpiration", ["Guttation", "Exudation", "Osmosis"], "Transpiration creates negative suction pressure (transpiration pull) that drives xylem sap upward."),
        ("Which plant growth hormone promotes cell elongation and is responsible for phototropism?", "Auxin", ["Gibberellin", "Cytokinin", "Abscisic acid"], "Auxins accumulate on the shaded side of shoot tips, stimulating elongation and bending toward light."),
        ("Which gaseous plant hormone is primarily responsible for the ripening of fleshy fruits?", "Ethylene", ["Auxin", "Cytokinin", "Abscisic acid"], "Ethylene gas (C2H4) accelerates fruit ripening, abscission, and senescence."),
        ("Which plant hormone is known as the 'stress hormone' that induces stomatal closure during drought?", "Abscisic Acid (ABA)", ["Auxin", "Gibberellic acid", "Cytokinin"], "ABA signals guard cells to lose turgor and close stomatal pores under water stress."),
        ("What is the normal blood pressure of a healthy adult human?", "120 / 80 mmHg", ["140 / 90 mmHg", "100 / 60 mmHg", "80 / 120 mmHg"], "120 mmHg represents systolic pressure (ventricular contraction); 80 mmHg represents diastolic pressure."),
        ("The light reactions of photosynthesis occur within which part of the chloroplast?", "Thylakoid membranes (Grana)", ["Stroma", "Outer membrane", "Intermembrane space"], "Chlorophyll pigments embedded in thylakoid membranes absorb light to drive photolysis and ATP synthesis."),
        ("The light-independent reactions (Calvin cycle) of photosynthesis take place in the:", "Stroma", ["Thylakoids", "Grana", "Lumen"], "Enzymatic fixation of CO2 into carbohydrates occurs in the fluid-filled stroma of chloroplasts."),
        ("Which type of white blood cells produce specific antibodies against pathogens?", "B lymphocytes (B cells)", ["T lymphocytes", "Neutrophils", "Monocytes"], "Plasma cells differentiated from activated B lymphocytes secrete targeted immunoglobulin antibodies."),
        ("In the human eye, which layer contains photoreceptor rod and cone cells?", "Retina", ["Cornea", "Choroid", "Sclera"], "The retina transduces light stimuli into action potentials transmitted via optic nerve."),
        ("Which photoreceptor cells in the human retina are responsible for daylight and color vision?", "Cones", ["Rods", "Bipolar cells", "Ganglion cells"], "Cones function in bright light and mediate high-acuity color vision (red, green, blue opsins)."),
        ("What is the master endocrine gland that controls most other endocrine glands in the human body?", "Pituitary gland", ["Thyroid gland", "Adrenal gland", "Thymus gland"], "The hypophysis (pituitary) secretes trophic hormones (TSH, ACTH, FSH, LH, GH) under hypothalamic control."),
        ("What is the 10% law of energy transfer in an ecological food chain formulated by Lindeman?", "Only ~10% of energy is transferred to next trophic level", ["90% of energy is transferred", "Energy remains constant", "10% of energy is lost as heat"], "Roughly 90% of captured energy is consumed by metabolic maintenance or lost as heat at each trophic level."),
        ("What is the causative agent of Tuberculosis (TB)?", "Mycobacterium tuberculosis (Bacteria)", ["Virus", "Plasmodium", "Fungus"], "Tuberculosis is an infectious bacterial disease caused by Mycobacterium tuberculosis."),
        ("Which enzyme in the human stomach initiates the digestion of dietary proteins?", "Pepsin", ["Amylase", "Lipase", "Trypsin"], "Chief cells secrete pepsinogen, activated by stomach HCl into active proteolytic pepsin."),
        ("What is the structural protein found in human hair, nails, and outer skin layer?", "Keratin", ["Collagen", "Myosin", "Actin"], "Keratin is an insoluble fibrous protein providing mechanical durability and water barrier."),
        ("What is the most abundant structural protein in the human body (found in connective tissue)?", "Collagen", ["Keratin", "Albumin", "Hemoglobin"], "Collagen constitutes roughly 25-35% of total body protein content, providing tensile strength to tissues."),
        ("In human females, fertilization of the ovum by sperm typically occurs in which organ?", "Fallopian tube (Ampulla)", ["Uterus", "Ovary", "Cervix"], "Fertilization normally takes place in the ampullary region of the fallopian tube (oviduct)."),
        ("What is the primary function of the Loop of Henle in the mammalian nephron?", "Concentration of urine via counter-current multiplier", ["Filtration of proteins", "Secretion of bile", "Absorption of glucose only"], "The Loop of Henle creates a hyperosmotic medullary gradient that drives water reabsorption from collecting ducts."),
        ("Which chamber of the human heart pumps oxygenated blood into the aorta for systemic circulation?", "Left ventricle", ["Right ventricle", "Left atrium", "Right atrium"], "The thick muscular left ventricle ejects oxygenated blood under high pressure into the systemic aorta."),
        ("In the ABO blood system, which alleles show codominance?", "Alleles I^A and I^B", ["Alleles I^A and i", "Alleles I^B and i", "All alleles"], "When both I^A and I^B alleles are inherited, both A and B glycoproteins are expressed on erythrocytes (AB blood)."),
        ("The process of breakdown of glucose into pyruvate in the cytoplasm is called:", "Glycolysis", ["Krebs cycle", "Electron transport", "Fermentation"], "Glycolysis converts 1 glucose into 2 pyruvate molecules, yielding a net 2 ATP and 2 NADH without requiring O2."),
        ("Where in the eukaryotic cell does the Krebs cycle (Citric Acid Cycle) take place?", "Mitochondrial matrix", ["Cytoplasm", "Mitochondrial cristae", "Endoplasmic reticulum"], "Pyruvate enters the mitochondrion; acetyl-CoA oxidation via the Krebs cycle occurs in the inner matrix.")
    ]
    for q, ca, wa, exp in bio_med:
        qs.append(make_q(q, ca, wa, "MEDIUM", exp))

    # --- HARD (33) ---
    bio_hard = [
        ("What is the primary CO2 acceptor molecule in the C3 photosynthetic pathway (Calvin cycle)?", "RuBP (Ribulose 1,5-bisphosphate)", ["PEP (Phosphoenolpyruvate)", "OAA (Oxaloacetate)", "PGA (3-phosphoglycerate)"], "RuBisCO catalyzes the carboxylation of the 5-carbon sugar RuBP with CO2 to form two 3-PGA molecules."),
        ("What is the primary CO2 acceptor in C4 plants (e.g., maize, sugarcane) located in mesophyll cells?", "Phosphoenolpyruvate (PEP)", ["RuBP", "Oxaloacetate", "Malate"], "PEP carboxylase fixes CO2 into PEP to produce 4-carbon oxaloacetic acid in mesophyll cells."),
        ("The classical experiment proving semiconservative replication of DNA using 15N was performed by:", "Meselson and Stahl", ["Hershey and Chase", "Watson and Crick", "Griffith"], "Matthew Meselson and Franklin Stahl (1958) used equilibrium density gradient centrifugation with heavy nitrogen."),
        ("Which immunoglobulin (antibody) is the ONLY one capable of crossing the human placenta to confer immunity?", "IgG", ["IgA", "IgM", "IgE"], "IgG is the most abundant serum antibody and the only isotype transported across the placenta via FcRn receptors."),
        ("Which immunoglobulin is prominently present in human colostrum and body secretions (saliva, tears)?", "Secretory IgA", ["IgG", "IgD", "IgE"], "Dimeric IgA with secretory component protects mucosal surfaces from pathogen attachment."),
        ("During generation of an action potential in a neuron, depolarization is caused by:", "Rapid influx of Sodium ions (Na+)", ["Efflux of Potassium ions", "Influx of Chloride ions", "Active efflux of Calcium ions"], "Opening of voltage-gated Na+ channels allows explosive entry of Na+ down its electrochemical gradient."),
        ("Repolarization of a neuronal membrane following an action potential is primarily driven by:", "Efflux of Potassium ions (K+)", ["Influx of Sodium ions", "Entry of Calcium ions", "Closure of all channels"], "Voltage-gated K+ channels open, allowing K+ ions to exit the cell, restoring the negative resting membrane potential."),
        ("What is the resting membrane potential of a typical mammalian neuron?", "-70 mV", ["+30 mV", "0 mV", "-90 mV"], "Maintained by the Na+/K+ ATPase pump and K+ leak channels, typical resting potential is ~ -70 millivolts."),
        ("In the lac operon of E. coli, lactose acts as:", "An Inducer", ["A Corepressor", "An Activator", "An Inhibitor"], "Allolactose binds the lac repressor protein, causing conformational change that releases it from the operator."),
        ("Which enzyme synthesizes DNA from an RNA template in retroviruses like HIV?", "Reverse Transcriptase", ["DNA Polymerase I", "RNA Polymerase II", "Taq Polymerase"], "RNA-dependent DNA polymerase (Reverse Transcriptase) transcribes viral single-stranded RNA into double-stranded DNA."),
        ("What is the start codon in the standard genetic code, which also codes for Methionine?", "AUG", ["UAA", "UAG", "UGA"], "AUG is the universal initiation codon for protein translation."),
        ("Which of the following triplets acts as a stop (nonsense) codon in translation?", "UAA, UAG, and UGA", ["AUG, CUG, and GUG", "AAA, UUU, and GGG", "UAU, UAC, and UGG"], "UAA (ochre), UAG (amber), and UGA (opal) signal termination of polypeptide chain synthesis."),
        ("The restriction enzyme EcoRI cleaves DNA at which palindromic recognition sequence?", "5'-GAATTC-3'", ["5'-GGATCC-3'", "5'-AAGCTT-3'", "5'-CTGCAG-3'"], "EcoRI recognizes 5'-G|AATTC-3' and produces complementary 4-nucleotide sticky ends."),
        ("During which stage of prophase I in meiosis does genetic crossing over (chiasma formation) occur?", "Pachytene", ["Leptotene", "Zygotene", "Diplotene"], "Non-sister chromatids of homologous chromosomes exchange genetic material during pachytene."),
        ("The synaptonemal complex between homologous chromosomes forms during which meiotic stage?", "Zygotene", ["Leptotene", "Pachytene", "Diakinesis"], "Synapsis of homologous chromosomes and assembly of the synaptonemal complex occurs in zygotene."),
        ("What is the role of surfactant produced by type II alveolar cells in human lungs?", "Reduces surface tension to prevent alveolar collapse", ["Kills bacteria", "Increases mucus secretion", "Supplies oxygen"], "Pulmonary surfactant (dipalmitoylphosphatidylcholine) lowers surface tension at the air-water interface."),
        ("Which hormone triggers the rupture of the Graafian follicle and ovulation in human females?", "Luteinizing Hormone (LH surge)", ["Follicle Stimulating Hormone", "Progesterone", "Prolactin"], "A sharp mid-cycle LH surge triggers final oocyte maturation and follicle rupture (ovulation)."),
        ("After ovulation, the ruptured ovarian follicle transforms into which temporary endocrine structure?", "Corpus luteum", ["Corpus albicans", "Corona radiata", "Zona pellucida"], "The corpus luteum secretes high levels of progesterone to maintain the endometrium for implantation."),
        ("In which part of the human kidney are the glomeruli and Bowman's capsules located?", "Renal cortex", ["Renal medulla", "Renal pelvis", "Renal calyx"], "The renal corpuscles (Bowman's capsule + glomerulus) and convoluted tubules are confined to the cortex."),
        ("Juxtaglomerular apparatus (JGA) cells secrete which enzyme in response to low renal blood pressure?", "Renin", ["Erythropoietin", "Angiotensin", "Aldosterone"], "Renin initiates the RAAS pathway (converting angiotensinogen to angiotensin I) to restore blood pressure."),
        ("Which hormone stimulates reabsorption of Na+ and water from renal distal tubules in the RAAS system?", "Aldosterone", ["Atrial Natriuretic Peptide", "Oxytocin", "Calcitonin"], "Aldosterone from the adrenal cortex promotes sodium retention and potassium excretion in distal nephrons."),
        ("What is the term for the irreversible binding of myosin heads to actin in dead muscle (rigor mortis)?", "Depletion of ATP", ["Excess calcium accumulation", "Accumulation of lactic acid", "Enzyme breakdown"], "Without ATP, myosin cross-bridges cannot detach from actin filaments, causing sustained muscle rigidity."),
        ("The sliding filament theory of muscle contraction was proposed by:", "H.E. Huxley and A.F. Huxley", ["Watson and Crick", "Robert Brown", "Singer and Nicolson"], "Huxley and colleagues proposed that actin and myosin filaments slide past each other without shortening."),
        ("What is the Fluid Mosaic Model of cell membrane structure proposed by Singer and Nicolson (1972)?", "Lipid bilayer with embedded mobile proteins", ["Solid protein layer with lipids inside", "Protein-lipid-protein sandwich", "Pure carbohydrate lattice"], "The plasma membrane is a quasi-fluid phospholipid bilayer with embedded and peripheral proteins."),
        ("Which cellular junction provides direct cytoplasmic communication channels between adjacent animal cells?", "Gap junctions", ["Tight junctions", "Desmosomes", "Hemidesmosomes"], "Connexon protein channels form gap junctions facilitating direct intercellular transfer of ions and small molecules."),
        ("The enzyme nitrogenase, responsible for biological nitrogen fixation in Rhizobium, is highly sensitive to:", "Oxygen (O2)", ["Carbon dioxide", "Nitrogen", "Hydrogen"], "Nitrogenase is irreversibly inactivated by O2; leghemoglobin acts as an oxygen scavenger to maintain anoxia."),
        ("What is the primary role of tRNA in protein translation?", "Carrying specific amino acids to the ribosome", ["Transcribing DNA", "Forming ribosomal structure", "Degrading unneeded proteins"], "tRNA molecules have an anticodon loop complementary to mRNA and an acceptor stem charged with the corresponding amino acid."),
        ("Which type of natural selection favors individuals at both extremes of a phenotypic distribution?", "Disruptive selection", ["Stabilizing selection", "Directional selection", "Artificial selection"], "Disruptive selection selects against intermediate phenotypes, potentially splitting a population into two distinct morphs."),
        ("The Hardy-Weinberg equilibrium principle states that allele frequencies in a population remain constant if:", "No mutation, selection, migration, or genetic drift occur", ["Population is small", "Mating is non-random", "Natural selection is strong"], "Genetic equilibrium requires a large, randomly mating diploid population with absence of evolutionary forces."),
        ("What is the key difference between Gram-positive and Gram-negative bacterial cell walls?", "Gram-positive has a thick peptidoglycan layer without outer membrane", ["Gram-negative has thicker peptidoglycan", "Gram-positive has lipopolysaccharides", "Gram-negative lacks cell wall"], "Gram-positive walls feature thick multilayered peptidoglycan and teichoic acids; Gram-negative have thin peptidoglycan and an outer lipid membrane."),
        ("Which technique amplifies specific segments of DNA exponentially using Taq DNA polymerase?", "Polymerase Chain Reaction (PCR)", ["Gel Electrophoresis", "Western Blotting", "ELISA"], "Kary Mullis invented PCR, which uses cycles of thermal denaturation, primer annealing, and extension."),
        ("Why is Taq polymerase chosen for Polymerase Chain Reaction (PCR)?", "It is thermostable at high temperatures (~95 deg C)", ["It replicates RNA", "It has proofreading only", "It is derived from human cells"], "Isolated from thermophilic bacterium Thermus aquaticus, it resists repeated denaturation steps at 95°C."),
        ("In the human auditory system, the organ of Corti containing sensory hair cells is located on the:", "Basilar membrane inside cochlea", ["Tympanic membrane", "Tectorial membrane alone", "Eustachian tube"], "The organ of Corti sits upon the basilar membrane within the cochlea and converts acoustic vibrations into nerve impulses.")
    ]
    for q, ca, wa, exp in bio_hard:
        qs.append(make_q(q, ca, wa, "HARD", exp))

    return qs
