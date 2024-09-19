from src.core.board.issue import Issue
from src.core.database import db
from src.core.board.label import Label

def list_issues():
    issues = Issue.query.all()

    return issues

def create_issue(**kwargs):
    issue = Issue(**kwargs)
    db.session.add(issue)
    db.session.commit()

    return issue

def assign_user(issue, user):
    issue.user = user
    db.session.add(issue)
    db.session.commit()

    return issue

def create_label(**kwargs):
    label = Label(**kwargs)
    db.session.add(label)
    db.session.commit()

    return label

def assign_labels(issue, labels):
    issue.labels = labels
    db.session.add(issue)
    db.session.commit()

    return issue