CREATE TABLE Products (
    ProductId STRING(36)  NOT NULL,
    Name      STRING(256) NOT NULL,
    Price     FLOAT64     NOT NULL
) PRIMARY KEY (ProductId);

CREATE TABLE Customers (
    CustomerId STRING(36)  NOT NULL,
    FirstName  STRING(256) NOT NULL,
    LastName   STRING(256) NOT NULL
) PRIMARY KEY (CustomerId);

CREATE TABLE Orders (
    OrderId    STRING(36) NOT NULL,
    ProductId  STRING(36) NOT NULL,
    CustomerId STRING(36) NOT NULL,
    Quantity   INT64      NOT NULL,
    FOREIGN KEY (CustomerId) REFERENCES Customers (CustomerId),
    FOREIGN KEY (ProductId)  REFERENCES Products  (ProductId)
) PRIMARY KEY (OrderId);

-- 外部キー制約で参照しているテーブルを取得するクエリ
SELECT
  tc.TABLE_NAME AS TableName,
  ARRAY_AGG(ccu.TABLE_NAME) AS foreign_tables
FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS ccu USING (CONSTRAINT_NAME)
WHERE CONSTRAINT_TYPE = "FOREIGN KEY"
GROUP BY tc.TABLE_NAME


-- Interleave
CREATE TABLE Singers (
  SingerId   INT64 NOT NULL,
  SingerName  STRING(1024)
) PRIMARY KEY (SingerId);

CREATE TABLE Albums (
 SingerId     INT64 NOT NULL,
 AlbumId      INT64 NOT NULL,
 AlbumTitle   STRING(MAX),
 ) PRIMARY KEY (SingerId, AlbumId),
INTERLEAVE IN PARENT Singers ON DELETE CASCADE;

CREATE TABLE Singers2 (
  SingerId   INT64 NOT NULL,
  SingerName  STRING(1024)
) PRIMARY KEY (SingerId);

CREATE TABLE Albums2 (
 SingerId     INT64 NOT NULL,
 AlbumId      INT64 NOT NULL,
 AlbumTitle   STRING(MAX),
 ) PRIMARY KEY (SingerId, AlbumId),
INTERLEAVE IN PARENT Singers2 ON DELETE NO ACTION;

-- 循環参照
CREATE TABLE Table1 (
  Table1Id INT64 NOT NULL,
  Table2Id INT64
) PRIMARY KEY (Table1Id);

CREATE TABLE Table2 (
  Table2Id INT64 NOT NULL,
  Table1Id INT64,
  FOREIGN KEY (Table1Id) REFERENCES Table1 (Table1Id)
) PRIMARY KEY (Table2Id);

ALTER TABLE Table1 ADD FOREIGN KEY (Table2Id) REFERENCES Table2 (Table2Id);

-- トポロジカルソートができるクエリ
WITH References AS (
  SELECT
    tc.TABLE_NAME AS TableName
    , ccu.TABLE_NAME AS ReferenceTo
  FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
  INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS ccu USING (CONSTRAINT_NAME)
  WHERE
    CONSTRAINT_TYPE = "FOREIGN KEY"
    AND tc.TABLE_NAME <> ccu.TABLE_NAME
)

SELECT
  t.TABLE_NAME AS TableName
  , children.TABLE_NAME AS ChildTableName
  , children.ON_DELETE_ACTION AS DeleteAction
  , r.ReferenceTo AS ReferenceTo
FROM INFORMATION_SCHEMA.TABLES AS t
LEFT JOIN INFORMATION_SCHEMA.TABLES AS children ON t.TABLE_NAME = children.PARENT_TABLE_NAME
LEFT JOIN References AS r ON t.TABLE_NAME = r.TableName
WHERE t.TABLE_TYPE = "BASE TABLE";

-- 循環参照はあきらめる。無理。
-- Ruby にトポロジカルソートする標準ライブラリtsortがある
-- 自己参照はDELETE <table> WHERE TRUE で問題ない
-- DeleteAction は一旦無視して、すべて削除する
