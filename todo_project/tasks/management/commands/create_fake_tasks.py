import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
from tasks.models import Task

User = get_user_model()
fake = Faker('fa_IR')


class Command(BaseCommand):
    help = 'ایجاد 5 تسک تصادفی با faker'

    def handle(self, *args, **kwargs):
        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR('هیچ یوزری وجود ندارد. اول یوزر بساز.'))
            return

        for _ in range(5):
            task = Task.objects.create(
                user=user,
                title=fake.sentence(nb_words=4),
                description=fake.paragraph(nb_sentences=2),
                is_done=random.choice([True, False]),
            )
            self.stdout.write(self.style.SUCCESS(
                f'تسک ساخته شد: {task.title} | done: {task.is_done}'
            ))