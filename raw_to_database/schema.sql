DROP TABLE IF EXISTS datos_abiertos.inViales;

CREATE TABLE datos_abiertos.inViales (
	id INT auto_increment NOT NULL PRIMARY KEY,
	folio varchar(50) unique NOT NULL,
	fecha_creacion DATE NULL,
	hora_creacion varchar(20) NULL,
	dia_semana varchar(20) NULL,
	fecha_cierre DATE NULL,
	hora_cierre varchar(20) NULL,
	tipo_incidente_c4 varchar(100) NULL,
	incidente_c4 varchar(100) NULL,
	alcaldia_inicio varchar(50) NULL,
	latitud DOUBLE NULL,
	longitud DOUBLE NULL,
	codigo_cierre varchar(50) NULL,
	clas_con_f_alarma varchar(50) NULL,
	tipo_entrada varchar(50) NULL,
	alcaldia_cierre varchar(50) NULL,
	colonia varchar(100) NULL
)