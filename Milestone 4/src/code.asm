.data
	VAR_global:	.space	0
	VAR_main_c:	.word	0
	VAR_main_b:	.word	0
	STR_4:	.asciiz	"float"
	STR_5:	.asciiz	"int"
	newLine:	.asciiz	"\n"
.text
main:
	li	$v0,	4
	la	$a0,	STR_4
	syscall
	li	$v0,	4
	la	$a0,	newLine
	syscall
	li	$v0,	4
	la	$a0,	STR_5
	syscall
	li	$v0,	4
	la	$a0,	newLine
	syscall
	li	$v0,	10
	syscall
