CREATE TABLE IF NOT EXISTS narrator (
	name	VARCHAR(244) NOT NULL,
	narrator_url	VARCHAR(244) NOT NULL,
	PRIMARY KEY(narrator_url)
);
CREATE TABLE IF NOT EXISTS author (
	name	VARCHAR(244) NOT NULL,
	author_url	VARCHAR(244) NOT NULL,
	PRIMARY KEY(author_url)
);
CREATE TABLE IF NOT EXISTS authors (
	author_url	VARCHAR(244),
	book_id	INTEGER(200),
	FOREIGN KEY(author_url) REFERENCES author(author_url),
	FOREIGN KEY(book_id) REFERENCES book(id)
);
CREATE TABLE IF NOT EXISTS narrators (
	narrator_url	VARCHAR(244),
	book_id	INTEGER(200),
	FOREIGN KEY(narrator_url) REFERENCES narrator(narrator_url),
	FOREIGN KEY(book_id) REFERENCES book(id)
);
CREATE TABLE IF NOT EXISTS url (
	url	VARCHAR(244),
	PRIMARY KEY(url)
);
CREATE TABLE IF NOT EXISTS seriesAuthors (
	author_url	VARCHAR(244),
	series_id	INTEGER(200)
);
CREATE TABLE IF NOT EXISTS series (
	title	VARCHAR(244),
	series_url	VARCHAR(244),
	id	INTEGER(200),
	UNIQUE(series_url),
	PRIMARY KEY(id)
);
CREATE TABLE IF NOT EXISTS book (
	title	VARCHAR(244) NOT NULL,
	series_url	VARCHAR(244) NOT NULL,
	length	INTEGER(200) NOT NULL,
	releaseDate	VARCHAR(244) NOT NULL,
	id	INTEGER(200),
	FOREIGN KEY(series_url) REFERENCES series(series_url),
	UNIQUE(title,series_url,length,releaseDate),
	PRIMARY KEY(id)
);
CREATE TABLE IF NOT EXISTS seriesCount (
	series_url	VARCHAR(244),
	books	INTEGER(200),
	PRIMARY KEY(series_url)
);
CREATE TABLE IF NOT EXISTS bookQ (
	book_id	INTEGER(200),
	PRIMARY KEY(book_id)
);
