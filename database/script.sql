PRAGMA foreign_keys = ON;

-- =========================
-- ESQUEMA PRINCIPAL
-- =========================
CREATE TABLE IF NOT EXISTS MACHINE (
  machine_id   INTEGER PRIMARY KEY,
  name         VARCHAR(100) NOT NULL,
  location     VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS SENSOR (
  sensor_id    INTEGER PRIMARY KEY,
  machine_id   INTEGER NOT NULL,
  model        VARCHAR(40)  NOT NULL, -- 'DHT22' ou 'MPU6050'
  interface    VARCHAR(20)  NOT NULL, -- 'GPIO' ou 'I2C'
  pin_data     INTEGER,
  i2c_addr     VARCHAR(10),
  CONSTRAINT fk_sensor_machine
    FOREIGN KEY (machine_id) REFERENCES MACHINE(machine_id)
);

CREATE TABLE IF NOT EXISTS READING_ENV (
  reading_id     BIGINT PRIMARY KEY,
  sensor_id      INTEGER NOT NULL,
  ts             TIMESTAMP NOT NULL,
  temperature_c  REAL,
  humidity_pct   REAL,
  CONSTRAINT fk_env_sensor
    FOREIGN KEY (sensor_id) REFERENCES SENSOR(sensor_id),
  CONSTRAINT ck_humidity_range CHECK (humidity_pct BETWEEN 0 AND 100)
);

CREATE TABLE IF NOT EXISTS READING_IMU (
  reading_id  BIGINT PRIMARY KEY,
  sensor_id   INTEGER NOT NULL,
  ts          TIMESTAMP NOT NULL,
  acc_x_g     REAL,
  acc_y_g     REAL,
  acc_z_g     REAL,
  CONSTRAINT fk_imu_sensor
    FOREIGN KEY (sensor_id) REFERENCES SENSOR(sensor_id)
);

-- Índices úteis
CREATE INDEX IF NOT EXISTS idx_env_sensor_ts ON READING_ENV (sensor_id, ts);
CREATE INDEX IF NOT EXISTS idx_imu_sensor_ts ON READING_IMU (sensor_id, ts);

-- =========================
-- DADOS MÍNIMOS (MACHINE/SENSOR)
-- =========================
INSERT OR IGNORE INTO MACHINE (machine_id, name, location)
VALUES (1, 'Linha A', 'Setor 1');

INSERT OR IGNORE INTO SENSOR (sensor_id, machine_id, model, interface, pin_data)
VALUES (101, 1, 'DHT22', 'GPIO', 15);

INSERT OR IGNORE INTO SENSOR (sensor_id, machine_id, model, interface, i2c_addr)
VALUES (102, 1, 'MPU6050', 'I2C', '0x68');

-- =========================
-- STAGING PARA .IMPORT DE CSV
-- (NÃO TEM PK/FK — APENAS ATERRISSA O CSV)
-- =========================
DROP TABLE IF EXISTS STG_ENV;
CREATE TABLE STG_ENV (
  timestamp     TEXT,
  temperature_c REAL,
  humidity_pct  REAL
);

DROP TABLE IF EXISTS STG_IMU;
CREATE TABLE STG_IMU (
  timestamp TEXT,
  acc_x_g   REAL,
  acc_y_g   REAL,
  acc_z_g   REAL
);
