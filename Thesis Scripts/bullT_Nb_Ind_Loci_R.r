

library(ggplot2)
library("reshape2")
library(RColorBrewer)
 
#load data from file
data <- read.csv("bullT_restricted_sens_spec.csv")

#format column names
names(data) <- gsub("\\.","_",names(data))

#set pval to use
p_val = 0.1
p_val_title = (1-p_val)*100
data  <- data[data$P_Value == p_val,]

sen_data <- data[data$Decline != '0',]
spec_data <- data[data$Decline == '0',]
#add percent signs
sen_data <-sen_data[ with(sen_data, order(Decline)),]
sen_data$Decline[sen_data$Decline=="5"]<- "5%"
sen_data$Decline[sen_data$Decline=="7"]<- "7%"
sen_data$Decline[sen_data$Decline=="10"]<- "10%"
sen_data$Decline[sen_data$Decline=="15"]<- "15%"
sen_data$Decline <-factor(sen_data$Decline)
#rename colums
names(sen_data)[names(sen_data) == "Cycles"] <- "Cohorts"
names(sen_data)[names(sen_data) == "Nb"] <- "Nb_Start"
names(sen_data)[names(sen_data) == "Individual_Count"] <- "Individuals"
names(spec_data)[names(spec_data) == "Individual_Count"] <- "Individuals"
names(spec_data)[names(spec_data) == "Cycles"] <- "Cohorts"
names(spec_data)[names(spec_data) == "Nb"] <- "Nb_Start"

print(head(sen_data))
#create base graph
g<-ggplot(sen_data, aes(y= Power_Percent, x= factor(Loci_Count)))+facet_grid(Cohorts ~ Nb_Start + Individuals,labeller =label_both)
#set refernce line
g<-g+geom_hline(yintercept= 0.8, linetype = "dashed")
#set Title and labels	
g<- g+labs(x = "SNPs" , y = "Power", linetype = "Decline")
#set text size and color/point type
g<- g  + theme(text = element_text(size = 18),axis.text.x = element_text(size = 20),axis.text.y = element_text(size = 18)) +scale_color_brewer(palette = "Dark2")+scale_shape_discrete(solid=T) 
g<-g+scale_linetype_manual(breaks=c("5%","7%","10%","15%"), values = c(1,2,3,4))
#print line graph
g+geom_line(aes(y= Power_Percent, x= factor(Loci_Count),group = Decline, linetype =factor(Decline)))+geom_point(aes(shape=factor(Decline)),show.legend = FALSE)


ggsave("bullT_nb_ind_loci_sen.png",device = "png",width = 14, height = 6)
print("sensitivity done")
#invert data from specificty to Type 1 error
spec_data$Power_Percent = 1-spec_data$Power_Percent
print(head(spec_data))
g<-ggplot(spec_data, aes(y= Power_Percent, x= factor(Loci_Count)))+facet_grid(Cohorts ~ Nb_Start + Individuals,labeller =label_both)
#set Title and labels	
g<- g+labs(x = "SNPs" , y = "Type 1 Error", colour = "Declines") + expand_limits(y=c(0, 0.23))
g<- g  + theme(text = element_text(size = 20),axis.text.x = element_text(size = 22),axis.text.y = element_text(size = 18)) +scale_color_brewer(palette = "Dark2")+scale_shape_discrete(solid=T) +geom_hline(yintercept= 0.1, linetype = "dashed")
#print line graph
g+geom_line(aes(group = Decline, linetype =factor(Decline)))+geom_point(aes(linetype=factor(Decline))) +theme(legend.position = "none")
ggsave("bullT_nb_ind_loci_spec.png",device = "png",width = 14, height = 6)

