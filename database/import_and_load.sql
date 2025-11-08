-- Importa CSVs para staging
.mode csv
.import --skip 1 '../document/dataset_env.csv' STG_ENV
.import --skip 1 '../document/dataset_imu.csv' STG_IMU

-- Verifica se importou
SELECT 'STG_ENV importado' AS status, COUNT(*) AS rows FROM STG_ENV;
SELECT 'STG_IMU importado' AS status, COUNT(*) AS rows FROM STG_IMU;

-- Carrega para tabelas finais
PRAGMA foreign_keys = ON;

INSERT INTO READING_ENV (reading_id, sensor_id, ts, temperature_c, humidity_pct)
SELECT
  COALESCE( (SELECT MAX(reading_id) FROM READING_ENV), 0 )
  + ROW_NUMBER() OVER (ORDER BY datetime(timestamp)),
  101,
  datetime(timestamp),
  temperature_c,
  humidity_pct
FROM STG_ENV;

INSERT INTO READING_IMU (reading_id, sensor_id, ts, acc_x_g, acc_y_g, acc_z_g)
SELECT
  COALESCE( (SELECT MAX(reading_id) FROM READING_IMU), 0 )
  + ROW_NUMBER() OVER (ORDER BY datetime(timestamp)),
  102,
  datetime(timestamp),
  acc_x_g,
  acc_y_g,
  acc_z_g
FROM STG_IMU;

-- Verificações finais
SELECT 'READING_ENV final' AS status, COUNT(*) AS rows FROM READING_ENV;
SELECT 'READING_IMU final' AS status, COUNT(*) AS rows FROM READING_IMU;
