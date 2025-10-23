from sqladmin import Admin

from admin.problems import TopicModelView, ProblemModelView, LanguageModelView, ExampleModelView
from admin.users import UserModelView, SubmissionModelView


def setup_admin(app, engine):
    admin = Admin(app, engine)
    admin.add_view(UserModelView)
    admin.add_view(TopicModelView)
    admin.add_view(ProblemModelView)
    admin.add_view(LanguageModelView)
    admin.add_view(ExampleModelView)
    admin.add_view(SubmissionModelView)
