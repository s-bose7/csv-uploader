# Domain Model Specification

## Tables

### Organization
- organization_id (string, PK)
- name (string)
- created_at (timestamp)
- updated_at (timestamp)
- address (string)
- dma (number)
- latitude (number)
- longitude (number)
- city (string)
- state (string)
- zip (string)
- slug (string)

### Agent
- agent_id (string, PK)
- agent_rank (number)
- should_schedule (boolean)
- segment_name (string, FK > Segments.segment_name)
- organization_id (string, FK > Organizations.organization_id)

### Segment
- segment_name (string, PK)
- created_at (timestamp)

### Contact
- email (string, PK)
- created_at (timestamp)
- updated_at (timestamp)
- agent_id (string, FK > Agents.agent_id)
- source (string)
- state (boolean)
- unresponsive_at (timestamp)
- is_marketable (boolean)
- hatchbuck_updated_at (timestamp)
- unmarkatable_message (string)

### Club
- club_id (string, PK)
- clud_name (string)
- organization_id (string, FK > Organizations.organization_id)
- segment_name (string)

## Relationships

### Organization
- One organization can have many agents (1 to N)
- One organization can have many clubs (1 to N)

### Agent
- One agent belongs to one organization (N to 1)
- One agent can have many contacts (1 to N)
- One agent belongs to one segment (N to 1)

### Segment
- One segment can have many agents (1 to N)
- One segment can have many clubs (1 to N)

### Contact
- One contact belongs to one agent (N to 1)

### Club
- One club belongs to one organization (N to 1)