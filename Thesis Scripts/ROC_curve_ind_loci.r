
library(ggplot2)
library(RColorBrewer)

count_positives <- function(x, input_frame){
		print(x) 
		#for 2 sided test
  	 	deciding_factor =  x/2
	 	print(deciding_factor)
	 	count_pos = 0
	 	count_pos =count_pos + sum(input_frame$P_Value_1 <deciding_factor)
	 	count_pos = count_pos + sum(input_frame$P_Value_1 >(1 - deciding_factor))
	 	count_pos = count_pos/1000.0
	 	print(count_pos)
	 	return (count_pos)
}


#get the decision matrix for all decision values
build_deciding_frame <- function(df, granularity){
	 Deciding_Factor = seq(0.0,1.0, by= granularity)
	 #print(Deciding_Factor)
	 num_rows = length(Deciding_Factor)
	 deciding_frame = data.frame(Species = character(),Nb = character(),Loci_Count = character(),Individual_Count = character(), Cycles = character(), Decline = character(), Deciding_Factor = double(), Positive_Results = integer())
	 
	 Species= df[1,'Species']
	 #print(Species)
	 Nb= df[1,'Nb']
	 Loci_Count= df[1,'Loci_Count']
	 Individual_Count =  df[1,'Individual_Count']
	 Decline = df[1,'Decline']
	 Cycles =  df[1,'Cycles']

	 Positive_Results  = 0
	 for (i in Deciding_Factor){
		Positive_Results  = 0
	 	Positive_Results =  count_positives(i,df)
	 	new_frame = data.frame(Species = Species,Nb = Nb,Loci_Count = Loci_Count,Individual_Count = Individual_Count, Cycles = Cycles, Decline = Decline, Deciding_Factor = i, Positive_Results = Positive_Results)
	 	deciding_frame = rbind(deciding_frame,new_frame)
	 }
	 print(head(deciding_frame))
	 return(deciding_frame)
}

GRANULARITY = 0.01
args = commandArgs(trailingOnly = TRUE)
full_frame = data.frame(Species = character(),Nb = character(),Loci_Count = character(),Individual_Count = character(), Cycles = character(), Decline = character(), Deciding_Factor = double(), Positive_Results = integer())
print(head(full_frame))	
	for(file in args){
		temp_frame = read.csv(file)
		names(temp_frame) <- gsub("\\.","_",names(temp_frame))
		print (names(temp_frame))
		print(head(temp_frame))
		result_frame  = build_deciding_frame(temp_frame, GRANULARITY)
		full_frame = rbind(full_frame, result_frame)
	}
print(head(full_frame))
specificty_frame = full_frame[full_frame$Decline == 0,]
sensitivity_frame = full_frame[full_frame$Decline !=0,]
print (specificty_frame)

unique_list = rapply(specificty_frame, function(x) length(unique(x)))

print(unique_list)
axis_list = list()
print(head(full_frame))

specificty_merge<- data.frame(specificty_frame)
full_frame$Cycles <-factor(full_frame$Cycles)
full_frame$Nb <-factor(full_frame$Nb)
full_frame$Loci_Count <-factor(full_frame$Loci_Count)
full_frame$Individual_Count <-factor(full_frame$Individual_Count)
full_frame$Decline <-factor(full_frame$Decline)
for (decline_val in unique(full_frame$Decline)){
	decline_frame =  full_frame[full_frame$Decline == decline_val,]
	print(head(decline_frame))
		specificity <- ggplot(decline_frame,aes(x = Deciding_Factor, y=Positive_Results,group = interaction(Individual_Count,Loci_Count)))
		spec_graph <- specificity+geom_line(aes(color = Loci_Count, linetype = Individual_Count))+ theme(axis.text.x = element_text(angle=45))
		spec_graph <- spec_graph+labs(x = "P-Value", y = "Sensitivity",colour = "SNPs", linetype = "Individuals")
		if(decline_val==0){ spec_graph<-spec_graph+ylab("(1-Specificity)")}
		spec_graph<- spec_graph+ggtitle(paste("Bull Trout Specificity Curve 50Nb 7 Breeding Cycles"))+scale_color_brewer(palette = "Dark2")
		spec_graph <- spec_graph+scale_x_continuous(breaks = seq(0.0, 1.0, 0.1))+scale_y_continuous(breaks = seq(0.0, 1.0, 0.1))
		print(spec_graph)
		ggsave(paste("specificity_ROC_ind_loci",decline_val,".png",sep ="_"),device = "png",width = 6, height = 3)

}
specificty_merge<- data.frame(specificty_frame)
specificty_merge$Decline[specificty_merge$Decline==0] =5
temp_merge <- data.frame(specificty_merge)
temp_merge$Decline[temp_merge$Decline==5] =7
specificty_merge <- rbind(specificty_merge,temp_merge)

temp_merge$Decline[temp_merge$Decline==7] =10
specificty_merge <- rbind(specificty_merge,temp_merge)
temp_merge$Decline[temp_merge$Decline==10] =15
specificty_merge <- rbind(specificty_merge,temp_merge)

names(specificty_merge)[names(specificty_merge) == "Positive_Results"] <- 'False_Positives'
sensitivity_frame <- merge(sensitivity_frame, specificty_merge)
print(head(sensitivity_frame))
sensitivity_frame$Cycles <-factor(sensitivity_frame$Cycles)
sensitivity_frame$Nb <-factor(sensitivity_frame$Nb)
sensitivity_frame$Loci_Count <-factor(sensitivity_frame$Loci_Count)
sensitivity_frame$Individual_Count <-factor(sensitivity_frame$Individual_Count)
sensitivity_frame$Decline <-factor(sensitivity_frame$Decline)
for (decline_val in unique(sensitivity_frame$Decline)){
	decline_frame =  sensitivity_frame[sensitivity_frame$Decline == decline_val,]

		sensitivity<-ggplot(decline_frame,aes(x=False_Positives, y = Positive_Results, group = interaction(Individual_Count,Loci_Count)))
		sense_graph = sensitivity+geom_line(aes(color = Loci_Count, linetype = Individual_Count))+ theme(axis.text.x = element_text(angle=45))+scale_color_brewer(palette = "Dark2")
		sense_graph <- sense_graph+labs(x = "(1-Specificity)", y = "Sensitivity",colour = "SNPs", linetype = "Individuals")	
		sense_graph <- sense_graph+ggtitle("Bull Trout ROC curve  50Nb 7 Breeding Cycles")+scale_x_continuous(breaks = seq(0.0, 1.0, 0.1))+scale_y_continuous(breaks = seq(0.0, 1.0, 0.1))
		print(sense_graph)
		ggsave(paste("sens_ROC_ind_loci",decline_val,".png",sep ="_"),device = "png",width = 6, height = 3)

	
}

