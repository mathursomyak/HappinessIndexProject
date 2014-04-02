#install.packages('ggmap')
library (ggmap)
library (plyr)
library (ggplot2)

happyData <- read.csv("C:/Users/skmathur/Documents/GitHub/HappinessIndexProject/StateCSVs/TwitterSentiment_AllState.csv", header=T)
names(happyData) <- c("StateAbbrv","Sentiment","Subjectivity","CountTweets","region" )
usa <- map_data('state')
mappy <- merge(happyData, usa, by= 'region')
mappy <- arrange(mappy,order)
mappy$senti <- as.factor(ceiling(mappy$Sentiment * 100))
#View(mappy)
states <- data.frame(state.center, state.abb)

s <- ggplot(data = mappy, aes(x=long, y=lat, group = group)) +
  geom_polygon(aes(fill = senti))+
  geom_path(color = 'grey', linestyle = 2)+
  scale_fill_brewer("sentiment", palette = 'PuRd')+
  geom_text(data = states, aes(x = x, y = y, label = state.abb, group = NULL), size = 2)+
  theme_bw()

s
