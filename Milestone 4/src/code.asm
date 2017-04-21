.data
	VAR_GLOBALTABLE_a:	.word	0
	VAR_b:	.space	16
	VAR_main_d:	.word	0
	VAR_main_bss:	.word	0
	VAR_main_result:	.word	0
.text
main:
	lw	$t0,	VAR_GLOBALTABLE_a
	li	$t0,	3
	lw	$t1,	VAR_main_d
	li	$t1,	2147483647
	lw	$t2,	VAR_main_bss
	li	$t2,	1
	move	$t3,	$t1
	addi	$t4,	$zero,	12
	sw	$t3,	VAR_b($t4)
	move	$t4,	$t2
	addi	$t5,	$zero,	8
	sw	$t4,	VAR_b($t5)
	addi	$t5,	$zero,	12
	lw	$t5,	VAR_b($t5)
	addi	$t6,	$zero,	8
	lw	$t6,	VAR_b($t6)
	mul	$t7,	$t5,	$t6
	lw	$t8,	VAR_main_result
	move	$t8,	$t7
	li	$v0,	1
	move	$a0,	$t8
	syscall
	li	$v0,	10
	syscall
