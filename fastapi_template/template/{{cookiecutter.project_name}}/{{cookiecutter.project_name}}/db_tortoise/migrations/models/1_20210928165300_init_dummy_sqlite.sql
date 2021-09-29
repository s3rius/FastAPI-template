-- upgrade --
CREATE TABLE IF NOT EXISTS "dummymodel" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(200) NOT NULL
) /* Model for demo purpose. */;
-- downgrade --
DROP TABLE "dummymodel";
