-- Primeiro remove todas as tabelas existentes (na ordem correta devido às FKs)
DROP TABLE IF EXISTS `spia5-dev-3`.`adaptacao_curricular_adaptacaohabilidade`;
DROP TABLE IF EXISTS `spia5-dev-3`.`adaptacao_curricular_adaptacaocurricularindividualizada`;
DROP TABLE IF EXISTS `spia5-dev-3`.`adaptacao_curricular_bncchabilidade`;
DROP TABLE IF EXISTS `spia5-dev-3`.`adaptacao_curricular_bnccdisciplina`;
DROP TABLE IF EXISTS `spia5-dev-3`.`adaptacao_curricular_bnccdisciplinaesconder`;
DROP TABLE IF EXISTS `spia5-dev-3`.`adaptacao_curricular_bnccobjetoconhecimento`;

-- Cria as novas tabelas
CREATE TABLE `adaptacao_curricular_bnccdisciplina` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `nome` varchar(100) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `adaptacao_curricular_bncchabilidade` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `objeto_conhecimento` longtext NOT NULL,
    `codigo` varchar(20) NOT NULL,
    `descricao` longtext NOT NULL,
    `ano` varchar(1) NOT NULL,
    `trimestre` varchar(1) NOT NULL,
    `disciplina_id` bigint NOT NULL,
    PRIMARY KEY (`id`),
    KEY `adaptacao_curricular_bn_disciplina_id_fk` (`disciplina_id`),
    CONSTRAINT `adaptacao_curricular_bn_disciplina_id_fk` FOREIGN KEY (`disciplina_id`) REFERENCES `adaptacao_curricular_bnccdisciplina` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `adaptacao_curricular_adaptacaocurricularindividualizada` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `data_cadastro` date NOT NULL,
    `aluno_id` bigint NOT NULL,
    `escola_id` bigint NOT NULL,
    `profissional_responsavel_id` bigint NOT NULL,
    PRIMARY KEY (`id`),
    KEY `adaptacao_curricular_ac_aluno_id_fk` (`aluno_id`),
    KEY `adaptacao_curricular_ac_escola_id_fk` (`escola_id`),
    KEY `adaptacao_curricular_ac_profissional_id_fk` (`profissional_responsavel_id`),
    CONSTRAINT `adaptacao_curricular_ac_aluno_id_fk` FOREIGN KEY (`aluno_id`) REFERENCES `neurodivergentes_neurodivergente` (`id`),
    CONSTRAINT `adaptacao_curricular_ac_escola_id_fk` FOREIGN KEY (`escola_id`) REFERENCES `escola_escola` (`id`),
    CONSTRAINT `adaptacao_curricular_ac_profissional_id_fk` FOREIGN KEY (`profissional_responsavel_id`) REFERENCES `profissionais_app_profissional` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `adaptacao_curricular_adaptacaohabilidade` (
    `id` bigint NOT NULL AUTO_INCREMENT,
    `descritivo_adaptacao` longtext NOT NULL,
    `aci_id` bigint NOT NULL,
    `habilidade_id` bigint NOT NULL,
    PRIMARY KEY (`id`),
    KEY `adaptacao_curricular_ah_aci_id_fk` (`aci_id`),
    KEY `adaptacao_curricular_ah_habilidade_id_fk` (`habilidade_id`),
    CONSTRAINT `adaptacao_curricular_ah_aci_id_fk` FOREIGN KEY (`aci_id`) REFERENCES `adaptacao_curricular_adaptacaocurricularindividualizada` (`id`),
    CONSTRAINT `adaptacao_curricular_ah_habilidade_id_fk` FOREIGN KEY (`habilidade_id`) REFERENCES `adaptacao_curricular_bncchabilidade` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
