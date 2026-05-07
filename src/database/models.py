"""Database models for IRCTC booking bot"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    """User account information"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Passenger(Base):
    """Passenger information for bookings"""
    __tablename__ = 'passengers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    berth_preference = Column(String(50))
    food_preference = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Passenger(name='{self.name}', age={self.age})>"


class BookingAttempt(Base):
    """Record of booking attempts"""
    __tablename__ = 'booking_attempts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    from_station = Column(String(50), nullable=False)
    to_station = Column(String(50), nullable=False)
    travel_date = Column(DateTime, nullable=False)
    train_number = Column(String(20))
    class_type = Column(String(50), nullable=False)
    quota = Column(String(50))
    num_passengers = Column(Integer, nullable=False)
    
    # Attempt tracking
    attempt_number = Column(Integer, default=1)
    status = Column(String(50), default='pending')  # pending, success, failed
    error_message = Column(Text)
    
    # PNR and booking info
    pnr = Column(String(20))
    booking_confirmation = Column(Text)
    
    # Timestamps
    booking_window_time = Column(DateTime)
    attempted_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime)
    
    def __repr__(self):
        return f"<BookingAttempt(train={self.train_number}, date={self.travel_date}, status='{self.status}')>"


class TrainInfo(Base):
    """Train information cache"""
    __tablename__ = 'train_info'

    id = Column(Integer, primary_key=True)
    train_number = Column(String(20), unique=True, nullable=False)
    train_name = Column(String(100), nullable=False)
    from_station = Column(String(50), nullable=False)
    to_station = Column(String(50), nullable=False)
    departure_time = Column(String(10))
    arrival_time = Column(String(10))
    days_of_operation = Column(String(100))  # e.g., "1234567" for all days
    
    # Availability info
    sleeper_available = Column(Integer, default=0)
    ac_2_tier_available = Column(Integer, default=0)
    ac_3_tier_available = Column(Integer, default=0)
    general_available = Column(Integer, default=0)
    
    # Tatkal availability
    tatkal_available = Column(Boolean, default=False)
    tatkal_booking_time = Column(String(10))
    
    # Timestamps
    fetched_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<TrainInfo(train={self.train_number}, name='{self.train_name}')>"


class BookingSession(Base):
    """Active booking session tracking"""
    __tablename__ = 'booking_sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    session_token = Column(String(255), unique=True, nullable=False)
    
    # Session state
    is_active = Column(Boolean, default=True)
    login_time = Column(DateTime, default=datetime.now)
    last_activity_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    logout_time = Column(DateTime)
    
    # Session metadata
    ip_address = Column(String(50))
    user_agent = Column(String(255))
    
    def __repr__(self):
        return f"<BookingSession(user_id={self.user_id}, active={self.is_active})>"


class BookingLog(Base):
    """Detailed booking activity log"""
    __tablename__ = 'booking_logs'

    id = Column(Integer, primary_key=True)
    booking_attempt_id = Column(Integer, nullable=False)
    action = Column(String(100), nullable=False)  # e.g., 'login', 'search', 'submit', 'payment'
    status = Column(String(50))  # 'success', 'failed', 'pending'
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<BookingLog(action='{self.action}', status='{self.status}')>"


class NotificationPreference(Base):
    """User notification preferences"""
    __tablename__ = 'notification_preferences'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    
    # Notification channels
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    push_enabled = Column(Boolean, default=False)
    
    # Notification triggers
    notify_on_success = Column(Boolean, default=True)
    notify_on_failure = Column(Boolean, default=True)
    notify_on_waitlist = Column(Boolean, default=True)
    
    # Contact info
    email = Column(String(100))
    phone = Column(String(20))
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<NotificationPreference(user_id={self.user_id})>"
