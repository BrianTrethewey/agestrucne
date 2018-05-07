library(ggplot2)

library(RColorBrewer)
round_dec_places= 3
num_subsample = 5
args = commandArgs(trailingOnly = TRUE)
for(file in args){
	temp_frame = read.table(file, sep = '\t',header = TRUE)
	names(temp_frame) <- gsub("\\.","_",names(temp_frame))
	print(head(temp_frame))
    sim_list= unique(temp_frame$original_file)
	
	#subsamples_count = length(sim_list)/num_subsample
	subsamples_count  = 10
	for (file_val  in 1:subsamples_count){
		sim_sample_list = sample(sim_list,num_subsample)
		sample_frame = temp_frame[0,]
		sample_frame_5 = temp_frame[0,]
		
		order_list = list()
		slope_10_list =list()
		slope_5_list =list()
			
		for (sim in sim_sample_list){
			sim_frame = temp_frame[temp_frame$original_file == sim,]
			sim_frame_5 = sim_frame[sim_frame$pop<=5,]
			print (sim_frame)
			sim_stats<- lm(ne_est_adj ~ pop, data = sim_frame)
			print (sim_stats$coef[[2]])
			sim_frame$indep_comparisons <- sim_stats$coef[[2]]
			
			sim_stats_5<-lm(ne_est_adj ~ pop, data = sim_frame_5)
			print (sim_stats_5$coef[[2]])
			sim_frame_5$indep_comparisons <- sim_stats_5$coef[[2]]

			order_list <-append(order_list,sim)
			slope_10_list <- append(slope_10_list,round(sim_stats$coef[[2]], round_dec_places) )
			slope_5_list <- append(slope_5_list ,round(sim_stats_5$coef[[2]], round_dec_places) )

			print (order_list)
			print(slope_10_list)
			print(slope_5_list)
			sample_frame <- rbind(sample_frame,sim_frame)
			sample_frame_5 <- rbind(sample_frame_5, sim_frame_5)
			sample_frame$indep_comparisons<- as.factor(sample_frame$indep_comparisons)
			sample_frame_5$indep_comparisons<- as.factor(sample_frame_5$indep_comparisons)

		}
		y_limits = range(sim_frame$ne_est_adj)
		print(y_limits)

		g<-ggplot(sample_frame,aes(pop,ne_est_adj, colour = original_file))
		g<- g+geom_point()+geom_smooth(method = "lm",se = FALSE)+ labs(x = "Cohort", y = "Nb Estimates", colour = "Slopes")+scale_x_continuous(breaks = c(1,2,3,4,5,6,7,8,9,10))+theme(legend.position = "bottom")
		g<- g+theme(axis.text.x = element_text(size = 14), axis.text.y = element_text(size = 14),legend.text = element_text(size = 8)) + scale_y_continuous(limits = y_limits)+ scale_color_discrete(breaks = order_list, labels = slope_10_list)
		g<- g + guides(col = guide_legend(nrow = 2))
		print(g) 
		print(file_val)
		ggsave(paste("scatter_10_",file_val,".png"),device = "png",width = 4, height = 4)
		f<-ggplot(sample_frame_5,aes(pop,ne_est_adj, colour = original_file))
		f<- f+geom_point()+geom_smooth(method = "lm",se = FALSE)+ labs(x = "Cohort", y = "Nb Estimates", colour = "Slopes")+scale_x_continuous(breaks = c(1,2,3,4,5))+theme(legend.position = "bottom")
		f<-f+theme(axis.text.x = element_text(size = 14), axis.text.y = element_text(size = 14))+ scale_y_continuous(limits = y_limits)+scale_color_discrete(breaks = order_list, labels = slope_5_list)
		f<-f+guides(col = guide_legend(nrow = 2))
		print(f) 
		print(file_val)
		ggsave(paste("scatter__5",file_val,".png"),device = "png",width = 4, height = 4)
}
}