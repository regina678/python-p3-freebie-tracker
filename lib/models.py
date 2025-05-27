from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    freebies = relationship("Freebie", backref="company")
    devs = relationship("Dev", secondary="freebies", backref="companies")

    def give_freebie(self, dev, item_name, value):
        """Creates a new Freebie associated with this company and the given dev."""
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        return freebie

    @classmethod
    def oldest_company(cls, session):
        """Returns the Company instance with the earliest founding year."""
        return session.query(cls).order_by(cls.founding_year).first()

    def __repr__(self):
        return f"<Company(name={self.name}, founding_year={self.founding_year})>"

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    freebies = relationship("Freebie", backref="dev")

    def received_one(self, item_name):
        """Returns True if the dev has a freebie with the given item_name, else False."""
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, new_dev, freebie):
        """Transfers the freebie to new_dev if it belongs to this dev."""
        if freebie.dev == self:
            freebie.dev = new_dev

    def __repr__(self):
        return f"<Dev(name={self.name})>"

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    def print_details(self):
        """Returns a formatted string with dev name, item name, and company name."""
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"

    def __repr__(self):
        return f"<Freebie(item_name={self.item_name}, value={self.value})>"