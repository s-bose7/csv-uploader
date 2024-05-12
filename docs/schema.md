# Domain Model Specification

## Tables

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
- irs_ein (VARCHAR)
- irs_ntee_code (VARCHAR)
- school_grade (VARCHAR)
- fall_start_date (DATE) # Use DATE for date without time
- winter_start_date (DATE)

### Agents
- id (SERIAL, PK)
- rank (INTEGER)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- club_id (INTEGER, FK > Clubs.id)
- contact_id (INTEGER, FK > Contacts.id)
- organization_id (INTEGER, FK > Organizations.id)

### Segments
- id (SERIAL, PK)
- name (VARCHAR)
- created_at (TIMESTAMP)

### Contacts
- id (SERIAL, PK)
- email (VARCHAR)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- custom_fields (JSONB)
- source (VARCHAR)
- first_name (VARCHAR)
- position (VARCHAR)
- organization_id (INTEGER, FK > Organizations.id)
- club_id (INTEGER, FK > Clubs.id)

### Clubs
- id (SERIAL, PK)
- name (VARCHAR)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- organization_id (INTEGER, FK > Organizations.id)

## Relationships

### Organizations
- One organization can belong to one segments (N to 1)
- One organization can have many agents (1 to N)
- One organization can have many contacts (1 to N)
- One organization can have many clubs (1 to N)


### Agents
- One agent belongs to one organizations (N to 1)
- One agent belongs to one contacts (1 to 1)
- One agent belongs to one clubs (N to 1)

### Segments
- One segment can have many organizations (1 to N)

### Contacts
- One contact belongs to one organization (N to 1)
- One contact can belong to one club (N to 1)
- One contact belongs to one agent (1 to 1)

### Clubs
- One club belongs to one organization (N to 1)
- One club can have many contacts (1 to N)
- One club can have many agents (1 to N)
