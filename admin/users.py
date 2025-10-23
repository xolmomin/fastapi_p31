from sqladmin import ModelView

from database import User, Submission


class UserModelView(ModelView, model=User):
    column_list = [User.id, User.first_name, User.last_name, User.email]


class SubmissionModelView(ModelView, model=Submission):
    column_list = [Submission.id]
