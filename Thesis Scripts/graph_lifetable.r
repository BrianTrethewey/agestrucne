library(ggplot2)
library(reshape2)
library(RColorBrewer)
args = commandArgs(trailingOnly = TRUE)

full_frame = data.frame()

title = "Wood Frog                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            "
subtit  = "100 Nb 5% Decline"
print(subtit)
file_name = 'wFrog_100_5D'

#palette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

#read all files into one frame
for(file in args){
	temp_frame = read.table(file, sep = '\t',header = TRUE)
	names(temp_frame) <- gsub("\\.","_",names(temp_frame))
	full_frame <- temp_frame
	full_frame <- melt(full_frame, id = "generation")
	print (head(full_frame,10))
	g <- ggplot(full_frame,aes(generation,value))+labs(x = "Breeding Cycle" , y =  "Individuals(Nc)", colour = "Age Class")+ggtitle(bquote(atop(.(title), atop(italic(.(subtit)),""))))
	ggraph <- g+geom_bar(stat = "identity",aes(fill = variable)) +scale_fill_brewer(palette = "Set3")
	print(ggraph)
	ggsave(paste("lifetable_",file_name,".png"),device = "png",width = 4, height = 3)
	}