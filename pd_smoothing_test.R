##
## Import required scripts
##
#source('I:/CRMPO/DEPT/Hachuel/SRAPI/Helper Scripts/PD_smoothing_helpers.R')

##
## Import raw data
##
data <- read.table(file = "commercial_pd_4q14.tsv",sep = '\t', header = TRUE)



# Test CRE Full
cre_full <- subset(x = data, subset = (data$segment == 'CRE' & data$lookback == 'full'))
results <- smooth_PD(defaults = cre_full$defaults, 
                     total = cre_full$total,
                     model_smooth_PD = cre_full$model_smooth_PD)

plot_results(results = results, 
             model_smooth_PD = cre_full$model_smooth_PD, 
             title = paste("PD Smooth Test for 4Q14", 'CRE', 'Full lookback', sep = ' '))
results$model_smooth_PD <- cre_full$model_smooth_PD
results <- subset(results, select = c(ORR,raw_PD, model_smooth_PD, smooth_PD))
results$error <- paste(round(100*(abs(results$smooth_PD-results$model_smooth_PD)/results$model_smooth_PD), digits = 5),"%", sep='')
names(results) <- c("ORR","Raw PD","Model Smooth PD","Algorithm Smooth PD", "Error")
print(results)


