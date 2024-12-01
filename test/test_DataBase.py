import unittest
import tempfile
import json
import os
from datetime import date
from database.database import DataBase


class TestDataBase(unittest.TestCase):

    def setUp(self):
        # Создаем временный файл для тестирования
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.db = DataBase(file_path=self.temp_file.name)

    def tearDown(self):
        # Удаляем временный файл после тестирования
        os.remove(self.temp_file.name)

    def test_init(self):
        self.assertEqual(self.db.file_path, self.temp_file.name)
        self.assertEqual(self.db.tasks, [])
        self.assertEqual(self.db.next_id, 1)

    def test_load_tasks(self):
        # Создаем временный файл с задачами
        with open(self.temp_file.name, 'w', encoding='utf-8') as file:
            json.dump([
                {"id": 1, "title": "Task 1", "description": "Description 1", "category": "Category 1",
                 "due_date": "2023-12-01", "priority": "high", "status": "not done"},
                {"id": 2, "title": "Task 2", "description": "Description 2", "category": "Category 2",
                 "due_date": "2023-12-02", "priority": "medium", "status": "not done"}
            ], file)

        db = DataBase(file_path=self.temp_file.name)
        self.assertEqual(len(db.tasks), 2)
        self.assertEqual(db.tasks[0].task_id, 1)
        self.assertEqual(db.tasks[1].task_id, 2)

    def test_get_next_id(self):
        # Создаем временный файл с задачами
        with open(self.temp_file.name, 'w', encoding='utf-8') as file:
            json.dump([
                {"id": 1, "title": "Task 1", "description": "Description 1", "category": "Category 1",
                 "due_date": "2023-12-01", "priority": "high", "status": "not done"},
                {"id": 2, "title": "Task 2", "description": "Description 2", "category": "Category 2",
                 "due_date": "2023-12-02", "priority": "medium", "status": "not done"}
            ], file)

        db = DataBase(file_path=self.temp_file.name)
        self.assertEqual(db.next_id, 3)

    def test_save_tasks(self): #err
        db = DataBase(file_path=self.temp_file.name)
        db.add_task("Task 1", "Description 1", "Category 1", date(2023, 12, 1), "high")
        db.save_tasks()

        with open(self.temp_file.name, 'r', encoding='utf-8') as file:
            tasks = json.load(file)
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0]['title'], "Task 1")

    def test_add_task(self):
        db = DataBase(file_path=self.temp_file.name)
        db.add_task("Task 1", "Description 1", "Category 1", date(2023, 12, 1), "high")
        self.assertEqual(len(db.tasks), 1)
        self.assertEqual(db.tasks[0].title, "Task 1")

    def test_delete_task(self):
        db = DataBase(file_path=self.temp_file.name)
        db.add_task("Task 1", "Description 1", "Category 1", date(2023, 12, 1), "high")
        db.add_task("Task 2", "Description 2", "Category 2", date(2023, 12, 2), "medium")
        self.assertEqual(len(db.tasks), 2)

        db.delete_task(1)
        self.assertEqual(len(db.tasks), 1)
        self.assertEqual(db.tasks[0].title, "Task 2")

    def test_search_task(self):
        db = DataBase(file_path=self.temp_file.name)
        db.add_task("Task 1", "Description 1", "Category 1", date(2023, 12, 1), "high")
        db.add_task("Task 2", "Description 2", "Category 2", date(2023, 12, 2), "medium")

        results = db.search_task(category="Category 1")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Task 1")

    def test_update_task_info(self):
        db = DataBase(file_path=self.temp_file.name)
        db.add_task("Task 1", "Description 1", "Category 1", date(2023, 12, 1), "high")

        db.update_task_info(1, title="Updated Task 1")
        self.assertEqual(db.tasks[0].title, "Updated Task 1")

    def test_update_task_status(self):
        db = DataBase(file_path=self.temp_file.name)
        db.add_task("Task 1", "Description 1", "Category 1", date(2023, 12, 1), "high")

        db.update_task_status(1, "done")
        self.assertEqual(db.tasks[0].status, "done")


if __name__ == '__main__':
    unittest.main()
