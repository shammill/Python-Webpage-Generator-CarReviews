# This is a simple SQL script to create the "car_reviews" database
# and the two tables that need to be populated, "car_details" and
# "car_ratings".  Run this script in the MySQL Workbench to set up
# the database in readiness for your Python programs.
#
# Warning: This script will delete any existing database called
# "car_reviews".

DROP DATABASE IF EXISTS car_reviews;

CREATE DATABASE car_reviews;

CREATE TABLE car_reviews.car_details
( carId VARCHAR(20),
  make VARCHAR(40),
  model VARCHAR(40),
  seriesYear VARCHAR(10),
  price INT(10), 
  engineSize VARCHAR(10),
  tankCapacity VARCHAR(10),
  bodyType VARCHAR(40),
  seatingCapacity INT(10),
  transmission VARCHAR(10)
);

CREATE TABLE car_reviews.car_ratings
( 
  ownerID VARCHAR(20),
  carId VARCHAR(20),
  overallRating INT(4),
  priceRating INT(4), 
  safetyRating INT(4),
  reliabilityRating INT(4),
  serviceRating INT(4),
  styleRating INT(4),
  postedDate VARCHAR(40)
) 

