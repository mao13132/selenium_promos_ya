# ---------------------------------------------
# Program by @developer_telegrams
# Tasks Management System
#
# Version   Date        Info
# 1.0       2024    Initial Version
#
# ---------------------------------------------
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, select, insert, update, delete

from settings import Base
from src.utils._logger import logger_msg


class TaskStatus(str, Enum):
    """Статусы задач"""
    PENDING = "pending"  # Ожидает выполнения
    RUNNING = "running"  # Выполняется
    COMPLETED = "completed"  # Завершена успешно
    FAILED = "failed"  # Завершена с ошибкой
    CANCELLED = "cancelled"  # Отменена


class Tasks(Base):
    """Таблица для хранения задач для алгоритма автоматизации"""
    __tablename__ = 'tasks'

    # Первичный ключ
    id_pk = Column(Integer, primary_key=True, nullable=False)

    # Название задачи
    title = Column(String(255), nullable=False, comment="Название задачи")

    # Описание задачи
    description = Column(Text, nullable=True, comment="Подробное описание задачи")

    # Тип задачи (для определения какой алгоритм использовать)
    task_type = Column(String(100), nullable=False, comment="Тип задачи для выбора алгоритма")

    account_id = Column(Integer, ForeignKey('accounts.id_pk'), nullable=True,
                        comment="ID аккаунта для выполнения задачи")

    # Статус задачи
    status = Column(String(20), nullable=False, default=TaskStatus.PENDING, comment="Статус выполнения задачи")

    # Результат выполнения задачи
    result = Column(Text, nullable=True, comment="Результат выполнения задачи")

    # Сообщение об ошибке (если есть)
    error_message = Column(Text, nullable=True, comment="Сообщение об ошибке")

    # Параметры задачи в JSON формате
    parameters = Column(Text, nullable=True, comment="Параметры задачи в JSON формате")

    # ID пользователя Telegram, создавшего задачу
    created_by_user_id = Column(String(50), nullable=True, comment="ID пользователя Telegram")

    # Время начала выполнения
    started_at = Column(DateTime, nullable=True, comment="Время начала выполнения")

    # Время завершения
    completed_at = Column(DateTime, nullable=True, comment="Время завершения")

    # Дата создания записи
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, comment="Дата создания")

    # Дата последнего обновления
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow,
                        comment="Дата обновления")

    # Активность задачи
    is_active = Column(Boolean, default=True, nullable=False, comment="Активна ли задача")


class TasksCRUD:
    """Универсальные CRUD операции для таблицы задач"""

    def __init__(self, session_maker):
        """Инициализация CRUD с фабрикой сессий"""
        self.session_maker = session_maker

    async def create(self, data: Dict[str, Any]) -> Optional[int]:
        """
        Создание новой задачи
        
        Args:
            data: Словарь с данными для создания задачи
            
        Returns:
            ID созданной задачи или None при ошибке
        """
        try:
            async with self.session_maker() as session:
                # Добавляем timestamp создания
                data['created_at'] = datetime.utcnow()
                data['updated_at'] = datetime.utcnow()

                query = insert(Tasks).values(**data)
                result = await session.execute(query)
                await session.commit()

                # Получаем ID созданной записи
                return result.inserted_primary_key[0]

        except Exception as e:
            error_msg = f"TasksCRUD create error: {e}"
            logger_msg(error_msg)
            return None

    async def read_by_id(self, task_id: int) -> Optional[Tasks]:
        """
        Получение задачи по ID
        
        Args:
            task_id: ID задачи
            
        Returns:
            Объект Tasks или None
        """
        try:
            async with self.session_maker() as session:
                query = select(Tasks).where(Tasks.id_pk == task_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()

        except Exception as e:
            error_msg = f"TasksCRUD read_by_id error: {e}"
            logger_msg(error_msg)
            return None

    async def read_by_filter(self, filters: Dict[str, Any]) -> List[Tasks]:
        """
        Получение задач по фильтрам
        
        Args:
            filters: Словарь с фильтрами для поиска
            
        Returns:
            Список объектов Tasks
        """
        try:
            async with self.session_maker() as session:
                query = select(Tasks).filter_by(**filters)
                result = await session.execute(query)
                return result.scalars().all()

        except Exception as e:
            error_msg = f"TasksCRUD read_by_filter error: {e}"
            logger_msg(error_msg)
            return []

    async def read_all(self) -> List[Tasks]:
        """
        Получение всех задач
        
        Returns:
            Список всех объектов Tasks
        """
        try:
            async with self.session_maker() as session:
                query = select(Tasks)
                result = await session.execute(query)
                return result.scalars().all()

        except Exception as e:
            error_msg = f"TasksCRUD read_all error: {e}"
            logger_msg(error_msg)
            return []

    async def update_by_id(self, task_id: int, data: Dict[str, Any]) -> bool:
        """
        Обновление задачи по ID
        
        Args:
            task_id: ID задачи для обновления
            data: Словарь с новыми данными
            
        Returns:
            True при успехе, False при ошибке
        """
        try:
            async with self.session_maker() as session:
                # Добавляем timestamp обновления
                data['updated_at'] = datetime.utcnow()

                query = update(Tasks).where(Tasks.id_pk == task_id).values(**data)
                result = await session.execute(query)
                await session.commit()

                return result.rowcount > 0

        except Exception as e:
            error_msg = f"TasksCRUD update_by_id error: {e}"
            logger_msg(error_msg)
            return False

    async def update_by_filter(self, filters: Dict[str, Any], data: Dict[str, Any]) -> int:
        """
        Обновление задач по фильтрам
        
        Args:
            filters: Словарь с фильтрами для поиска задач
            data: Словарь с новыми данными
            
        Returns:
            Количество обновленных записей
        """
        try:
            async with self.session_maker() as session:
                # Добавляем timestamp обновления
                data['updated_at'] = datetime.utcnow()

                query = update(Tasks).filter_by(**filters).values(**data)
                result = await session.execute(query)
                await session.commit()

                return result.rowcount

        except Exception as e:
            error_msg = f"TasksCRUD update_by_filter error: {e}"
            logger_msg(error_msg)
            return 0

    async def delete_by_id(self, task_id: int) -> bool:
        """
        Удаление задачи по ID
        
        Args:
            task_id: ID задачи для удаления
            
        Returns:
            True при успехе, False при ошибке
        """
        try:
            async with self.session_maker() as session:
                query = delete(Tasks).where(Tasks.id_pk == task_id)
                result = await session.execute(query)
                await session.commit()

                return result.rowcount > 0

        except Exception as e:
            error_msg = f"TasksCRUD delete_by_id error: {e}"
            logger_msg(error_msg)
            return False

    async def delete_by_filter(self, filters: Dict[str, Any]) -> int:
        """
        Удаление задач по фильтрам
        
        Args:
            filters: Словарь с фильтрами для поиска задач
            
        Returns:
            Количество удаленных записей
        """
        try:
            async with self.session_maker() as session:
                query = delete(Tasks).filter_by(**filters)
                result = await session.execute(query)
                await session.commit()

                return result.rowcount

        except Exception as e:
            error_msg = f"TasksCRUD delete_by_filter error: {e}"
            logger_msg(error_msg)
            return 0

    # Специализированные методы для работы с задачами

    async def get_pending_tasks(self) -> List[Tasks]:
        """
        Получение всех задач в ожидании выполнения
        
        Returns:
            Список задач со статусом PENDING
        """
        return await self.read_by_filter({
            'status': TaskStatus.PENDING,
            'is_active': True
        })

    async def get_running_tasks(self) -> List[Tasks]:
        """
        Получение всех выполняющихся задач
        
        Returns:
            Список задач со статусом RUNNING
        """
        return await self.read_by_filter({
            'status': TaskStatus.RUNNING,
            'is_active': True
        })

    async def get_tasks_by_user(self, user_id: str) -> List[Tasks]:
        """
        Получение всех задач пользователя
        
        Args:
            user_id: ID пользователя Telegram
            
        Returns:
            Список задач пользователя
        """
        return await self.read_by_filter({
            'created_by_user_id': user_id,
            'is_active': True
        })

    async def get_tasks_by_type(self, task_type: str) -> List[Tasks]:
        """
        Получение задач по типу
        
        Args:
            task_type: Тип задачи
            
        Returns:
            Список задач указанного типа
        """
        return await self.read_by_filter({
            'task_type': task_type,
            'is_active': True
        })

    async def update_task_status(self, task_id: int, status: str, error_message: str = None) -> bool:
        """
        Обновление статуса задачи
        
        Args:
            task_id: ID задачи
            status: Новый статус
            error_message: Сообщение об ошибке (опционально)
            
        Returns:
            True при успехе, False при ошибке
        """
        update_data = {'status': status}

        # Устанавливаем время в зависимости от статуса
        if status == TaskStatus.RUNNING:
            update_data['started_at'] = datetime.utcnow()
        elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            update_data['completed_at'] = datetime.utcnow()
            update_data['is_active'] = False

        if error_message:
            update_data['error_message'] = error_message
            update_data['is_active'] = False

        return await self.update_by_id(task_id, update_data)

    async def start_task(self, task_id: int) -> bool:
        """
        Запуск задачи (изменение статуса на RUNNING)
        
        Args:
            task_id: ID задачи
            
        Returns:
            True при успехе, False при ошибке
        """
        return await self.update_task_status(task_id, TaskStatus.RUNNING)

    async def complete_task(self, task_id: int, result: str = None) -> bool:
        """
        Завершение задачи успешно
        
        Args:
            task_id: ID задачи
            result: Результат выполнения
            
        Returns:
            True при успехе, False при ошибке
        """
        update_data = {
            'status': TaskStatus.COMPLETED,
            'is_active': False,
            'completed_at': datetime.utcnow()
        }

        if result:
            update_data['result'] = result

        return await self.update_by_id(task_id, update_data)

    async def fail_task(self, task_id: int, error_message: str) -> bool:
        """
        Завершение задачи с ошибкой
        
        Args:
            task_id: ID задачи
            error_message: Сообщение об ошибке
            
        Returns:
            True при успехе, False при ошибке
        """
        return await self.update_task_status(task_id, TaskStatus.FAILED, error_message)

    async def cancel_task(self, task_id: int) -> bool:
        """
        Отмена задачи
        
        Args:
            task_id: ID задачи
            
        Returns:
            True при успехе, False при ошибке
        """
        return await self.update_task_status(task_id, TaskStatus.CANCELLED)

    async def get_tasks_by_priority(self, priority: str) -> List[Tasks]:
        """
        Получение задач по приоритету
        
        Args:
            priority: Приоритет задачи
            
        Returns:
            Список задач с указанным приоритетом
        """
        return await self.read_by_filter({
            'priority': priority,
            'is_active': True
        })

    async def get_tasks_by_account(self, account_id: int) -> List[Tasks]:
        """
        Получение задач по ID аккаунта
        
        Args:
            account_id: ID аккаунта
            
        Returns:
            Список задач для указанного аккаунта
        """
        return await self.read_by_filter({
            'account_id': account_id,
            'is_active': True
        })

    async def assign_task_to_account(self, task_id: int, account_id: int) -> bool:
        """
        Назначение задачи на аккаунт
        
        Args:
            task_id: ID задачи
            account_id: ID аккаунта
            
        Returns:
            True при успехе, False при ошибке
        """
        return await self.update_by_id(task_id, {'account_id': account_id})

    async def get_unassigned_tasks(self) -> List[Tasks]:
        """
        Получение задач без назначенного аккаунта
        
        Returns:
            Список задач без назначенного аккаунта
        """
        return await self.read_by_filter({
            'account_id': None,
            'is_active': True
        })
