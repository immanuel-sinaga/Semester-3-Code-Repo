-- Create the database
CREATE DATABASE logistics;

-- Use the database
USE logistics;

-- Create the customers table
CREATE TABLE customers (
    CustomerID INT(11) NOT NULL AUTO_INCREMENT,
    CustomerName VARCHAR(32) NOT NULL,
    CustomerPhone VARCHAR(32) NOT NULL,
    PRIMARY KEY (CustomerID)
);

-- Create the deliveryagents table
CREATE TABLE deliveryagents (
    DeliveryAgentID INT(11) NOT NULL AUTO_INCREMENT,
    DeliveryAgentName VARCHAR(32) NOT NULL,
    PRIMARY KEY (DeliveryAgentID)
);

-- Create the orders table
CREATE TABLE orders (
    OrderID INT(11) NOT NULL AUTO_INCREMENT,
    CustomerID INT(11) NOT NULL,
    DeliveryAgentID INT(11) NOT NULL,
    DeliveryDate DATE NOT NULL,
    DeliveryAddress VARCHAR(32) NOT NULL,
    PRIMARY KEY (OrderID),
    FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
    FOREIGN KEY (DeliveryAgentID) REFERENCES deliveryagents(DeliveryAgentID)
);

-- Create the orderdetails table
CREATE TABLE orderdetails (
    OrderID INT(11) NOT NULL,
    ItemName VARCHAR(32) NOT NULL,
    Quantity INT(11) NOT NULL,
    Price INT(11) NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES orders(OrderID)
);
