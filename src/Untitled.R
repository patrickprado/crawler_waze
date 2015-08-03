jams <- read.csv("/Users/pprado/Desktop/8º Período/POC II/crawler_waze/src/lon_lat_070415.txt", sep=',', header = FALSE)
colnames(jams) <- c("lon", "lat")
head(jams)


library(rworldmap)
newmap <- getMap(resolution = "low")
plot(newmap, xlim = c(-48, 0), ylim = c(-22, 0), asp = 1)

points(jams$lon, jams$lat, col = "red", cex = .6)
