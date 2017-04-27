.data
	newLine:	.asciiz	"\n"
	VAR_main_result:	.word	0
	VAR_main_n:	.word	0
.text
fib:
	add	$t0,	$zero,	$a1
	addi	$sp,	$sp,	-4
	sw	$ra,	0($sp)
	ble	$a1,	1,	L_1
	li	$t1,	0
	b	L_2
L_1:
	li	$t1,	1
L_2:
	beq	$t1,	0,	L_3
	add	$v1,	$zero,	$a1
	lw	$ra,	0($sp)
	addi	$sp,	$sp,	4
	jr	$ra
L_3:
	sub	$t2,	$a1,	1
	addi	$sp,	$sp,	-4
	sw	$t2,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a1,	0($sp)
	add	$a1,	$zero,	$t2
	jal	fib
	lw	$a1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t2,	0($sp)
	addi	$sp,	$sp,	4
	add	$t3,	$zero,	$v1
	sub	$t4,	$a1,	2
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
	add	$a1,	$zero,	$t4
	jal	fib
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
	add	$t5,	$zero,	$v1
	add	$t6,	$t3,	$t5
	add	$v1,	$zero,	$t6
	lw	$ra,	0($sp)
	addi	$sp,	$sp,	4
	jr	$ra
	lw	$ra,	0($sp)
	addi	$sp,	$sp,	4
	jr	$ra
main:
	lw	$t0,	VAR_main_n
	li	$t0,	20
	li	$v0,	5
	syscall
	move	$t0,	$v0
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	add	$a1,	$zero,	$t0
	jal	fib
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	add	$t1,	$zero,	$v1
	lw	$t2,	VAR_main_result
	move	$t2,	$t1
	li	$v0,	1
	move	$a0,	$t2
	syscall
	li	$v0,	4
la	$a0,	newLine
	syscall
	li	$v0,	10
	syscall
