-- Backup Railway MySQL
-- Gerado em: 2026-06-02 17:54:13.531111

SET FOREIGN_KEY_CHECKS=0;

CREATE TABLE `avaliacoes` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `users_id` bigint unsigned DEFAULT NULL,
  `rings_id` bigint unsigned DEFAULT NULL,
  `nota` int DEFAULT NULL,
  `comentario` text,
  `data_avaliacao` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `users_id` (`users_id`,`rings_id`),
  KEY `rings_id` (`rings_id`),
  CONSTRAINT `avaliacoes_ibfk_1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `avaliacoes_ibfk_2` FOREIGN KEY (`rings_id`) REFERENCES `rings` (`id`) ON DELETE CASCADE,
  CONSTRAINT `avaliacoes_chk_1` CHECK ((`nota` between 1 and 10))
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `avaliacoes` (`id`, `users_id`, `rings_id`, `nota`, `comentario`, `data_avaliacao`) VALUES
(1, 1, 1, 8, 'Ring silk touch, o vermelho não funciona as vezes, mas muito rapido', '2026-05-25 15:48:10'),
(2, 1, 2, 9, 'Sem problemas', '2026-05-25 16:02:28'),
(3, 1, 3, 7, 'funciona peça a peça, mas o vermelho falha', '2026-05-25 16:03:40'),
(4, 1, 4, 1, 'As vezes manda 6 duplicado, vira 12', '2026-05-25 16:04:27'),
(5, 4, 5, 10, 'Pessoal que almeja top gun gostam de usar este ring', '2026-05-25 17:04:14'),
(6, 4, 1, 10, 'Pessoal que almeja top gun gostam de usar este ring', '2026-05-25 17:04:45'),
(8, 2, 1, 8, 'Ring touch botão parece está quebrado porém é super rápido, basicamente um touch screan top de mais', '2026-05-26 00:04:47'),
(9, 2, 5, 10, 'Ring top, atualizado software recentemente, sem problemas. Top para farmácia ', '2026-05-26 00:07:44'),
(10, 2, 2, 9, 'Ring top, botões novos sem bipagem duplicada ', '2026-05-26 00:09:03'),
(12, 2, 4, 1, 'Ring pessimo, duplica as contagens 3, 12 etc 
Muitos problemas com divergência ', '2026-05-26 00:13:34'),
(13, 3, 6, 6, 'O leitor é bom, mas tá bugando o 1/12', '2026-05-26 01:38:30'),
(19, 3, 7, 6, 'Paia tbm tá bugando o 1/12', '2026-05-26 02:32:48'),
(21, 3, 8, 7, 'Ok', '2026-05-26 23:12:22'),
(22, 5, 9, 9, 'Funciona com eficiência e não trava ', '2026-05-27 04:50:51'),
(23, 1, 10, 9, 'Bom', '2026-05-27 04:51:44'),
(24, 7, 11, 8, 'Muito bom pra mim', '2026-05-27 05:18:17'),
(25, 6, 12, 6, 'Ring bom,porém apresentou falhas durante a contagem,travando em alguns momentos.', '2026-05-27 05:21:01'),
(26, 1, 13, 1, 'Horrivel, o pior', '2026-05-28 08:04:43'),
(27, 1, 14, 9, 'Bom ring, parece que ta no wide', '2026-05-29 04:46:31'),
(28, 3, 4, 8, 'Pica pra peça a peça, widei legal', '2026-05-29 04:51:34'),
(30, 1, 15, 9, 'muito bom', '2026-06-02 06:09:41'),
(31, 1, 16, 6, '1 bugado n manda nd', '2026-06-02 06:10:21');

CREATE TABLE `rings` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `numero` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `rings` (`id`, `numero`) VALUES
(1, '550'),
(2, '555'),
(3, '506'),
(4, '494'),
(5, '545'),
(6, '586'),
(7, '583'),
(8, '541'),
(9, '505'),
(10, '567'),
(11, '497'),
(12, '556'),
(13, '493'),
(14, '499'),
(15, '507'),
(16, '495');

CREATE TABLE `users` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) DEFAULT NULL,
  `senha` varchar(4) DEFAULT NULL,
  `badge` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `users` (`id`, `nome`, `senha`, `badge`) VALUES
(1, 'Gab', '0534', '91800354'),
(2, 'Patrick', '1253', '91800355'),
(3, 'Predo', '0722', '67400553'),
(4, 'Murilo', '2866', '67400555'),
(5, 'Cassia', '0726', '91800356'),
(6, 'Akemi', '1187', '22550602'),
(7, 'Agatinha', '0813', '22550594'),
(8, 'Luis Lobão', '1234', '67400545');

SET FOREIGN_KEY_CHECKS=1;
