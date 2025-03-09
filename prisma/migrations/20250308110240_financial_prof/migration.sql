-- CreateTable
CREATE TABLE "FinancialProfile" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "Income" DOUBLE PRECISION NOT NULL,
    "Age" INTEGER NOT NULL,
    "Dependents" INTEGER NOT NULL,
    "Disposable_Income" DOUBLE PRECISION NOT NULL,
    "Desired_Savings" DOUBLE PRECISION NOT NULL,
    "Groceries" DOUBLE PRECISION NOT NULL,
    "Transport" DOUBLE PRECISION NOT NULL,
    "Eating_Out" DOUBLE PRECISION NOT NULL,
    "Entertainment" DOUBLE PRECISION NOT NULL,
    "Utilities" DOUBLE PRECISION NOT NULL,
    "Healthcare" DOUBLE PRECISION NOT NULL,
    "Education" DOUBLE PRECISION NOT NULL,
    "Miscellaneous" DOUBLE PRECISION NOT NULL,
    "Occupation" TEXT NOT NULL,
    "City_Tier" TEXT NOT NULL,

    CONSTRAINT "FinancialProfile_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "FinancialProfile_userId_key" ON "FinancialProfile"("userId");

-- AddForeignKey
ALTER TABLE "FinancialProfile" ADD CONSTRAINT "FinancialProfile_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
