from sqlalchemy import create_engine
DB_URL = 'postgresql://kubxndksaqwkzn:b946a1fb79f8103768009eb146dbc5c67acf2ab9a67534a1d0d33252f0d2daf6@ec2-34-231-63-30.compute-1.amazonaws.com:5432/d9nbe338h1pj2m'
DB_ENGINE = create_engine(DB_URL)