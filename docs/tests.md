# Data Integrity Checks
One can run the individual integrity checks by executing SQL from psql shell or by preparing the data 
and running the `main.py -environment` script again and again.

## Update an existing organization's name:

View before updating the name:

```bash
 id |                  name                                  slug                      
----+----------------------------------------+-----------------------------------------------
  1 | Saa Wrestling                          | saawrestlingpobox252
  2 | Indiana 4H Foundation                  | indiana4hfoundation615wstatest
  3 | Woodward Granger Youth Tackle Football | woodwardgrangeryouthtacklefootball1908lowellst
  4 | Southeast Valley Baseball Association  | southeastvalleybaseballassociationpobox1396
  5 | Brooke County Nfl Flag Football        | brookecountynflflagfootball173capitoldr
  6 | Coeur Dalene Jr Tackle Football        | coeurdalenejrtacklefootballpobox658

```

View after updating the name:

NOTE: Changes in slug will be auto triggered using PL/SQL triggers.

```bash
 id |                  name                          slug                      
----+----------------------------------------+----------------+------------------------------
  1 | Charity 101 foundation                 | charity101foundationpobox252 # Updated
  2 | Indiana 4H Foundation                  | indiana4hfoundation615wstatest
  3 | Woodward Granger Youth Tackle Football | woodwardgrangeryouthtacklefootball1908lowellst
  4 | Southeast Valley Baseball Association  | southeastvalleybaseballassociationpobox1396
  5 | Brooke County Nfl Flag Football        | brookecountynflflagfootball173capitoldr
  6 | Coeur Dalene Jr Tackle Football        | coeurdalenejrtacklefootballpobox658

```

## Update email of an existing organization/contact

View before updating the emails:

```bash
 id | organization_id |                 email                 
----+-----------------+---------------------------------------
  1 |               1 | saawrestlingrams@gmail.com
  2 |               2 | shelly@in4h.org
  3 |               3 | wgyouthfootball@gmail.com
  4 |               4 | bo.jensen1845@gmail.com
  5 |               5 | brookecountynflflagfootball@gmail.com
  6 |               6 | cdajrtackle@gmail.com
```
View after updating the emails:

```bash
 id | organization_id |                 email                 
----+-----------------+---------------------------------------
  1 |               1 | abcorganization@gmail.com # Updated
  2 |               2 | shelly@in4h.org
  3 |               3 | wgyouthfootball@gmail.com
  4 |               4 | bo.jensen1845@gmail.com
  5 |               5 | brookecountynflflagfootball@gmail.com
  6 |               6 | cdajrtackle@gmail.com

```


## Update an existing contact to be linked with a new club

View before updating the club:

```bash
 contact_id |                 email                 | club_id | club_name 
------------+---------------------------------------+---------+-----------
          1 | saawrestlingrams@gmail.com            |       1 | club_1
          2 | shelly@in4h.org                       |       2 | club_2
          3 | wgyouthfootball@gmail.com             |       3 | club_3
          4 | bo.jensen1845@gmail.com               |       4 | club_4
          5 | brookecountynflflagfootball@gmail.com |       5 | club_5

```
View after updating the club:

```bash
 contact_id |                 email                 | club_id | club_name 
------------+---------------------------------------+---------+-----------
          1 | saawrestlingrams@gmail.com            |       6 | club_6 # Updated
          2 | shelly@in4h.org                       |       2 | club_2
          3 | wgyouthfootball@gmail.com             |       3 | club_3
          4 | bo.jensen1845@gmail.com               |       4 | club_4
          5 | brookecountynflflagfootball@gmail.com |       5 | club_5

```

## Add a new custom field to an existing organization

View before updating the custom field:

```bash
                             custom_fields                              
------------------------------------------------------------------------
 {"irs_ein": 823385206.0, "irs_ntee_code": null, "school_grade": null}
 {"irs_ein": 351097611.0, "irs_ntee_code": null, "school_grade": null}
 {"irs_ein": 842048006.0, "irs_ntee_code": null, "school_grade": null}
 {"irs_ein": 870578791.0, "irs_ntee_code": "N63", "school_grade": null}
 {"irs_ein": 863214157.0, "irs_ntee_code": null, "school_grade": null}
 {"irs_ein": 820501975.0, "irs_ntee_code": null, "school_grade": null}
```
View after updating the custom field:

```bash
                             custom_fields                              
------------------------------------------------------------------------
 {"irs_ein": 823385206.0, "irs_ntee_code": null, "school_grade": null}
 {"irs_ein": 351097611.0, "irs_ntee_code": null, "school_grade": null}
 {"irs_ein": 842048006.0, "irs_ntee_code": null, "tax_code": 54YTHF7} # Updated
 {"irs_ein": 870578791.0, "irs_ntee_code": "N63", "school_grade": null}
 {"irs_ein": 863214157.0, "irs_ntee_code": null, "school_grade": null}
 {"irs_ein": 820501975.0, "irs_ntee_code": null, "college_level": null} # Updated

```

## Upload new contacts to an existing organization

View of agents before uploading the contacts:

```bash
 id | rank |         created_at         | contact_id | organization_id 
----+------+----------------------------+------------+-----------------
  1 |    1 | 2024-06-28 14:11:52.304378 |          1 |               1
  2 |    1 | 2024-06-28 14:11:52.32616  |          2 |               2
  3 |    1 | 2024-06-28 14:11:52.342452 |          3 |               3
  4 |    1 | 2024-06-28 14:11:52.355635 |          4 |               4
  5 |    1 | 2024-06-28 14:11:52.36891  |          5 |               5
  6 |    1 | 2024-06-28 14:11:52.384416 |          6 |               6

```
View of agents after uploading the contacts:

NOTE: Changes in agent rank will be auto triggered using PL/SQL triggers.

```bash
 id | rank |         created_at         | contact_id | organization_id 
----+------+----------------------------+------------+-----------------
  1 |    1 | 2024-06-28 14:11:52.304378 |          1 |               1
  7 |    2 | 2024-06-28 20:32:45.15342  |          7 |               1 # New contact
  8 |    3 | 2024-06-28 20:33:15.22641  |          8 |               1 # New contact
  2 |    1 | 2024-06-28 14:11:52.32616  |          2 |               2
  3 |    1 | 2024-06-28 14:11:52.342452 |          3 |               3
  4 |    1 | 2024-06-28 14:11:52.355635 |          4 |               4
  5 |    1 | 2024-06-28 14:11:52.36891  |          5 |               5
  6 |    1 | 2024-06-28 14:11:52.384416 |          6 |               6
```