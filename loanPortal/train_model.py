from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import os, django
import joblib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redcarpet.settings')
django.setup()
from loanPortal.models import UserLoan, AccuracyTable
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


def train_model():
    print("started")
    loans = UserLoan.objects.filter(loan_status__in=['Rj', 'Ap'])
    loan_filter = loans.select_related('loans__profile').values_list(
        'principle', 'user__profile__married', 'user__profile__dependents', 'user__profile__education',
        'user__profile__self_employed', 'user__profile__income', 'user__profile__credit_history',
        'user__profile__gender')
    X = pd.DataFrame.from_records(loan_filter, columns=('principle', 'married', 'dependents', 'education', 'self_employed',
                                                        'income', 'credit_history', 'gender'))
    print(X, "wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
    statue_filter = loans.values_list('loan_status')
    Y = pd.DataFrame.from_records(statue_filter, columns=('Status',))['Status']
    Y.replace('Ap', 1, inplace=True)
    Y.replace('Rj', 0, inplace=True)
    X['married'].replace(False, 0, inplace=True)
    X['married'].replace(True, 1, inplace=True)
    X['education'].replace('N', 0, inplace=True)
    X['education'].replace('G', 1, inplace=True)
    X['gender'].replace('F', 0, inplace=True)
    X['gender'].replace('M', 1, inplace=True)
    X['self_employed'].replace(False, 0, inplace=True)
    X['self_employed'].replace(True, 1, inplace=True)
    x_train, x_cv, y_train, y_cv = train_test_split(X, Y, test_size=0.3)
    model = LogisticRegression()
    model.fit(x_train, y_train)
    joblib.dump(model, str(BASE_DIR / 'ml_models/trained_model.pkl'))
    saved_model = joblib.load(str(BASE_DIR / 'ml_models/trained_model.pkl'))
    pred_cv = saved_model.predict(x_cv)
    accuracy = accuracy_score(y_cv, pred_cv)
    AccuracyTable.objects.create(accuracy=accuracy)
    print("doneeeeeee")


def get_approval_probability(principle, married, dependents, education, self_employed, income, credit_history, gender):
    m = 1 if married else 0
    e = 0 if education == 'N' else 1
    g = 0 if gender == 'F' else 1
    emp = 1 if self_employed else 0
    db_dict = {'principle': principle, 'married': m, 'dependents': dependents, 'education': e, 'self_employed': emp,
               'income': income, 'credit_history': credit_history, 'gender': g}
    y = pd.DataFrame(db_dict, index=[0])
    saved_model = joblib.load(str(BASE_DIR / 'ml_models/trained_model.pkl'))
    pred_cv = saved_model.predict(y)
    return pred_cv[0]
