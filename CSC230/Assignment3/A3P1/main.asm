.include "m2560def.inc"
;
; ***********************************************************
; * Cameron Lindsay                                         *
; * V00927778                                               *
; * CSC230                                                  *
; * Creation Date: 02-Feb-2020                              *
; * Program version (Part): 1.0                             *
; * Input:                                                  *
; * Output:                                                 *
; ***********************************************************

; *************************
; * Code segment follows: *
; *************************
.cseg
.org 0
;************************
; Your code starts here:

; ***********************************************************
; Part 1                                                    *
; ***********************************************************

; diff = number1
;.def diff = r16

; number1 = 103;
; number2 = 41;
; number3 = 15;
;ldi diff, 103
;ldi r17, 41
;ldi r18, 15

; diff -= number2;
;sub diff, r17

; diff -= number3;
;sub diff, r18

; result = diff
;sts result, diff


; ***********************************************************
; Part 2                                                    *
; ***********************************************************

; *************************
; * Loop Pseudocode: *
; number = /* choose a number in (0x00, 0xFF] */ 
; count = 0; while (number > 0) { dest[count++] = number
; * Output number on LEDs *
; * delay 0.5 second *
; number --
; *************************

; number = /* choose a number in (0x00, 0xFF] */
.def number = r16
.def portMask = r17
.def outnumber = r18
.def temp = r19

ldi number, 0x14
ldi portMask, 0b00100000

storenumber:
	st Y+, number
	rjmp ledoutput 

ledoutput:
	;portmask = 0b00100000
	mov temp, number
	and temp, portmask
	lsr temp
	lsr temp
	or outnumber, temp
	lsr portmask 
	;portmask = 0b00010000
	mov temp, number
	and temp, portmask
	lsr temp
	lsr temp
	lsr temp
	or outnumber, temp
	out PORTB, outnumber
	ldi outnumber, 0
	lsr portmask 
	;portmask = 0b00001000
	mov temp, number
	and temp, portmask
	lsr temp
	lsr temp
	or outnumber, temp
	lsr portmask 
	;portmask = 0b00000100
	mov temp, number
	and temp, portmask
	lsl temp
	or outnumber, temp
	lsr portmask
	;portmask = 0b00000010
	mov temp, number
	and temp, portmask
	lsl temp
	lsl temp
	lsl temp
	or outnumber, temp
	lsr portmask
	;portmask = 0b00000001
	mov temp, number
	and temp, portmask
	lsl temp
	lsl temp
	lsl temp
	lsl temp
	lsl temp
	lsl temp
	lsl temp
	or outnumber, temp
	sts PORTL, outnumber
	breq done
	rjmp delay			

delay:
	ldi r24, 0x2A; approx. 0.5 second delay
outer:
	ldi r23, 0xFF
middle: 
	ldi r22, 0xFF
inner: 
	dec r22
	brne inner
	dec r23
	brne middle
	dec r24
	brne outer
	rjmp after

after: 
	breq done
	dec number
	rjmp storenumber

;Note: Code adapted from Assignment 3 part 2 of L. Jacksons CSC230 Course
;
; Your code finishes here.
;*************************

done:	
	jmp done

; *************************
; * Data segment follows: *
; *************************
.dseg
.org 0x200
