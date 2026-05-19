CREATE TABLE IF NOT EXISTS objetivos_bunker (
    id TEXT PRIMARY KEY,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    tipo TEXT NOT NULL,
    nombre TEXT NOT NULL,
    distancia_agua_metros REAL,
    verificado INTEGER DEFAULT 0
);
