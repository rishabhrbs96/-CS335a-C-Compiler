.data
	VAR_global:	.space	404
	VAR_partition_pivot:	.word	0
	VAR_partition_i:	.word	0
	VAR_partition_t:	.word	0
	VAR_partition_j:	.word	0
	VAR_quickSort_pi:	.word	0
	VAR_swap_temp:	.word	0
	VAR_main_i:	.word	0
	newLine:	.asciiz	"\n"
.text
partition:
	add	$t0,	$zero,	$a1
	add	$t1,	$zero,	$a2
	addi	$sp,	$sp,	-4
	sw	$ra,	0($sp)
	mul	$t2,	$a2,	4
	addi	$t2,	$t2,	0
	lw	$t2,	VAR_global($t2)
	lw	$t3,	VAR_partition_pivot
	move	$t3,	$t2
	sub	$t2,	$a1,	1
	lw	$t4,	VAR_partition_i
	move	$t4,	$t2
	lw	$t2,	VAR_partition_j
	move	$t2,	$a1
L_7:
	sub	$t5,	$a2,	1
	ble	$t2,	$t5,	L_1
	li	$t5,	0
	b	L_2
L_1:
	li	$t5,	1
L_2:
	beq	$t5,	0,	L_8
	mul	$t5,	$t2,	4
	addi	$t5,	$t5,	0
	lw	$t5,	VAR_global($t5)
	ble	$t5,	$t3,	L_3
	li	$t5,	0
	b	L_4
L_3:
	li	$t5,	1
L_4:
	beq	$t5,	0,	L_5
	add	$t4,	$t4,	1
	addi	$sp,	$sp,	-4
	sw	$t3,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t2,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t4,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a2,	0($sp)
	add	$a1,	$zero,	$t4
	add	$a2,	$zero,	$t2
	jal	swap
	lw	$a2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$a1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t4,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t3,	0($sp)
	addi	$sp,	$sp,	4
L_5:
	add	$t2,	$t2,	1
	b	L_7
L_8:
	add	$t5,	$t4,	1
	addi	$sp,	$sp,	-4
	sw	$t3,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t2,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t5,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t4,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a2,	0($sp)
	add	$a1,	$zero,	$t5
	add	$a2,	$zero,	$a2
	jal	swap
	lw	$a2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$a1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t4,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t5,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t3,	0($sp)
	addi	$sp,	$sp,	4
	add	$t6,	$t4,	1
	add	$v1,	$zero,	$t6
	lw	$ra,	0($sp)
	addi	$sp,	$sp,	4
	jr	$ra
	lw	$ra,	0($sp)
	addi	$sp,	$sp,	4
	jr	$ra
quickSort:
	add	$t0,	$zero,	$a1
	add	$t1,	$zero,	$a2
	addi	$sp,	$sp,	-4
	sw	$ra,	0($sp)
	blt	$a1,	$a2,	L_9
	li	$t7,	0
	b	L_10
L_9:
	li	$t7,	1
L_10:
	beq	$t7,	0,	L_11
	addi	$sp,	$sp,	-4
	sw	$t3,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t2,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t6,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t5,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t4,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a2,	0($sp)
	add	$a1,	$zero,	$a1
	add	$a2,	$zero,	$a2
	jal	partition
	lw	$a2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$a1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t4,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t5,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t6,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t3,	0($sp)
	addi	$sp,	$sp,	4
	add	$t7,	$zero,	$v1
	lw	$t8,	VAR_quickSort_pi
	move	$t8,	$t7
	sub	$t7,	$t8,	1
	addi	$sp,	$sp,	-4
	sw	$t8,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t3,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t2,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t7,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t6,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t5,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t4,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a2,	0($sp)
	add	$a1,	$zero,	$a1
	add	$a2,	$zero,	$t7
	jal	quickSort
	lw	$a2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$a1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t4,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t5,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t6,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t7,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t3,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t8,	0($sp)
	addi	$sp,	$sp,	4
	add	$t9,	$t8,	1
	addi	$sp,	$sp,	-4
	sw	$t9,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t8,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t3,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t2,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t7,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t6,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t5,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t4,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a2,	0($sp)
	add	$a1,	$zero,	$t9
	add	$a2,	$zero,	$a2
	jal	quickSort
	lw	$a2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$a1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t4,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t5,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t6,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t7,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t2,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t3,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t8,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t9,	0($sp)
	addi	$sp,	$sp,	4
L_11:
	lw	$ra,	0($sp)
	addi	$sp,	$sp,	4
	jr	$ra
swap:
	add	$t0,	$zero,	$a1
	add	$t1,	$zero,	$a2
	addi	$sp,	$sp,	-4
	sw	$ra,	0($sp)
	mul	$s0,	$a1,	4
	addi	$s0,	$s0,	0
	lw	$s0,	VAR_global($s0)
	lw	$s1,	VAR_swap_temp
	move	$s1,	$s0
	mul	$s0,	$a2,	4
	addi	$s0,	$s0,	0
	lw	$s0,	VAR_global($s0)
	move	$s2,	$s0
	mul	$s0,	$a1,	4
	addi	$s0,	$s0,	0
	sw	$s2,	VAR_global($s0)
	move	$s2,	$s1
	mul	$s0,	$a2,	4
	addi	$s0,	$s0,	0
	sw	$s2,	VAR_global($s0)
	lw	$ra,	0($sp)
	addi	$sp,	$sp,	4
	jr	$ra
main:
	li	$v0,	5
	syscall
	addi	$t0,	$zero,	400
	lw	$t0,	VAR_global($t0)
	move	$t0,	$v0
	addi	$t1,	$zero,	400
	sw	$t0,	VAR_global($t1)
	lw	$t0,	VAR_main_i
	li	$t0,	0
L_15:
	addi	$t1,	$zero,	400
	lw	$t1,	VAR_global($t1)
	blt	$t0,	$t1,	L_13
	li	$t2,	0
	b	L_14
L_13:
	li	$t2,	1
L_14:
	beq	$t2,	0,	L_16
	mul	$t3,	$t0,	4
	addi	$t3,	$t3,	0
	sw	$t2,	VAR_global($t3)
	li	$v0,	5
	syscall
	move	$t2,	$v0
	mul	$t3,	$t0,	4
	addi	$t3,	$t3,	0
	sw	$t2,	VAR_global($t3)
	add	$t0,	$t0,	1
	b	L_15
L_16:
	addi	$t3,	$zero,	400
	lw	$t3,	VAR_global($t3)
	sub	$t2,	$t3,	1
	addi	$sp,	$sp,	-4
	sw	$t2,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	addi	$a1,	$zero,	0
	add	$a2,	$zero,	$t2
	jal	quickSort
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t2,	0($sp)
	addi	$sp,	$sp,	4
	li	$t0,	0
L_19:
	addi	$t4,	$zero,	400
	lw	$t4,	VAR_global($t4)
	blt	$t0,	$t4,	L_17
	li	$t5,	0
	b	L_18
L_17:
	li	$t5,	1
L_18:
	beq	$t5,	0,	L_20
	mul	$t5,	$t0,	4
	addi	$t5,	$t5,	0
	lw	$t5,	VAR_global($t5)
	li	$v0,	1
	move	$a0,	$t5
	syscall
	li	$v0,	4
	la	$a0,	newLine
	syscall
	add	$t0,	$t0,	1
	b	L_19
L_20:
	li	$v0,	10
	syscall
