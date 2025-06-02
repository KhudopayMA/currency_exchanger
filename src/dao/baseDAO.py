# from fastapi import status
# from fastapi.exceptions import HTTPException
# from sqlalchemy import select, insert, Result, Sequence, Row, RowMapping
# from sqlalchemy.exc import SQLAlchemyError
#
# from src.database.database import DataBase
# from src.model.base import Base
#
#
# class BaseDAO:
#     model: type[Base]
#
#     @classmethod
#     async def create(cls, **kwargs):
#         try:
#             async with DataBase.session() as session:
#                 statement = insert(cls.model).values(kwargs).returning(cls.model)
#                 result = await session.execute(statement)
#                 await session.commit()
#                 return result.all()
#         except SQLAlchemyError as e:
#             print(str(e))
#             # todo logger
#             raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
#
#     @classmethod
#     async def read(cls):
#         try:
#             async with DataBase.session() as session:
#                 statement = select(cls.model).order_by(cls.model.id)
#                 result: Result = await session.execute(statement)
#                 rows = result.scalars().all()
#                 return rows
#         except SQLAlchemyError:
#             # todo logger
#             raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
#
#     @classmethod
#     async def update(cls):
#         pass
#
#     @classmethod
#     async def delete(cls):
#         pass

