from django.core.management.base import BaseCommand
from quiz.models import Question, Choice, Subject
from django.db import transaction

QUESTIONS = [
    # Mathematics (30)
    ("The sum of the first n terms of an arithmetic progression is given by S_n. The nth term is given by:", [("S_n - S_{n-1}", True), ("S_n + S_{n-1}", False), ("S_n / n", False), ("S_n - S_{n-2}", False)]),
    ("For what value of k are the roots of the quadratic equation x^2 + kx + 4 = 0 equal?", [("k = ±4", True), ("k = 2", False), ("k = -2", False), ("k = 0", False)]),
    ("The modulus of the complex number z = 3 + 4i is:", [("5", True), ("7", False), ("1", False), ("25", False)]),
    ("If A and B are two sets such that n(A) = 3 and n(B) = 6, then what is the minimum number of elements in A U B?", [("6", True), ("3", False), ("9", False), ("0", False)]),
    ("The value of lim (x->0) (sin x)/x is:", [("1", True), ("0", False), ("Infinity", False), ("Undefined", False)]),
    ("What is the derivative of x^x with respect to x?", [("x^x(1 + ln x)", True), ("x^x", False), ("x*x^(x-1)", False), ("x^x ln x", False)]),
    ("The integral of sec^2(x) dx is:", [("tan(x) + C", True), ("sec(x)tan(x) + C", False), ("ln|sec(x)| + C", False), ("cot(x) + C", False)]),
    ("If a vector has direction angles α, β, and γ, then cos^2(α) + cos^2(β) + cos^2(γ) is equal to:", [("1", True), ("0", False), ("2", False), ("3", False)]),
    ("The eccentricity of a parabola is:", [("1", True), ("0", False), ("Less than 1", False), ("Greater than 1", False)]),
    ("In how many ways can 5 distinct books be arranged on a shelf?", [("120", True), ("24", False), ("25", False), ("5", False)]),
    ("The probability of getting a sum of 9 when two dice are rolled is:", [("1/9", True), ("1/12", False), ("1/6", False), ("1/36", False)]),
    ("The variance of the first n natural numbers is:", [("(n^2 - 1)/12", True), ("(n^2 + 1)/12", False), ("n(n+1)/2", False), ("(n^2 - 1)/6", False)]),
    ("What is the principal value of sin^-1(-1/2)?", [("-π/6", True), ("π/6", False), ("5π/6", False), ("7π/6", False)]),
    ("The equation of the circle with center (0,0) and radius r is:", [("x^2 + y^2 = r^2", True), ("x^2 - y^2 = r^2", False), ("x^2 + y^2 = r", False), ("x + y = r^2", False)]),
    ("The determinant of the identity matrix I_n is:", [("1", True), ("n", False), ("0", False), ("n!", False)]),
    ("If A is an invertible matrix, then det(A^-1) is equal to:", [("1/det(A)", True), ("det(A)", False), ("-det(A)", False), ("0", False)]),
    ("The number of subsets of a set containing n elements is:", [("2^n", True), ("n^2", False), ("2n", False), ("n!", False)]),
    ("What is the 10th term of the arithmetic progression 2, 5, 8, 11, ...?", [("29", True), ("32", False), ("26", False), ("35", False)]),
    ("The distance between the parallel lines ax+by+c1=0 and ax+by+c2=0 is:", [("|c1 - c2|/√(a^2+b^2)", True), ("|c1 + c2|/√(a^2+b^2)", False), ("|c1 - c2|/(a+b)", False), ("0", False)]),
    ("The fundamental period of the function f(x) = sin(x) is:", [("2π", True), ("π", False), ("π/2", False), ("4π", False)]),
    ("Which of the following functions is neither even nor odd?", [("e^x", True), ("x^2", False), ("sin(x)", False), ("cos(x)", False)]),
    ("The maximum value of 3sin(x) + 4cos(x) is:", [("5", True), ("7", False), ("1", False), ("12", False)]),
    ("A matrix is skew-symmetric if:", [("A^T = -A", True), ("A^T = A", False), ("det(A) = 0", False), ("A = A^-1", False)]),
    ("The area of a triangle with vertices (0,0), (a,0), and (0,b) is:", [("1/2 |ab|", True), ("|ab|", False), ("1/2 (a+b)", False), ("ab", False)]),
    ("The binomial expansion of (x+y)^n has how many terms?", [("n+1", True), ("n", False), ("n-1", False), ("2n", False)]),
    ("The locus of a point whose distance from a fixed point is constant is a:", [("Circle", True), ("Line", False), ("Parabola", False), ("Ellipse", False)]),
    ("What is the product of the roots of the equation ax^2 + bx + c = 0?", [("c/a", True), ("-b/a", False), ("-c/a", False), ("b/a", False)]),
    ("The value of log_a(a) is:", [("1", True), ("0", False), ("a", False), ("Undefined", False)]),
    ("A continuous function f(x) defined on a closed interval [a,b] attains its maximum and minimum values on the interval. This is stated by:", [("Extreme Value Theorem", True), ("Mean Value Theorem", False), ("Rolle's Theorem", False), ("Intermediate Value Theorem", False)]),
    ("The integral of e^x dx is:", [("e^x + C", True), ("xe^{x-1} + C", False), ("ln(x) + C", False), ("e^{x+1}/(x+1) + C", False)]),

    # Physics (30)
    ("A particle of mass m is moving with velocity v. Its kinetic energy is:", [("1/2 mv^2", True), ("mv^2", False), ("1/2 mv", False), ("mv", False)]),
    ("According to Newton's Law of Cooling, the rate of cooling of a body is proportional to:", [("The temperature difference between the body and its surroundings", True), ("The temperature of the body", False), ("The mass of the body", False), ("The specific heat capacity of the body", False)]),
    ("The moment of inertia of a solid sphere of mass M and radius R about its diameter is:", [("2/5 MR^2", True), ("2/3 MR^2", False), ("1/2 MR^2", False), ("MR^2", False)]),
    ("In a uniform circular motion, the acceleration is directed:", [("Towards the center of the circle", True), ("Along the tangent", False), ("Away from the center", False), ("Upwards", False)]),
    ("The first law of thermodynamics is a statement of:", [("Conservation of Energy", True), ("Conservation of Mass", False), ("Conservation of Momentum", False), ("Conservation of Charge", False)]),
    ("What is the SI unit of electric dipole moment?", [("Coulomb-meter (C·m)", True), ("Coulomb (C)", False), ("Volt-meter (V·m)", False), ("Farad-meter (F·m)", False)]),
    ("The magnetic field at the center of a circular loop of radius R carrying current I is:", [("μ0*I / (2R)", True), ("μ0*I / (2πR)", False), ("μ0*I*R / 2", False), ("Zero", False)]),
    ("According to Gauss's Law in electrostatics, the total electric flux through a closed surface is equal to:", [("q/ε0", True), ("q*ε0", False), ("0", False), ("q", False)]),
    ("The equivalent resistance of two resistors R1 and R2 connected in parallel is:", [("(R1*R2)/(R1+R2)", True), ("R1+R2", False), ("(R1+R2)/(R1*R2)", False), ("R1-R2", False)]),
    ("In an LCR series AC circuit, resonance occurs when:", [("X_L = X_C", True), ("R = X_L", False), ("R = X_C", False), ("Z = 0", False)]),
    ("The phenomenon of bending of light around the corners of an obstacle is called:", [("Diffraction", True), ("Interference", False), ("Polarization", False), ("Dispersion", False)]),
    ("In Young's Double Slit Experiment, the fringe width is given by:", [("λD/d", True), ("λd/D", False), ("dD/λ", False), ("λ/dD", False)]),
    ("The resolving power of a telescope increases with:", [("Increase in diameter of objective lens", True), ("Decrease in diameter of objective lens", False), ("Increase in focal length", False), ("Increase in wavelength of light used", False)]),
    ("According to Einstein's photoelectric equation, the maximum kinetic energy of emitted photoelectrons is:", [("hf - Φ", True), ("hf + Φ", False), ("Φ - hf", False), ("hf", False)]),
    ("The Rydberg constant R is related to the wavelength λ of spectral lines of hydrogen atom by:", [("1/λ = R(1/n1^2 - 1/n2^2)", True), ("λ = R(1/n1^2 - 1/n2^2)", False), ("1/λ = R(n1^2 - n2^2)", False), ("λ = R(n2^2 - n1^2)", False)]),
    ("The binding energy per nucleon is maximum for which nucleus?", [("Fe-56", True), ("U-238", False), ("He-4", False), ("O-16", False)]),
    ("In a p-type semiconductor, the majority charge carriers are:", [("Holes", True), ("Electrons", False), ("Neutrons", False), ("Protons", False)]),
    ("Which logic gate's output is HIGH only when all its inputs are HIGH?", [("AND", True), ("OR", False), ("NAND", False), ("NOR", False)]),
    ("The process of superimposing a low-frequency signal on a high-frequency carrier wave is called:", [("Modulation", True), ("Demodulation", False), ("Attenuation", False), ("Amplification", False)]),
    ("The root mean square (rms) speed of gas molecules at absolute temperature T is proportional to:", [("√T", True), ("T", False), ("T^2", False), ("1/√T", False)]),
    ("Which material exhibits zero electrical resistance at low temperatures?", [("Superconductor", True), ("Semiconductor", False), ("Insulator", False), ("Ferromagnetic", False)]),
    ("The coefficient of restitution (e) for a perfectly elastic collision is:", [("1", True), ("0", False), ("Between 0 and 1", False), ("Infinity", False)]),
    ("Kepler's Second Law (Law of Areas) is a consequence of the conservation of:", [("Angular momentum", True), ("Linear momentum", False), ("Energy", False), ("Mass", False)]),
    ("The upthrust or buoyant force experienced by a body immersed in a fluid is equal to:", [("The weight of the fluid displaced", True), ("The volume of the fluid displaced", False), ("The density of the fluid", False), ("The mass of the body", False)]),
    ("The velocity of sound in a gas is independent of:", [("Pressure (at constant temperature)", True), ("Temperature", False), ("Density", False), ("Humidity", False)]),
    ("The internal energy of an ideal gas depends only on its:", [("Temperature", True), ("Pressure", False), ("Volume", False), ("Density", False)]),
    ("Carnot engine operates between two temperatures T1 (source) and T2 (sink). Its efficiency is:", [("1 - T2/T1", True), ("1 - T1/T2", False), ("T1/T2", False), ("T2/T1", False)]),
    ("The electric potential at a distance r from a point charge q is proportional to:", [("1/r", True), ("1/r^2", False), ("r", False), ("r^2", False)]),
    ("The magnetic susceptibility of a diamagnetic substance is:", [("Small and negative", True), ("Small and positive", False), ("Large and positive", False), ("Zero", False)]),
    ("Which ray has the highest penetrating power?", [("Gamma rays", True), ("Alpha rays", False), ("Beta rays", False), ("X-rays", False)]),

    # Chemistry (20)
    ("What is the bond angle in a molecule with sp3 hybridization (e.g., CH4)?", [("109.5°", True), ("120°", False), ("180°", False), ("90°", False)]),
    ("Which of the following quantum numbers determines the shape of an orbital?", [("Azimuthal (l)", True), ("Principal (n)", False), ("Magnetic (m)", False), ("Spin (s)", False)]),
    ("The IUPAC name of CH3-CH2-CHO is:", [("Propanal", True), ("Propanone", False), ("Propanol", False), ("Propanoic acid", False)]),
    ("In an SN2 reaction, the configuration of the chiral center usually undergoes:", [("Inversion", True), ("Retention", False), ("Racemization", False), ("No change", False)]),
    ("Which reagent is used in the Lucas test to distinguish between primary, secondary, and tertiary alcohols?", [("Anhydrous ZnCl2 + conc. HCl", True), ("Br2 in CCl4", False), ("AgNO3 in NH4OH", False), ("Alkaline KMnO4", False)]),
    ("The geometry of SF6 molecule is:", [("Octahedral", True), ("Tetrahedral", False), ("Square planar", False), ("Trigonal bipyramidal", False)]),
    ("According to Le Chatelier's principle, increasing the pressure of a gaseous equilibrium system will shift the reaction towards the side with:", [("Fewer moles of gas", True), ("More moles of gas", False), ("Higher temperature", False), ("Lower volume", False)]),
    ("The standard enthalpy of formation of an element in its standard state is:", [("Zero", True), ("Positive", False), ("Negative", False), ("1", False)]),
    ("In the Nernst equation, E = E° - (RT/nF)lnQ, what does 'n' represent?", [("Number of moles of electrons transferred", True), ("Number of moles of reactants", False), ("Principal quantum number", False), ("Avogadro's number", False)]),
    ("The half-life of a first-order reaction is:", [("Independent of initial concentration", True), ("Directly proportional to initial concentration", False), ("Inversely proportional to initial concentration", False), ("Zero", False)]),
    ("Which of the following is an ore of aluminum?", [("Bauxite", True), ("Hematite", False), ("Galena", False), ("Cinnabar", False)]),
    ("The contact process is used for the industrial production of:", [("Sulfuric acid", True), ("Ammonia", False), ("Nitric acid", False), ("Sodium carbonate", False)]),
    ("Which series of lines in the hydrogen spectrum lies in the visible region?", [("Balmer series", True), ("Lyman series", False), ("Paschen series", False), ("Brackett series", False)]),
    ("The oxidation number of Cr in K2Cr2O7 is:", [("+6", True), ("+3", False), ("+7", False), ("+4", False)]),
    ("Aromaticity requires a cyclic, planar molecule with a fully conjugated pi system containing how many pi electrons?", [("4n + 2", True), ("4n", False), ("2n", False), ("n", False)]),
    ("The Cannizzaro reaction is given by aldehydes that:", [("Do not have an alpha-hydrogen", True), ("Have an alpha-hydrogen", False), ("Are aliphatic only", False), ("Contain a ketone group", False)]),
    ("Polymers formed by the condensation of hexamethylenediamine and adipic acid are called:", [("Nylon 6,6", True), ("Bakelite", False), ("Teflon", False), ("Polyester", False)]),
    ("The separation of an azeotropic mixture by simple fractional distillation is:", [("Impossible", True), ("Possible", False), ("Requires high pressure", False), ("Requires low temperature", False)]),
    ("The crystal lattice of NaCl is:", [("Face-centered cubic (FCC)", True), ("Body-centered cubic (BCC)", False), ("Simple cubic (SC)", False), ("Hexagonal close-packed (HCP)", False)]),
    ("Which transition metal is present in Vitamin B12?", [("Cobalt", True), ("Iron", False), ("Zinc", False), ("Magnesium", False)])
]

class Command(BaseCommand):
    help = 'Seed 80 JEE questions'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding 80 JEE questions...")

        try:
            subject, _ = Subject.objects.get_or_create(
                name="JEE Preparation"
            )

            with transaction.atomic():
                for q_text, choices in QUESTIONS:
                    question, created = Question.objects.get_or_create(
                        text=q_text,
                        subject=subject,
                        defaults={'text': q_text, 'subject': subject}
                    )
                    
                    if created:
                        for c_text, is_corr in choices:
                            Choice.objects.create(
                                question=question,
                                text=c_text,
                                is_correct=is_corr
                            )

            self.stdout.write(self.style.SUCCESS(f'Successfully added 80 JEE questions!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding questions: {e}'))
