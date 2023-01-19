from typing import Any, List
from flask import abort
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()
ma = Marshmallow()


def insert(obj: Any) -> int:
    try:
        db.session.add(obj)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        abort(500, description=str(err))
    return obj.id


def insert_many(objs: List[Any]) -> None:
    try:
        db.session.add_all(objs)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        abort(500, description=str(err))


def delete(obj: Any) -> None:
    try:
        db.session.delete(obj)
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        abort(500, description=str(err))


def delete_many(objs: Any) -> None:
    for obj in objs:
        try:
            db.session.delete(obj)
        except SQLAlchemyError as err:
            db.session.rollback()
            abort(500, description=str(err))
    db.session.commit()


def commit() -> None:
    try:
        db.session.commit()
    except SQLAlchemyError as err:
        db.session.rollback()
        abort(500, description=str(err))
