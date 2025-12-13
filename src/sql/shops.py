# ---------------------------------------------
# Program by @developer_telegrams
# Shops Management
#
# Version   Date        Info
# 1.0       2025    Initial Version
#
# ---------------------------------------------
from datetime import datetime
from typing import Dict, Any, Optional, List

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, select, insert, update, delete

from settings import Base
from src.utils._logger import logger_msg


class Shops(Base):
    __tablename__ = 'shops'

    id_pk = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False, unique=True)
    percent_values = Column(Text, nullable=True)
    status = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class ShopsCRUD:
    def __init__(self, session_maker):
        self.session_maker = session_maker

    async def create(self, data: Dict[str, Any]) -> Optional[int]:
        try:
            async with self.session_maker() as session:
                data['created_at'] = datetime.utcnow()
                data['updated_at'] = datetime.utcnow()
                query = insert(Shops).values(**data)
                result = await session.execute(query)
                await session.commit()
                return result.inserted_primary_key[0]
        except Exception as e:
            logger_msg(f"ShopsCRUD create error: {e}")
            return None

    async def read_by_id(self, shop_id: int) -> Optional[Shops]:
        try:
            async with self.session_maker() as session:
                query = select(Shops).where(Shops.id_pk == shop_id)
                result = await session.execute(query)
                return result.scalar_one_or_none()
        except Exception as e:
            logger_msg(f"ShopsCRUD read_by_id error: {e}")
            return None

    async def read_by_filter(self, filters: Dict[str, Any]) -> List[Shops]:
        try:
            async with self.session_maker() as session:
                query = select(Shops).filter_by(**filters)
                result = await session.execute(query)
                return result.scalars().all()
        except Exception as e:
            logger_msg(f"ShopsCRUD read_by_filter error: {e}")
            return []

    async def read_all(self) -> List[Shops]:
        try:
            async with self.session_maker() as session:
                query = select(Shops)
                result = await session.execute(query)
                return result.scalars().all()
        except Exception as e:
            logger_msg(f"ShopsCRUD read_all error: {e}")
            return []

    async def update_by_id(self, shop_id: int, data: Dict[str, Any]) -> bool:
        try:
            async with self.session_maker() as session:
                data['updated_at'] = datetime.utcnow()
                query = update(Shops).where(Shops.id_pk == shop_id).values(**data)
                result = await session.execute(query)
                await session.commit()
                return result.rowcount > 0
        except Exception as e:
            logger_msg(f"ShopsCRUD update_by_id error: {e}")
            return False

    async def update_by_filter(self, filters: Dict[str, Any], data: Dict[str, Any]) -> int:
        try:
            async with self.session_maker() as session:
                data['updated_at'] = datetime.utcnow()
                query = update(Shops).filter_by(**filters).values(**data)
                result = await session.execute(query)
                await session.commit()
                return result.rowcount
        except Exception as e:
            logger_msg(f"ShopsCRUD update_by_filter error: {e}")
            return 0

    async def delete_by_id(self, shop_id: int) -> bool:
        try:
            async with self.session_maker() as session:
                query = delete(Shops).where(Shops.id_pk == shop_id)
                result = await session.execute(query)
                await session.commit()
                return result.rowcount > 0
        except Exception as e:
            logger_msg(f"ShopsCRUD delete_by_id error: {e}")
            return False

    async def delete_by_filter(self, filters: Dict[str, Any]) -> int:
        try:
            async with self.session_maker() as session:
                query = delete(Shops).filter_by(**filters)
                result = await session.execute(query)
                await session.commit()
                return result.rowcount
        except Exception as e:
            logger_msg(f"ShopsCRUD delete_by_filter error: {e}")
            return 0

    async def get_active_shops(self) -> List[Shops]:
        return await self.read_by_filter({'status': True})

    async def get_by_name(self, name: str) -> Optional[Shops]:
        try:
            shops = await self.read_by_filter({'name': name})
            return shops[0] if shops else None
        except Exception:
            return None

    async def update_percent_values(self, shop_id: int, percent_values: str) -> bool:
        return await self.update_by_id(shop_id, {'percent_values': percent_values})

