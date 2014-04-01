install.packages('ggmap')
library (ggmap)
library (plyr)

happyData <- read.csv(file.choose(), header=T)
View(happyData)
View(usa)
usa<-map_data('state')
mappy <- merge(happyData, usa, by= 'region')
mappy <- arrange(mappy,order)
mappy$senti <- as.factor(ceiling(mappy$Sentiment * 100))
View(mappy)
states <- data.frame(state.center, state.abb)

s <- ggplot(data = mappy, aes(x=long, y=lat, group = group)) +
  geom_polygon(aes(fill = senti))+
  geom_path(color = 'grey', linestyle = 2)+
  scale_fill_brewer("sentiment", palette = 'PuRd')

s




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

data(usa.)
