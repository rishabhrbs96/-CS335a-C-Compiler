.data
	VAR_a:	.word	0
	VAR_b:	.word	0
	VAR_c:	.word	0
.text
main:
	lw	$t0,	VAR_a
	li	$t0,	2
	lw	$t1,	VAR_b
	li	$t1,	10
	add	$t2,	$t1,	$t0
	lw	$t3,	VAR_c
	move	$t3,	$t2
	li	$v0,	1
	move	$a0,	$t3
	syscall
	li	$v0,	10
	syscall
