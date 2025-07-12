import os
import django
import random
from faker import Faker
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')  # ✅ Update if needed
django.setup()

from django.contrib.auth.models import User, Group
from events.models import Catagory, Event

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
    print(f"✅ Created {len(categories)} categories.")

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
    print(f"✅ Created {len(events)} events.")

    # 3. Create Users and assign to 'Participant' group
    participant_group, _ = Group.objects.get_or_create(name='Participant')
    users = []

    for _ in range(30):
        username = fake.unique.user_name()
        user = User.objects.create_user(
            username=username,
            email=fake.unique.email(),
            password='testpass123'  # set a simple password
        )
        user.groups.add(participant_group)
        users.append(user)
    print(f"✅ Created {len(users)} participant users.")

    # 4. Assign users to events
    for event in events:
        assigned_users = random.sample(users, random.randint(2, 8))
        event.participants.set(assigned_users)
    print("✅ Assigned users to events.")

    print("🎉 Database population completed successfully!")

if __name__ == "__main__":
    populate_db()
