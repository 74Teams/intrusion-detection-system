from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class RuleModel(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sid = Column(Integer, unique=True, nullable=False, index=True)
    rev = Column(Integer, default=1)
    action = Column(String(10), default="alert")
    protocol = Column(String(10), nullable=False)
    src_ip = Column(String(50), default="any")
    src_port = Column(String(20), default="any")
    direction = Column(String(5), default="->")
    dst_ip = Column(String(50), default="any")
    dst_port = Column(String(20), default="any")
    msg = Column(String(255), nullable=False)
    classtype = Column(String(50), nullable=True)
    severity = Column(Integer, default=2)
    raw_rule = Column(Text, nullable=False)
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    events = relationship("EventModel", back_populates="rule")

class EventModel(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    rule_id = Column(Integer, ForeignKey("rules.id"), nullable=True)
    sid = Column(Integer, nullable=True)
    source_type = Column(String(20), default="RULE_ENGINE")  
    attack_type = Column(String(100), nullable=False)
    severity = Column(Integer, nullable=False)
    src_ip = Column(String(45), nullable=False)
    src_port = Column(Integer, nullable=True)
    dst_ip = Column(String(45), nullable=False)
    dst_port = Column(Integer, nullable=True)
    protocol = Column(String(10), nullable=False)
    http_method = Column(String(10), nullable=True)
    http_uri = Column(Text, nullable=True)
    summary = Column(Text, nullable=False)
    status = Column(String(20), default="NEW")

    rule = relationship("RuleModel", back_populates="events")
    payload = relationship("EventPayloadModel", back_populates="event", uselist=False)

class EventPayloadModel(Base):
    __tablename__ = "event_payloads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    matched_content = Column(Text, nullable=True)
    http_headers = Column(Text, nullable=True)
    http_body = Column(Text, nullable=True)
    packet_raw_hex = Column(Text, nullable=True)

    event = relationship("EventModel", back_populates="payload")
