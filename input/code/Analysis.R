library(stargazer)
library(tidyr)
library(dplyr)
library(stringr)
# library(pml)
library(lfe)
library(ggplot2)
library(here)
#library(plotly)


setwd(here())

#-- Read Data --#

data_tourism <- read.csv("input/raw_data/API_ST.INT.ARVL_DS2_en_csv_v2_10139871.csv",skip =4)
data_ranking <- read.csv("input/raw_data/restaurant_ranking.csv")


#-- Create output folder --- #
if (!dir.exists("./output")) {
  dir.create("./output")
}
if (!dir.exists("./output/graphs")) {
  dir.create("./output/graphs")
}

if (!dir.exists("./output/data")) {
  dir.create("./output/data")
}




df_tourismlong <- data_tourism
df_tourismlong[3:39]<-list(NULL)  

df_tourismlong <- df_tourismlong %>%
  gather(year,arrivals,X1995:X2017)

df_tourismlong[3]<-NULL

df_tourismlong$year<-str_replace(df_tourismlong$year,"X","")
df_tourismlong$year<-as.numeric(df_tourismlong$year)

colnames(df_tourismlong)[colnames(df_tourismlong)=="Country.Name"] <- "country"


df_tot <- full_join(data_ranking,df_tourismlong, by = c("country", "year"))



new_data <-  df_tot %>% group_by(country, year) %>%mutate(numeric_restaurant= as.numeric(restaurant))
new_data <- new_data%>% mutate_if(is.numeric, replace_na, 0)
new_data <- new_data%>% mutate(g = ifelse(numeric_restaurant > 0, 1, 0 ))
new_data <- new_data%>% group_by(country) %>% mutate(tot_restaurant = sum(g))
new_data <- new_data%>% filter(tot_restaurant > 0, year < 2017, year > 2002)

final_data <- new_data %>% group_by(country, year,arrivals) %>% summarize(num_restaurant = sum(g))

sum_data <- new_data %>% group_by(country, year) %>% mutate(num_restaurant= sum(g))
sum_data <- sum_data %>% group_by(country) %>% summarize(mean_rest = mean(num_restaurant), mean_arr = mean(arrivals))



my_lm <- lm(arrivals ~ num_restaurant + factor(country) +factor(year) ,   data = final_data)

stargazer(my_lm, type = "latex", summary=FALSE, align=TRUE, 
          title="Correlation international tourist arrivals and number of restaurant", out="output/data/corr.tex",
          omit= c("factor\\(year","factor\\(country"),
          omit.labels = c("Year FE","Country FE"))

# Scatterplot of mean arrivals and number of restaurant across country
png(filename=paste("output/graphs/graph_1.png"), res=100, width = 1400, height = 600)
ggplot(sum_data, aes(x = mean_rest, y = mean_arr)) + geom_jitter() + geom_smooth(model = lm)
dev.off()



# Scatterplot of  arrivals and number of restaurant  for all years 
for (i in 2003:2016) {
  filter_i <- final_data %>% filter (year == i)
  png(filename=paste("output/graphs/graph_year",i,".png"), res=100, width = 1400, height = 600)
  ggplot(filter_i, aes(x = num_restaurant, y = arrivals)) + geom_jitter() + geom_smooth(model = lm)
  dev.off()
}


png(filename=paste("output/graphs/graph_2.png"), res=100, width = 1400, height = 600)
ggplot(final_data, aes(x = num_restaurant, y = arrivals)) + geom_jitter() + facet_wrap(~ year)
dev.off()


#sp <- ggplot(sum_data, aes(mean_rest, mean_arr)) + 
#jpeg(paste('../output/graphs/scatterplot', '.jpeg', sep=""), width = 1000, height = 1000, units = "px", pointsize = 12,
#     quality = 75)
#grid.arrange(direct, strategy ,nrow=2,
#             top = textGrob('Effect of Initial Expectations', vjust = 1, gp = gpar(fontface = "bold", cex = 1.5)),
#             bottom = textGrob( "Blue = accept, Black = reject.", gp = gpar(fontface = 3, fontsize = 12),  hjust = 1,  x = 1))
#dev.off()


#sp <- ggplot(new_data, aes(num_restaurant, arrivals)) + geom_jitter() + geom_smooth(model = lm)
#sp + facet_grid(year ~ .)

#jpeg(paste('../output/graphs/scatterplots', '.jpeg', sep=""), width = 1000, height = 1000, units = "px", pointsize = 12,
#     quality = 75)
#grid.arrange(direct, strategy ,nrow=2,
#             top = textGrob('Effect of Initial Expectations', vjust = 1, gp = gpar(fontface = "bold", cex = 1.5)),
#             bottom = textGrob( "Blue = accept, Black = reject.", gp = gpar(fontface = 3, fontsize = 12),  hjust = 1,  x = 1))
#dev.off()



