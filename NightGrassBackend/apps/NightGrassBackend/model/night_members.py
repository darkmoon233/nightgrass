# -*- coding: utf-8 -*-
from NightGrassBackend.apps.NightGrassBackend.model.base import TimestampMixin, MixCtlModel
from NightGrassBackend.extentions import db

from sqlalchemy import Column, Integer, String


class NightMembers(db.Model, TimestampMixin, MixCtlModel):
    __tablename__ = "nightgrass_test"
    __table_args__ = ({"mysql_engine": "InnoDB", "mysql_charset": "utf8"},)
    id = Column(Integer, nullable=False, default="", primary_key=True)
    name = Column(String(64), nullable=False, index=True)
