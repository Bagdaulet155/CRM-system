from django.test import TestCase
from .models import Item  # Импортируем модель для тестирования

class ItemModelTest(TestCase):
    
    # Тестируем создание объекта модели
    def test_item_creation(self):
        # Создаем новый объект модели Item
        item = Item.objects.create(name="Тестовая вещь")
        
        # Проверяем, что атрибут name правильно сохранен
        self.assertEqual(item.name, "Тестовая вещь")
        
        # Проверяем, что строковое представление объекта возвращает правильное имя
        self.assertEqual(str(item), "Тестовая вещь")
