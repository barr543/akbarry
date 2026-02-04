-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 04, 2026 at 04:42 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rapot_akbar`
--

-- --------------------------------------------------------

--
-- Table structure for table `absensi_akbar`
--

CREATE TABLE `absensi_akbar` (
  `id_absen` varchar(100) NOT NULL,
  `nis` int(11) NOT NULL,
  `sakit` int(11) NOT NULL,
  `izin` int(11) NOT NULL,
  `alfa` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `absensi_akbar`
--

INSERT INTO `absensi_akbar` (`id_absen`, `nis`, `sakit`, `izin`, `alfa`) VALUES
('A001', 10243300, 2, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `guru_akbar`
--

CREATE TABLE `guru_akbar` (
  `id_guru` varchar(100) NOT NULL,
  `nama_guru` varchar(50) NOT NULL,
  `id_mapel` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `guru_akbar`
--

INSERT INTO `guru_akbar` (`id_guru`, `nama_guru`, `id_mapel`) VALUES
('G001', 'Joki', 'M001'),
('G002', 'Dika', 'M002'),
('G003', 'Cahya', 'M003');

-- --------------------------------------------------------

--
-- Table structure for table `kelas_akbar`
--

CREATE TABLE `kelas_akbar` (
  `id_kelas` varchar(100) NOT NULL,
  `nama_kelas` varchar(50) NOT NULL,
  `id_guru` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kelas_akbar`
--

INSERT INTO `kelas_akbar` (`id_kelas`, `nama_kelas`, `id_guru`) VALUES
('K001', 'XI RPL B', 'G001'),
('K002', 'XI RPL B', 'G002'),
('K003', 'XI MEKA A', 'G003');

-- --------------------------------------------------------

--
-- Table structure for table `mapel_akbar`
--

CREATE TABLE `mapel_akbar` (
  `id_mapel` varchar(100) NOT NULL,
  `nama_mapel` varchar(50) NOT NULL,
  `kkm` int(11) NOT NULL,
  `jenis_mapel` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mapel_akbar`
--

INSERT INTO `mapel_akbar` (`id_mapel`, `nama_mapel`, `kkm`, `jenis_mapel`) VALUES
('M001', 'B.Jepang', 75, 'Umum'),
('M002', 'B.Indonesia', 75, 'Umum'),
('M003', 'B.Inggris', 80, 'Umum'),
('M004', 'Olahraga', 75, 'Pilihan');

-- --------------------------------------------------------

--
-- Table structure for table `nilai_akbar`
--

CREATE TABLE `nilai_akbar` (
  `id_nilai` varchar(10) NOT NULL,
  `nis` int(11) NOT NULL,
  `id_mapel` varchar(100) NOT NULL,
  `nilai_tugas` int(11) NOT NULL,
  `nilai_uts` int(11) NOT NULL,
  `nilai_uas` int(11) NOT NULL,
  `nilai_akhir` int(11) NOT NULL,
  `deskripsi` varchar(50) NOT NULL,
  `semester` varchar(50) NOT NULL,
  `tahun_ajaran` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nilai_akbar`
--

INSERT INTO `nilai_akbar` (`id_nilai`, `nis`, `id_mapel`, `nilai_tugas`, `nilai_uts`, `nilai_uas`, `nilai_akhir`, `deskripsi`, `semester`, `tahun_ajaran`) VALUES
('N001', 10243211, 'M001', 80, 90, 70, 80, 'Baik, tingkatkan konsistensi belajar', '1', 2026),
('N002', 10243211, 'M001', 78, 87, 67, 77, 'Cukup baik, perlu lebih giat latihan.', '1', 2026),
('N003', 10243221, 'M003', 76, 76, 76, 76, 'Cukup baik, perlu lebih giat latihan.', '1', 2026);

-- --------------------------------------------------------

--
-- Table structure for table `siswa_akbar`
--

CREATE TABLE `siswa_akbar` (
  `nis` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `tempat_lahir` varchar(100) NOT NULL,
  `tgl_lahir` date NOT NULL,
  `alamat` varchar(100) NOT NULL,
  `id_kelas` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `siswa_akbar`
--

INSERT INTO `siswa_akbar` (`nis`, `nama`, `tempat_lahir`, `tgl_lahir`, `alamat`, `id_kelas`) VALUES
(10243211, 'caca', 'bandung', '2008-07-08', 'disana', 'K002'),
(10243221, 'chyaa', 'bandung', '2007-02-08', 'di mana', 'K003'),
(10243300, 'bar', 'cimahi', '2009-05-06', 'Jl.padasuka', 'K001');

-- --------------------------------------------------------

--
-- Table structure for table `user_akbar`
--

CREATE TABLE `user_akbar` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` enum('admin','guru','wali kelas') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_akbar`
--

INSERT INTO `user_akbar` (`id`, `username`, `password`, `role`) VALUES
(12345610, 'jay', 'Jay123', 'wali kelas'),
(12345678, 'joy', 'Joy123', 'admin'),
(12345679, 'Larr', 'Larr123', 'guru');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `absensi_akbar`
--
ALTER TABLE `absensi_akbar`
  ADD PRIMARY KEY (`id_absen`),
  ADD KEY `nis` (`nis`);

--
-- Indexes for table `guru_akbar`
--
ALTER TABLE `guru_akbar`
  ADD PRIMARY KEY (`id_guru`),
  ADD KEY `id_mapel` (`id_mapel`);

--
-- Indexes for table `kelas_akbar`
--
ALTER TABLE `kelas_akbar`
  ADD PRIMARY KEY (`id_kelas`),
  ADD KEY `id_guru` (`id_guru`);

--
-- Indexes for table `mapel_akbar`
--
ALTER TABLE `mapel_akbar`
  ADD PRIMARY KEY (`id_mapel`);

--
-- Indexes for table `nilai_akbar`
--
ALTER TABLE `nilai_akbar`
  ADD PRIMARY KEY (`id_nilai`),
  ADD KEY `nis` (`nis`,`id_mapel`),
  ADD KEY `nilai_ahkam_ibfk_1` (`id_mapel`);

--
-- Indexes for table `siswa_akbar`
--
ALTER TABLE `siswa_akbar`
  ADD PRIMARY KEY (`nis`),
  ADD KEY `id_kelas` (`id_kelas`);

--
-- Indexes for table `user_akbar`
--
ALTER TABLE `user_akbar`
  ADD PRIMARY KEY (`id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `absensi_akbar`
--
ALTER TABLE `absensi_akbar`
  ADD CONSTRAINT `absensi_akbar_ibfk_1` FOREIGN KEY (`nis`) REFERENCES `siswa_akbar` (`nis`);

--
-- Constraints for table `guru_akbar`
--
ALTER TABLE `guru_akbar`
  ADD CONSTRAINT `guru_akbar_ibfk_1` FOREIGN KEY (`id_mapel`) REFERENCES `mapel_akbar` (`id_mapel`);

--
-- Constraints for table `kelas_akbar`
--
ALTER TABLE `kelas_akbar`
  ADD CONSTRAINT `kelas_akbar_ibfk_1` FOREIGN KEY (`id_guru`) REFERENCES `guru_akbar` (`id_guru`);

--
-- Constraints for table `nilai_akbar`
--
ALTER TABLE `nilai_akbar`
  ADD CONSTRAINT `nilai_akbar_ibfk_1` FOREIGN KEY (`id_mapel`) REFERENCES `mapel_akbar` (`id_mapel`),
  ADD CONSTRAINT `nilai_akbar_ibfk_2` FOREIGN KEY (`nis`) REFERENCES `siswa_akbar` (`nis`);

--
-- Constraints for table `siswa_akbar`
--
ALTER TABLE `siswa_akbar`
  ADD CONSTRAINT `siswa_akbar_ibfk_1` FOREIGN KEY (`id_kelas`) REFERENCES `kelas_akbar` (`id_kelas`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
