import argparse


class Worker:
    def __init__(self, id: int, email: str, name: str, department: str, hours_worked: float, salary: float):
        self.id = id
        self.email = email
        self.name = name
        self.department = department
        self.hours_worked = hours_worked
        self.salary = salary
        self.full_salary = salary * hours_worked

    def __repr__(self):
        return f'[id: {self.id}, name: {self.name}, departament: {self.department}, hours_worked: {self.hours_worked}, salary: {self.salary}]\n'


class Report:
    def __init__(self, path: str):
        self.data = self.__read_file(path)
        self.workers: list[Worker] = self.__for_array(self.data)
        self.payout = self.__print_payout()

    def __read_file(self, path: str, sep=',') -> list[list[str]]:
        data = []
        try:
            with open(path, 'r') as file:
                for row in file:
                    data.append(row.strip().split(sep))
            return data
        except FileNotFoundError as err:
            print('Неправильный путь до файла')
        except:
            print('Ошибка в пути к файлу')

    def __for_array(self, arr: list[list]) -> list[Worker]:
        first_row = arr.pop(0)
        id_idx = first_row.index('id')
        email_idx = first_row.index('email')
        name_idx = first_row.index('name')
        department_idx = first_row.index('department')
        hours_worked_idx = first_row.index('hours_worked')

        if 'salary' in first_row:
            salary = 'salary'
        elif 'hourly_rate' in first_row:
            salary = 'hourly_rate'
        else:
            salary = 'rate'

        salary_idx = first_row.index(salary)

        staff: list[Worker] = []
        for row in arr:
            worker = Worker(
                id=int(row[id_idx]),
                email=row[email_idx],
                name=row[name_idx],
                department=row[department_idx],
                hours_worked=float(row[hours_worked_idx]),
                salary=float(row[salary_idx])
            )
            staff.append(worker)

        staff.sort(key=lambda x: x.department)

        return staff

    def __made_payout(self, staff: list[Worker]) -> dict[str, dict[str, float]]:
        full_money = {}
        for worker in staff:
            if worker.department not in list(full_money.keys()):
                full_money[worker.department] = {
                    'hours': worker.hours_worked, 'payout': worker.full_salary}
            else:
                full_money[worker.department]['hours'] += worker.hours_worked
                full_money[worker.department]['payout'] += worker.full_salary

        return full_money

    def __print_payout(self):
        full_money = self.__made_payout(self.workers)

        result = [
            f"{'':<15}{'name':<20}{'hours':<10}{'rate':<10}{'payout':<10}"]
        i = 0
        for item in full_money:
            result.append(f'{item}')
            while i < len(self.workers) and self.workers[i].department == item:
                result.append(
                    f"{'-'*12:<15}{self.workers[i].name:<20}{self.workers[i].hours_worked:<10}{self.workers[i].salary:<10}{self.workers[i].full_salary:<10}")
                i += 1
            result.append(
                f"{'':<35}{full_money[item]['hours']:<10}{'':<10}{full_money[item]['payout']:<10}")
        result.append(f"{'-'*70}")

        result = '\n'.join(result)
        return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'files',
        nargs='+',
        help='Введите пути к файлам'
    )
    parser.add_argument(
        '--report',
        required=True,
        help='Укажите название отчета'
    )
    try:
        args = parser.parse_args()
    except:
        print('У вас ошибка в запросе')
        print('Убедитесь что он вылядит так: python3 main2.py <пути к файлам через пробел> --report <название отчета>')
        exit(1)

    if args.report == 'payout':
        for i in range(len(args.files)):
            print(f"Отчет {i+1}")
            report = Report(args.files[i])
            print(report.payout)
    else:
        print('Нет такого отчета в функционале')


if __name__ == "__main__":
    main()
