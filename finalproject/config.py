from sqlalchemy import create_engine
DB_URL = 'postgres://sdbzvxegowxftb:1dc5433255ead59faed22eb2544fb84008f9c0067e4e2fac6e4c28fa290ade93@ec2-107-23-76-12.compute-1.amazonaws.com:5432/dehmh5f8fepnth'
DB_ENGINE = create_engine(DB_URL)