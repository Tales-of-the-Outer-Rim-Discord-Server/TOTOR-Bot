CREATE TABLE IF NOT EXISTS BountyHunter (
    DiscordID integer PRIMARY KEY,
    HunterName TEXT,
    Bounties_Completed integer,
    Bounty_Value integer,
    Guild TEXT
);

CREATE TABLE IF NOT EXISTS BountyBoard (
    PlacedByID integer PRIMARY KEY,
    TargetID integer,
    ValueDead integer,
    ValueAlive integer,
    OtherInfo TEXT
);

CREATE TABLE IF NOT EXISTS Assassins (
    DiscordID integer PRIMARY KEY,
    AssassinName TEXT,
    Completed integer DEFAULT 0,
    AssainationValue integer DEFAULT 0
);