from sqlalchemy import Column, Float, Integer, String, DateTime
from sqlalchemy.sql import func
from backend.models.database import Base


class UsageRecord(Base):
    __tablename__ = "usage_records"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String, index=True)  # EC2/S3/Lambda/DataTransfer
    resource_id = Column(String, nullable=True)
    instance_type = Column(String, nullable=True)
    hours_used = Column(Float, default=0)
    cpu_utilization = Column(Float, default=0)
    storage_gb = Column(Float, default=0)
    requests = Column(Float, default=0)
    invocations = Column(Float, default=0)
    duration = Column(Float, default=0)
    bandwidth = Column(Float, default=0)
    cost = Column(Float, default=0)
    usage_date = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
