import json
import os
from pathlib import Path

from database import Problem, Topic, User, Submission, Example, Language

FIXTURE_PATH = os.path.join(Path(__file__).parent.parent, 'fixtures')


async def load_problems_from_json(l: list):  # ['problems', 'topics']
    if not len(l):
        print('At least one fixture must be provided.')
        return

    class_list = [Problem, Topic, User, Submission, Example, Language]
    for class_item in class_list:
        for item in l:
            class_name = (class_item.__name__ + 's').lower()
            if class_name == item:
                _path = os.path.join(FIXTURE_PATH, item)
                with open(f'{_path}.json', encoding="utf-8") as file:
                    objects = json.load(file)
                    for obj in objects:
                        await class_item.create(**obj)

                    print(f"✅ {len(objects)} {item} successfully loaded!")
