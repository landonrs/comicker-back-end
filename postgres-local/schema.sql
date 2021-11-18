-- schema.sql
-- Since we might run the import many times we'll drop if exists
DROP DATABASE IF EXISTS comicker;

CREATE DATABASE comicker;

-- Make sure we're using our `comicker` database
\c comicker;

-- We can create our comic table
CREATE TABLE IF NOT EXISTS comic (
  "comicId" VARCHAR PRIMARY KEY,
  title VARCHAR,
  panels jsonb,
  "createDate" TIMESTAMPTZ not null,
  "lastUpdated" TIMESTAMPTZ not null DEFAULT CURRENT_TIMESTAMP
);