# ---------------------------------------------
# Program by @developer_telegrams
# Accounts Management
#
# Version   Date        Info
# 1.0       2024    Initial Version
#
# ---------------------------------------------
from datetime import datetime
from typing import Dict, Any, Optional, List

from sqlalchemy import Column, Integer, String, Boolean, DateTime, select, insert, update, delete

from settings import Base
from src.utils._logger import logger_msg


class Accounts(Base):
    """Таблица для хранения учетных записей для автоматизации selenium"""
    __tablename__ = 'accounts'

    id_pk = Column(Integer, primary_key=True, nullable=False)

    name = Column(String, nullable=False, unique=True, comment="Имя аккаунта")

    login = Column(String, nullable=False, unique=True, comment="Логин для входа")

    # Статус активности аккаунта
    status = Column(Boolean, default=True, nullable=False, comment="Активен ли аккаунт")
    
    # Текстовый статус для записи ошибок
    status_text = Column(String, nullable=True, comment="Текстовое описание статуса/ошибок")
    
    # Название учетки Chrome
    chrome_profile = Column(String, nullable=False, comment="Название профиля Chrome")
    
    # Статус авторизации
    auth_status = Column(Boolean, default=False, nullable=False, comment="Авторизован ли аккаунт")
    
    # Дата создания записи
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Дата последнего обновления
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class AccountsCRUD:
    """Универсальные CRUD операции для таблицы аккаунтов"""
    
    def __init__(self, session_maker):
        self.session_maker = session_maker

    async def create(self, data: Dict[str, Any]) -> Optional[int]:
        """
        Создание новой записи
        
        Args:
            data: Словарь с данными для создания записи
            
        Returns:
            ID созданной записи или None при ошибке
        """
        try:
            async with self.session_maker() as session:
                # Добавляем timestamp создания
                data['created_at'] = datetime.utcnow()
                data['updated_at'] = datetime.utcnow()
                
                query = insert(Accounts).values(**data)
                result = await session.execute(query)
                await session.commit()
                
                # Получаем ID созданной записи
                return result.inserted_primary_key[0]
                
        except Exception as e:
            error_msg = f"AccountsCRUD create error: {e}"
            logger_msg(error_msg)
            return None

    async def read_by_id(self, account_id: int) -> Optional[Accounts]:
        """
        Получение записи по ID
        
        Args:
            account_id: ID записи
            
        Returns:
            Объект Accounts или None
        """
        try:
            async with self.session_maker() as session:
                query = select(Accounts).where(Accounts.id_pk == account_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
                
        except Exception as e:
            error_msg = f"AccountsCRUD read_by_id error: {e}"
            logger_msg(error_msg)
            return None

    async def read_by_filter(self, filters: Dict[str, Any]) -> List[Accounts]:
        """
        Получение записей по фильтрам
        
        Args:
            filters: Словарь с фильтрами для поиска
            
        Returns:
            Список объектов Accounts
        """
        try:
            async with self.session_maker() as session:
                query = select(Accounts).filter_by(**filters)
                result = await session.execute(query)
                return result.scalars().all()
                
        except Exception as e:
            error_msg = f"AccountsCRUD read_by_filter error: {e}"
            logger_msg(error_msg)
            return []

    async def read_all(self) -> List[Accounts]:
        """
        Получение всех записей
        
        Returns:
            Список всех объектов Accounts
        """
        try:
            async with self.session_maker() as session:
                query = select(Accounts)
                result = await session.execute(query)
                return result.scalars().all()
                
        except Exception as e:
            error_msg = f"AccountsCRUD read_all error: {e}"
            logger_msg(error_msg)
            return []

    async def update_by_id(self, account_id: int, data: Dict[str, Any]) -> bool:
        """
        Обновление записи по ID
        
        Args:
            account_id: ID записи для обновления
            data: Словарь с новыми данными
            
        Returns:
            True при успехе, False при ошибке
        """
        try:
            async with self.session_maker() as session:
                # Добавляем timestamp обновления
                data['updated_at'] = datetime.utcnow()
                
                query = update(Accounts).where(Accounts.id_pk == account_id).values(**data)
                result = await session.execute(query)
                await session.commit()
                
                return result.rowcount > 0
                
        except Exception as e:
            error_msg = f"AccountsCRUD update_by_id error: {e}"
            logger_msg(error_msg)
            return False

    async def update_by_filter(self, filters: Dict[str, Any], data: Dict[str, Any]) -> int:
        """
        Обновление записей по фильтрам
        
        Args:
            filters: Словарь с фильтрами для поиска записей
            data: Словарь с новыми данными
            
        Returns:
            Количество обновленных записей
        """
        try:
            async with self.session_maker() as session:
                # Добавляем timestamp обновления
                data['updated_at'] = datetime.utcnow()
                
                query = update(Accounts).filter_by(**filters).values(**data)
                result = await session.execute(query)
                await session.commit()
                
                return result.rowcount
                
        except Exception as e:
            error_msg = f"AccountsCRUD update_by_filter error: {e}"
            logger_msg(error_msg)
            return 0

    async def delete_by_id(self, account_id: int) -> bool:
        """
        Удаление записи по ID
        
        Args:
            account_id: ID записи для удаления
            
        Returns:
            True при успехе, False при ошибке
        """
        try:
            async with self.session_maker() as session:
                query = delete(Accounts).where(Accounts.id_pk == account_id)
                result = await session.execute(query)
                await session.commit()
                
                return result.rowcount > 0
                
        except Exception as e:
            error_msg = f"AccountsCRUD delete_by_id error: {e}"
            logger_msg(error_msg)
            return False

    async def delete_by_filter(self, filters: Dict[str, Any]) -> int:
        """
        Удаление записей по фильтрам
        
        Args:
            filters: Словарь с фильтрами для поиска записей
            
        Returns:
            Количество удаленных записей
        """
        try:
            async with self.session_maker() as session:
                query = delete(Accounts).filter_by(**filters)
                result = await session.execute(query)
                await session.commit()
                
                return result.rowcount
                
        except Exception as e:
            error_msg = f"AccountsCRUD delete_by_filter error: {e}"
            logger_msg(error_msg)
            return 0

    async def get_by_login(self, login: str) -> Optional[Accounts]:
        """
        Получение аккаунта по логину (телефону)
        
        Args:
            login: Телефон для поиска
            
        Returns:
            Объект Accounts или None
        """
        return await self.read_by_filter({'login': login})

    async def update_auth_status(self, login: str, auth_status: bool, status_text: str = None) -> bool:
        """
        Обновление статуса авторизации аккаунта
        
        Args:
            login: Телефон аккаунта
            auth_status: Новый статус авторизации
            status_text: Дополнительная информация о статусе
            
        Returns:
            True при успехе, False при ошибке
        """
        update_data = {'auth_status': auth_status}
        if status_text is not None:
            update_data['status_text'] = status_text
            
        result = await self.update_by_filter({'login': login}, update_data)
        return result > 0

    async def get_active_accounts(self) -> List[Accounts]:
        """
        Получение всех активных аккаунтов
        
        Returns:
            Список активных аккаунтов
        """
        return await self.read_by_filter({'status': True})

    async def get_authorized_accounts(self) -> List[Accounts]:
        """
        Получение всех авторизованных аккаунтов
        
        Returns:
            Список авторизованных аккаунтов
        """
        return await self.read_by_filter({'auth_status': True, 'status': True})
