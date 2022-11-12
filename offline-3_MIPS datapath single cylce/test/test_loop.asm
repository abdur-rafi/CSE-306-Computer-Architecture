sub $t0, $t0, $t0
sub $t1,$t1,$t1
sub $t2,$t2,$t2
sub $t3,$t3,$t3
sub $t4,$t4,$t4
addi $t0, $t0, 15
IF:
sw $t1, 0($t0)
addi $t1, $t1, 1
beq $t0, $zero, endIf
subi $t0, $t0, 1
j IF
endIf: