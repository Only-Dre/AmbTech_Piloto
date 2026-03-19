USE ambienteA;

CREATE TABLE IF NOT EXISTS status_ambiente (

    id INT AUTO_INCREMENT NOT NULL,

    data_hora TIMESTAMP NOT NULL,

    temperatura DOUBLE(10, 2) NOT NULL,

    umidade DOUBLE(10, 2) NOT NULL,

    origem_dado VARCHAR(50) NOT NULL,

    data_insercao TIMESTAMP NOT NULL,

    PRIMARY KEY (id)
);