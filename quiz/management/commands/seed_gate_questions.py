from django.core.management.base import BaseCommand
from quiz.models import Question, Choice, Subject

QUESTIONS = [
    # General Aptitude
    ("What is the synonym of 'abundant'?", [
        ("Scarce", False),
        ("Plentiful", True),
        ("Rare", False),
        ("Limited", False),
    ]),
    ("If 5 men can do a job in 10 days, how many days will 10 men take?", [
        ("5", True),
        ("10", False),
        ("20", False),
        ("2", False),
    ]),
    ("Find the odd one out: Apple, Banana, Carrot, Orange", [
        ("Apple", False),
        ("Banana", False),
        ("Carrot", True),
        ("Orange", False),
    ]),
    ("2 + 2 * 3 = ?", [
        ("8", True),
        ("12", False),
        ("6", False),
        ("4", False),
    ]),
    ("What is the capital of France?", [
        ("London", False),
        ("Paris", True),
        ("Berlin", False),
        ("Rome", False),
    ]),
    ("Antonym of 'happy'", [
        ("Sad", True),
        ("Joyful", False),
        ("Glad", False),
        ("Cheerful", False),
    ]),
    ("If all bloops are razzes and some razzes are fizzles, then some bloops are fizzles. True or False?", [
        ("True", False),
        ("False", True),
    ]),
    ("10% of 200 is", [
        ("20", True),
        ("200", False),
        ("2", False),
        ("0.2", False),
    ]),
    ("Which is larger: 0.5 or 1/2?", [
        ("0.5", False),
        ("1/2", False),
        ("Equal", True),
        ("None", False),
    ]),
    ("What comes next: A, C, E, ?", [
        ("F", False),
        ("G", True),
        ("H", False),
        ("I", False),
    ]),
    # Engineering Mathematics
    ("What is the derivative of x^2?", [
        ("x", False),
        ("2x", True),
        ("x^2", False),
        ("2", False),
    ]),
    ("Integral of 1/x dx =", [
        ("x", False),
        ("ln|x|", True),
        ("1/x", False),
        ("e^x", False),
    ]),
    ("Rank of matrix [[1,2],[2,4]]", [
        ("1", True),
        ("2", False),
        ("0", False),
        ("3", False),
    ]),
    ("Eigenvalue of [[2,0],[0,2]]", [
        ("1", False),
        ("2", True),
        ("3", False),
        ("0", False),
    ]),
    ("Limit of sin(x)/x as x->0", [
        ("0", False),
        ("1", True),
        ("∞", False),
        ("-1", False),
    ]),
    ("Solution to x^2 - 4 = 0", [
        ("2", False),
        ("-2", False),
        ("2,-2", True),
        ("4", False),
    ]),
    ("Probability of rolling 6 on a die", [
        ("1/6", True),
        ("1/2", False),
        ("1/3", False),
        ("1/4", False),
    ]),
    ("Laplace transform of 1", [
        ("1/s", True),
        ("s", False),
        ("1", False),
        ("0", False),
    ]),
    ("Determinant of [[1,0],[0,1]]", [
        ("0", False),
        ("1", True),
        ("2", False),
        ("-1", False),
    ]),
    ("Fourier transform of e^-a|t|", [
        ("2a/(a^2 + w^2)", False),
        ("2a/(a^2 - w^2)", False),
        ("1/(a + iw)", True),
        ("None", False),
    ]),
    # Digital Logic
    ("What is AND gate output for 1,1?", [
        ("0", False),
        ("1", True),
        ("X", False),
        ("Z", False),
    ]),
    ("NOR gate is", [
        ("OR + NOT", True),
        ("AND + NOT", False),
        ("XOR", False),
        ("XNOR", False),
    ]),
    ("Flip flop type for memory", [
        ("SR", False),
        ("JK", False),
        ("D", True),
        ("T", False),
    ]),
    ("Binary of 5", [
        ("101", True),
        ("110", False),
        ("100", False),
        ("111", False),
    ]),
    ("Full adder has", [
        ("2 inputs", False),
        ("3 inputs", True),
        ("4 inputs", False),
        ("1 input", False),
    ]),
    ("Multiplexer selects", [
        ("One input", True),
        ("Multiple", False),
        ("All", False),
        ("None", False),
    ]),
    ("Decoder converts", [
        ("Binary to decimal", True),
        ("Decimal to binary", False),
        ("Hex to binary", False),
        ("None", False),
    ]),
    ("K-map for 3 variables has", [
        ("4 cells", False),
        ("8 cells", True),
        ("16", False),
        ("2", False),
    ]),
    ("Boolean expression for XOR", [
        ("AB + AB'", False),
        ("AB' + A'B", True),
        ("AB", False),
        ("A+B", False),
    ]),
    ("Shift register shifts", [
        ("Bits", True),
        ("Bytes", False),
        ("Words", False),
        ("None", False),
    ]),
    # Computer Organization and Architecture
    ("CPU stands for", [
        ("Central Processing Unit", True),
        ("Central Program Unit", False),
        ("Computer Processing Unit", False),
        ("None", False),
    ]),
    ("Cache is", [
        ("Fast memory", True),
        ("Slow memory", False),
        ("Storage", False),
        ("None", False),
    ]),
    ("Pipeline stages include", [
        ("Fetch", False),
        ("Decode", False),
        ("Execute", False),
        ("All", True),
    ]),
    ("Interrupt is", [
        ("Hardware", False),
        ("Software", False),
        ("Both", True),
        ("None", False),
    ]),
    ("ALU performs", [
        ("Arithmetic", False),
        ("Logic", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Register is", [
        ("Fast storage", True),
        ("Slow storage", False),
        ("Memory", False),
        ("None", False),
    ]),
    ("Von Neumann architecture has", [
        ("Stored program", True),
        ("No program", False),
        ("External program", False),
        ("None", False),
    ]),
    ("Bus is", [
        ("Communication line", True),
        ("Storage", False),
        ("Processor", False),
        ("None", False),
    ]),
    ("Memory hierarchy", [
        ("Cache, RAM, Disk", True),
        ("Disk, RAM, Cache", False),
        ("RAM, Cache, Disk", False),
        ("None", False),
    ]),
    ("RISC vs CISC", [
        ("RISC simple, CISC complex", True),
        ("Opposite", False),
        ("Same", False),
        ("None", False),
    ]),
    # Programming and Data Structures
    ("What is a variable?", [
        ("Constant", False),
        ("Changing value", True),
        ("Function", False),
        ("None", False),
    ]),
    ("Loop in C", [
        ("for", False),
        ("while", False),
        ("do-while", False),
        ("All", True),
    ]),
    ("Array index starts from", [
        ("0", True),
        ("1", False),
        ("-1", False),
        ("2", False),
    ]),
    ("Pointer points to", [
        ("Value", False),
        ("Address", True),
        ("Function", False),
        ("None", False),
    ]),
    ("Recursion is", [
        ("Function calls itself", True),
        ("Loop", False),
        ("Iteration", False),
        ("None", False),
    ]),
    ("Struct in C", [
        ("Data type", True),
        ("Function", False),
        ("Variable", False),
        ("None", False),
    ]),
    ("Dynamic memory", [
        ("malloc", False),
        ("calloc", False),
        ("Both", True),
        ("None", False),
    ]),
    ("File handling", [
        ("fopen", False),
        ("fclose", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Preprocessor", [
        ("#include", False),
        ("#define", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Error types", [
        ("Syntax", False),
        ("Runtime", False),
        ("Logical", False),
        ("All", True),
    ]),
    # Algorithms
    ("Sorting algorithm O(n log n)", [
        ("Bubble", False),
        ("Quick", True),
        ("Insertion", False),
        ("Selection", False),
    ]),
    ("Searching O(log n)", [
        ("Linear", False),
        ("Binary", True),
        ("Hash", False),
        ("None", False),
    ]),
    ("Graph traversal", [
        ("DFS", False),
        ("BFS", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Shortest path", [
        ("Dijkstra", False),
        ("Bellman", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Tree height", [
        ("log n", True),
        ("n", False),
        ("n^2", False),
        ("None", False),
    ]),
    ("Dynamic programming", [
        ("Memoization", False),
        ("Tabulation", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Greedy algorithm", [
        ("Always optimal", False),
        ("Sometimes", True),
        ("Never", False),
        ("None", False),
    ]),
    ("NP-complete", [
        ("P", False),
        ("NP", False),
        ("NPC", True),
        ("None", False),
    ]),
    ("Time complexity of fib", [
        ("O(2^n)", True),
        ("O(n)", False),
        ("O(log n)", False),
        ("O(n^2)", False),
    ]),
    ("Hash table collision", [
        ("Chaining", False),
        ("Open addressing", False),
        ("Both", True),
        ("None", False),
    ]),
    # Theory of Computation
    ("DFA accepts", [
        ("Regular", True),
        ("Context free", False),
        ("Context sensitive", False),
        ("Recursive", False),
    ]),
    ("Regular language", [
        ("Finite automata", True),
        ("Pushdown", False),
        ("Turing", False),
        ("None", False),
    ]),
    ("Context free grammar", [
        ("Productions", False),
        ("Rules", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Turing machine", [
        ("Accepts recursively enumerable", True),
        ("Regular", False),
        ("CFL", False),
        ("None", False),
    ]),
    ("Pumping lemma for", [
        ("Regular", False),
        ("CFL", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Chomsky hierarchy", [
        ("Type 0,1,2,3", True),
        ("1,2,3,4", False),
        ("A,B,C,D", False),
        ("None", False),
    ]),
    ("NFA to DFA", [
        ("Subset construction", True),
        ("State elimination", False),
        ("Both", False),
        ("None", False),
    ]),
    ("Minimization", [
        ("DFA", True),
        ("NFA", False),
        ("Both", False),
        ("None", False),
    ]),
    ("Decidable problem", [
        ("Halting", False),
        ("Post correspondence", True),
        ("Both", False),
        ("None", False),
    ]),
    ("Undecidable", [
        ("Halting", False),
        ("PCP", False),
        ("Both", True),
        ("None", False),
    ]),
    # Compiler Design
    ("Lexical analysis", [
        ("Tokens", True),
        ("Parse tree", False),
        ("Code", False),
        ("None", False),
    ]),
    ("Parser", [
        ("LL", False),
        ("LR", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Syntax tree", [
        ("Parse tree", False),
        ("AST", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Semantic analysis", [
        ("Type checking", True),
        ("Code generation", False),
        ("Optimization", False),
        ("None", False),
    ]),
    ("Intermediate code", [
        ("Three address", False),
        ("Quadruples", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Code optimization", [
        ("Dead code", False),
        ("Constant folding", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Symbol table", [
        ("Identifiers", False),
        ("Types", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Error recovery", [
        ("Panic mode", False),
        ("Phrase level", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Compiler phases", [
        ("6", False),
        ("7", True),
        ("8", False),
        ("9", False),
    ]),
    ("Bootstrapping", [
        ("Compiler compiles itself", True),
        ("Interpreter", False),
        ("Both", False),
        ("None", False),
    ]),
    # Operating System
    ("Process states", [
        ("Ready", False),
        ("Running", False),
        ("Waiting", False),
        ("All", True),
    ]),
    ("Scheduling", [
        ("FCFS", False),
        ("SJF", False),
        ("RR", False),
        ("All", True),
    ]),
    ("Deadlock", [
        ("Mutual exclusion", False),
        ("Hold and wait", False),
        ("No preemption", False),
        ("All", True),
    ]),
    ("Memory management", [
        ("Paging", False),
        ("Segmentation", False),
        ("Both", True),
        ("None", False),
    ]),
    ("File system", [
        ("FAT", False),
        ("NTFS", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Synchronization", [
        ("Semaphore", False),
        ("Mutex", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Virtual memory", [
        ("Demand paging", False),
        ("Thrashing", False),
        ("Both", True),
        ("None", False),
    ]),
    ("I/O", [
        ("Polling", False),
        ("Interrupt", False),
        ("DMA", False),
        ("All", True),
    ]),
    ("Thread", [
        ("Lightweight process", True),
        ("Heavy", False),
        ("Same", False),
        ("None", False),
    ]),
    ("Kernel", [
        ("Monolithic", False),
        ("Microkernel", False),
        ("Hybrid", False),
        ("All", True),
    ]),
    # Databases
    ("Relational model", [
        ("Tables", False),
        ("Relations", False),
        ("Both", True),
        ("None", False),
    ]),
    ("SQL", [
        ("DDL", False),
        ("DML", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Normalization", [
        ("1NF", False),
        ("2NF", False),
        ("3NF", False),
        ("All", True),
    ]),
    ("Keys", [
        ("Primary", False),
        ("Foreign", False),
        ("Candidate", False),
        ("All", True),
    ]),
    ("Join", [
        ("Inner", False),
        ("Outer", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Transaction", [
        ("ACID", True),
        ("BASE", False),
        ("Both", False),
        ("None", False),
    ]),
    ("Indexing", [
        ("B-tree", False),
        ("Hash", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Concurrency", [
        ("Locking", False),
        ("Timestamp", False),
        ("Both", True),
        ("None", False),
    ]),
    ("ER diagram", [
        ("Entity", False),
        ("Relationship", False),
        ("Both", True),
        ("None", False),
    ]),
    ("Query optimization", [
        ("Cost based", False),
        ("Rule based", False),
        ("Both", True),
        ("None", False),
    ]),
]


class Command(BaseCommand):
    help = 'Seed 100 GATE-related questions into the quiz app (idempotent)'

    def handle(self, *args, **options):
        created = 0
        gate_subj, _ = Subject.objects.get_or_create(name='GATE')
        # Remove existing GATE questions
        Question.objects.filter(subject=gate_subj).delete()
        for q_text, choices in QUESTIONS:
            q = Question.objects.create(text=q_text, subject=gate_subj)
            created += 1
            # create choices
            for choice_text, is_correct in choices:
                Choice.objects.create(question=q, text=choice_text, is_correct=is_correct)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created} GATE questions.'))
