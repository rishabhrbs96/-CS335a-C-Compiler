.data
	VAR_global:	.space	408
	VAR_bs_first:	.word	0
	VAR_bs_last:	.word	0
	VAR_bs_middle:	.word	0
	VAR_main_i:	.word	0
	newLine:	.asciiz	"\n"
.text
bs:
	addi	$sp,	$sp,	-4
	sw	$ra,	0($sp)
	lw	$t0,	VAR_bs_first
	li	$t0,	0
	addi	$t2,	$zero,	400
	lw	$t2,	VAR_global($t2)
	sub	$t1,	$t2,	1
	lw	$t3,	VAR_bs_last
	move	$t3,	$t1
	add	$t1,	$t0,	$t3
	div	$t4,	$t1,	2
	lw	$t1,	VAR_bs_middle
	move	$t1,	$t4
L_9:
	ble	$t0,	$t3,	L_1
	li	$t4,	0
	b	L_2
L_1:
	li	$t4,	1
L_2:
	beq	$t4,	0,	L_10
	mul	$t4,	$t1,	4
	addi	$t4,	$t4,	0
	lw	$t4,	VAR_global($t4)
	addi	$t5,	$zero,	404
	lw	$t5,	VAR_global($t5)
	blt	$t4,	$t5,	L_3
	li	$t4,	0
	b	L_4
L_3:
	li	$t4,	1
L_4:
	beq	$t4,	0,	L_7
	add	$t4,	$t1,	1
	move	$t0,	$t4
	b	L_8
L_7:
	mul	$t4,	$t1,	4
	addi	$t4,	$t4,	0
	lw	$t4,	VAR_global($t4)
	beq	$t4,	0,	L_5
	add	$t4,	$t1,	1
	add	$v1,	$zero,	$t4
	lw	$ra,	0($sp)
	addi	$sp,	$sp,	4
	jr	$ra
	b	L_6
L_5:
	sub	$t6,	$t1,	1
	move	$t3,	$t6
L_6:
L_8:
	add	$t6,	$t0,	$t3
	div	$t7,	$t6,	2
	move	$t1,	$t7
	b	L_9
L_10:
	addi	$v1,	$zero,	0
	lw	$ra,	0($sp)
	addi	$sp,	$sp,	4
	jr	$ra
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
L_13:
	addi	$t1,	$zero,	400
	lw	$t1,	VAR_global($t1)
	blt	$t0,	$t1,	L_11
	li	$t2,	0
	b	L_12
L_11:
	li	$t2,	1
L_12:
	beq	$t2,	0,	L_14
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
	b	L_13
L_14:
	li	$v0,	5
	syscall
	addi	$t2,	$zero,	404
	lw	$t2,	VAR_global($t2)
	move	$t2,	$v0
	addi	$t3,	$zero,	404
	sw	$t2,	VAR_global($t3)
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	jal	bs
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	add	$t2,	$zero,	$v1
	li	$v0,	1
	move	$a0,	$t2
	syscall
	li	$v0,	4
	la	$a0,	newLine
	syscall
	li	$v0,	10
	syscall
