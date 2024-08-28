-- schema.sql

-- Create Users table
CREATE TABLE Users (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    ResetToken VARCHAR(255) NULL
);

-- Create Downloads table
CREATE TABLE Downloads (
    DownloadID INT AUTO_INCREMENT PRIMARY KEY,
    Filename VARCHAR(255) NOT NULL,
    UserID INT,
    FOREIGN KEY (UserID) REFERENCES Users(ID) ON DELETE CASCADE
);
