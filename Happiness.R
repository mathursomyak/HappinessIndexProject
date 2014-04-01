install.packages('ggmap')
library (ggmap)

usa<-map_data('usa')
usa
sf<-data.frame(long=-122.26,lat=37.47)
p <- ggplot(legend=FALSE) +
  geom_polygon(data=usa, aes(x=long, y=lat,group=group)) +
  theme(panel.background = element_blank()) +
  theme(panel.grid.major = element_blank()) +
  theme(panel.grid.minor = element_blank()) +
  theme(axis.text.x = element_blank(),
        axis.text.y = element_blank(),
        axis.ticks = element_blank()) +
  xlab("") + ylab("")

p
