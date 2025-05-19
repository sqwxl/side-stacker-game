drop table if exists game;
drop table if exists player;
drop table if exists move;

create table player (
    id integer primary key,
    created_on text default current_timestamp,
    token text unique not null check (length(token) > 0)
);

create index if not exists idx_player_token on player (token);

create table game (
    id integer primary key,
    code text not null unique,
    created_on text default current_timestamp,
    ended_on text,
    winner_id integer references player (id),
    player_0_id integer references player (id),
    player_1_id integer references player (id)
);

create table move (
    id integer primary key,
    game_id integer not null references game (id) on delete cascade,
    created_on text default current_timestamp,
    turn integer not null,
    col integer not null,
    row integer not null,

    unique (game_id, col, row),
    unique (game_id, turn)
);

create index if not exists idx_move_game_id on move (game_id);

-- ai players
insert into player (token)
values
('00000000-0000-0000-0000-000000000000'), -- easy
('00000000-0000-0000-0000-000000000001'), -- medium
('00000000-0000-0000-0000-000000000002'); -- hard
