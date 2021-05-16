# coding=utf-8
from datetime import datetime

from flask import g
from sqlalchemy import Column, DateTime, Integer, desc

from marshmallow import Schema, fields
from NightGrassBackend.extentions import db


class TimestampMixin(object):
    """TimestampMixin
    时间戳扩展插件，便于快捷定义类信息
    """

    id = Column(Integer, autoincrement=True, primary_key=True)
    create_time = Column(DateTime, index=True, nullable=False, default=datetime.now)
    update_time = Column(
        DateTime,
        index=True,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
    )

    def to_dict(self, exclude=None):
        rst_dict = {}
        for column in self.__table__.columns:
            key = column.name
            if exclude and key in exclude:
                continue
            value = getattr(self, key)
            if isinstance(value, datetime):
                rst_dict[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                rst_dict[key] = value
        return rst_dict


class BaseSchema(Schema):
    """BaseSchema
    基础marchmallow 类，便于快速使用
    """

    id = fields.Integer(dump_only=True)
    create_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S", dump_only=True)
    update_time = fields.DateTime(format="%Y-%m-%d %H:%M:%S", dump_only=True)

    class Meta:
        strict = True


class MixCtlModel(object):
    """测试时使用"""

    @classmethod
    def db_add(cls, objlist):
        """
        在db中增加 对象
        Args:
            objlist:

        Returns:

        """
        res = []
        try:
            if isinstance(objlist, (list, tuple)):
                for _obj in objlist:
                    db.session.add(_obj)
                db.session.commit()
                for _obj in objlist:
                    _obj = db.session.merge(_obj)
                    res.append(_obj)
            else:
                db.session.add(objlist)
                db.session.commit()
                res = db.session.merge(objlist)
            return res
        except Exception as e:
            db.session.rollback()
            raise NameError(str(e))
        finally:
            pass
            # db.session.close()

    @classmethod
    def insert_one(cls, **kwargs):
        tmpdict = {k: v for k, v in kwargs.items() if hasattr(cls, k)}
        clsinstance = cls(**tmpdict)
        return cls.db_add(clsinstance)

    @classmethod
    def queryfirst(cls, desc_tag=False, **kwargs):
        # 如果所有都为空
        if not any(kwargs.values()):
            return None

        mt = cls.query
        tag = False
        for k, v in kwargs.items():
            if k and hasattr(cls, k):
                mt = mt.filter(getattr(cls, k) == v)
                tag = True
        # 防止所有的都为空
        if not tag:
            return None

        if desc_tag:
            mt = mt.order_by(desc(cls.id))
        try:
            # 默认采用倒叙
            res = mt.first()
            if not res:
                return None
            return res
        finally:
            pass
            # db.session.close()

    @classmethod
    def update(cls, updatedict={}, **kwargs):
        if not any(kwargs.values()):
            return False

        updata = {k: v for k, v in updatedict.items() if hasattr(cls, k)}
        if not updata:
            return False

        mt = cls.query
        tag = False
        for k, v in kwargs.items():
            if k and hasattr(cls, k):
                mt = mt.filter(getattr(cls, k) == v)
                tag = True

        if not tag:
            return False
        try:
            mt.update(updata)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
        finally:
            pass
            # db.session.close()

    @classmethod
    def delete(cls, **kwargs):
        """
        删除cls对象
        Args:
            **kwargs: Table表的列和值组成的字典
        Returns:
        """
        if not any(kwargs.values()):
            return False

        mt = cls.query
        tag = False
        for k, v in kwargs.items():
            if k and hasattr(cls, k):
                mt = mt.filter(getattr(cls, k) == v)
                tag = True

        if not tag:
            return False

        try:
            mt.delete(synchronize_session=False)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False

        finally:
            pass
            # dbconn.session.close()
