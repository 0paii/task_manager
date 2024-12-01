from datetime import date


class Task:
    def __init__(self, task_id: int, title: str, description: str, category: str, due_date: date, priority: str, status: str):
        """
        Метод __init__
        :param task_id: id задачи
        :param title: название задачи
        :param description: описание задачи
        :param category: категория задачи
        :param due_date: срок выполнения
        :param priority: приоритет задачи (низкий, средний, высокий)
        :param status: статус задачи (выполнена, не выполнена)
        """
        self.task_id = task_id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def __str__(self):
        """
        Метод __str__
        :return: str
        """
        return (f"ID: {self.task_id}, "
                f"Название: {self.title}, "
                f"Описание: {self.description}, "
                f"Категория: {self.category}, "
                f"Дата выполнения: {self.due_date}, "
                f"Приоритет: {self.priority}, "
                f"Статус: {self.status}")

    def search(self, **kwargs) -> bool:
        """
        Метод search
        :param kwargs: словарь, содержащий поля, по которым производится поиск
        :return: bool, True если задача была найдена, False если не найдена
        """
        if all(value is None for value in kwargs.values()):  # Проверка на пустой словарь
            return False
        result = True
        for key, value in kwargs.items():
            if value is not None:  # Проверка на пустоту значения
                if key == 'id':
                    result = self.__dict__.get(key) == int(value) and result
                elif key == 'due_date':
                    result = self.__dict__.get(key) == value and result
                else:
                    result = self.__dict__.get(key).lower() == value.lower() and result
        return result
