import unittest
import datetime
from unittest.mock import patch, MagicMock, mock_open
from io import StringIO
from main import IOWorker, main


class TestIOWorker(unittest.TestCase):

    def setUp(self):
        self.database = MagicMock()
        self.worker = IOWorker(self.database)

    @patch('builtins.input', side_effect=['title', 'description', 'category', '01.01.2025', 'средний', 'не выполнена'])
    def test_get_task_params_valid(self, mock_input):
        expected_params = {
            "title": "title",
            'description': "description",
            'category': "category",
            'due_date': datetime.date(2025, 1, 1),
            'priority': "средний",
            'status': "не выполнена"
        }
        result = self.worker.get_task_params()
        self.assertEqual(result, expected_params)

    @patch('builtins.input', side_effect=['', '', '', '', '', ''])
    def test_get_task_params_empty(self, mock_input):
        result = self.worker.get_task_params()
        self.assertEqual(result, {})

    @patch('builtins.input', side_effect=['', '', '', 'invalid_date', '', ''])
    def test_get_task_params_invalid_date(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = self.worker.get_task_params()
            self.assertIsNone(result)
            self.assertIn("Введите корректный срок выполнения", fake_out.getvalue())

    @patch('builtins.input', side_effect=['title', 'description', 'category', '01.01.2023', 'средний', 'не выполнена'])
    def test_get_task_params_past_date(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = self.worker.get_task_params()
            self.assertIsNone(result)
            self.assertIn("Срок выполнения задачи не корректен", fake_out.getvalue())

    @patch('builtins.input',
           side_effect=['title', 'description', 'category', '01.01.2025', 'invalid_priority', 'не выполнена'])
    def test_get_task_params_invalid_priority(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = self.worker.get_task_params()
            self.assertIsNone(result)
            self.assertIn("Введите корректный приоритет", fake_out.getvalue())

    @patch('builtins.input',
           side_effect=['title', 'description', 'category', '01.01.2025', 'средний', 'invalid_status'])
    def test_get_task_params_invalid_status(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = self.worker.get_task_params()
            self.assertIsNone(result)
            self.assertIn("Введите корректный статус", fake_out.getvalue())

    @patch('builtins.input', side_effect=['title', 'description', 'category', '01.01.2025', 'средний'])
    def test_add_task_valid(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.add_task()
            self.database.add_task.assert_called_once_with('title', 'description', 'category',
                                                           datetime.date(2025, 1, 1), 'средний')
            self.assertIn("Задача добавлена", fake_out.getvalue())

    @patch('builtins.input', side_effect=['title', 'description', 'category', '01.01.2023', 'средний'])
    def test_add_task_past_date(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.add_task()
            self.database.add_task.assert_not_called()
            self.assertIn("Срок выполнения задачи не корректен", fake_out.getvalue())

    @patch('builtins.input', side_effect=['1'])
    def test_delete_task_valid(self, mock_input):
        self.database.delete_task.return_value = True
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.delete_task()
            self.database.delete_task.assert_called_once_with(1)
            self.assertIn("Задача с id: 1 удалена", fake_out.getvalue())

    @patch('builtins.input', side_effect=['invalid'])
    def test_delete_task_invalid_id(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.delete_task()
            self.database.delete_task.assert_not_called()
            self.assertIn("id введен некорректно", fake_out.getvalue())

    @patch('builtins.input', side_effect=['1'])
    def test_delete_task_not_found(self, mock_input):
        self.database.delete_task.return_value = False
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.delete_task()
            self.database.delete_task.assert_called_once_with(1)
            self.assertIn("Задача с id: 1 не найдена", fake_out.getvalue())

    @patch('builtins.input', side_effect=['title', 'description', 'category', '01.01.2025', 'средний', 'не выполнена'])
    def test_search_task(self, mock_input):
        self.database.search_task.return_value = [{'id': 1, 'title': 'title'}]
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.search_task()
            self.database.search_task.assert_called_once_with(
                title='title', description='description', category='category', due_date=datetime.date(2025, 1, 1),
                priority='средний', status='не выполнена'
            )
            self.assertIn("{'id': 1, 'title': 'title'}", fake_out.getvalue())

    @patch('builtins.input',
           side_effect=['1', 'title', 'description', 'category', '01.01.2025', 'средний', 'не выполнена'])
    def test_update_task_valid(self, mock_input):
        self.database.update_task_info.return_value = True
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.update_task()
            self.database.update_task_info.assert_called_once_with(
                1, title='title', description='description', category='category', due_date=datetime.date(2025, 1, 1),
                priority='средний', status='не выполнена'
            )
            self.assertIn("Задача успешно изменена", fake_out.getvalue())

    @patch('builtins.input',
           side_effect=['invalid', 'title', 'description', 'category', '01.01.2025', 'средний', 'не выполнена'])
    def test_update_task_invalid_id(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.update_task()
            self.database.update_task_info.assert_not_called()
            self.assertIn("Введите корректный id задачи", fake_out.getvalue())

    @patch('builtins.input',
           side_effect=['1', 'title', 'description', 'category', '01.01.2025', 'средний', 'не выполнена'])
    def test_update_task_not_found(self, mock_input):
        self.database.update_task_info.return_value = False
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.update_task()
            self.database.update_task_info.assert_called_once_with(
                1, title='title', description='description', category='category', due_date=datetime.date(2025, 1, 1),
                priority='средний', status='не выполнена'
            )
            self.assertIn("Введен id несуществующей задачи", fake_out.getvalue())

    @patch('builtins.input', side_effect=['1', 'выполнена'])
    def test_update_task_status_valid(self, mock_input):
        self.database.update_task_status.return_value = True
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.update_task_status()
            self.database.update_task_status.assert_called_once_with(1, 'выполнена')
            self.assertIn("Статус задачи с id: 1 изменен на выполнена", fake_out.getvalue())

    @patch('builtins.input', side_effect=['invalid', 'выполнена'])
    def test_update_task_status_invalid_id(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.update_task_status()
            self.database.update_task_status.assert_not_called()
            self.assertIn("ID не корректен", fake_out.getvalue())

    @patch('builtins.input', side_effect=['1', 'invalid_status'])
    def test_update_task_status_invalid_status(self, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.update_task_status()
            self.database.update_task_status.assert_not_called()
            self.assertIn("Введите корректный статус", fake_out.getvalue())

    @patch('builtins.input', side_effect=['1', 'выполнена'])
    def test_update_task_status_not_found(self, mock_input):
        self.database.update_task_status.return_value = False
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.update_task_status()
            self.database.update_task_status.assert_called_once_with(1, 'выполнена')
            self.assertIn("Задача с id: 1 не найдена", fake_out.getvalue())

    def test_show_all_tasks_empty(self):
        self.database.tasks = []
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.show_all_tasks()
            self.assertIn("Задач нет", fake_out.getvalue())

    def test_show_all_tasks_non_empty(self):
        self.database.tasks = [{'id': 1, 'title': 'title'}]
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.worker.show_all_tasks()
            self.assertIn("{'id': 1, 'title': 'title'}", fake_out.getvalue())

    @patch('builtins.input', side_effect=['7'])
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='[]')
    def test_main_exit(self, mock_open, mock_exists, mock_input):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with self.assertRaises(SystemExit):
                main()
            self.assertIn("Меню:", fake_out.getvalue())


if __name__ == '__main__':
    unittest.main()
