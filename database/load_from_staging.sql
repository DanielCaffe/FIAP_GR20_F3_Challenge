PRAGMA foreign_keys = ON;

-- Gera IDs sequenciais baseados na ordem temporal e insere nas tabelas finais

-- ENV (sensor_id = 101)
INSERT INTO READING_ENV (reading_id, sensor_id, ts, temperature_c, humidity_pct)
SELECT
  COALESCE( (SELECT MAX(reading_id) FROM READING_ENV), 0 )
  + ROW_NUMBER() OVER (ORDER BY datetime(timestamp)),
  101,
  datetime(timestamp),
  temperature_c,
  humidity_pct
FROM STG_ENV;

-- IMU (sensor_id = 102)
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

-- (Opcional) limpar staging depois do load
-- DELETE FROM STG_ENV;
-- DELETE FROM STG_IMU;

-- Verificações
SELECT 'SENSORS' AS what, COUNT(*) AS n FROM SENSOR
UNION ALL
SELECT 'READING_ENV', COUNT(*) FROM READING_ENV
UNION ALL
SELECT 'READING_IMU', COUNT(*) FROM READING_IMU;
