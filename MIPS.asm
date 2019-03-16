#############################################################
# This program computesthe first twelve Fibonacci numbers and 
# storethem in array, then display them on $s0
################################################################
.data
	fibs: .space 12        # "array" of 12 words to contain fib values
	size: .word  12       # size of "array" 
	one:  .word  1
	four: .word  4
.text
		or $t0, $zero, $zero 	# load address of array "fibs"
		lw $t5, size ($zero) 	# load array size
		lw $t8, one ($zero) 	# load one in $t8
		lw $t9, four ($zero) 	# load four in $t9 
		add $t2, $zero, $t8 	# 1 is first and second Fib. number
								# (li   $t2, 1)
		sw $t2, 0($t0) 			# F[0] = 1
		sw $t2, 4($t0)			# F[1] = F[0] = 1
		sub $t1, $t5, $t8
		sub $t1, $t1, $t8		# Counter for loop, will execute
								# (size-2) times
loop:	lw $t3, 0($t0)			# Get value from array F[n] 
		lw $t4, 4($t0)			# Get value from array F[n+1]
		add $t2, $t3, $t4		# $t2 = F[n] + F[n+1]
		sw $t2, 8($t0)			# Store F[n+2] = F[n] + F[n+1] in
								# array
		add $t0, $t0, $t9		# increment address of Fib. number 
		sub $t1, $t1, $t8		#decrement loop counter
		slt $at, $zero, $t1		# repeat if not finished yet 
								#(bgt $t1, $zero, loop)
		beq $at, $zero, exit
		j loop
exit: 	and $a0, $zero, $a0		# first argument for output (array) 
		add $a1, $zero, $t5		# second argument for output (size)
		j output				# jump to output routine.
ret:	sub $s0, $s0, $t8		# put last value of $s0 = -1 
								# ($s0  = 0 -1)
#this routine should output 1st 12 fibonacci numbers in $s0
output:	and $t0, $t0, $zero		#initialize counter (i = 0)
for:	add $t1, $t0, $t0
		add $t1, $t1, $t1		#multiply i by 4
		add $t2, $a0, $t1		#address of array element
		lw $s0, 0($t2)			#load value of array element (F[i])
		add $t0, $t0, $t8		#i++
		slt $at, $t0, $a1		# repeat if not finished yet.
								# (bgt $a1, $t0, for)
		bne $at, $zero, for
		nor $t8, $zero, $zero	# $t8 = 1's (i.e. = -1)
		nor$s0, $s0, $t8		# $s0 = 0
exit2:	j ret					#return