create database Theatre;
use theatre;

create table person(
PersonID int(6) not null,
FirstName varchar(35) not null,
MInit varchar(35),
LastName varchar(35) not null,
PersonType varchar(25) not null,
DateHired date not null,
PhoneNumber varchar(12) not null,
Address varchar(70) not null,
Title varchar(30),
-- username varchar(50) not null,
-- password varchar(50) not null,
email varchar(30),
Instrument varchar(30),
primary key (PersonID));

-- create table City(
-- CityID varchar(5) not null,
-- State varchar(2) not null,
-- County varchar(30) not null,
-- primary key(CityID));

create table venue(
VenueID int(5) not null,
Name varchar(50)not null,
Address varchar(70)not null,
PhoneNumber varchar(12)not null,
-- CityID varchar(5) not null,
Longitude float not null,
Latitude float not null,
primary key(VenueID));

create table performance(
PerformanceID int(5) not null,
VenueID int(5) not null,
-- ShowID varchar(5) not null,
PerformanceDate date not null,
PerformanceTime time not null,
primary key(PerformanceID),
foreign key(VenueID) references venue(VenueID));

create table role(
RoleID int(5) not null,
RoleName varchar(35) not null,
PersonID int(6) not null,
PerformanceID int(5) not null,
primary key(RoleID),
foreign key(PersonID) references person(PersonID),
foreign key(PerformanceID) references performance(PerformanceID));

insert into person
(PersonID, FirstName, Minit, LastName, PersonType, DateHired, PhoneNumber, Address, Title, email)
Values
(1, 'Khaila', null, 'Wilcoxon', 'Actress', '2022-01-01', '202-555-0121', '387 Ziemann Lane', null, 'kwilcoxon@gmail.com'), 
(2, 'Storm', null, 'Lever', 'Actress', '2022-01-01', '687-331-4200', '32042 Mollie Knoll', null, 'slevel@gmail.com'), 
(3, 'Jasmine', null, 'Forsberg', 'Actress', '2022-01-01', '916-240-9388', '183 Elza Estates Apt 993', null, 'jforsberg@gmail.com'), 
(4, 'Olivia', null, 'Donalson', 'Actress', '2022-01-01', '202-796-5398', '869 Kaylie Inlet', null, 'odonalson@gmail.com'), 
(5, 'Didi', null,  'Romero', 'Actress', '2022-01-01', '505-348-4630', '6564 Carlos Ridge Suite 537', null, 'dromero@gmail.com'), 
(6, 'Gaberila', null, 'Carrillo', 'Actress', '2022-01-01', '851-870-2932', '344 Kling Parkways Apt 246', null, 'gcarrillo@gmail.com'), 
(7, 'Erin', null, 'Ramirez', 'Alternate', '2022-01-01', '473-348-4013', '836 Ashtyn Vista', null, 'eramirez@gmail.com'), 
-- Anne Boleyn, Katherine Howard, Catherine Parr
(8, 'Cassie', null, 'Silva', 'Alternate/Dance Captain', '2022-01-01', '202-432-4832', '4687 Lonie Crest', null,'csilva@gmail.com'), 
-- Anne Boleyn, Anna of Cleves, Katherine Howard
(9, 'Kelsee', null, 'Sweigard', 'Alternate', '2022-01-01', '382-871-8755', '4467 Lowe Lights Suite 802', null, 'ksweigard@gmail.com'), 
-- Catherine of Aragon, Jane Seymour, Catherine Parr
(10, 'Kelly', 'D', 'Taylor', 'Alternate', '2022-01-01', '458-318-4735', '60655 Amira Landing', null, 'kdtaylor@gmail.com'), 
-- Catherine of Aragon, Jane Seymour, Anna of Cleves
(11, 'Jamie', null, 'Armitage', 'Admin', '2022-01-01', '857-999-0906', '468 Lovebird Lane', 'Director', 'jarmitage@gmail.com');

insert into venue
(VenueID, Name, Address, PhoneNumber, Latitude, Longitude)
Values
(1, 'CIBC Theater', '18 West Monroe Street', '312-977-1700', 41.880833, -87.628333), 
(2, 'National Theatre', '1321 Pennsylvania Ave NW', '202-628-6161', 38.896481, -77.030441), 
(3, 'Smith Center', '361 Symphony Park Avenue', '702-749-2000', 36.168980, -115.151200),
(4, 'Dr. Philips Center', ' 445 S Magnolia Ave', '844-513-2014 ', 28.537710, -81.376602), 
(5, 'Boward Center for the Performing Arts', '201 SW 5th Ave', '954-462-0222', 26.119660, -80.149420);

insert into performance
(PerformanceID, VenueID, PerformanceDate, PerformanceTime)
Values
(1, 1, '2022-06-03', '19:00:00'),
(2, 1, '2022-06-04', '19:00:00'),
(3, 1, '2022-06-05', '19:00:00'),
(4, 2, '2022-06-10', '19:00:00'),
(5, 2, '2022-06-11', '19:00:00'),
(6, 2, '2022-06-12', '19:00:00'),
(7, 3, '2022-06-17', '19:00:00'),
(8, 3, '2022-06-18', '19:00:00'),
(9, 3, '2022-06-19', '19:00:00'),
(10, 4, '2022-06-24', '19:00:00'),
(11, 4, '2022-06-25', '19:00:00'),
(12, 4, '2022-06-26', '19:00:00'),
(13, 5, '2022-07-01', '19:00:00'),
(14, 5, '2022-07-03', '14:00:00'),
(15, 5, '2022-07-03', '19:00:00');

-- Catherine of Aragon: Khalia Wilcoxon (1),                                       Kelsee Sweigard (9), Kelly Denice Taylor (10)
-- Anne Boleyn:         Storm Lever (2),       Erin Ramirez (7), Cassie Silva (8) 
-- Jane Seymour:        Jasmine Forsberg(3),                                       Kelsee Sweigard (9), Kelly Denice Taylor (10)
-- Anna of Cleves:      Olivia Donalson (4),                     Cassie Silva (8),                      Kelly Denice Taylor (10)
-- Katherine Howard:    Didi Romero (5),       Erin Ramirez (7), Cassie Silva (8)
-- Catherine Parr:      Gabriela Carrillo (6), Erin Ramirez (7),                   Kelsee Sweigard (9)

insert into role
(RoleID, RoleName, PersonID, PerformanceID)
Values
(1, "Catherine of Aragon", 1, 1), 
(2, "Anne Boleyn",         2, 1),
(3, "Jane Seymour",        3, 1), 
(4, "Anna of Cleves",      4, 1),
(5, "Katherine Howard",    5, 1),
(6, "Catherine Parr",      6, 1),

(7, "Catherine of Aragon", 9, 2), 
(8, "Anne Boleyn",         2, 2),
(9, "Jane Seymour",        3, 2), 
(10, "Anna of Cleves",      4, 2),
(11, "Katherine Howard",    5, 2),
(12, "Catherine Parr",      6, 2),

(13, "Catherine of Aragon", 1, 3), 
(14, "Anne Boleyn",         8, 3),
(15, "Jane Seymour",        3, 3), 
(16, "Anna of Cleves",      4, 3),
(17, "Katherine Howard",    5, 3),
(18, "Catherine Parr",      6, 3),

(19, "Catherine of Aragon", 1, 4), 
(20, "Anne Boleyn",         2, 4),
(21, "Jane Seymour",        10, 4), 
(22, "Anna of Cleves",      4, 4),
(23, "Katherine Howard",    5, 4),
(24, "Catherine Parr",      6, 4),

(25, "Catherine of Aragon", 1, 5), 
(26, "Anne Boleyn",         2, 5),
(27, "Jane Seymour",        3, 5), 
(28, "Anna of Cleves",      8, 5),
(29, "Katherine Howard",    5, 5),
(30, "Catherine Parr",      6, 5),

(31, "Catherine of Aragon", 1, 6), 
(32, "Anne Boleyn",         2, 6),
(33, "Jane Seymour",        3, 6), 
(34, "Anna of Cleves",      4, 6),
(35, "Katherine Howard",    7, 6),
(36, "Catherine Parr",      6, 6),

(37, "Catherine of Aragon", 1, 7), 
(38, "Anne Boleyn",         2, 7),
(39, "Jane Seymour",        3, 7), 
(40, "Anna of Cleves",      4, 7),
(41, "Katherine Howard",    5, 7),
(42, "Catherine Parr",      9, 7),

(43, "Catherine of Aragon", 1, 8), 
(44, "Anne Boleyn",         2, 8),
(45, "Jane Seymour",        3, 8), 
(46, "Anna of Cleves",      4, 8),
(47, "Katherine Howard",    5, 8),
(48, "Catherine Parr",      6, 8),

(49, "Catherine of Aragon", 10, 9), 
(50, "Anne Boleyn",         2, 9),
(51, "Jane Seymour",        3, 9), 
(52, "Anna of Cleves",      4, 9),
(53, "Katherine Howard",    5, 9),
(54, "Catherine Parr",      6, 9),

(55, "Catherine of Aragon", 1, 10), 
(56, "Anne Boleyn",         8, 10),
(57, "Jane Seymour",        3, 10),
(58, "Anna of Cleves",      4, 10),
(59, "Katherine Howard",    5, 10),
(60, "Catherine Parr",      6, 10),

(61, "Catherine of Aragon", 1, 11), 
(62, "Anne Boleyn",         10, 11),
(63, "Jane Seymour",        3, 11), 
(64, "Anna of Cleves",      4, 11),
(65, "Katherine Howard",    5, 11),
(66, "Catherine Parr",      6, 11),

(67, "Catherine of Aragon", 1, 12), 
(68, "Anne Boleyn",         2, 12),
(69, "Jane Seymour",        9, 12), 
(70, "Anna of Cleves",      4, 12),
(71, "Katherine Howard",    5, 12),
(72, "Catherine Parr",      6, 12),

(73, "Catherine of Aragon", 1, 13), 
(74, "Anne Boleyn",         2, 13),
(75, "Jane Seymour",        3, 13), 
(76, "Anna of Cleves",      8, 13),
(77, "Katherine Howard",    5, 13),
(78, "Catherine Parr",      7, 13),

(79, "Catherine of Aragon", 1, 14), 
(80, "Anne Boleyn",         2, 14),
(81, "Jane Seymour",        3, 14), 
(82, "Anna of Cleves",      4, 14),
(83, "Katherine Howard",    5, 14),
(84, "Catherine Parr",      6, 14),

(85, "Catherine of Aragon", 1, 15), 
(86, "Anne Boleyn",         8, 15),
(87, "Jane Seymour",        3, 15), 
(88, "Anna of Cleves",      4, 15),
(89, "Katherine Howard",    5, 15),
(90, "Catherine Parr",      7, 15),
