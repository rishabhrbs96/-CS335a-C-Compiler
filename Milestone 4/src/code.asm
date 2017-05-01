.data
	VAR_global:	.space	0
	VAR_main_a:	.word	0
	newLine:	.asciiz	"\n"
.text
main:
	li	$v0,	5
	syscall
	lw	$t0,	VAR_main_a
	move	$t0,	$v0
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	add	$a1,	$zero,	$t0
	jal	ev
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	li	$v0,	10
	syscall
ev:
	add	$t0,	$zero,	$a1
	addi	$sp,	$sp,	-4
	sw	$ra,	0($sp)
	bgt	$a1,	0,	L_1
	li	$t1,	0
	b	L_2
L_1:
	li	$t1,	1
L_2:
	beq	$t1,	0,	L_3
	li	$v0,	1
	move	$a0,	$a1
	syscall
	li	$v0,	4
	la	$a0,	newLine
	syscall
	sub	$t1,	$a1,	1
	addi	$sp,	$sp,	-4
	sw	$t1,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$t0,	0($sp)
	addi	$sp,	$sp,	-4
	sw	$a1,	0($sp)
	add	$a1,	$zero,	$t1
	jal	od
	lw	$a1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t1,	0($sp)
	addi	$sp,	$sp,	4
L_3:
	lw	$ra,	0($sp)
	addi	$sp,	$sp,	4
	jr	$ra
od:
	add	$t0,	$zero,	$a1
	addi	$sp,	$sp,	-4
	sw	$ra,	0($sp)
	bgt	$a1,	0,	L_5
	li	$t2,	0
	b	L_6
L_5:
	li	$t2,	1
L_6:
	beq	$t2,	0,	L_7
	li	$v0,	1
	move	$a0,	$a1
	syscall
	li	$v0,	4
	la	$a0,	newLine
	syscall
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
	jal	ev
	lw	$a1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t0,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t1,	0($sp)
	addi	$sp,	$sp,	4
	lw	$t2,	0($sp)
	addi	$sp,	$sp,	4
L_7:
	lw	$ra,	0($sp)
	addi	$sp,	$sp,	4
	jr	$ra
