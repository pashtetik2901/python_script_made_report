import pytest
from main import Worker, Report

@pytest.fixture
def sample_data():
    return [
        ['id', 'email', 'name', 'department', 'hours_worked', 'salary'],
        ['1', 'a@b.com', 'Alexader', 'IT', '40', '10'],
        ['2', 'b@b.com', 'Boris', 'IT', '35', '12'],
        ['3', 'c@b.com', 'Fedor', 'HR', '30', '15']
    ]

def test_worker_creation():
    w = Worker(1, 'example@test.ru', 'Dima', 'Proger', 12, 10)
    assert w.id == 1
    assert w.email == 'example@test.ru'
    assert w.name == 'Dima'
    assert w.department == 'Proger'
    assert w.hours_worked == 12
    assert w.salary == 10
    assert w.full_salary == 120

def test_for_array(sample_data):
    report = Report.__new__(Report)
    workers = report._Report__for_array(sample_data.copy())
    assert len(workers) == 3
    assert workers[0].department == 'HR'
    assert workers[1].salary == 10
    assert workers[2].name == 'Boris'

def test_made_payout(sample_data):
    report = Report.__new__(Report)
    workers = report._Report__for_array(sample_data.copy())
    payout = report._Report__made_payout(workers)
    assert 'HR' in payout
    assert 'IT' in payout
    assert payout['IT']['hours'] == 40 + 35
    assert payout['IT']['payout'] == 40*10 + 35*12
    assert payout['HR']['hours'] == 30
    assert payout['HR']['payout'] == 30*15

def test_read_file(tmp_path):
    file = tmp_path / "test.csv"
    file.write_text("id,email,name,department,hours_worked,salary\n1,a@b.com,Boris,IT,40,10\n")
    report = Report.__new__(Report)
    data = report._Report__read_file(str(file))
    assert isinstance(data, list)
    assert data[0][0] == 'id'
    assert data[1][0] == '1'
    assert data[1][2] == 'Boris'

def test_print_payout(sample_data):
    report = Report.__new__(Report)
    report.workers = report._Report__for_array(sample_data.copy())
    report.payout = report._Report__print_payout()
    assert 'Alexader' in report.payout
    assert 'IT' in report.payout
    assert 'Boris' in report.payout
    assert 'HR' in report.payout

def test_read_file_not_exist():
    report = Report.__new__(Report)
    data = report._Report__read_file('non_exist_file.csv')
    assert data is None




