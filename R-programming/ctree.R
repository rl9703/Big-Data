install.packages("party")
library(party)
ba <- read_delim("Desktop/ba.csv", ";")
target = price_range>1 ~ business_accepts_bitcoin + street_parking + bike_parking + garage_parking + dogs_allowed + wheelchair_access + business_accepts_creaditcard + parking_lot + valet_parking
treePlot <- ctree(target,data=ba) 
plot(treePlot)