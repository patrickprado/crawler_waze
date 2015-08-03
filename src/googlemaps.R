# loading the required packages
require(ggplot2)
require(ggmap)

# creating a sample data.frame with your lat/lon points
jams <- read.csv("/Users/pprado/Desktop/8º Período/POC II/crawler_waze/src/lon_lat_afonso_pena_to_savassi.txt", sep=',', header = FALSE)
colnames(jams) <- c("lon", "lat")
head(jams)

# getting the map
mapgilbert <- get_map(location = c(lon = mean(jams$lon), lat = mean(jams$lat)), zoom = 14,
                      maptype = "terrain", scale = 2)

# plotting the map with some points on it
ggmap(mapgilbert) +
  geom_point(data = jams, aes(x = lon, y = lat, fill = "red", alpha = 0.8, title="Avenidas Bias Fortes e Contorno - 07/04/2015 - 17h"), size = 1, shape = 21) +
  guides(fill=FALSE, alpha=FALSE, size=FALSE)

