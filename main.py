import sys
from datetime import date, datetime
from os.path import exists
from database.database import DataBase


class IOWorker:
    """
    Класс обработчика данных базы

    Attributes:
        database (DataBase): Объект базы
    """

    def __init__(self, database):
        """
        Конструктор класса IOWorker

        :param database: Объект базы
        """
        self.database = database

    def get_task_params(self):
        """
        Метод, запрашивающий у пользователя параметры задачи.

        Метод запрашивает у пользователя название, описание, категорию, срок выполнения, приоритет и статус
        задачи. Все параметры являются необязательными. Затем он создает словарь из полученных параметров.
        Если параметры не корректны, выводятся соответствующие сообщения об ошибках.
        Если параметры корректны, они возвращаются в виде словаря.

        :return: dict, словарь с параметрами задачи
        """
        try:
            title = input("Введите название задачи (опционально): ").lower()
            description = input("Введите описание задачи (опционально): ").lower()
            category = input("Введите категорию задачи (опционально): ").lower()
            due_date = input("Введите срок выполнения задачи (дд.мм.гггг) (опционально): ")
            if due_date and datetime.strptime(due_date, '%d.%m.%Y').date() < date.today():
                print("\nСрок выполнения задачи не корректен\n")
                return
            priority = input("Введите приоритет задачи (низкий, средний, высокий) (опционально): ").lower()
            if priority and priority not in ["низкий", "средний", "высокий"]:
                print("\nВведите корректный приоритет\n")
                return
            status = input("Введите статус задачи (выполнена, не выполнена) (опционально): ").lower()
            if status and status not in ["выполнена", "не выполнена"]:
                print("\nВведите корректный статус\n")
                return
            params = {
                "title": title if title else None,
                'description': description if description else None,
                'category': category if category else None,
                'due_date': datetime.strptime(due_date, '%d.%m.%Y').date() if due_date else None,
                'priority': priority if priority else None,
                'status': status if status else None
            }
            return {k: v for k, v in params.items() if v is not None}
        except AttributeError:
            print("\nОшибка данных\n")
        except ValueError:
            print("\nВведите корректный срок выполнения\n")

    def add_task(self):
        """
        Метод для добавления задачи в базу.

        Запрашивает у пользователя название, описание, категорию, срок выполнения и приоритет задачи.
        Проверяет корректность введенного срока выполнения. Если данные корректны,
        добавляет задачу в базу и выводит сообщение об успешном добавлении.
        В случае ошибки выводит соответствующее сообщение.

        :return: None
        """
        try:
            title = input("Введите название задачи: ").lower()
            description = input("Введите описание задачи: ").lower()
            category = input("Введите категорию задачи: ").lower()
            due_date = datetime.strptime(input("Введите срок выполнения задачи (дд.мм.гггг): "), '%d.%m.%Y').date()
            if due_date <= date.today():
                print("\nСрок выполнения задачи не корректен\n")
                return
            priority = input("Введите приоритет задачи (низкий, средний, высокий): ").lower()
            if priority not in ["низкий", "средний", "высокий"]:
                print("\nВведите корректный приоритет\n")
                return
            self.database.add_task(title, description, category, due_date, priority)
            print("\nЗадача добавлена.\n")
        except AttributeError:
            print("\nДанные задачи не корректны\n")
        except ValueError:
            print("\nВведите корректный срок выполнения\n")

    def delete_task(self):
        """
        Метод, удаляющий задачу из базы задач.

        :return: None
        """
        try:
            task_id = int(input("Введите id задачи для удаления: "))
            if self.database.delete_task(task_id):
                print(f"\nЗадача с id: {task_id} удалена.\n")
            else:
                print(f"\nЗадача с id: {task_id} не найдена.\n")
        except ValueError:
            print("\nid введен некорректно\n")

    def search_task(self):
        """
        Метод, выполняющий поиск задачи по заданным критериям.

        Этот метод запрашивает у пользователя название, описание, категорию, срок выполнения, приоритет и статус
        задачи, которые могут быть использованы в качестве критериев поиска.
        Все параметры являются необязательными. Затем он вызывает метод
        search_task из объекта базы с указанными параметрами.
        Если найдены подходящие задачи, они выводятся на экран.

        :return: None
        """
        search_params = self.get_task_params()
        result = self.database.search_task(**search_params)
        if result:
            for task in result:
                print(task)
        else:
            print("\nЗадач не найдено\n")

    def update_task(self):
        """
        Метод для изменения задачи в базе.

        Метод запрашивает у пользователя ID задачи и новые данные для ее изменения.
        Если данные введены некорректно, выводится соответствующее сообщение.
        В противном случае, метод вызывает соответствующий метод базы для изменения задачи.
        Если задача изменена успешно, выводится подтверждающее сообщение.
        Если задача с указанным ID не найдена, выводится соответствующее сообщение об ошибке.

        :return: None
        """
        try:
            task_id = int(input("Введите ID задачи для изменения: "))
            change_params = self.get_task_params()
            if change_params:
                if self.database.update_task_info(task_id, **change_params):
                    print("\nЗадача успешно изменена\n")
                else:
                    print("\nВведен id несуществующей задачи\n")
        except ValueError:
            print("\nВведите корректный id задачи\n")

    def update_task_status(self):
        """
        Изменяет статус задачи в базе.

        Метод запрашивает у пользователя ID задачи и новый статус ('Выполнена' или 'Не выполнена').
        Если статус введен некорректно, выводится сообщение об ошибке.
        В противном случае, метод вызывает соответствующий метод библиотеки для изменения статуса задачи.
        Если задача найдена и статус изменен успешно, выводится подтверждающее сообщение.
        Если задача с указанным ID не найдена, выводится соответствующее сообщение об ошибке.

        :return: None
        """
        try:
            task_id = int(input("Введите ID задачи для изменения статуса: "))
            new_task_status = input("Введите новый статус ('Выполнена' или 'Не выполнена'): ").lower()
            if new_task_status not in ["выполнена", "не выполнена"]:
                print("\nВведите корректный статус\n")
            else:
                if self.database.update_task_status(task_id, new_task_status):
                    print(f"\nСтатус задачи с id: {task_id} изменен на {new_task_status}.\n")
                else:
                    print(f"\nЗадача с id: {task_id} не найдена.\n")
        except ValueError:
            print("\nID не корректен\n")

    def show_all_tasks(self):
        """
        Выводит на экран список всех задач базы.

        Метод сначала проверяет, не является ли список задач пустым.
        Если он пуст, выводится сообщение об этом.
        Если в базе есть задачи, то они выводятся на экран.

        :return: None
        """
        if not self.database.tasks:
            print("\nЗадач нет\n")
            return
        for task in self.database.tasks:
            print(task)


def main():
    """
    Главная функция программы.

    Создает объект класса DataBase, создает объект класса IOWorker, передавая ему
    созданный объект DataBase, и запускает основной цикл работы программы.

    В цикле отображается меню, пользователь выбирает пункты меню, и
    соответствующие методы объекта IOWorker вызываются.

    """
    if not exists("database.json"):
        open("database.json", "w+").close()
    database = DataBase()
    worker = IOWorker(database)
    while True:
        print("Меню:\n"
              "1. Добавить задачу.\n"
              "2. Удалить задачу.\n"
              "3. Изменить информацию о задачи.\n"
              "4. Изменить статус задачи.\n"
              "5. Отобразить все задачи.\n"
              "6. Найти задачу.\n"
              "7. Выход.\n"
              )
        choice = input("Выберите действие: ")
        match choice:
            case "1":
                worker.add_task()

            case "2":
                worker.delete_task()

            case "3":
                worker.update_task()

            case "4":
                worker.update_task_status()

            case "5":
                worker.show_all_tasks()

            case "6":
                worker.search_task()

            case "7":
                sys.exit()

            case _:
                print("\nПожалуйста выберите номер из меню ниже :)\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nДля этого есть отдельная функция, пожалуйста используйте её)\n")
