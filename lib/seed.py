#!/usr/bin/env python3

# Script goes here!
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, Dev, Freebie

engine = create_engine('sqlite:///freebies.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Clear existing data
session.query(Freebie).delete()
session.query(Dev).delete()
session.query(Company).delete()

# Create sample companies
company1 = Company(name="TechCorp", founding_year=2000)
company2 = Company(name="InnovateInc", founding_year=2010)
session.add_all([company1, company2])

# Create sample devs
dev1 = Dev(name="Alice")
dev2 = Dev(name="Bob")
session.add_all([dev1, dev2])

# Commit companies and devs
session.commit()

# Create sample freebies
freebie1 = Freebie(item_name="T-shirt", value=20, dev=dev1, company=company1)
freebie2 = Freebie(item_name="Mug", value=10, dev=dev1, company=company2)
freebie3 = Freebie(item_name="Sticker", value=5, dev=dev2, company=company1)
session.add_all([freebie1, freebie2, freebie3])

# Commit freebies
session.commit()

print("Database seeded successfully!")