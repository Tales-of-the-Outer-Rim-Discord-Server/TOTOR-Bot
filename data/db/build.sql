CREATE TABLE IF NOT EXISTS Schedule (
    Identifier INTEGER PRIMARY KEY AUTOINCREMENT,
    SessionNumb int,
    Attending text,
    Tentative text,
    NotAvailable text,
    SessionStart text
);

