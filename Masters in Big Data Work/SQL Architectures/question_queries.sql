-- 1. Which are the top 3 relevant elements of the Solar System?

SELECT Q.ELEMENT_NAME, 
SUM(Q.ELEMENT_MASS_IN_BODY) AS PRESENCE_IN_EM, -- In Earth Masses (Astronomical standard unit)
SUM(Q.ELEMENT_MASS_IN_BODY * 5.972E24) AS PRESENCE_IN_KG -- Converted to Kg
FROM (
SELECT A.NAME AS BODY_NAME, A.MASS_EM AS BODY_MASS_EM, 
C.NAME AS ELEMENT_NAME, B.PERCENTAGE AS ELEMENT_RATIO, 
(B.PERCENTAGE * A.MASS_EM) AS ELEMENT_MASS_IN_BODY -- Multiply percentage by planet with mass
FROM bodies AS A
INNER JOIN composition AS B
ON A.BODY_ID = B.BODY_ID
INNER JOIN elements AS C
ON B.ATOMIC_NUMBER = C.ATOMIC_NUMBER) AS Q
GROUP BY Q.ELEMENT_NAME
ORDER BY PRESENCE_IN_KG DESC
LIMIT 3;

-- 2. At a maximum constant speed of 40.000 km/h, show how much time it
-- would take for the Apollo 10 mission, to make a round trip from the
-- earth to each of the other planets (the table has distance from sun).

SELECT A.NAME, 
-- Because 1 AU is the distance from Earth to the Sun, 
-- if we subtract 1 from the other planet's distances to the Sun we get their distance to Earth.
-- DISTANCE_PARENT_AU refers to the distance between body and the object it orbits, so all planets have the distance to the Sun
ABS(B.DISTANCE_PARENT_AU - 1) AS DISTANCE_TO_EARTH_AU, -- In Astronomical Units (Astronomical standard distance)
ABS(B.DISTANCE_PARENT_AU - 1)*1.496E8 AS DISTANCE_TO_EARTH_KM, -- In Kilometers
(((ABS(B.DISTANCE_PARENT_AU - 1)*1.496E8)/40000)*2)/24 AS ROUND_TRIP_DAYS -- Expression to convert AU to Days for roundtrip at 40000km/h
FROM bodies AS A
INNER JOIN body_relation AS B
ON A.BODY_ID = B.BODY_ID
-- For easy access for understanding, we join here with body_types to allow to lookup with string and not body type id.
INNER JOIN body_types AS C
ON A.BODY_TYPE_ID = C.BODY_TYPE_ID
WHERE C.NAME = 'Planet'
AND A.NAME <> 'Earth'; 

-- 3. Calculate solar system's total mass not including the black matter.

SELECT SUM(MASS_EM) AS TOTAL_MASS_EM, -- In Earth Masses (Astronomical standard unit)
SUM(MASS_EM)*5.972E24 AS TOTAL_MASS_KG -- Converted to Kg
FROM bodies;

-- 4. Which planet has the minimum number of rotation days per revolution.

-- If by revolution we mean 'rotation on axis':
SELECT A.NAME, MIN(A.ROTATION_DAYS) AS MIN_ROTATION_DAYS
FROM bodies AS A
-- For easy access for understanding, we join here with body_types to allow to lookup with string and not body type id.
INNER JOIN body_types AS B
ON A.body_type_id = B.body_type_id
WHERE B.NAME = 'Planet';

-- If by revolution we mean 'revolving around the sun':
SELECT A.NAME, MIN(B.ORBIT_YR*365/A.ROTATION_DAYS) AS MIN_ROTATION_DAYS
FROM bodies AS A
INNER JOIN body_relation AS B
ON A.BODY_ID = B.BODY_ID
-- For easy access for understanding, we join here with body_types to allow to lookup with string and not body type id.
INNER JOIN body_types AS C
ON A.body_type_id = C.body_type_id
WHERE C.NAME = 'Planet';


-- 5. What are the 5 bodies with the most other bodies orbiting them?

SELECT A.NAME, B.ORBITING_BODIES
FROM bodies AS A
INNER JOIN (
-- Counting instances of 'child' bodies orbiting 'parent' bodies from their relationship table
SELECT PARENT_ID, COUNT(BODY_ID) AS ORBITING_BODIES 
FROM body_relation
GROUP BY PARENT_ID) AS B
ON A.BODY_ID = B.PARENT_ID
ORDER BY ORBITING_BODIES DESC
LIMIT 5;