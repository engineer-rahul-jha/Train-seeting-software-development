CREATE TABLE Seats (
    seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    row INTEGER NOT NULL,
    seat_number INTEGER NOT NULL,
    is_booked BOOLEAN DEFAULT 0
);

INSERT INTO Seats (row, seat_number, is_booked) VALUES
    (1, 1, 0), (1, 2, 0), (1, 3, 0), (1, 4, 0), (1, 5, 0), (1, 6, 0), (1, 7, 0),
    (2, 1, 0), (2, 2, 0), (2, 3, 0), (2, 4, 0), (2, 5, 0), (2, 6, 0), (2, 7, 0),
   
    (11, 1, 0), (11, 2, 0), (11, 3, 0);  
