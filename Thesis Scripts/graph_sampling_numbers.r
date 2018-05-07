library(ggplot2)
library(RColorBrewer)
args = commandArgs(trailingOnly = TRUE)

full_frame = data.frame()

title = "Wood Frog"
subtit  = "25 Nb 15% Decline"
print(subtit)
file_name = 'wFrog_25_15D'

palette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

#read all files into one frame
for(file in args){
	temp_frame = read.table(file, sep = '\t',header = TRUE)
	names(temp_frame) <- gsub("\\.","_",names(temp_frame))
	full_frame <- rbind(full_frame,temp_frame)
	print (head(full_frame,10))
}
full_frame$sample_value <- factor(full_frame$sample_value)
g <- ggplot(full_frame,aes(x = pop, y = indiv_count)) +labs(y="Individuals Sampled", x = "Breeding Cycle Monitored", colour = "Sampling Paradigm") 
g <- g+scale_x_discrete(limits = c(2,4,6,8,10))+ggtitle(bquote(atop(.(title), atop(italic(.(subtit)),""))))+scale_color_brewer(palette = "Dark2")
g_line <- g+ geom_line(aes(group = interaction(original_file, sample_value), color = sample_value)) 

ggsave(paste("sampling_",file_name,".png"),device = "png",width = 4, height = 4)
