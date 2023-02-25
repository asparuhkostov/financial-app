-- CreateTable
CREATE TABLE "user" (
    "id" TEXT NOT NULL,
    "national_identification_number" TEXT NOT NULL,
    "country_of_residence" TEXT NOT NULL,
    "password" TEXT NOT NULL,

    CONSTRAINT "user_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "user_national_identification_number_key" ON "user"("national_identification_number");
