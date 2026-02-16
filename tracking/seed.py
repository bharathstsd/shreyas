from datetime import date, timedelta
import random

from tracking.models import Person, WeeklyCheckin


def run():
    print("Seeding test data...")

    # Get or create a coach
    coach, _ = Person.objects.get_or_create(
        mobile="9000000000",
        defaults={
            "name": "Test Coach",
            "role": "coach",
        },
    )

    # Create test clients
    client_names = ["Ramesh", "Suresh", "Anil", "Kavya", "Deepa"]

    clients = []
    for i, name in enumerate(client_names):
        client, _ = Person.objects.get_or_create(
            mobile=f"900000000{i+1}",
            defaults={
                "name": name,
                "role": "client",
                "sponsor": coach,
            },
        )
        clients.append(client)

    today = date.today()

    # Create check-ins
    for client in clients:
        base_weight = random.randint(70, 100)

        # 14 days ago
        WeeklyCheckin.objects.update_or_create(
            person=client,
            date=today - timedelta(days=14),
            defaults={
                "weight": base_weight,
                "body_fat_percent": random.uniform(20, 35),
            },
        )

        # 7 days ago
        WeeklyCheckin.objects.update_or_create(
            person=client,
            date=today - timedelta(days=7),
            defaults={
                "weight": base_weight - random.uniform(1, 4),
                "body_fat_percent": random.uniform(18, 32),
            },
        )

        # today
        WeeklyCheckin.objects.update_or_create(
            person=client,
            date=today,
            defaults={
                "weight": base_weight - random.uniform(3, 8),
                "body_fat_percent": random.uniform(15, 30),
            },
        )

    print("Test data created successfully.")
