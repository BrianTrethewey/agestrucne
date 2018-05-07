
library(ggplot2)
library(reshape2)
library(RColorBrewer)

args = commandArgs(trailingOnly = TRUE)

full_frame = data.frame()

title = "Wood Frog"
subtit  = " 100 Nb 0% Decline"
print(subtit)
file_name = 'wFrog_100_400_0D_100I'

for(file in args){
	temp_frame = read.table(file, sep = '\t',header = TRUE)
	names(temp_frame) <- gsub("\\.","_",names(temp_frame))
	full_frame <- rbind(full_frame,temp_frame)
}
full_frame$pop <- factor(full_frame$pop)

full_frame$sample_value <- factor(full_frame$sample_value)
print(head(full_frame))
g <- ggplot(full_frame, aes(pop,ne_est_adj, fill = sample_value ))+scale_fill_brewer(palette = "Dark2")
g <- g+ labs(x = "Breeding Cycle", y = "Nb")+ggtitle(bquote(atop(.(title), atop(italic(.(subtit)),""))))+theme(legend.position = "none")
ggraph<- g+geom_boxplot()
print(ggraph)
ggsave(paste("nb_",file_name,".png"),device = "png",width = 4, height = 4)
