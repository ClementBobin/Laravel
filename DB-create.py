import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get database connection details from environment variables
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()
    print("Connected to the database!")

    # SQL script to create tables and indices
    create_weather_station_table = """
    CREATE TABLE IF NOT EXISTS "WeatherStation" (
        "Id" SERIAL PRIMARY KEY,
        "Name" VARCHAR NOT NULL,
        "Latitude" FLOAT NOT NULL,
        "Longitude" FLOAT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS "WeatherStation_index_0"
    ON "WeatherStation" ("Id");
    """

    create_weather_datas_table = """
    CREATE TABLE IF NOT EXISTS "WeatherDatas" (
        "Id" SERIAL PRIMARY KEY,
        "WeatherStationId" INTEGER NOT NULL,
        "Timestamp" TIMESTAMPTZ NOT NULL,
        "Current_temperature_2m" FLOAT,
        "Current_relative_humidity_2m" FLOAT,
        "Current_apparent_temperature" FLOAT,
        "Current_is_day" BOOLEAN,
        "Current_precipitation" FLOAT,
        "Current_rain" FLOAT,
        "Current_showers" FLOAT,
        "Current_snowfall" FLOAT,
        "Current_weather_code" INTEGER,
        "Current_cloud_cover" FLOAT,
        "Current_pressure_msl" FLOAT,
        "Current_surface_pressure" FLOAT,
        "Current_wind_speed_10m" FLOAT,
        "Current_wind_direction_10m" FLOAT,
        "Current_wind_gusts_10m" FLOAT,

        -- Hourly Weather Variables
        "Hourly_temperature_2m" FLOAT,
        "Hourly_relative_humidity_2m" FLOAT,
        "Hourly_dew_point_2m" FLOAT,
        "Hourly_apparent_temperature" FLOAT,
        "Hourly_precipitation" FLOAT,
        "Hourly_rain" FLOAT,
        "Hourly_snowfall" FLOAT,
        "Hourly_weather_code" INTEGER,
        "Hourly_cloud_cover_total" FLOAT,
        "Hourly_cloud_cover_low" FLOAT,
        "Hourly_cloud_cover_mid" FLOAT,
        "Hourly_cloud_cover_high" FLOAT,
        "Hourly_pressure_msl" FLOAT,
        "Hourly_surface_pressure" FLOAT,
        "Hourly_vapour_pressure_deficit" FLOAT,
        "Hourly_reference_evapotranspiration" FLOAT,
        "Hourly_wind_speed_10m" FLOAT,
        "Hourly_wind_speed_20m" FLOAT,
        "Hourly_wind_speed_50m" FLOAT,
        "Hourly_wind_speed_100m" FLOAT,
        "Hourly_wind_speed_150m" FLOAT,
        "Hourly_wind_speed_200m" FLOAT,
        "Hourly_wind_direction_10m" FLOAT,
        "Hourly_wind_direction_20m" FLOAT,
        "Hourly_wind_direction_50m" FLOAT,
        "Hourly_wind_direction_100m" FLOAT,
        "Hourly_wind_direction_150m" FLOAT,
        "Hourly_wind_direction_200m" FLOAT,
        "Hourly_wind_gusts_10m" FLOAT,
        "Hourly_temperature_20m" FLOAT,
        "Hourly_temperature_50m" FLOAT,
        "Hourly_temperature_100m" FLOAT,
        "Hourly_temperature_150m" FLOAT,
        "Hourly_temperature_200m" FLOAT,

        -- Daily Weather Variables
        "Daily_weather_code" INTEGER,
        "Daily_max_temperature_2m" FLOAT,
        "Daily_min_temperature_2m" FLOAT,
        "Daily_max_apparent_temperature" FLOAT,
        "Daily_min_apparent_temperature" FLOAT,
        "Daily_sunrise" TIMESTAMPTZ,
        "Daily_sunset" TIMESTAMPTZ,
        "Daily_daylight_duration" INTEGER,
        "Daily_sunshine_duration" INTEGER,
        "Daily_uv_index" FLOAT,
        "Daily_uv_index_clear_sky" FLOAT,
        "Daily_precipitation_sum" FLOAT,
        "Daily_rain_sum" FLOAT,
        "Daily_showers_sum" FLOAT,
        "Daily_snowfall_sum" FLOAT,
        "Daily_precipitation_hours" INTEGER,
        "Daily_precipitation_probability_max" FLOAT,
        "Daily_max_wind_speed_10m" FLOAT,
        "Daily_max_wind_gusts_10m" FLOAT,
        "Daily_dominant_wind_direction_10m" FLOAT,
        "Daily_shortwave_radiation_sum" FLOAT,
        "Daily_reference_evapotranspiration" FLOAT,

        FOREIGN KEY ("WeatherStationId") REFERENCES "WeatherStation" ("Id")
            ON UPDATE NO ACTION ON DELETE CASCADE
    );
    CREATE INDEX IF NOT EXISTS "WeatherDatas_index_0"
    ON "WeatherDatas" ("Id");
    """
    create_trigger_function = """
    CREATE OR REPLACE FUNCTION delete_old_weather_data() RETURNS TRIGGER AS $$
    BEGIN
        DELETE FROM "WeatherDatas" WHERE "Timestamp" < NOW() - INTERVAL '1 week';
        RETURN OLD;
    END;
    $$ LANGUAGE plpgsql;
    """

    create_trigger = """
    CREATE TRIGGER delete_old_weather_data_trigger
    BEFORE DELETE ON "WeatherDatas"
    FOR EACH ROW
    EXECUTE FUNCTION delete_old_weather_data();
    """

    create_cities_table = """
    CREATE TABLE IF NOT EXISTS "Cities" (
        "Id" SERIAL PRIMARY KEY,
        "Name" VARCHAR NOT NULL,
        "Latitude" FLOAT NOT NULL,
        "Longitude" FLOAT NOT NULL
    );
    CREATE INDEX IF NOT EXISTS "Cities_index_0"
    ON "Cities" ("Id");
    """

    create_departements_table = """
    CREATE TABLE IF NOT EXISTS "Departements" (
        "Id" SERIAL PRIMARY KEY,
        "Name" VARCHAR NOT NULL,
        "Latitude" FLOAT NOT NULL,
        "Longitude" FLOAT NOT NULL,
        "Numero" VARCHAR NOT NULL
    );
    CREATE INDEX IF NOT EXISTS "Departements_index_0"
    ON "Departements" ("Id");
    """

<<<<<<< Updated upstream
=======
    create_permissions_table = """
    CREATE TABLE IF NOT EXISTS "permissions" (
        "id" SERIAL PRIMARY KEY,
        "name" VARCHAR NOT NULL,
        "guard_name" VARCHAR NOT NULL,
        "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE UNIQUE INDEX IF NOT EXISTS "permissions_unique_index"
    ON "permissions" ("name", "guard_name");
    """

    create_roles_table = """
    CREATE TABLE IF NOT EXISTS "roles" (
        "id" SERIAL PRIMARY KEY,
        "name" VARCHAR NOT NULL,
        "guard_name" VARCHAR NOT NULL,
        "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE UNIQUE INDEX IF NOT EXISTS "Roles_unique_index"
    ON "roles" ("name", "guard_name");
    """

    create_model_has_permissions_table = """
    CREATE TABLE IF NOT EXISTS "model_has_permissions" (
        "permission_id" INTEGER NOT NULL,
        "model_type" VARCHAR NOT NULL,
        "model_id" INTEGER NOT NULL,
        PRIMARY KEY ("permission_id", "model_id", "model_type"),
        FOREIGN KEY ("permission_id") REFERENCES "permissions" ("id") ON DELETE CASCADE
    );
    CREATE INDEX IF NOT EXISTS "ModelHasPermissions_model_id_model_type_index"
    ON "model_has_permissions" ("model_id", "model_type");
    """

    create_model_has_roles_table = """
    CREATE TABLE IF NOT EXISTS "model_has_roles" (
        "role_id" INTEGER NOT NULL,
        "model_type" VARCHAR NOT NULL,
        "model_id" INTEGER NOT NULL,
        PRIMARY KEY ("role_id", "model_id", "model_type"),
        FOREIGN KEY ("role_id") REFERENCES "roles" ("id") ON DELETE CASCADE
    );
    CREATE INDEX IF NOT EXISTS "ModelHasRoles_model_id_model_type_index"
    ON "model_has_roles" ("model_id", "model_type");
    """

    create_role_has_permissions_table = """
    CREATE TABLE IF NOT EXISTS "role_has_permissions" (
        "permission_id" INTEGER NOT NULL,
        "role_id" INTEGER NOT NULL,
        PRIMARY KEY ("permission_id", "role_id"),
        FOREIGN KEY ("permission_id") REFERENCES "permissions" ("id") ON DELETE CASCADE,
        FOREIGN KEY ("role_id") REFERENCES "roles" ("id") ON DELETE CASCADE
    );
    """

    create_users_table = """
    CREATE TABLE IF NOT EXISTS "users" (
        "id" SERIAL PRIMARY KEY,
        "firstname" VARCHAR NOT NULL,
        "lastname" VARCHAR NOT NULL,
        "email" VARCHAR NOT NULL UNIQUE,
        "password" VARCHAR NOT NULL,
        "manager_id" INTEGER,
        "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY ("manager_id") REFERENCES "users" ("id")
    );
    CREATE INDEX IF NOT EXISTS "Users_index_0"
    ON "users" ("id");
    """

    create_invite_table = """
    CREATE TABLE IF NOT EXISTS "invites" (
        "id" SERIAL PRIMARY KEY,
        "token" VARCHAR NOT NULL UNIQUE,
        "expires_at" TIMESTAMP,
        "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE UNIQUE INDEX IF NOT EXISTS "invites_token_unique_index"
    ON "invites" ("token");
    """

    create_session_table = '''
    CREATE TABLE IF NOT EXISTS "sessions" (
        "id" VARCHAR PRIMARY KEY,
        "user_id" INTEGER,
        "ip_address" VARCHAR(45),
        "user_agent" TEXT,
        "payload" TEXT,
        "last_activity" INTEGER,
        FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE SET NULL
    );
    CREATE INDEX IF NOT EXISTS "sessions_user_id_index" ON "sessions" ("user_id");
    CREATE INDEX IF NOT EXISTS "sessions_last_activity_index" ON "sessions" ("last_activity");
    '''

    create_password_reset_tokens_table = '''
    CREATE TABLE IF NOT EXISTS "password_reset_tokens" (
        "email" VARCHAR(255) NOT NULL,
        "token" VARCHAR(255) NOT NULL,
        "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY ("email")
    );
    '''

    create_jobs_table = """
    CREATE TABLE IF NOT EXISTS "jobs" (
        "id" SERIAL PRIMARY KEY,
        "queue" VARCHAR NOT NULL,
        "payload" TEXT NOT NULL,
        "attempts" INTEGER NOT NULL,
        "reserved_at" INTEGER,
        "available_at" INTEGER NOT NULL,
        "created_at" INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS "jobs_queue_index" ON "jobs" ("queue");
    """

    create_job_batches_table = """
    CREATE TABLE IF NOT EXISTS "job_batches" (
        "id" VARCHAR PRIMARY KEY,
        "name" VARCHAR NOT NULL,
        "total_jobs" INTEGER NOT NULL,
        "pending_jobs" INTEGER NOT NULL,
        "failed_jobs" INTEGER NOT NULL,
        "failed_job_ids" TEXT NOT NULL,
        "options" TEXT,
        "cancelled_at" INTEGER,
        "created_at" INTEGER NOT NULL,
        "finished_at" INTEGER
    );
    """

    create_failed_jobs_table = """
    CREATE TABLE IF NOT EXISTS "failed_jobs" (
        "id" SERIAL PRIMARY KEY,
        "uuid" VARCHAR NOT NULL UNIQUE,
        "connection" TEXT NOT NULL,
        "queue" TEXT NOT NULL,
        "payload" TEXT NOT NULL,
        "exception" TEXT NOT NULL,
        "failed_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

    create_cache_table = """
    CREATE TABLE IF NOT EXISTS "cache" (
        "key" VARCHAR PRIMARY KEY,
        "value" TEXT,
        "expiration" INTEGER
    );
    """

    create_cache_locks_table = """
    CREATE TABLE IF NOT EXISTS "cache_locks" (
        "key" VARCHAR PRIMARY KEY,
        "owner" VARCHAR,
        "expiration" INTEGER
    );
    """

>>>>>>> Stashed changes
    # Execute the SQL scripts to create tables and indexes
    cursor.execute(create_weather_station_table)
    cursor.execute(create_weather_datas_table)
    cursor.execute(create_cities_table)
    cursor.execute(create_departements_table)
    cursor.execute(create_trigger_function)
    cursor.execute(create_trigger)

<<<<<<< Updated upstream
=======
    print("Connected to PostgreSQL!")
    conn.close()

    # SQL to create 'invite' database
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'invites'")
    exists = cursor.fetchone()
    if not exists:
        create_invite_db = f"CREATE DATABASE invites WITH OWNER = '{DB_USER}';"
        cursor.execute(create_invite_db)
        print("Database 'invites' created successfully!")
    else:
        print("Database 'invites' already exists.")
    conn.autocommit = False

    # Close the connection to the 'postgres' database and reconnect to the new 'invite' database
    conn.close()

    # Now connect to the 'invite' database to create the tables
    conn = psycopg2.connect(dbname='invites', user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()
    print("Connected to the 'invites' database!")

    # Create tables for roles, permissions, models, model_has_roles, role_has_permissions, and users inside the newly created db user
    cursor.execute(create_permissions_table)
    cursor.execute(create_roles_table)
    cursor.execute(create_model_has_permissions_table)
    cursor.execute(create_model_has_roles_table)
    cursor.execute(create_role_has_permissions_table)
    cursor.execute(create_users_table)
    cursor.execute(create_invite_table)
    cursor.execute(create_session_table)
    cursor.execute(create_password_reset_tokens_table)
    cursor.execute(create_jobs_table)
    cursor.execute(create_job_batches_table)
    cursor.execute(create_failed_jobs_table)
    cursor.execute(create_cache_table)
    cursor.execute(create_cache_locks_table)

    print("Tables created successfully in the 'invite' database!")

>>>>>>> Stashed changes
    # Commit the transaction
    conn.commit()

    print("Tables and indexes created successfully!")

except Exception as e:
    print(f"Error occurred: {e}")
    if conn:
        conn.rollback()

finally:
    # Close the connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
        print("Connection closed.")
