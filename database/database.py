import json
from task.task import Task
from typing import List
from datetime import date


class DataBase:
    """
    Класс DataBase, представляющий набор задач

    Attributes:
        file_path (str): путь к файлу с данными библиотеки
        _tasks (list): список задач
        _next_id (int): следующий id задачи

    """

    def __init__(self, file_path='database.json'):
        """
        Конструктор класса DataBase

        :param file_path: путь к файлу с данными
        """
        self.file_path = file_path
        self._tasks = self.load_tasks()
        self._next_id = self.get_next_id()

    @property
    def tasks(self) -> List[Task]:
        """
        Property, возвращающий список задач

        Returns:
            list: список задач
        """
        return self._tasks

    @property
    def next_id(self) -> int:
        """
        Property, возвращающий следующий id задачи

        Returns:
            int: следующий id задачи
        """
        return self._next_id

    def datetime_encoder(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        raise TypeError(f"Объект типа {type(obj).__name__} не сериализуем в формате JSON")

    def datetime_decoder(self, obj):
        try:
            return date.fromisoformat(obj)
        except (ValueError, TypeError):
            pass

    def load_tasks(self) -> List[Task]:
        """
        Метод, загружающий список задач из файла.

        :return: List[Task], Список задач
        """
        result = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            try:
                temp_result = json.load(file)
                for task in temp_result:
                    result.append(Task(task['id'],
                                       task['title'],
                                       task['description'],
                                       task['category'],
                                       self.datetime_decoder(task['due_date']),
                                       task['priority'],
                                       task['status']))
                return result
            except json.JSONDecodeError:
                return result

    def get_next_id(self) -> int:
        """
        Метод, возвращающий следующий id задачи.

        :return: int, следующий id задачи
        """
        return max([task.task_id for task in self._tasks], default=0) + 1

    def save_tasks(self):
        """
        Метод, сохраняющий список задач в файл

        Метод проходит по списку задач, создает из них словари,
        и сохраняет их в файле, указанном в self.file_path
        """
        result = []
        with open(self.file_path, 'w', encoding='utf-8') as file:
            for task in self.tasks:
                result.append({
                    "id": task.task_id,
                    "title": task.title,
                    "description": task.description,
                    "category": task.category,
                    "due_date": self.datetime_encoder(task.due_date),
                    "priority": task.priority,
                    "status": task.status
                })
            json.dump(result, file, ensure_ascii=False, indent=4)

    def add_task(self, task_title: str, task_description: str, task_category: str, task_due_date: date,
                 task_priority: str):
        """
        Метод, добавляющий задачу в список задач.

        :param task_title: str, название задачи
        :param task_description: str, описание задачи
        :param task_category: str, категория задачи
        :param task_due_date: date, срок выполнения задачи
        :param task_priority: str, приоритет задачи (низкий, средний, высокий)
        """
        task = Task(self._next_id, task_title, task_description, task_category, task_due_date, task_priority,
                    status='не выполнена')
        self._tasks.append(task)
        self._next_id += 1
        self.save_tasks()

    def delete_task(self, task_id: int) -> bool:
        """
        Метод, удаляющий задачу из базы задач.

        :param task_id: int, id задачи, которую нужно удалить
        :return: bool, True если задача была удалена, False если не найдена
        """
        for task in self._tasks:
            if task.task_id == task_id:
                self._tasks.remove(task)
                self.save_tasks()
                return True
        return False

    def search_task(self, **kwargs) -> List[Task]:
        """
        Метод, выполняющий поиск задач по заданным критериям.

        :param kwargs: словарь, содержащий поля, по которым производится поиск
        :return: list[Task], список задач, удовлетворяющих критериям поиска
        """
        results = [task for task in self._tasks if task.search(**kwargs)]
        return results

    def update_task_info(self, task_id: int, **kwargs) -> bool:
        """
        Метод, обновляющий информацию о задаче.

        :param task_id: int, id задачи, информацию о которой нужно обновить
        :param kwargs: dict, словарь, содержащий новые параметры
        :return: bool, True если задача была обновлена, False если не найдена
        """
        for task in self._tasks:
            if task.task_id == task_id:
                for key, value in kwargs.items():
                    setattr(task, key, value)
                self.save_tasks()
                return True
        return False

    def update_task_status(self, task_id: int, new_task_status: str) -> bool:
        """
        Метод, изменяющий статус задачи.

        :param task_id: int, id задачи, которую нужно изменить
        :param new_task_status: str, новый статус задачи
        :return: bool, True если задача была найдена и статус был изменен, False если не найдена
        """
        for task in self._tasks:
            if task.task_id == task_id:
                task.status = new_task_status
                self.save_tasks()
                return True
        return False
