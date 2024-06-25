# Domain Model Specification (Logical & Physical Schema)

## Tables

### Segments
- id (SERIAL, PK)
- name (VARCHAR)
- created_at (TIMESTAMP)

#### Preview:
```bash
gp_db_contacts=# \d+ segments
                                        Table "public.segments"                                   
   Column   |            Type             | Collation | Nullable |               Default                |
------------+-----------------------------+-----------+----------+--------------------------------------+
 id         | integer                     |           | not null | nextval('segments_id_seq'::regclass) |
 name       | character varying           |           |          |                                      |
 created_at | timestamp without time zone |           |          | now()                                |
```

### Organizations
- id (SERIAL, PK) # Autoincrementing integer
- segment_id (INTEGER, FK > Segments.id)
- name (VARCHAR)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- street_address (VARCHAR)
- geom (GEOMETRY) # PostgreSQL geometry data type for spatial data
- latitude (FLOAT)
- longitude (FLOAT)
- city (VARCHAR)
- state (VARCHAR)
- zip (VARCHAR)
- slug (VARCHAR)
- custom_fields (JSONB) # PostgreSQL JSON data type

#### Preview:
```bash
gp_db_contacts=# \d+ organizations;
                                        Table "public.organizations"
     Column     |            Type             | Collation | Nullable |                  Default                  |
----------------+-----------------------------+-----------+----------+-------------------------------------------+
 id             | integer                     |           | not null | nextval('organizations_id_seq'::regclass) |
 segment_id     | integer                     |           | not null |                                           |
 name           | character varying           |           |          |                                           |
 created_at     | timestamp without time zone |           |          | now()                                     |
 updated_at     | timestamp without time zone |           |          |                                           |
 street_address | character varying           |           |          |                                           |
 latitude       | double precision            |           |          |                                           |
 longitude      | double precision            |           |          |                                           |
 city           | character varying           |           |          |                                           |
 state          | character varying           |           |          |                                           |
 zip            | character varying           |           |          |                                           |
 slug           | character varying           |           | not null |                                           |
 custom_fields  | json                        |           |          |                                           |
 geom           | geometry(Point,4326)        |           |          |                                           |
 category       | character varying           |           |          |                                           |

```

### Clubs
- id (SERIAL, PK)
- name (VARCHAR)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- organization_id (INTEGER, FK > Organizations.id)

#### Preview:
```bash
gp_db_contacts=# \d+ clubs
                                        Table "public.clubs"
     Column      |            Type             | Collation | Nullable |              Default              |
-----------------+-----------------------------+-----------+----------+-----------------------------------+
 id              | integer                     |           | not null | nextval('clubs_id_seq'::regclass) | 
 name            | character varying           |           |          |                                   |
 created_at      | timestamp without time zone |           |          | now()                             | 
 updated_at      | timestamp without time zone |           |          |                                   | 
 organization_id | integer                     |           | not null |                                   | 

```

### Contacts
- id (SERIAL, PK)
- email (VARCHAR)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- custom_fields (JSONB)
- organization_id (INTEGER, FK > Organizations.id)
- club_id (INTEGER, FK > Clubs.id)

#### Preview:
```bash
gp_db_contacts=# \d+ contacts;
                                        Table "public.contacts"
     Column      |            Type             | Collation | Nullable |               Default                | 
-----------------+-----------------------------+-----------+----------+--------------------------------------+
 id              | integer                     |           | not null | nextval('contacts_id_seq'::regclass) | 
 email           | character varying           |           | not null |                                      |
 created_at      | timestamp without time zone |           |          | now()                                | 
 updated_at      | timestamp without time zone |           |          |                                      | 
 custom_fields   | json                        |           |          |                                      |
 organization_id | integer                     |           | not null |                                      | 
 club_id         | integer                     |           |          |                                      | 

```

### Agents
- id (SERIAL, PK)
- rank (INTEGER)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- club_id (INTEGER, FK > Clubs.id)
- contact_id (INTEGER, FK > Contacts.id)
- organization_id (INTEGER, FK > Organizations.id)

#### Preview:
```bash
gp_db_contacts=# \d+ agents;
                                    Table "public.agents"
     Column      |            Type             | Collation | Nullable |              Default               |
-----------------+-----------------------------+-----------+----------+------------------------------------+
 id              | integer                     |           | not null | nextval('agents_id_seq'::regclass) |
 rank            | integer                     |           |          |                                    |
 created_at      | timestamp without time zone |           |          | now()                              |
 updated_at      | timestamp without time zone |           |          |                                    |
 club_id         | integer                     |           |          |                                    |
 contact_id      | integer                     |           | not null |                                    |
 organization_id | integer                     |           | not null |                                    |

```

## Relationships

### Segments
- One segment can have many organizations (1 to N)

### Organizations
- One organization can belong to one segments (N to 1)
- One organization can have many agents (1 to N)
- One organization can have many contacts (1 to N)
- One organization can have many clubs (1 to N)

### Clubs
- One club belongs to one organization (N to 1)
- One club can have many contacts (1 to N)
- One club can have many agents (1 to N)

### Contacts
- One contact belongs to one organization (N to 1)
- One contact can belong to one club (N to 1)
- One contact belongs to one agent (1 to 1)

### Agents
- One agent belongs to one organizations (N to 1)
- One agent belongs to one contacts (1 to 1)
- One agent belongs to one clubs (N to 1)



