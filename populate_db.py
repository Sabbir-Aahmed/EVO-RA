import os
import django
import random
from faker import Faker
from datetime import timedelta
from django.utils import timezone
from events.models import Catagory, Event, Participant  

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'events_management.settings')
django.setup()



fake = Faker()

def populate_db():
    # 1. Create Categories
    categories = []
    for _ in range(5):
        category = Catagory.objects.create(
            name=fake.word().capitalize(),
            description=fake.sentence()
        )
        categories.append(category)
    print(f"Created {len(categories)} categories.")

    # 2. Create Events
    events = []
    for _ in range(15):
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=200),
            date=fake.date_between(start_date='-10d', end_date='+20d'),
            time=fake.time(),
            location=fake.city(),
            category=random.choice(categories)
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    # 3. Create Participants
    participants = []
    for _ in range(30):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
        participants.append(participant)
    print(f"Created {len(participants)} participants.")

    # 4. Assign Participants to Events
    for event in events:
        assigned_participants = random.sample(participants, random.randint(2, 8))
        event.participants.set(assigned_participants)
    print("Assigned participants to all events.")

    print("Database population completed successfully.")

if __name__ == "__main__":
    populate_db()
