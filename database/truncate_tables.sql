-- Limpa todas as tabelas mantendo a estrutura
DELETE FROM reading_env;
DELETE FROM reading_imu;
DELETE FROM alert;

-- Reseta os contadores de ID (opcional)
DELETE FROM sqlite_sequence WHERE name IN ('reading_env', 'reading_imu', 'alert');

-- Mensagem de confirmação
SELECT 'Tabelas truncadas com sucesso!' AS status;
