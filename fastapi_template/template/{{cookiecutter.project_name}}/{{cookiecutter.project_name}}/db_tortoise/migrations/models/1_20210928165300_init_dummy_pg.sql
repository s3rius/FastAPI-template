-- upgrade --
CREATE TABLE IF NOT EXISTS "dummymodel" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL
);
COMMENT ON TABLE "dummymodel" IS 'Model for demo purpose.';
-- downgrade --
DROP TABLE "dummymodel";
