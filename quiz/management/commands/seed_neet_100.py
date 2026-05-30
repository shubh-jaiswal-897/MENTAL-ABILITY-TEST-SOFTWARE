from django.core.management.base import BaseCommand
from quiz.models import Question, Choice, Subject
from django.db import transaction

QUESTIONS = [
    # Biology (40)
    ("Which of the following acts as the primary site for photosynthesis in a typical leaf?", [("Mesophyll cells", True), ("Epidermal cells", False), ("Guard cells", False), ("Xylem vessels", False)]),
    ("The basic functional unit of the human kidney is the:", [("Nephron", True), ("Neuron", False), ("Alveolus", False), ("Villus", False)]),
    ("Which hormone regulates the sleep-wake cycle in humans?", [("Melatonin", True), ("Thyroxine", False), ("Adrenaline", False), ("Insulin", False)]),
    ("In human females, meiosis-II is not completed until?", [("Fertilization", True), ("Puberty", False), ("Uterine implantation", False), ("Birth", False)]),
    ("Which of the following is considered the 'pacemaker' of the heart?", [("SA Node", True), ("AV Node", False), ("Bundle of His", False), ("Purkinje fibers", False)]),
    ("What type of joint is present between the atlas and axis vertebrae?", [("Pivot joint", True), ("Hinge joint", False), ("Saddle joint", False), ("Gliding joint", False)]),
    ("DNA replication occurs during which phase of the cell cycle?", [("S phase", True), ("G1 phase", False), ("G2 phase", False), ("M phase", False)]),
    ("The enzyme responsible for unwinding the DNA double helix is:", [("Helicase", True), ("DNA Polymerase", False), ("Ligase", False), ("Primase", False)]),
    ("Which gas is primarily responsible for the greenhouse effect?", [("Carbon dioxide", True), ("Oxygen", False), ("Nitrogen", False), ("Argon", False)]),
    ("What is the scientific name of the modern human?", [("Homo sapiens", True), ("Homo habilis", False), ("Homo erectus", False), ("Homo neanderthalensis", False)]),
    ("Which part of the brain is responsible for maintaining posture and balance?", [("Cerebellum", True), ("Cerebrum", False), ("Medulla oblongata", False), ("Hypothalamus", False)]),
    ("The process by which RNA is synthesized from a DNA template is called:", [("Transcription", True), ("Translation", False), ("Replication", False), ("Mutation", False)]),
    ("Which blood cells are involved in the immune response?", [("Leukocytes (WBCs)", True), ("Erythrocytes (RBCs)", False), ("Platelets", False), ("Thrombocytes", False)]),
    ("What is the primary function of ribosomes?", [("Protein synthesis", True), ("Lipid synthesis", False), ("Energy production", False), ("DNA replication", False)]),
    ("Mendel's law of independent assortment applies to genes located on:", [("Different chromosomes", True), ("The same chromosome", False), ("Sex chromosomes only", False), ("Mitochondrial DNA", False)]),
    ("Which organelle is known as the 'suicidal bag' of the cell?", [("Lysosome", True), ("Mitochondria", False), ("Golgi apparatus", False), ("Endoplasmic reticulum", False)]),
    ("The term 'ecology' was coined by:", [("Ernst Haeckel", True), ("Charles Darwin", False), ("Gregor Mendel", False), ("Louis Pasteur", False)]),
    ("In which part of the digestive system does most nutrient absorption occur?", [("Small intestine", True), ("Large intestine", False), ("Stomach", False), ("Esophagus", False)]),
    ("What is the main component of the plant cell wall?", [("Cellulose", True), ("Chitin", False), ("Peptidoglycan", False), ("Glycogen", False)]),
    ("Which hormone lowers blood glucose levels?", [("Insulin", True), ("Glucagon", False), ("Adrenaline", False), ("Cortisol", False)]),
    ("The fluid part of blood, without cells, is called:", [("Plasma", True), ("Serum", False), ("Lymph", False), ("Water", False)]),
    ("Which disease is caused by the deficiency of Vitamin A?", [("Night blindness", True), ("Scurvy", False), ("Rickets", False), ("Beri-beri", False)]),
    ("What is the structural and functional unit of the nervous system?", [("Neuron", True), ("Nephron", False), ("Glial cell", False), ("Axon", False)]),
    ("The theory of evolution by natural selection was proposed by:", [("Charles Darwin", True), ("Jean-Baptiste Lamarck", False), ("Gregor Mendel", False), ("Hugo de Vries", False)]),
    ("Which type of RNA carries amino acids to the ribosome?", [("tRNA", True), ("mRNA", False), ("rRNA", False), ("snRNA", False)]),
    ("The process of water movement through a plant and its evaporation is called:", [("Transpiration", True), ("Photosynthesis", False), ("Respiration", False), ("Guttation", False)]),
    ("Which of the following is a fat-soluble vitamin?", [("Vitamin D", True), ("Vitamin B1", False), ("Vitamin C", False), ("Vitamin B12", False)]),
    ("What is the primary function of the large intestine?", [("Water absorption", True), ("Protein digestion", False), ("Nutrient absorption", False), ("Bile production", False)]),
    ("The human skeleton consists of how many bones?", [("206", True), ("201", False), ("212", False), ("198", False)]),
    ("Which gland is known as the 'master gland'?", [("Pituitary gland", True), ("Thyroid gland", False), ("Adrenal gland", False), ("Pineal gland", False)]),
    ("The genetic material in HIV is:", [("RNA", True), ("DNA", False), ("Protein", False), ("Lipid", False)]),
    ("What is the term for a symbiotic relationship where both organisms benefit?", [("Mutualism", True), ("Commensalism", False), ("Parasitism", False), ("Amensalism", False)]),
    ("Which pigment gives human skin its color?", [("Melanin", True), ("Hemoglobin", False), ("Chlorophyll", False), ("Carotene", False)]),
    ("The process of converting atmospheric nitrogen into ammonia is called:", [("Nitrogen fixation", True), ("Nitrification", False), ("Denitrification", False), ("Ammonification", False)]),
    ("Which organ produces bile?", [("Liver", True), ("Gallbladder", False), ("Pancreas", False), ("Stomach", False)]),
    ("What is the role of the restriction enzymes in recombinant DNA technology?", [("To cut DNA at specific sequences", True), ("To join DNA fragments", False), ("To synthesize DNA", False), ("To amplify DNA", False)]),
    ("The visible part of the ear is called the:", [("Pinna", True), ("Cochlea", False), ("Tympanic membrane", False), ("Ossicle", False)]),
    ("Which gas is essential for aerobic respiration?", [("Oxygen", True), ("Carbon dioxide", False), ("Nitrogen", False), ("Hydrogen", False)]),
    ("The total number of chromosomes in a normal human somatic cell is:", [("46", True), ("23", False), ("44", False), ("22", False)]),
    ("Which biomolecule is the primary source of energy for cells?", [("Glucose", True), ("Protein", False), ("Lipid", False), ("Nucleic acid", False)]),

    # Chemistry (20)
    ("According to Bohr's model, the angular momentum of an electron is an integral multiple of:", [("h/2pi", True), ("h", False), ("h/pi", False), ("2h/pi", False)]),
    ("Which of the following elements exhibits maximum catenation property?", [("Carbon", True), ("Silicon", False), ("Sulfur", False), ("Phosphorus", False)]),
    ("The oxidation state of oxygen in OF2 is:", [("+2", True), ("-2", False), ("-1", False), ("+1", False)]),
    ("Which of the following is an intensive property?", [("Temperature", True), ("Mass", False), ("Volume", False), ("Internal Energy", False)]),
    ("Hess's Law deals with:", [("Changes in enthalpy", True), ("Rate of reaction", False), ("Equilibrium constant", False), ("Influence of pressure on volume", False)]),
    ("What is the coordination number of atoms in a face-centered cubic (FCC) structure?", [("12", True), ("8", False), ("6", False), ("4", False)]),
    ("The catalyst used in the Haber process for synthesizing ammonia is:", [("Iron", True), ("Platinum", False), ("Nickel", False), ("Vanadium pentoxide", False)]),
    ("Which of the following is not a colligative property?", [("Refractive index", True), ("Osmotic pressure", False), ("Elevation of boiling point", False), ("Depression of freezing point", False)]),
    ("The general formula for alkanes is:", [("CnH2n+2", True), ("CnH2n", False), ("CnH2n-2", False), ("CnH2n+1", False)]),
    ("Which polymer is used to make non-stick cookware?", [("Teflon", True), ("PVC", False), ("Polystyrene", False), ("Bakelite", False)]),
    ("The reaction of an acid with a base to form salt and water is called:", [("Neutralization", True), ("Hydrolysis", False), ("Esterification", False), ("Saponification", False)]),
    ("What is the shape of a water (H2O) molecule?", [("Bent / V-shaped", True), ("Linear", False), ("Tetrahedral", False), ("Trigonal planar", False)]),
    ("Which element has the highest electron affinity?", [("Chlorine", True), ("Fluorine", False), ("Oxygen", False), ("Nitrogen", False)]),
    ("The process of coating iron with zinc to prevent rusting is called:", [("Galvanization", True), ("Anodizing", False), ("Electroplating", False), ("Alloying", False)]),
    ("Which of the following is a primary alcohol?", [("Ethanol", True), ("Isopropanol", False), ("tert-Butanol", False), ("Phenol", False)]),
    ("What is the pH of a 0.01 M HCl solution?", [("2", True), ("1", False), ("3", False), ("4", False)]),
    ("In the periodic table, halogens belong to which group?", [("Group 17", True), ("Group 16", False), ("Group 18", False), ("Group 15", False)]),
    ("Which of the following represents the ideal gas law?", [("PV = nRT", True), ("P1V1 = P2V2", False), ("V/T = k", False), ("P/T = k", False)]),
    ("The SI unit of molarity is:", [("mol/L", True), ("mol/kg", False), ("g/L", False), ("mol", False)]),
    ("Which intermolecular force is the strongest?", [("Hydrogen bonding", True), ("Dipole-dipole interaction", False), ("London dispersion force", False), ("Van der Waals force", False)]),

    # Physics (20)
    ("The work done by a conservative force along a closed path is:", [("Zero", True), ("Positive", False), ("Negative", False), ("Infinite", False)]),
    ("Which law states that the induced EMF is proportional to the rate of change of magnetic flux?", [("Faraday's Law", True), ("Lenz's Law", False), ("Ampere's Law", False), ("Gauss's Law", False)]),
    ("In a p-n junction diode at equilibrium, the net current is:", [("Zero", True), ("Maximum", False), ("Dependent on temperature only", False), ("Dependent on doping concentration", False)]),
    ("The escape velocity from the Earth's surface is approximately:", [("11.2 km/s", True), ("9.8 km/s", False), ("3 × 10^8 m/s", False), ("8.0 km/s", False)]),
    ("In simple harmonic motion (SHM), the acceleration is directly proportional to:", [("Displacement", True), ("Velocity", False), ("Time", False), ("Mass", False)]),
    ("The principle of conservation of linear momentum is a consequence of:", [("Newton's Third Law", True), ("Newton's First Law", False), ("Newton's Second Law", False), ("Law of Universal Gravitation", False)]),
    ("What is the dimensional formula for force?", [("MLT^-2", True), ("ML^2T^-2", False), ("MLT^-1", False), ("M^0L^0T^0", False)]),
    ("The resistance of an ideal voltmeter should be:", [("Infinite", True), ("Zero", False), ("1 Ohm", False), ("Equal to internal resistance", False)]),
    ("Which phenomenon proves the transverse nature of light?", [("Polarization", True), ("Interference", False), ("Diffraction", False), ("Reflection", False)]),
    ("The energy of a photon is given by the equation:", [("E = hf", True), ("E = mc^2", False), ("E = 1/2 mv^2", False), ("E = mgh", False)]),
    ("According to Coulomb's Law, the force between two point charges is inversely proportional to:", [("The square of the distance between them", True), ("The distance between them", False), ("The product of their charges", False), ("Their mass", False)]),
    ("What is the SI unit of magnetic flux?", [("Weber", True), ("Tesla", False), ("Henry", False), ("Gauss", False)]),
    ("In a step-up transformer, which of the following increases?", [("Voltage", True), ("Current", False), ("Power", False), ("Frequency", False)]),
    ("The focal length of a plane mirror is:", [("Infinity", True), ("Zero", False), ("Negative", False), ("Positive and finite", False)]),
    ("The process by which a heavy nucleus splits into lighter nuclei is called:", [("Nuclear fission", True), ("Nuclear fusion", False), ("Radioactivity", False), ("Alpha decay", False)]),
    ("Which quantity remains constant in an adiabatic process?", [("Heat", True), ("Temperature", False), ("Pressure", False), ("Volume", False)]),
    ("The refractive index of a medium is related to the speed of light by:", [("n = c/v", True), ("n = v/c", False), ("n = c*v", False), ("n = c+v", False)]),
    ("Which rule is used to find the direction of the magnetic field around a straight current-carrying conductor?", [("Right-hand thumb rule", True), ("Fleming's left-hand rule", False), ("Fleming's right-hand rule", False), ("Lenz's rule", False)]),
    ("The half-life of a radioactive substance is the time it takes for:", [("Half of the atoms to decay", True), ("All of the atoms to decay", False), ("The mass to double", False), ("The activity to reach zero", False)]),
    ("Which elementary particle has no electrical charge?", [("Neutron", True), ("Proton", False), ("Electron", False), ("Positron", False)])
]

class Command(BaseCommand):
    help = 'Seed 80 NEET questions'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding 80 NEET questions...")

        try:
            subject, _ = Subject.objects.get_or_create(
                name="NEET Preparation"
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

            self.stdout.write(self.style.SUCCESS(f'Successfully added 80 NEET questions!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding questions: {e}'))
