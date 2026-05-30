from django.core.management.base import BaseCommand
from quiz.models import Question, Choice, Subject
from django.db import transaction

QUESTIONS = [
    # Polity (20)
    ("Which of the following is not a Fundamental Right in India?", [("Right to Property", True), ("Right to Equality", False), ("Right to Freedom", False), ("Right against Exploitation", False)]),
    ("Who is the Supreme Commander of the Indian Armed Forces?", [("President of India", True), ("Prime Minister", False), ("Chief of Defence Staff", False), ("Minister of Defence", False)]),
    ("The Directive Principles of State Policy are borrowed from which country's constitution?", [("Ireland", True), ("USA", False), ("UK", False), ("USSR", False)]),
    ("Under which Article of the Constitution can the President declare a National Emergency?", [("Article 352", True), ("Article 356", False), ("Article 360", False), ("Article 370", False)]),
    ("Who appoints the Chief Election Commissioner of India?", [("President", True), ("Prime Minister", False), ("Chief Justice of India", False), ("Parliament", False)]),
    ("Which schedule of the Indian Constitution contains the anti-defection law?", [("Tenth Schedule", True), ("Eighth Schedule", False), ("Ninth Schedule", False), ("Eleventh Schedule", False)]),
    ("The concept of 'Judicial Review' in India is borrowed from the constitution of:", [("USA", True), ("UK", False), ("Canada", False), ("Australia", False)]),
    ("What is the maximum strength of the Lok Sabha provided by the Constitution?", [("552", True), ("545", False), ("550", False), ("500", False)]),
    ("Who was the Chairman of the Drafting Committee of the Indian Constitution?", [("Dr. B.R. Ambedkar", True), ("Dr. Rajendra Prasad", False), ("Jawaharlal Nehru", False), ("Sardar Vallabhbhai Patel", False)]),
    ("Which constitutional amendment reduced the voting age from 21 to 18 years?", [("61st Amendment", True), ("42nd Amendment", False), ("44th Amendment", False), ("73rd Amendment", False)]),
    ("Right to Information (RTI) Act came into force in which year?", [("2005", True), ("2002", False), ("2008", False), ("2010", False)]),
    ("How many members are nominated to the Rajya Sabha by the President?", [("12", True), ("2", False), ("10", False), ("14", False)]),
    ("Which Article deals with the establishment of a Finance Commission in India?", [("Article 280", True), ("Article 324", False), ("Article 148", False), ("Article 315", False)]),
    ("Panchayati Raj was first introduced in which state?", [("Rajasthan", True), ("Andhra Pradesh", False), ("Gujarat", False), ("Maharashtra", False)]),
    ("Who presides over the joint sitting of the two houses of Parliament?", [("Speaker of Lok Sabha", True), ("President", False), ("Vice President", False), ("Prime Minister", False)]),
    ("Which part of the Constitution deals with Fundamental Duties?", [("Part IV A", True), ("Part III", False), ("Part IV", False), ("Part V", False)]),
    ("Who has the power to pardon in case of capital punishment?", [("President", True), ("Governor", False), ("Chief Justice of India", False), ("Prime Minister", False)]),
    ("The minimum age required to become a member of the Rajya Sabha is:", [("30 years", True), ("25 years", False), ("35 years", False), ("21 years", False)]),
    ("Which writ is issued by a higher court when a lower court has considered a case going beyond its jurisdiction?", [("Prohibition", True), ("Mandamus", False), ("Habeas Corpus", False), ("Quo Warranto", False)]),
    ("Who is the ex-officio chairman of NITI Aayog?", [("Prime Minister", True), ("President", False), ("Finance Minister", False), ("Home Minister", False)]),

    # History (20)
    ("Who was the founder of the Maurya Empire?", [("Chandragupta Maurya", True), ("Ashoka", False), ("Bindusara", False), ("Bimbisara", False)]),
    ("The Harappan Civilization was discovered in the year:", [("1921", True), ("1920", False), ("1922", False), ("1931", False)]),
    ("Who wrote the Arthashastra?", [("Chanakya", True), ("Megasthenes", False), ("Kalidasa", False), ("Banabhatta", False)]),
    ("The battle of Plassey was fought in the year:", [("1757", True), ("1764", False), ("1857", False), ("1761", False)]),
    ("Who was the first Governor-General of independent India?", [("Lord Mountbatten", True), ("C. Rajagopalachari", False), ("Rajendra Prasad", False), ("Jawaharlal Nehru", False)]),
    ("The Indian National Congress was founded in which year?", [("1885", True), ("1857", False), ("1905", False), ("1919", False)]),
    ("Who gave the slogan 'Do or Die' during the Quit India Movement?", [("Mahatma Gandhi", True), ("Subhas Chandra Bose", False), ("Bhagat Singh", False), ("Jawaharlal Nehru", False)]),
    ("The first Round Table Conference was held in which city?", [("London", True), ("New Delhi", False), ("Bombay", False), ("Calcutta", False)]),
    ("Who is known as the 'Iron Man of India'?", [("Sardar Vallabhbhai Patel", True), ("Bal Gangadhar Tilak", False), ("Lala Lajpat Rai", False), ("Subhas Chandra Bose", False)]),
    ("The Jallianwala Bagh massacre took place on:", [("April 13, 1919", True), ("March 23, 1931", False), ("August 9, 1925", False), ("February 5, 1922", False)]),
    ("Which Veda contains charms and spells to ward off evils and diseases?", [("Atharva Veda", True), ("Rig Veda", False), ("Sama Veda", False), ("Yajur Veda", False)]),
    ("Who built the Sanchi Stupa?", [("Ashoka", True), ("Chandragupta Maurya", False), ("Harshavardhana", False), ("Kanishka", False)]),
    ("The capital of the Chola empire was:", [("Thanjavur", True), ("Madurai", False), ("Kanchipuram", False), ("Uraiyur", False)]),
    ("Ibn Battuta, the famous traveler, came from:", [("Morocco", True), ("Persia", False), ("Egypt", False), ("Afghanistan", False)]),
    ("Who introduced the 'Permanent Settlement' in Bengal in 1793?", [("Lord Cornwallis", True), ("Lord Wellesley", False), ("Lord Dalhousie", False), ("Warren Hastings", False)]),
    ("The Swadeshi Movement was launched in response to:", [("Partition of Bengal", True), ("Rowlatt Act", False), ("Jallianwala Bagh", False), ("Simon Commission", False)]),
    ("Who was the founder of the Ramakrishna Mission?", [("Swami Vivekananda", True), ("Ramakrishna Paramahamsa", False), ("Raja Ram Mohan Roy", False), ("Dayananda Saraswati", False)]),
    ("In which session did the Indian National Congress declare 'Purna Swaraj'?", [("Lahore Session, 1929", True), ("Karachi Session, 1931", False), ("Surat Session, 1907", False), ("Lucknow Session, 1916", False)]),
    ("Who was the political guru of Mahatma Gandhi?", [("Gopal Krishna Gokhale", True), ("Bal Gangadhar Tilak", False), ("Dadabhai Naoroji", False), ("Rabindranath Tagore", False)]),
    ("The Home Rule League was started by:", [("Annie Besant and Bal Gangadhar Tilak", True), ("Mahatma Gandhi", False), ("Subhas Chandra Bose", False), ("Jawaharlal Nehru", False)]),

    # Geography (20)
    ("Which is the longest river in India?", [("Ganga", True), ("Godavari", False), ("Brahmaputra", False), ("Indus", False)]),
    ("The highest peak in the Western Ghats is:", [("Anamudi", True), ("Doda Betta", False), ("Mullayanagiri", False), ("Kalsubai", False)]),
    ("Which Indian state has the longest coastline?", [("Gujarat", True), ("Andhra Pradesh", False), ("Tamil Nadu", False), ("Maharashtra", False)]),
    ("The Tropic of Cancer does not pass through which of the following states?", [("Odisha", True), ("Gujarat", False), ("Rajasthan", False), ("Madhya Pradesh", False)]),
    ("Majuli, the largest river island in the world, is located in which river?", [("Brahmaputra", True), ("Ganga", False), ("Amazon", False), ("Nile", False)]),
    ("Which planet is known as the 'Red Planet'?", [("Mars", True), ("Venus", False), ("Jupiter", False), ("Saturn", False)]),
    ("The layer of the atmosphere closest to the Earth's surface is:", [("Troposphere", True), ("Stratosphere", False), ("Mesosphere", False), ("Thermosphere", False)]),
    ("What is the name of the boundary line between India and China?", [("McMahon Line", True), ("Radcliffe Line", False), ("Durand Line", False), ("Line of Control", False)]),
    ("Which ocean is the largest in the world?", [("Pacific Ocean", True), ("Atlantic Ocean", False), ("Indian Ocean", False), ("Arctic Ocean", False)]),
    ("The imaginary lines connecting places of equal atmospheric pressure are called:", [("Isobars", True), ("Isotherms", False), ("Isohyets", False), ("Contours", False)]),
    ("Kharif crops are sown in:", [("June-July", True), ("October-November", False), ("March-April", False), ("January-February", False)]),
    ("Which soil is best suited for cotton cultivation?", [("Black soil", True), ("Alluvial soil", False), ("Red soil", False), ("Laterite soil", False)]),
    ("The deepest trench in the world is the Mariana Trench, located in:", [("Pacific Ocean", True), ("Atlantic Ocean", False), ("Indian Ocean", False), ("Arctic Ocean", False)]),
    ("Which is the smallest continent by land area?", [("Australia", True), ("Europe", False), ("Antarctica", False), ("South America", False)]),
    ("The headquarters of the World Meteorological Organization (WMO) is located in:", [("Geneva", True), ("New York", False), ("Paris", False), ("Rome", False)]),
    ("Which water body separates India and Sri Lanka?", [("Palk Strait", True), ("Strait of Malacca", False), ("Strait of Hormuz", False), ("Bering Strait", False)]),
    ("The famous 'Ring of Fire' is located in:", [("Pacific Ocean", True), ("Atlantic Ocean", False), ("Indian Ocean", False), ("Mediterranean Sea", False)]),
    ("What is the main cause of tides in the ocean?", [("Gravitational pull of the Moon and Sun", True), ("Earth's rotation", False), ("Ocean currents", False), ("Wind", False)]),
    ("Which is the largest desert in the world?", [("Sahara Desert", True), ("Arabian Desert", False), ("Gobi Desert", False), ("Kalahari Desert", False)]),
    ("The Equator passes through how many countries?", [("13", True), ("10", False), ("15", False), ("12", False)]),

    # Economy (20)
    ("The Reserve Bank of India (RBI) was nationalized in which year?", [("1949", True), ("1935", False), ("1955", False), ("1969", False)]),
    ("What does 'GDP' stand for?", [("Gross Domestic Product", True), ("Gross Development Product", False), ("General Domestic Product", False), ("Gross Dividend Profit", False)]),
    ("Which sector contributes the most to India's GDP?", [("Services Sector", True), ("Agricultural Sector", False), ("Industrial Sector", False), ("Manufacturing Sector", False)]),
    ("Goods and Services Tax (GST) was implemented in India on:", [("July 1, 2017", True), ("April 1, 2017", False), ("July 1, 2016", False), ("January 1, 2018", False)]),
    ("NITI Aayog replaced which institution?", [("Planning Commission", True), ("Finance Commission", False), ("National Development Council", False), ("Inter-State Council", False)]),
    ("Who is responsible for issuing the one-rupee note in India?", [("Ministry of Finance", True), ("Reserve Bank of India", False), ("State Bank of India", False), ("President of India", False)]),
    ("The concept of Five Year Plans in India was introduced by:", [("Jawaharlal Nehru", True), ("Mahatma Gandhi", False), ("B.R. Ambedkar", False), ("Sardar Patel", False)]),
    ("What is inflation?", [("A sustained increase in the general price level", True), ("A decrease in prices", False), ("Increase in money supply only", False), ("Decrease in employment", False)]),
    ("Which committee recommended the establishment of NABARD?", [("B. Sivaraman Committee", True), ("Narasimham Committee", False), ("Rangarajan Committee", False), ("Kelkar Committee", False)]),
    ("Sensex is the stock market index of which exchange?", [("Bombay Stock Exchange (BSE)", True), ("National Stock Exchange (NSE)", False), ("New York Stock Exchange", False), ("London Stock Exchange", False)]),
    ("Foreign Direct Investment (FDI) refers to:", [("Investment by a firm in another country's business", True), ("Investment in domestic stock market", False), ("Government grants to foreign countries", False), ("Exporting goods to foreign markets", False)]),
    ("The current account deficit (CAD) measures:", [("The difference between value of imports and exports", True), ("The fiscal deficit of the government", False), ("The total debt of the country", False), ("The revenue collection shortfall", False)]),
    ("Which bank is known as the 'Lender of Last Resort' in India?", [("Reserve Bank of India (RBI)", True), ("State Bank of India (SBI)", False), ("World Bank", False), ("NABARD", False)]),
    ("What does SEBI stand for?", [("Securities and Exchange Board of India", True), ("State Exchange Board of India", False), ("Stock and Equity Board of India", False), ("Securities and Equity Bureau of India", False)]),
    ("The slogan 'Garibi Hatao' (Remove Poverty) was introduced in which Five Year Plan?", [("Fifth Five Year Plan", True), ("Fourth Five Year Plan", False), ("Sixth Five Year Plan", False), ("Third Five Year Plan", False)]),
    ("Repo Rate is the rate at which:", [("RBI lends to commercial banks", True), ("Commercial banks lend to RBI", False), ("Commercial banks lend to public", False), ("RBI lends to the government", False)]),
    ("What is the base year for measuring the Consumer Price Index (CPI) in India?", [("2012", True), ("2010", False), ("2015", False), ("2004-05", False)]),
    ("Which sector employs the largest percentage of the workforce in India?", [("Agriculture", True), ("Manufacturing", False), ("Services", False), ("IT Sector", False)]),
    ("A mixed economy means:", [("Co-existence of public and private sectors", True), ("Co-existence of agriculture and industry", False), ("Co-existence of rich and poor", False), ("Co-existence of foreign and domestic companies", False)]),
    ("The 'Navratna' status is given to:", [("Public Sector Enterprises", True), ("Private Companies", False), ("Multinational Corporations", False), ("NGOs", False)])
]

class Command(BaseCommand):
    help = 'Seed 80 UPSC questions'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding 80 UPSC questions...")

        try:
            subject, _ = Subject.objects.get_or_create(
                name="UPSC Preparation"
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

            self.stdout.write(self.style.SUCCESS(f'Successfully added 80 UPSC questions!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error seeding questions: {e}'))
