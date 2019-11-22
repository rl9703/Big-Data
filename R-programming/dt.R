library("rpart")
ba <- read_delim("Desktop/ba.csv", ";")
cols <- c('business_accepts_bitcoin', 'street_parking','bike_parking','garage_parking','dogs_allowed','wheelchair_access','business_accepts_creaditcard','parking_lot', 'valet_parking')
ba[cols] <- lapply(ba[cols], as.factor)

set.seed(1)
train <- sample(1:nrow(ba), 0.75 * nrow(ba))
target = price_range ~ business_accepts_bitcoin + street_parking + bike_parking + garage_parking + dogs_allowed + wheelchair_access + business_accepts_creaditcard + parking_lot + valet_parking
baTree <- rpart(target, data = ba[train, ], method = 'class')
plot(baTree)
text(baTree,pretty=0)
baPred <- predict(baTree, ba[-train, ], type = 'class')
x=table(baPred, ba[-train, ]$price_range)
x=sum(diag(x))*100/sum(x)
x
