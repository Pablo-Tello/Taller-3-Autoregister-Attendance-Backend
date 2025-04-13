-- Script para llenar la tabla calendario con fechas del año 2025 para Perú

-- Primero, verificamos si existen los ciclos académicos para 2025
-- Si no existen, los creamos
INSERT INTO ciclo_academico (str_idCicloAcademico, str_nombre, dt_fecha_inicio, dt_fecha_fin, int_duracion_semanas, bool_activo)
SELECT '2025-1', 'Ciclo Académico 2025-1', '2025-03-17', '2025-08-02', 20, 1
WHERE NOT EXISTS (SELECT 1 FROM ciclo_academico WHERE str_idCicloAcademico = '2025-1');

INSERT INTO ciclo_academico (str_idCicloAcademico, str_nombre, dt_fecha_inicio, dt_fecha_fin, int_duracion_semanas, bool_activo)
SELECT '2025-2', 'Ciclo Académico 2025-2', '2025-08-18', '2026-01-03', 20, 1
WHERE NOT EXISTS (SELECT 1 FROM ciclo_academico WHERE str_idCicloAcademico = '2025-2');

-- Insertamos las fechas del año 2025
INSERT INTO calendario (dt_fecha, str_tipo_dia, str_descripcion, bool_laborable)
WITH RECURSIVE fechas_2025 AS (
    SELECT CAST('2025-01-01' AS DATE) AS fecha
    UNION ALL
    SELECT DATE_ADD(fecha, INTERVAL 1 DAY)
    FROM fechas_2025
    WHERE fecha < '2025-12-31'
)
SELECT
    f.fecha,
    CASE
        -- Feriados nacionales de Perú 2025
        WHEN f.fecha = '2025-01-01' THEN 'F'
        WHEN f.fecha = '2025-04-17' THEN 'F'
        WHEN f.fecha = '2025-04-18' THEN 'F'
        WHEN f.fecha = '2025-05-01' THEN 'F'
        WHEN f.fecha = '2025-06-29' THEN 'F'
        WHEN f.fecha = '2025-07-28' THEN 'F'
        WHEN f.fecha = '2025-07-29' THEN 'F'
        WHEN f.fecha = '2025-08-30' THEN 'F'
        WHEN f.fecha = '2025-10-08' THEN 'F'
        WHEN f.fecha = '2025-11-01' THEN 'F'
        WHEN f.fecha = '2025-12-08' THEN 'F'
        WHEN f.fecha = '2025-12-25' THEN 'F'
        -- Fines de semana
        WHEN DAYOFWEEK(f.fecha) = 1 THEN 'S'
        -- Días laborables
        ELSE 'L'
    END,
    CASE
        WHEN f.fecha = '2025-01-01' THEN 'Año Nuevo'
        WHEN f.fecha = '2025-04-17' THEN 'Jueves Santo'
        WHEN f.fecha = '2025-04-18' THEN 'Viernes Santo'
        WHEN f.fecha = '2025-05-01' THEN 'Día del Trabajo'
        WHEN f.fecha = '2025-06-29' THEN 'San Pedro y San Pablo'
        WHEN f.fecha = '2025-07-28' THEN 'Fiestas Patrias'
        WHEN f.fecha = '2025-07-29' THEN 'Fiestas Patrias'
        WHEN f.fecha = '2025-08-30' THEN 'Santa Rosa de Lima'
        WHEN f.fecha = '2025-10-08' THEN 'Combate de Angamos'
        WHEN f.fecha = '2025-11-01' THEN 'Día de Todos los Santos'
        WHEN f.fecha = '2025-12-08' THEN 'Inmaculada Concepción'
        WHEN f.fecha = '2025-12-25' THEN 'Navidad'
        WHEN DAYOFWEEK(f.fecha) = 1 THEN 'Domingo'
        ELSE NULL
    END,
    CASE
        WHEN f.fecha = '2025-01-01' THEN 0
        WHEN f.fecha = '2025-04-17' THEN 0
        WHEN f.fecha = '2025-04-18' THEN 0
        WHEN f.fecha = '2025-05-01' THEN 0
        WHEN f.fecha = '2025-06-29' THEN 0
        WHEN f.fecha = '2025-07-28' THEN 0
        WHEN f.fecha = '2025-07-29' THEN 0
        WHEN f.fecha = '2025-08-30' THEN 0
        WHEN f.fecha = '2025-10-08' THEN 0
        WHEN f.fecha = '2025-11-01' THEN 0
        WHEN f.fecha = '2025-12-08' THEN 0
        WHEN f.fecha = '2025-12-25' THEN 0
        WHEN DAYOFWEEK(f.fecha) = 1 THEN 0
        ELSE 1
    END
FROM fechas_2025 f
WHERE NOT EXISTS (
    SELECT 1 FROM calendario c
    WHERE c.dt_fecha = f.fecha
);

