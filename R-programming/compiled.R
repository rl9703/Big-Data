data('iris')

iris.new<- iris[,c(1,2,3,4)]

normalize <- function(x){
  return ((x-min(x))/(max(x)-min(x)))
}

iris.new$Sepal.Length<- normalize(iris.new$Sepal.Length)
iris.new$Sepal.Width<- normalize(iris.new$Sepal.Width)
iris.new$Petal.Length<- normalize(iris.new$Petal.Length)
iris.new$Petal.Width<- normalize(iris.new$Petal.Width)

result<- kmeans(iris.new,3)

iris.class<- iris[,"Species"]

par(mfrow=c(2,2), mar=c(5,4,2,2))
plot(iris.new[c(1,2)], col=result$cluster)# Plot to see how Sepal.Length and Sepal.Width data points have been distributed in clusters
plot(iris.new[c(1,2)], col=iris.class)# Plot to see how Sepal.Length and Sepal.Width data points have been distributed originally as per "class" attribute in dataset
plot(iris.new[c(3,4)], col=result$cluster)# Plot to see how Petal.Length and Petal.Width data points have been distributed in clusters
plot(iris.new[c(3,4)], col=iris.class)

table(result$cluster,iris.class)

sse = rep(0,15)

for (each in 1:15){
  kmeans.model_new = kmeans(iris.new, each,nstart = 50)
  sse[each] = kmeans.model_new$tot.withinss
}


plot(1:15, sse, type="b",
     xlab = "Number of Clusters",
     ylab = "Internal cluster sum of squares")

bss = rep(0,15)

for (each in 1:15){
  kmeans.model_new2 = kmeans(iris.new, each, nstart = 50)
  bss[each] = kmeans.model_new2$betweenss
}

plot(1:15, bss, type="b",
     xlab = "Number of Clusters",
     ylab = "Between cluster sum of squares")