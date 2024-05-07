# Domain Model Specification

## Tables

### Organizations
- id (SERIAL, PK) # Autoincrementing integer
- segment_id (INTEGER, FK > Segment.id)
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
- category (VARCHAR)
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
- club_id (INTEGER, FK > Club.id)
- contact_id (INTEGER, FK > Contact.id)
- organization_id (INTEGER, FK > Organization.id)

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
- organization_id (INTEGER, FK > Organization.id)
- club_id (INTEGER, FK > Club.id)

### Clubs
- id (SERIAL, PK)
- name (VARCHAR)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- organization_id (INTEGER, FK > Organization.id)

## Relationships

### Organizations
- One organization can belong to one segment (N to 1)
- One organization can have many agent (1 to N)
- One organization can have many contact (1 to N)
- One organization can have many club (1 to N)


### Agents
- One agent belongs to one organization (N to 1)
- One agent belongs to one contact (1 to 1)
- One agent belongs to one club (N to 1)

### Segments
- One segment can have many organization (1 to N)

### Contacts
- One contact belongs to one organization (N to 1)
- One contact can belong to one club (N to 1)
- One contact belongs to one agent (1 to 1)

### Clubs
- One club belongs to one organization (N to 1)
- One club can have many contact (1 to N)
- One club can have many agent (1 to N)
