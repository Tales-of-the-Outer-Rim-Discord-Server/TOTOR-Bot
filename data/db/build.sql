-- CREATE TABLE IF NOT EXISTS rules (
--     RuleNo integer PRIMARY KEY,
--     Rule TEXT
-- );

CREATE TABLE IF NOT EXISTS BountyHunter (
    DiscordID integer PRIMARY KEY,
    HunterName TEXT DEFAULT BLANK,
    Bounties_Completed integer DEFAULT 0,
    Bounty_Value integer DEFAULT 0,
    Guild TEXT DEFAULT NONE
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
    AssassinName TEXT DEFAULT BLANK,
    Completed integer DEFAULT 0,
    AssainationValue integer DEFAULT 0
);