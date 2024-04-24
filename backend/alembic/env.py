from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import os



load_dotenv()

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

section = config.config_ini_section
config.set_section_option(section, 'DB_USER', os.getenv('DB_USER'))
config.set_section_option(section, 'DB_DATABASE', os.getenv('DB_DATABASE'))
config.set_section_option(section, 'DB_HOST', os.getenv('DB_HOST'))
config.set_section_option(section, 'DB_PASSWORD', os.getenv('DB_PASSWORD'))



# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ensure that the sqlalchemy.url key is present in the configuration
if not config.get_section(config.config_ini_section):
    raise Exception("Configuration file is missing [alembic] section.")
if not config.get_section_option(config.config_ini_section, 'sqlalchemy.url'):
    raise Exception("Configuration file is missing sqlalchemy.url setting.")

# Connect to your database engine using the URL from the configuration
url = config.get_section_option(config.config_ini_section, 'sqlalchemy.url')
engine = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix='sqlalchemy.',
    poolclass=pool.NullPool)

# Include the models' MetaData object in the context
target_metadata = None

# Configure the context with the necessary metadata and options
context.configure(
    url=url,
    target_metadata=target_metadata,
    compare_type=True,
    compare_server_default=True,
    compare_ignore_options={"sqlalchemy_migrate_version"}
)

# Run migrations online if necessary
# with engine.connect() as connection:
#     context.configure(
#         connection=connection,
#         target_metadata=target_metadata
#     )
#     with context.begin_transaction():
#         context.run_migrations()
