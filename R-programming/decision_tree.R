install.packages("rpart")
install.packages("rpart.plot")
library("rpart")
library("rpart.plot")

ba <- read_delim("Desktop/ba.csv", ";")

indexes = sample(50, 150)
ba_train = ba[indexes,]
ba_test = ba[-indexes,]

target = price_range ~ business_accepts_bitcoin + street_parking + parking_lot + valet_parking

tree = rpart(target, data = ba_train, method = "class")
rpart.plot(tree)