.data
	VAR_a:	.space	16
	VAR_i:	.word	0
	VAR_j:	.word	0
	VAR_result:	.word	0
.text
main:
	lw	$t0,	VAR_result
	li	$t0,	0
	lw	$t1,	VAR_i
	li	$t1,	0
L_7:
	blt	$t1,	2,	L_1
	li	$t2,	0
	b	L_2
L_1:
	li	$t2,	1
L_2:
	beq	$t2,	0,	L_8
	lw	$t3,	VAR_j
	li	$t3,	0
L_5:
	blt	$t3,	2,	L_3
	li	$t4,	0
	b	L_4
L_3:
	li	$t4,	1
L_4:
	beq	$t4,	0,	L_6
	add	$t5,	$t1,	$t3
	move	$t6,	$t5
	mul	$t7,	$t1,	2
	add	$t7,	$t7,	$t3
	mul	$t7,	$t7,	4
	sw	$t6,	VAR_a($t7)
	add	$t3,	$t3,	1
	b	L_5
L_6:
	add	$t1,	$t1,	1
	b	L_7
L_8:
	li	$t1,	0
L_15:
	blt	$t1,	2,	L_9
	li	$t7,	0
	b	L_10
L_9:
	li	$t7,	1
L_10:
	beq	$t7,	0,	L_16
	li	$t3,	0
L_13:
	blt	$t3,	2,	L_11
	li	$t8,	0
	b	L_12
L_11:
	li	$t8,	1
L_12:
	beq	$t8,	0,	L_14
	mul	$t9,	$t1,	$t3
	add	$s0,	$t0,	$t9
	move	$t0,	$s0
	add	$t3,	$t3,	1
	b	L_13
L_14:
	add	$t1,	$t1,	1
	b	L_15
L_16:
	li	$v0,	1
	move	$a0,	$t0
	syscall
	li	$v0,	10
	syscall
