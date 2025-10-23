from sqladmin import ModelView

from database import Topic, Problem, Language, Example


class TopicModelView(ModelView, model=Topic):
    column_list = [Topic.id, Topic.name]


class ProblemModelView(ModelView, model=Problem):
    column_list = [Problem.id, Problem.name, Problem.difficulty, Problem.topics]
    column_details_exclude_list = [Problem.created_at, Problem.updated_at]
    form_excluded_columns = [Problem.created_at, Problem.updated_at]


class LanguageModelView(ModelView, model=Language):
    column_list = [Language.id, Language.name]
    form_excluded_columns = [Language.submissions]


class ExampleModelView(ModelView, model=Example):
    column_list = [Example.id, Example.problem]
