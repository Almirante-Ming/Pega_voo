CREATE TABLE Usuario (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_completo VARCHAR(150) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    genero VARCHAR(20),
    telefone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash VARCHAR(),
    origem_cadastro VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

CREATE TABLE Voo (
    id_voo SERIAL PRIMARY KEY,
    numero_voo VARCHAR(20) NOT NULL,
    origem VARCHAR(10) NOT NULL,
    destino VARCHAR(10) NOT NULL,
    data_ida DATE NOT NULL,
    companhia_aerea VARCHAR(100) NOT NULL,
    tier tier_passagem NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP
);

CREATE TABLE Reserva (
    id_reserva VARCHAR(20) PRIMARY KEY,
    id_usuario UUID NOT NULL,
    id_voo INT NOT NULL,
    data_reserva TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'ativa',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id),
    FOREIGN KEY (id_voo) REFERENCES Voo(id_voo)
);