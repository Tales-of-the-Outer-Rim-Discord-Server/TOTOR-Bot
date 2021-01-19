CREATE TABLE IF NOT EXISTS BountyHunter (
    DiscordID integer PRIMARY KEY,
    HunterName TEXT,
    Completed integer DEFAULT 0,
    Total_Jobs_Value integer DEFAULT 0,
    Guild TEXT DEFAULT "No Guild"
);

CREATE TABLE IF NOT EXISTS BountyBoard (
    BountyNum integer PRIMARY KEY AUTOINCREMENT,
    PlacedByID integer,
    TargetID integer,
    ValueDead integer,
    ValueAlive integer,
    OtherInfo TEXT DEFAULT 'No Other Information'
);

CREATE TABLE IF NOT EXISTS Assassins (
    DiscordID integer PRIMARY KEY,
    AssassinName TEXT,
    Completed integer DEFAULT 0,
    Total_Jobs_Value integer DEFAULT 0
);