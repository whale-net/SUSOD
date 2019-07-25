/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for dbSUSOD
CREATE DATABASE IF NOT EXISTS `dbSUSOD` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE `dbSUSOD`;

-- Dumping structure for table dbSUSOD.Albums
CREATE TABLE IF NOT EXISTS `Albums` (
  `AlbumID` int(11) NOT NULL AUTO_INCREMENT,
  `AlbumName` varchar(128) NOT NULL,
  `CoverImage` int(11) NOT NULL,
  `EnteredBy` int(11) NOT NULL,
  `CreatedDate` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedBy` int(11) NOT NULL,
  `UpdatedDate` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`AlbumID`),
  KEY `IX_Albums_AlbumNameAlbumID` (`AlbumName`,`AlbumID`) USING BTREE,
  KEY `IX_Albums_CoverImage` (`CoverImage`) USING BTREE,
  KEY `IX_Albums_EnteredBy` (`EnteredBy`) USING BTREE,
  KEY `IX_Albums_UpdatedBy` (`UpdatedBy`) USING BTREE,
  CONSTRAINT `FK_Albums_CoverImage` FOREIGN KEY (`CoverImage`) REFERENCES `DataFiles` (`DataFileID`),
  CONSTRAINT `FK_Albums_EnteredBy` FOREIGN KEY (`EnteredBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_Albums_UpdatedBy` FOREIGN KEY (`UpdatedBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table dbSUSOD.AlbumsArtists
CREATE TABLE IF NOT EXISTS `AlbumsArtists` (
  `AlbumArtistsID` int(11) NOT NULL,
  `AlbumID` int(11) NOT NULL,
  `ArtistID` int(11) NOT NULL,
  PRIMARY KEY (`AlbumArtistsID`),
  UNIQUE KEY `IXU_AlbumsArtists_AlbumIDArtistID` (`AlbumID`,`ArtistID`) USING BTREE,
  KEY `IX_AlbumsArtists_AlbumID` (`AlbumID`) USING BTREE,
  KEY `IX_AlbumsArtists_ArtistID` (`ArtistID`) USING BTREE,
  CONSTRAINT `FK_AlbumsArtists_AlbumID` FOREIGN KEY (`AlbumID`) REFERENCES `Albums` (`AlbumID`),
  CONSTRAINT `FK_AlbumsArtists_ArtistID` FOREIGN KEY (`ArtistID`) REFERENCES `Artists` (`ArtistID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table dbSUSOD.Artists
CREATE TABLE IF NOT EXISTS `Artists` (
  `ArtistID` int(11) NOT NULL AUTO_INCREMENT,
  `ArtistName` varchar(128) NOT NULL,
  `ArtistImage` int(11) DEFAULT NULL,
  `EnteredBy` int(11) NOT NULL,
  `CreatedDate` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedBy` int(11) NOT NULL,
  `UpdatedDate` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`ArtistID`),
  KEY `IX_Artists_ArtistImage` (`ArtistImage`),
  KEY `IX_Artists_ArtistNameArtistID` (`ArtistName`,`ArtistID`),
  KEY `IX_Artists_EnteredBy` (`EnteredBy`) USING BTREE,
  KEY `IX_Artists_UpdatedBy` (`UpdatedBy`),
  CONSTRAINT `FK_Artists_ArtistImage` FOREIGN KEY (`ArtistImage`) REFERENCES `DataFiles` (`DataFileID`),
  CONSTRAINT `FK_Artists_EnteredBy` FOREIGN KEY (`EnteredBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_Artists_UpdatedBy` FOREIGN KEY (`UpdatedBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table dbSUSOD.DataFiles
CREATE TABLE IF NOT EXISTS `DataFiles` (
  `DataFileID` int(11) NOT NULL AUTO_INCREMENT,
  `EnteredBy` int(11) NOT NULL,
  `CreatedDate` datetime NOT NULL DEFAULT current_timestamp(),
  `FileData` longblob DEFAULT NULL,
  `FilePath` varchar(4096) DEFAULT NULL,
  `UseFilePath` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0=UseBlob 1=UseFilePath (File >4GB)',
  `FileName` varchar(255) NOT NULL,
  `DataFileTypeID` int(11) NOT NULL,
  PRIMARY KEY (`DataFileID`),
  KEY `IX_DataFiles_EnteredBy` (`EnteredBy`) USING BTREE,
  KEY `IX_DataFiles_FilePath` (`FilePath`(191)),
  KEY `IX_DataFiles_UseFilePath` (`UseFilePath`),
  KEY `IX_DataFiles_FileName` (`FileName`(191)),
  KEY `FK_DataFiles_DataFileTypeID` (`DataFileTypeID`),
  CONSTRAINT `FK_DataFiles_DataFileTypeID` FOREIGN KEY (`DataFileTypeID`) REFERENCES `DataFileTypes` (`DataFileTypeID`),
  CONSTRAINT `FK_DataFiles_EnteredBy` FOREIGN KEY (`EnteredBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table dbSUSOD.DataFileTypes
CREATE TABLE IF NOT EXISTS `DataFileTypes` (
  `DataFileTypeID` int(11) NOT NULL AUTO_INCREMENT,
  `EnteredBy` int(11) NOT NULL,
  `CreatedDate` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedDate` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Extension` varchar(16) NOT NULL,
  `MIMEType` varchar(50) DEFAULT NULL,
  `UpdatedBy` int(11) NOT NULL,
  PRIMARY KEY (`DataFileTypeID`),
  UNIQUE KEY `IXU_DataFileTypes_Extension` (`Extension`),
  KEY `IX_DataFileTypes_EnteredBy` (`EnteredBy`),
  KEY `IX_DataFileTypes_UpdatedBy` (`UpdatedBy`),
  CONSTRAINT `FK_DataFileTypes_EnteredBy` FOREIGN KEY (`EnteredBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_DataFileTypes_UpdatedBy` FOREIGN KEY (`UpdatedBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table dbSUSOD.Playlists
CREATE TABLE IF NOT EXISTS `Playlists` (
  `PlaylistID` int(11) NOT NULL AUTO_INCREMENT,
  `PlaylistName` varchar(128) NOT NULL,
  `PlaylistImage` int(11) DEFAULT NULL,
  `EnteredBy` int(11) NOT NULL,
  `CreatedDate` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedBy` int(11) NOT NULL,
  `UpdatedDate` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`PlaylistID`),
  KEY `IX_Playlists_EnteredBy` (`EnteredBy`) USING BTREE,
  KEY `IX_Playlists_PlaylistNamePlaylistID` (`PlaylistName`,`PlaylistID`),
  KEY `IX_Playlists_PlaylistImage` (`PlaylistImage`),
  KEY `IX_Playlists_UpdatedBy` (`UpdatedBy`),
  CONSTRAINT `FK_Playlists_EnteredBy` FOREIGN KEY (`EnteredBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_Playlists_PlaylistImage` FOREIGN KEY (`PlaylistImage`) REFERENCES `DataFiles` (`DataFileID`),
  CONSTRAINT `FK_Playlists_UpdatedBy` FOREIGN KEY (`UpdatedBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table dbSUSOD.PlaylistsSongs
CREATE TABLE IF NOT EXISTS `PlaylistsSongs` (
  `PlaylistID` int(11) NOT NULL,
  `SongID` int(11) NOT NULL,
  UNIQUE KEY `IXU_PlaylistsSongs_PlaylistIDSongID` (`PlaylistID`,`SongID`),
  KEY `IX_PlaylistsSongs_SongID` (`SongID`) USING BTREE,
  KEY `IX_PlaylistsSongs_PlaylistID` (`PlaylistID`),
  CONSTRAINT `FK_PlaylistsSongs_PlaylistID` FOREIGN KEY (`PlaylistID`) REFERENCES `Playlists` (`PlaylistID`),
  CONSTRAINT `FK_PlaylistsSongs_SongID` FOREIGN KEY (`SongID`) REFERENCES `Songs` (`SongID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table dbSUSOD.Plays
CREATE TABLE IF NOT EXISTS `Plays` (
  `PlayID` int(11) NOT NULL,
  `CreatedDate` datetime NOT NULL DEFAULT current_timestamp(),
  `EnteredBy` int(11) NOT NULL,
  `SongID` int(11) DEFAULT NULL,
  `VideoID` int(11) DEFAULT NULL,
  PRIMARY KEY (`PlayID`),
  KEY `IX_Plays_EnteredBy` (`EnteredBy`),
  KEY `IX_Plays_SongID` (`SongID`),
  KEY `IX_Plays_VideoID` (`VideoID`),
  CONSTRAINT `FK_Plays_SongID` FOREIGN KEY (`SongID`) REFERENCES `Songs` (`SongID`),
  CONSTRAINT `FK_Plays_VideoID` FOREIGN KEY (`VideoID`) REFERENCES `Videos` (`VideoID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table dbSUSOD.Songs
CREATE TABLE IF NOT EXISTS `Songs` (
  `SongID` int(11) NOT NULL AUTO_INCREMENT,
  `SongName` varchar(128) NOT NULL,
  `CreatedDate` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedDate` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `AlbumID` int(11) DEFAULT NULL,
  `DataFileID` int(11) NOT NULL,
  `EnteredBy` int(11) NOT NULL,
  `UpdatedBy` int(11) NOT NULL,
  PRIMARY KEY (`SongID`),
  KEY `IX_Songs_SongName` (`SongName`),
  KEY `IX_Songs_DataFileID` (`DataFileID`),
  KEY `IX_Songs_EnteredBy` (`EnteredBy`),
  KEY `IX_Songs_AlbumID` (`AlbumID`) USING BTREE,
  KEY `IX_Songs_UpdatedBy` (`UpdatedBy`),
  CONSTRAINT `FK_Songs_AlbumID` FOREIGN KEY (`AlbumID`) REFERENCES `Albums` (`AlbumID`),
  CONSTRAINT `FK_Songs_DataFileID` FOREIGN KEY (`DataFileID`) REFERENCES `DataFiles` (`DataFileID`),
  CONSTRAINT `FK_Songs_EnteredBy` FOREIGN KEY (`EnteredBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_Songs_UpdatedBy` FOREIGN KEY (`UpdatedBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table dbSUSOD.Users
CREATE TABLE IF NOT EXISTS `Users` (
  `UserID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(20) NOT NULL,
  `Password` varchar(200) NOT NULL COMMENT 'can be expanded to support larger hashes',
  `CreatedDate` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedDate` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `IXU_Users_Username` (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

-- Dumping structure for table dbSUSOD.Videos
CREATE TABLE IF NOT EXISTS `Videos` (
  `VideoID` int(11) NOT NULL,
  `EnteredBy` int(11) NOT NULL,
  `CreatedDate` datetime NOT NULL DEFAULT current_timestamp(),
  `UpdatedDate` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `DataFileID` int(11) NOT NULL,
  `UpdatedBy` int(11) NOT NULL,
  PRIMARY KEY (`VideoID`),
  KEY `IX_Videos_EnteredBy` (`EnteredBy`),
  KEY `IX_Videos_DataFileID` (`DataFileID`),
  KEY `IX_Videos_UpdatedBy` (`UpdatedBy`),
  CONSTRAINT `FK_Videos_DataFileID` FOREIGN KEY (`DataFileID`) REFERENCES `DataFiles` (`DataFileID`),
  CONSTRAINT `FK_Videos_EnteredBy` FOREIGN KEY (`EnteredBy`) REFERENCES `Users` (`UserID`),
  CONSTRAINT `FK_Videos_UpdatedBy` FOREIGN KEY (`UpdatedBy`) REFERENCES `Users` (`UserID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Data exporting was unselected.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
