-- Insert data into the customers table
INSERT INTO customers (CustomerID, CustomerName, CustomerPhone)
VALUES
    (1, 'Andi Setiawan', '81234567890'),
    (2, 'Siti Nurhaliza', '82345678901'),
    (3, 'Budi Santoso', '83456789012'),
    (4, 'Ani Lestari', '84567890123'),
    (5, 'Dedi Prasetyo', '85678901234'),
    (6, 'Laila Rahmawati', '86789012345');

-- Insert data into the deliveryagents table
INSERT INTO deliveryagents (DeliveryAgentID, DeliveryAgentName)
VALUES
    (1, 'Alex'),
    (2, 'Maria'),
    (3, 'Sarah'),
    (4, 'John'),
    (5, 'Mike');

-- Insert data into the orders table
INSERT INTO orders (OrderID, CustomerID, DeliveryAgentID, DeliveryDate, DeliveryAddress)
VALUES
    (101, 1, 1, '2024-12-25', 'Jl. Merdeka No. 12, Jakarta'),
    (102, 2, 2, '2024-12-26', 'Jl. Ahmad Yani No. 34, Bandung'),
    (103, 3, 1, '2024-12-27', 'Jl. Diponegoro No. 56, Surabaya'),
    (104, 4, 3, '2024-12-28', 'Jl. Sudirman No. 78, Semarang'),
    (105, 1, 2, '2024-12-29', 'Jl. Merdeka No. 12, Jakarta'),
    (106, 5, 3, '2024-12-30', 'Jl. Kartini No. 90, Yogyakarta'),
    (107, 6, 1, '2024-12-31', 'Jl. Pahlawan No. 101, Medan');

-- Insert data into the orderdetails table
INSERT INTO orderdetails (OrderID, ItemName, Quantity, Price)
VALUES
    (101, 'Box A', 5, 150),
    (101, 'Box B', 3, 100),
    (102, 'Box C', 2, 100),
    (102, 'Box D', 1, 50),
    (103, 'Box E', 10, 300),
    (104, 'Box A', 1, 150),
    (104, 'Box B', 2, 100),
    (105, 'Box F', 6, 180),
    (106, 'Box G', 4, 200),
    (106, 'Box H', 5, 150),
    (107, 'Box I', 3, 120);
