.data
.text
main:
	move	$t0,	$t1
	li	$v0,	1
	move	$a0,	$t2
	syscall
	li	$v0,	10
	syscall
