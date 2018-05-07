library(ggplot2)
library(reshape2)
library(RColorBrewer)
#load data
wFrog_data <- read.csv("wFrog_sensitivity_specificity.csv")
print(head(wFrog_data))
bullT_data <- read.csv("bullT_sensitivity_specificity.csv")
bullT_data <- bullT_data[bullT_data$Nb != 25,]
print(unique(bullT_data$Nb))
#combine data into one frame
full_data <- rbind(bullT_data, wFrog_data)
print(head(full_data))
names(full_data) <- gsub("\\.","_",names(full_data))
print(head(full_data))
specificty_data <- full_data[full_data$Decline == 0 ,]
specificty_data$P_Value <- factor(specificty_data$P_Value)

g <- ggplot(specificty_data,aes(x = P_Value, y = Power_Percent))+labs(x = 'P Value Cutoff', y = 'Specificity', title = 'Specificity By P-value Cutoff')
g_graph <- g+geom_boxplot(aes(fill = Species))+ scale_fill_hue(l=45)+scale_color_brewer(palette = "Dark2")
ggsave("Specificity_by_p_val.png",device = "png",width = 4, height = 4)


g <- ggplot(specificty_data,aes(x = Species, y = Power_Percent))+labs(x = 'P Value Cutoff', y = 'Specificity', title = 'Specificity By Species')
g_graph <- g+geom_boxplot(aes(fill = P_Value))+ scale_fill_hue(l=45)+scale_color_brewer(palette = "Dark2")
ggsave("Specificity_by_species.png",device = "png",width = 4, height = 4)