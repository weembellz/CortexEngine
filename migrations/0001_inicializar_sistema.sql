-- Capa Central: El Estado del Mundo (World State)
CREATE TABLE IF NOT EXISTS world_state (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL, -- Datos en JSON (clima, deuda, alertas BOE)
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Capa Narrativa: Feed Global de Eventos de la IA
CREATE TABLE IF NOT EXISTS system_events (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL, -- 'BOE', 'Clima', 'Noticias'
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    impact_metrics TEXT, -- JSON con el impacto macro: {"alquiler": -5}
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Capa Life OS: Datos del Operador
CREATE TABLE IF NOT EXISTS life_os_vault (
    category TEXT NOT NULL, -- 'wallet', 'subvencion', 'terrario'
    item_key TEXT NOT NULL,
    data TEXT NOT NULL,
    PRIMARY KEY (category, item_key)
);
