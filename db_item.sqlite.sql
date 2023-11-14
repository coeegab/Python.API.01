-- Apaga o banco de dados que existem
-- CUIDADO! Isso destrói todos os dados do banco.

DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS owner;

-- Cria a tabela 'owner'.
CREATE TABLE owner(
    owner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    owner_name TEXT,
    owner_email TEXT,
    owner_password TEXT,
    owner_birth DATE,
    owner_status TEXT DEFAULT 'on',
    owner_field1 TEXT,
    owner_field2 TEXT
);

-- Popular a tabela 'owner' com dados 'fake'
INSERT INTO owner 
	(owner_id, owner_date, owner_name, owner_email,
	owner_password, owner_birth, owner_status)
VALUES
('1', '2023-09-22 22:220:22', 'Gabx7', 'gabx7@gmail.com',
'157', '2005/09/02', 'on');
	
INSERT INTO owner (owner_name, owner_email, owner_password, owner_birth, owner_status) VALUES
    ('John Doe', 'john.doe@email.com', 'password123', '1990-05-15', 'on'),
    ('Jane Smith', 'jane.smith@email.com', 'pass456', '1985-08-22', 'off'),
    ('Bob Johnson', 'bob.johnson@email.com', 'pass789', '1982-03-10', 'on'),
    ('Charlie Davis', 'charlie.davis@email.com', 'xyz789', '1988-07-03', 'on'),
	('Alice Brown', 'alice.brown@email.com', 'abc123', '1995-11-28', 'off');
	
	
CREATE TABLE item(
	item_id INTEGER PRIMARY KEY AUTOINCREMENT,
	item_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	item_name TEXT,
	item_description TEXT,
	item_location TEXT,
	item_owner INTEGER,
	item_status TEXT DEFAULT 'on',
	item_field1 TEXT,
    item_field2 TEXT,
	FOREIGN KEY(item_owner)REFERENCES owner (owner_id)
);

-- Criar a tabela 'item' com dados 'fake'

INSERT INTO item (item_date,item_name, item_description, item_location, item_owner, item_status)
VALUES
    ('2023-06-22 19:11:22','Laptop', 'A high-performance laptop with 16GB RAM', 'Office', 1, 'on'),
    ('2023-07-02 20:54:03','Camera', 'Digital camera with 20MP resolution', 'Studio', 2, 'off'),
    ('2023-05-06 20:23:59','Bicycle', 'Mountain bike with 21 gears', 'Garage', 3, 'on'),
	('2023-07-08 20:12:44','Car', 'car future', 'Rua', 4, 'on'),
    ('2023-09-06 20:20:29','Bookshelf', 'Wooden bookshelf with five shelves', 'Living Room', 5, 'off'),
    ('2023-05-07 11:20:27','Smartphone', 'Latest smartphone with dual cameras', 'Bedroom', 6, 'on');



