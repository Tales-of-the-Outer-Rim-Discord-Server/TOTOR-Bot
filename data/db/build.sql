CREATE TABLE IF NOT EXISTS rules (
    RuleNo integer PRIMARY KEY,
    Rule TEXT
);

CREATE TABLE IF NOT EXISTS BountyHunter (
    DiscordID integer PRIMARY KEY,
    Bounties_Completed integer,
    Bounty_Value integer
);

CREATE TABLE IF NOT EXISTS Bounty_Board (
    PlacedByID integer PRIMARY KEY,
    TargetID integer,
    ValueDead integer,
    ValueAlive integer,
    OtherInfo TEXT
)