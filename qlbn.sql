-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Máy chủ: 127.0.0.1
-- Thời gian đã tạo: Th7 17, 2025 lúc 03:00 PM
-- Phiên bản máy phục vụ: 10.4.24-MariaDB
-- Phiên bản PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Cơ sở dữ liệu: `qlbn`
--

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `khoa`
--

CREATE TABLE `khoa` (
  `khoa_id` int(11) NOT NULL,
  `ten_khoa` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Đang đổ dữ liệu cho bảng `khoa`
--

INSERT INTO `khoa` (`khoa_id`, `ten_khoa`) VALUES
(1, 'Khoa cấp cứu '),
(2, 'Khoa Chan Thuong ');

-- --------------------------------------------------------

--
-- Cấu trúc bảng cho bảng `thongtinbenhnhan`
--

CREATE TABLE `thongtinbenhnhan` (
  `benhnhan_id` int(11) NOT NULL,
  `ho_ten` varchar(100) NOT NULL,
  `ngay_sinh` date NOT NULL,
  `gioi_tinh` varchar(10) NOT NULL,
  `dia_chi` varchar(255) NOT NULL,
  `so_dien_thoai` varchar(50) NOT NULL,
  `khoa_id` int(11) NOT NULL,
  `ngay_nhap_vien` date NOT NULL,
  `ngay_ra_vien` date DEFAULT NULL,
  `chan_doan` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Đang đổ dữ liệu cho bảng `thongtinbenhnhan`
--

INSERT INTO `thongtinbenhnhan` (`benhnhan_id`, `ho_ten`, `ngay_sinh`, `gioi_tinh`, `dia_chi`, `so_dien_thoai`, `khoa_id`, `ngay_nhap_vien`, `ngay_ra_vien`, `chan_doan`) VALUES
(1, 'Minh Anh', '2004-11-10', 'nam ', 'Thái Bình ', '0369733661', 1, '2025-07-15', '2025-07-30', 'bị đau bụng '),
(6, 'Nguyen Minh Anh ', '2004-11-10', 'nam', 'Thai Binh', '369733662', 1, '2025-07-16', '0000-00-00', 'Dau Hong');

--
-- Chỉ mục cho các bảng đã đổ
--

--
-- Chỉ mục cho bảng `khoa`
--
ALTER TABLE `khoa`
  ADD PRIMARY KEY (`khoa_id`);

--
-- Chỉ mục cho bảng `thongtinbenhnhan`
--
ALTER TABLE `thongtinbenhnhan`
  ADD PRIMARY KEY (`benhnhan_id`),
  ADD KEY `khoa_thongtinbn` (`khoa_id`);

--
-- AUTO_INCREMENT cho các bảng đã đổ
--

--
-- AUTO_INCREMENT cho bảng `khoa`
--
ALTER TABLE `khoa`
  MODIFY `khoa_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT cho bảng `thongtinbenhnhan`
--
ALTER TABLE `thongtinbenhnhan`
  MODIFY `benhnhan_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Các ràng buộc cho các bảng đã đổ
--

--
-- Các ràng buộc cho bảng `thongtinbenhnhan`
--
ALTER TABLE `thongtinbenhnhan`
  ADD CONSTRAINT `khoa_thongtinbn` FOREIGN KEY (`khoa_id`) REFERENCES `khoa` (`khoa_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
