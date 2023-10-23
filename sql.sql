--Creating a Table:
CREATE TABLE table_name (
    column1 datatype1 constraint,
    column2 datatype2 constraint,
    ...
);

--Inserting Data into a Table:
INSERT INTO table_name (column1, column2, ...)
VALUES (value1, value2, ...);

-- Selecting Data from a Table:
SELECT column1, column2, ...
FROM table_name
WHERE condition;

--Updating Data in a Table:
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;

--Deleting Data from a Table:
DELETE FROM table_name
WHERE condition;

-- Filtering Data:
SELECT column1, column2, ...
FROM table_name
WHERE condition
ORDER BY column1 ASC/DESC;

-- Joining Tables:
SELECT column1, column2, ...
FROM table1
JOIN table2 ON table1.column_name = table2.column_name;

-- Grouping and Aggregating Data:
SELECT column1, COUNT(column2)
FROM table_name
GROUP BY column1;

-- Adding Constraints:
ALTER TABLE table_name
ADD CONSTRAINT constraint_name constraint_details;

-- Indexing Columns:
CREATE INDEX index_name
ON table_name (column_name);

-- Granting Permissions:
GRANT privilege_type1, privilege_type2, ...
ON object_type object_name
TO user_or_role;

-- Revoking Permissions:
REVOKE privilege_type1, privilege_type2, ...
ON object_type object_name
FROM user_or_role;

