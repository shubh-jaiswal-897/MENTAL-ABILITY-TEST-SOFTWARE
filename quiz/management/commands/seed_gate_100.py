from django.core.management.base import BaseCommand
from quiz.models import Question, Choice, Subject
from django.db import transaction

QUESTIONS = [
    # Computer Science / IT (40)
    ("Which of the following sorting algorithms has the best average-case time complexity?", [("Merge Sort", True), ("Quick Sort", False), ("Bubble Sort", False), ("Insertion Sort", False)]),
    ("The minimum number of states in a DFA accepting strings ending with '00' over the alphabet {0,1} is:", [("3", True), ("2", False), ("4", False), ("5", False)]),
    ("Which data structure is used for Breadth First Search (BFS) of a graph?", [("Queue", True), ("Stack", False), ("Priority Queue", False), ("Linked List", False)]),
    ("In a relational database, what is the primary purpose of a foreign key?", [("To enforce referential integrity", True), ("To uniquely identify a row", False), ("To speed up queries", False), ("To prevent null values", False)]),
    ("Which protocol is used for secure communication over the Internet?", [("HTTPS", True), ("HTTP", False), ("FTP", False), ("Telnet", False)]),
    ("The OSI model consists of how many layers?", [("7", True), ("5", False), ("4", False), ("6", False)]),
    ("In an IP address of IPv4, how many bits are used?", [("32 bits", True), ("64 bits", False), ("128 bits", False), ("16 bits", False)]),
    ("Which of the following is an example of a greedy algorithm?", [("Dijkstra's Algorithm", True), ("Floyd-Warshall Algorithm", False), ("Bellman-Ford Algorithm", False), ("Dynamic Programming", False)]),
    ("What is the time complexity of binary search in a sorted array?", [("O(log n)", True), ("O(n)", False), ("O(n log n)", False), ("O(1)", False)]),
    ("Which page replacement algorithm suffers from Belady's Anomaly?", [("FIFO", True), ("LRU", False), ("Optimal", False), ("Second Chance", False)]),
    ("The maximum number of nodes in a binary tree of height h is (assuming root is at height 0):", [("2^(h+1) - 1", True), ("2^h - 1", False), ("2^(h-1)", False), ("2^h", False)]),
    ("A B-Tree of order m has maximum how many children per node?", [("m", True), ("m-1", False), ("m/2", False), ("2m", False)]),
    ("Which type of grammar produces Context-Free Languages?", [("Type 2", True), ("Type 0", False), ("Type 1", False), ("Type 3", False)]),
    ("The process of converting a logical address to a physical address is handled by:", [("MMU", True), ("CPU", False), ("ALU", False), ("Cache", False)]),
    ("Which of the following scheduling algorithms can lead to starvation?", [("Shortest Job First (SJF)", True), ("Round Robin", False), ("First Come First Serve", False), ("Fair Share", False)]),
    ("In cryptography, RSA is a type of:", [("Asymmetric key algorithm", True), ("Symmetric key algorithm", False), ("Hash function", False), ("Block cipher", False)]),
    ("What is the decimal equivalent of the binary number 1011?", [("11", True), ("10", False), ("12", False), ("13", False)]),
    ("Which logic gate is known as the Universal Gate?", [("NAND", True), ("AND", False), ("OR", False), ("XOR", False)]),
    ("What does SQL stand for?", [("Structured Query Language", True), ("Sequential Query Language", False), ("Standard Query Language", False), ("System Query Language", False)]),
    ("Which command is used to delete a table in SQL?", [("DROP", True), ("DELETE", False), ("REMOVE", False), ("TRUNCATE", False)]),
    ("What is the default port for HTTP?", [("80", True), ("443", False), ("21", False), ("22", False)]),
    ("Which layer of the OSI model handles routing?", [("Network Layer", True), ("Data Link Layer", False), ("Transport Layer", False), ("Physical Layer", False)]),
    ("A complete graph with n vertices has how many edges?", [("n(n-1)/2", True), ("n", False), ("n-1", False), ("n^2", False)]),
    ("Which traversal of a Binary Search Tree (BST) visits nodes in ascending order?", [("Inorder", True), ("Preorder", False), ("Postorder", False), ("Level order", False)]),
    ("Which data structure is typically used to implement recursion?", [("Stack", True), ("Queue", False), ("Heap", False), ("Array", False)]),
    ("A language is called regular if and only if it is accepted by a:", [("DFA", True), ("Pushdown Automaton", False), ("Turing Machine", False), ("Linear Bounded Automaton", False)]),
    ("Pumping lemma is primarily used to prove that a language is:", [("Not regular", True), ("Regular", False), ("Context-Free", False), ("Decidable", False)]),
    ("Which normal form resolves transitive dependencies?", [("3NF", True), ("1NF", False), ("2NF", False), ("BCNF", False)]),
    ("The ACID properties in a database mean Atomicity, Consistency, Isolation, and:", [("Durability", True), ("Dependency", False), ("Data", False), ("Distributed", False)]),
    ("Which component is the brain of a computer?", [("CPU", True), ("Memory", False), ("Hard Drive", False), ("Motherboard", False)]),
    ("Which boolean algebra theorem states that (A + B)' = A' . B'?", [("De Morgan's Law", True), ("Commutative Law", False), ("Associative Law", False), ("Distributive Law", False)]),
    ("What is a race condition in operating systems?", [("When multiple threads access shared data concurrently and the outcome depends on the order of execution", True), ("When two processes are waiting for each other indefinitely", False), ("When a process runs faster than another", False), ("When a CPU is overloaded", False)]),
    ("Which IPC mechanism is used for synchronization?", [("Semaphore", True), ("Pipe", False), ("Shared Memory", False), ("Message Queue", False)]),
    ("The transport layer protocol that provides reliable, connection-oriented service is:", [("TCP", True), ("UDP", False), ("IP", False), ("ICMP", False)]),
    ("Ping uses which protocol?", [("ICMP", True), ("TCP", False), ("UDP", False), ("ARP", False)]),
    ("Which sort has worst-case time complexity of O(n log n)?", [("Merge Sort", True), ("Quick Sort", False), ("Bubble Sort", False), ("Selection Sort", False)]),
    ("An undirected graph is Eulerian if and only if:", [("All vertices have even degree", True), ("It is a tree", False), ("It is a bipartite graph", False), ("It has an odd number of vertices", False)]),
    ("Which of the following is not a property of a transaction?", [("Flexibility", True), ("Atomicity", False), ("Isolation", False), ("Durability", False)]),
    ("Which command in Linux is used to list files in a directory?", [("ls", True), ("cd", False), ("pwd", False), ("cat", False)]),
    ("What is the root node of the Linux file system?", [("/", True), ("/home", False), ("/root", False), ("/bin", False)]),

    # Engineering Math & Aptitude (40)
    ("The limit of sin(x)/x as x approaches 0 is:", [("1", True), ("0", False), ("Infinity", False), ("Undefined", False)]),
    ("The derivative of e^x with respect to x is:", [("e^x", True), ("x*e^(x-1)", False), ("ln(x)", False), ("1/e^x", False)]),
    ("The integral of 1/x dx is:", [("ln|x| + C", True), ("x^2/2 + C", False), ("-1/x^2 + C", False), ("e^x + C", False)]),
    ("A square matrix A is called orthogonal if:", [("A * A^T = I", True), ("A = A^T", False), ("A = -A^T", False), ("det(A) = 0", False)]),
    ("The eigenvalues of an upper triangular matrix are:", [("The diagonal elements", True), ("The off-diagonal elements", False), ("Always zero", False), ("The determinant", False)]),
    ("The rank of a matrix is the maximum number of:", [("Linearly independent rows or columns", True), ("Zero rows", False), ("Non-zero elements", False), ("Eigenvalues", False)]),
    ("The probability of getting a sum of 7 when two six-sided dice are rolled is:", [("1/6", True), ("1/12", False), ("1/36", False), ("1/7", False)]),
    ("Two events A and B are independent if:", [("P(A ∩ B) = P(A) * P(B)", True), ("P(A U B) = P(A) + P(B)", False), ("P(A|B) = 0", False), ("P(A) = P(B)", False)]),
    ("The expected value of a constant c is:", [("c", True), ("0", False), ("1", False), ("Infinity", False)]),
    ("Which distribution models the number of events occurring in a fixed interval of time?", [("Poisson distribution", True), ("Normal distribution", False), ("Binomial distribution", False), ("Exponential distribution", False)]),
    ("The area under the standard normal curve is:", [("1", True), ("0", False), ("Infinity", False), ("pi", False)]),
    ("A differential equation is linear if:", [("The dependent variable and its derivatives appear to the first power only", True), ("It has constant coefficients", False), ("It can be solved by separation of variables", False), ("It involves trigonometric functions", False)]),
    ("The Laplace transform of 1 is:", [("1/s", True), ("s", False), ("1/s^2", False), ("e^s", False)]),
    ("Euler's formula states that e^(ix) equals:", [("cos(x) + i*sin(x)", True), ("sin(x) + i*cos(x)", False), ("cos(x) - i*sin(x)", False), ("e^x", False)]),
    ("The divergence of the curl of any vector field is:", [("0", True), ("1", False), ("The vector field itself", False), ("Infinity", False)]),
    ("A vector is irrotational if its:", [("Curl is zero", True), ("Divergence is zero", False), ("Gradient is zero", False), ("Magnitude is one", False)]),
    ("The sum of angles in a triangle on a flat plane is:", [("180 degrees", True), ("90 degrees", False), ("360 degrees", False), ("270 degrees", False)]),
    ("If A is a 3x3 matrix and det(A) = 5, what is det(2A)?", [("40", True), ("10", False), ("20", False), ("5", False)]),
    ("A function f(x) is continuous at x=a if:", [("Limit as x->a of f(x) equals f(a)", True), ("f'(a) exists", False), ("f(x) is defined everywhere", False), ("f(a) = 0", False)]),
    ("The Maclaurin series for sin(x) starts with:", [("x - x^3/3! + ...", True), ("1 - x^2/2! + ...", False), ("x + x^2/2 + ...", False), ("1 + x + ...", False)]),
    ("A bag contains 5 red and 3 blue balls. The probability of drawing a red ball is:", [("5/8", True), ("3/8", False), ("1/2", False), ("5/3", False)]),
    ("If A can do a work in 10 days and B in 15 days, together they can do it in:", [("6 days", True), ("5 days", False), ("12.5 days", False), ("8 days", False)]),
    ("The next number in the series 2, 6, 12, 20, 30 is:", [("42", True), ("40", False), ("36", False), ("48", False)]),
    ("If x is 20% more than y, then y is what percent less than x?", [("16.67%", True), ("20%", False), ("15%", False), ("25%", False)]),
    ("The cost price of 20 articles is the same as the selling price of x articles. If the profit is 25%, what is x?", [("16", True), ("15", False), ("18", False), ("25", False)]),
    ("If RED is coded as 27 and GREEN is coded as 49, how is BLUE coded?", [("40", True), ("38", False), ("42", False), ("45", False)]),
    ("Pointing to a man, a woman said, 'His mother is the only daughter of my mother.' How is the woman related to the man?", [("Mother", True), ("Aunt", False), ("Sister", False), ("Grandmother", False)]),
    ("A train 100m long is running at the speed of 30 km/hr. Time taken to pass a man standing near the line is:", [("12 seconds", True), ("10 seconds", False), ("15 seconds", False), ("20 seconds", False)]),
    ("Find the odd one out: 3, 5, 11, 14, 17, 21", [("14", True), ("21", False), ("3", False), ("17", False)]),
    ("Synonym of 'ABANDON' is:", [("Forsake", True), ("Keep", False), ("Cherish", False), ("Pursue", False)]),
    ("Antonym of 'TRANSPARENT' is:", [("Opaque", True), ("Clear", False), ("Lucid", False), ("Translucent", False)]),
    ("He is good ___ mathematics.", [("at", True), ("in", False), ("with", False), ("about", False)]),
    ("The boy was accused ___ stealing.", [("of", True), ("for", False), ("with", False), ("about", False)]),
    ("A sum of money doubles itself in 10 years at simple interest. The rate of interest is:", [("10%", True), ("5%", False), ("12%", False), ("8%", False)]),
    ("The ratio of ages of A and B is 3:4. After 4 years, it will be 4:5. Present age of A is:", [("12", True), ("15", False), ("16", False), ("9", False)]),
    ("What is the LCM of 12, 15, and 20?", [("60", True), ("120", False), ("30", False), ("90", False)]),
    ("The square root of 625 is:", [("25", True), ("15", False), ("35", False), ("45", False)]),
    ("The product of two consecutive even numbers is 288. The numbers are:", [("16 and 18", True), ("14 and 16", False), ("18 and 20", False), ("12 and 14", False)]),
    ("How many days are there in a leap year?", [("366", True), ("365", False), ("364", False), ("367", False)]),
    ("In a class of 40 students, 25 play cricket, 20 play football. How many play both if everyone plays at least one?", [("5", True), ("10", False), ("15", False), ("0", False)])
]

class Command(BaseCommand):
    help = 'Seed 80 GATE questions'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding 80 GATE questions...")

        try:
            subject, _ = Subject.objects.get_or_create(
                name="GATE Preparation"
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

            self.stdout.write(self.style.SUCCESS(f'Successfully added 80 GATE questions!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding questions: {e}'))
