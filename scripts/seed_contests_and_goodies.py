import os
import sys
import django
from django.utils import timezone
from datetime import timedelta

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testmybrain.settings")
django.setup()

from quiz.models import Question, Contest, GoodieItem

def seed():
    print("Seeding Contests and Premium Goodies Store Items with Scaled XP Prices...")

    now = timezone.now()

    # Seed Weekly & Monthly Contests
    contests_data = [
        {
            "title": "Weekly Reasoning Clash #101",
            "contest_type": Contest.WEEKLY,
            "description": "Compete against top mind-athletes in a 60-minute fast-paced logical reasoning challenge!",
            "start_time": now - timedelta(hours=2),
            "end_time": now + timedelta(days=5),
            "duration_minutes": 60,
            "xp_prize": 500
        },
        {
            "title": "Weekly Quantitative Showdown #102",
            "contest_type": Contest.WEEKLY,
            "description": "Master numerical speed and problem solving in this weekly math aptitude contest.",
            "start_time": now + timedelta(days=6),
            "end_time": now + timedelta(days=12),
            "duration_minutes": 45,
            "xp_prize": 500
        },
        {
            "title": "Monthly Aptitude Grandmaster Tournament",
            "contest_type": Contest.MONTHLY,
            "description": "The ultimate monthly championship! 90 minutes of high-difficulty logical, quantitative, and verbal questions with huge XP prizes & Goodies rewards.",
            "start_time": now - timedelta(days=1),
            "end_time": now + timedelta(days=20),
            "duration_minutes": 90,
            "xp_prize": 2500
        }
    ]

    all_qs = list(Question.objects.all())
    for c_data in contests_data:
        contest, created = Contest.objects.get_or_create(
            title=c_data["title"],
            defaults=c_data
        )
        if not created:
            contest.xp_prize = c_data["xp_prize"]
            contest.save()
        if all_qs:
            contest.questions.set(all_qs[:10])
            contest.save()

    # Seed Goodies Store Items with Scaled XP Prices (ranging up to 6,000+ XP)
    goodies_data = [
        {
            "name": "Engraved Metallic Black Keyring",
            "description": "Precision laser-engraved matte black metal keychain with golden MENTAL ABILITY TEST SOFTWARE logo.",
            "coin_cost": 800,
            "icon_class": "fas fa-key",
            "image_path": "images/goodies/keyring.png",
            "stock": 50
        },
        {
            "name": "Verified Aptitude Certificate",
            "description": "Official digital performance certificate signed by MENTAL ABILITY TEST SOFTWARE.",
            "coin_cost": 500,
            "icon_class": "fas fa-certificate",
            "image_path": None,
            "stock": 1000
        },
        {
            "name": "Black Snapback Hat / Cap",
            "description": "Sleek matte black snapback hat featuring embroidered MENTAL ABILITY TEST SOFTWARE insignia.",
            "coin_cost": 1800,
            "icon_class": "fas fa-hat-cowboy",
            "image_path": "images/goodies/cap.png",
            "stock": 30
        },
        {
            "name": "Black Edition T-Shirt",
            "description": "Premium black cotton T-Shirt branded with MENTAL ABILITY TEST SOFTWARE gold logo.",
            "coin_cost": 3500,
            "icon_class": "fas fa-tshirt",
            "image_path": "images/goodies/tshirt.png",
            "stock": 25
        },
        {
            "name": "Black Streetwear Hoodie",
            "description": "Luxury heavyweight black hoodie sweatshirt with embroidered MENTAL ABILITY TEST SOFTWARE logo.",
            "coin_cost": 6000,
            "icon_class": "fas fa-user-ninja",
            "image_path": "images/goodies/hoodie.png",
            "stock": 20
        },
        {
            "name": "Aptitude Scholar Backpack",
            "description": "Waterproof dark edition laptop backpack designed for competitive coders and aptitude scholars.",
            "coin_cost": 7500,
            "icon_class": "fas fa-briefcase",
            "image_path": None,
            "stock": 15
        }
    ]

    for g_data in goodies_data:
        g, created = GoodieItem.objects.get_or_create(
            name=g_data["name"],
            defaults=g_data
        )
        if not created:
            g.description = g_data["description"]
            g.coin_cost = g_data["coin_cost"]
            g.icon_class = g_data["icon_class"]
            g.image_path = g_data["image_path"]
            g.save()

    print("Contests and Goodies Store Prices Successfully Updated!")

if __name__ == "__main__":
    seed()
