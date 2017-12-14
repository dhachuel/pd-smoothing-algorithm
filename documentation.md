****
# PD Smoothing Documentation
****

## Motivation
The goal of the PD smoothing algorithm is to minimize potential human error when smoothing PD distributions.

## Pseudo Code
```ruby
###################################################
# Function IS_MONOTONE()
#
# -------------------------------------------------
#
# This function returns TRUE if the given array
# values have an increasing monotonic relationship.
#
###################################################
FUNCTION is_monotone(array)
{  

  FOR i in 2:LENGTH(array)
    IF array[i] < array[i-1]
      RETURN FALSE
	
  RETURN TRUE
  
}


#########################################################
# Function PRE_PROCESS()
#
# -------------------------------------------------------
#
# This function converts 0 values to minimim PD (0.0003) 
# and returns a copy of input array.
#
#########################################################
FUNCTION pre_process(array)
{   

  FOR i in 2:LENGTH(array)
    IF array[i] == 0
      SET array[i] = 0.0003

	RETURN array
	
}



###########################################################################
# Function SMOOTH()
#
# -------------------------------------------------------------------------
#
# This function smoothes an array of PDs making sure there is a strickly
# indirect relationship between PDs and risk ratings.
# It uses the count of defaults and total count for each risk rating level.
#
###########################################################################
FUNCTION smooth(total, defaults)
{

	# Define raw PD vector
	SET raw = defaults / total
	
	# Smooth until it is monotone
	WHILE !is_monotone(raw)
		
		# Begin loop
		SET i = 0
		WHILE i < LENGTH(raw)
			
			IF raw[i] >= raw[i+1] AND raw[i] != 0.0003
				# Loop to count how many times current_item_pd >= next_item_pd
				SET count = 1
				WHILE raw[i] == raw[i + count]
					count++
				
				# Calculate PD for range
				SET defaulted_range_sum = SUM( defaults[i:(i + count)] )
				SET total_range_sum = SUM( total[i:(i + count)] )
				SET raw[i:(i + count)] = default_range_sum / total_range_sum

				# Update counter
				SET i = i + count
			
			# Go to next
			i++
			
	RETURN raw
	
}	
 

   
```