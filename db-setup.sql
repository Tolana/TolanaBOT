BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "narrator" (
	"name"	TEXT NOT NULL,
	"narrator-url"	TEXT NOT NULL,
	PRIMARY KEY("narrator-url")
);
CREATE TABLE IF NOT EXISTS "author" (
	"name"	TEXT NOT NULL,
	"author-url"	TEXT NOT NULL,
	PRIMARY KEY("author-url")
);
CREATE TABLE IF NOT EXISTS "authors" (
	"author-url"	TEXT,
	"book_id"	INTEGER,
	FOREIGN KEY("book_id") REFERENCES "book"("id"),
	FOREIGN KEY("author-url") REFERENCES "author"("author-url")
);
CREATE TABLE IF NOT EXISTS "narrators" (
	"narrator-url"	TEXT,
	"book_id"	INTEGER,
	FOREIGN KEY("narrator-url") REFERENCES "narrator"("narrator-url"),
	FOREIGN KEY("book_id") REFERENCES "book"("id")
);
CREATE TABLE IF NOT EXISTS "url" (
	"url"	TEXT,
	PRIMARY KEY("url")
);
CREATE TABLE IF NOT EXISTS "seriesAuthors" (
	"author-url"	TEXT,
	"series_id"	INTEGER
);
CREATE TABLE IF NOT EXISTS "series" (
	"title"	TEXT,
	"series-url"	TEXT,
	"id"	INTEGER,
	PRIMARY KEY("id"),
	UNIQUE("series-url")
);
CREATE TABLE IF NOT EXISTS "book" (
	"title"	TEXT NOT NULL,
	"series-url"	TEXT NOT NULL,
	"length"	INTEGER NOT NULL,
	"releaseDate"	TEXT NOT NULL,
	"id"	INTEGER,
	FOREIGN KEY("series-url") REFERENCES "series"("series-url"),
	PRIMARY KEY("id"),
	UNIQUE("title","series-url","length","releaseDate")
);
COMMIT;
