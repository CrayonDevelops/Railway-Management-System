-- Create the database
CREATE DATABASE railwaymanagement;
USE railwaymanagement;

-- Create passengers table
CREATE TABLE passengers (
    passengerid INT PRIMARY KEY,
    name VARCHAR(100),
    contact VARCHAR(20)
);

-- Create trains table
CREATE TABLE trains (
    trid INT PRIMARY KEY,
    platno INT,
    status VARCHAR(50),
    depart DATE,
    depart_time TIME,
    arrival DATE,
    arrival_time TIME
);

-- Create routes table
CREATE TABLE routes (
    rtid INT PRIMARY KEY,
    trid INT,
    station_name VARCHAR(100),
    stopnum INT,
    arrival_date DATE,
    arrival_time TIME,
    depart_date DATE,
    depart_time TIME
);

-- Create seats table
CREATE TABLE seats (
    seatid INT PRIMARY KEY AUTO_INCREMENT,
    trid INT,
    seatnum VARCHAR(10),
    class VARCHAR(20),
    price INT,
    status VARCHAR(20) DEFAULT 'Available'
);

-- Create bookings table
CREATE TABLE bookings (
    bookingid INT PRIMARY KEY AUTO_INCREMENT,
    trid INT,
    passengerid INT,
    from_stid VARCHAR(100),
    to_stid VARCHAR(100),
    dateofdepart DATE,
    timeofdepart TIME,
    dateofarrival DATE,
    timeofarrival TIME,
    seatnum VARCHAR(10),
    bookingdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    price INT,
    status VARCHAR(100)
);

-- Create payments table
CREATE TABLE payments (
    paymentid INT PRIMARY KEY AUTO_INCREMENT,
    bookingid INT,
    price INT,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create users table
CREATE TABLE users (
    userid INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50),
    usertype ENUM('client', 'admin') DEFAULT 'client',
    passengerid INT
);
