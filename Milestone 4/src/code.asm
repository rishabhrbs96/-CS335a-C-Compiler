.data
	VAR_a:	.word	0
	VAR_b:	.word	0
	VAR_result:	.word	0
	VAR_t:	.word	0
.text
main:
	lw	$t0,	VAR_a
	li	$t0,	0
	lw	$t1,	VAR_b
	li	$t1,	1
	lw	$t2,	VAR_result
	li	$t2,	0
	lw	$t3,	VAR_t
	li	$t3,	2
L_3:
	ble	$t3,	10,	L_1
	li	$t4,	0
	b	L_2
L_1:
	li	$t4,	1
L_2:
	beq	$t4,	0,	L_4
	add	$t5,	$t0,	$t1
	move	$t2,	$t5
	move	$t0,	$t1
	move	$t1,	$t2
	add	$t3,	$t3,	1
	b	L_3
L_4:
	li	$v0,	1
	move	$a0,	$t2
	syscall
	li	$v0,	10
	syscall
