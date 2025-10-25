import random

from faker import Faker

from database import Topic, Problem, Language, User, Submission, Example

faker = Faker('uz-Uz')


class GenerateDataService:

    def __init__(self, key: str, number: int):
        self.key = key
        self.number = number

    async def generate_topic(self):
        for _ in range(self.number):
            await Topic.create(name=faker.user_name().title())
        print('Topic generated')

    async def generate_example(self):
        for _ in range(self.number):
            await Example.create(
                order_number=faker.random_int(1, 100),
                input=faker.street_name(),
                output=faker.street_name(),
                explanation=faker.sentence(),
                problem_id=random.choice(await Problem.values('id', flat=True)),
            )
        print('Example generated')

    async def generate_language(self):
        await Language.create(name='python')
        print('Language generated')

    async def generate(self):
        # key=topic
        # number=5
        if hasattr(self, f'generate_{self.key}'):
            await getattr(self, f'generate_{self.key}')()
        print('Generating data is Finished')
