; CSC 230
; Assignment 5
; Spring 2020
;
; Author:
; Cameron Lindsay
; V00927778
; 
;
; This displays a series of messages that scroll via LCD cache in dseg, interrupts occur every second and change the output with a reversal of scrolling occurring after 10 seconds;
; Code used includes code written from CSC 230 Lab 6:
;		Author unknown (copy_string.asm)
; code from CSC 230 Lab 7:
;		Created by: Sudhakar Ganti (Fall 2016), 
;		Modified by: Tom Arjannikov (Spring 2020)
; code from CSC 230 Lab 9:
;      Author unknown (timers_interrupt_sim.asm) 
; and code from CSC 230 Assignment 5 outline:
;		LillAnne Jackson (Spring 2020)
; Areas have been modified in adherence to CSC 230 Assignment 5 by myself, Cameron Lindsay, March 2020 
;************************************************************************************************************************************************************
;
.cseg
.org 0x0000
	jmp initialize

.org 0x0028
	jmp timer1_ISR

.org 0x0072

;Pseudocode from Assignment 5 Part A Outline (LillAnne Jackson, Spring 2020)
;copy the strings from program to data memory
;create the two reversed strings, store in data memory
;startString = "******************"
;line1 = startString
;line2 = startString
;display(line1,line2)
;msg_counter=0
;direction = 0
;busy wait
initialize:
; These strings contain the (up to) 18 characters to be displayed on the LCD
; Each time through, the 18 characters are copied into these memory locations
	.equ msg_length = 18
	.def temp = r17
	.def msg_counter = r19
	.def switch = r20
	
	clr switch
	ldi msg_counter, 101

	; initialize the stack pointer (SP) to the end of RAM
	ldi temp, low(RAMEND)
	out SPL, temp
	ldi temp, high(RAMEND)
	out SPH, temp

	; copy messages from program memory to data memory
	ldi YH, high(msg1)
	ldi YL, low(msg1)
	ldi ZH, high(msg1_p << 1)
	ldi ZL, low(msg1_p << 1)
	call get_message
	
	ldi YH, high(msg2)
	ldi YL, low(msg2)
	ldi ZH, high(msg2_p << 1)
	ldi ZL, low(msg2_p << 1)
	call get_message

	; reverse messages in dseg using hardware stack
	ldi temp, high(msg1)
	push temp
	ldi temp, low(msg1)
	push temp
	ldi temp, high(msg3)
	push temp
	ldi temp, low(msg3)
	push temp
	call reverse
	pop temp
	pop temp
	pop temp
	pop temp
	
	ldi temp, high(msg2)
	push temp
	ldi temp, low(msg2)
	push temp
	ldi temp, high(msg4)
	push temp
	ldi temp, low(msg4)
	push temp
	call reverse
	pop temp
	pop temp
	pop temp
	pop temp

	; copy starting strings from program memory to data memory
	ldi YH, high(line1)
	ldi YL, low(line1)
	ldi ZH, high(startString << 1)
	ldi ZL, low(startString << 1)
	call get_message

	ldi YH, high(line2)
	ldi YL, low(line2)
	call get_message
	
	; 'display' starting string to LCD caches in dseg using software stack
	#define pushSW(Rr) st -Y, Rr ; Software stack "push commands
	#define popSW(Rr) ld Rr,Y+ ; Software stack "pop" commands
	
	ldi YH, high(RAMEND - 200 - 1); relatively arbitrary, just want to ensure I dont overwrite anything pushed onto the stack
	ldi YL, low(RAMEND - 200 - 1)
	ldi temp, high(line1)
	pushSW(temp)
	ldi temp, low(line1)
	pushSW(temp)
	ldi temp, high(line2)
	pushSW(temp)
	ldi temp, low(line2)
	pushSW(temp)
	call display
	popSW(temp)
	popSW(temp)
	popSW(temp)
	popSW(temp)
	
	call timer1_setup
	
	rjmp main

main:
rjmp main

get_message:
	; protect registers
	push ZH
	push ZL
	push YH
	push YL
	push temp

	gm_loop:
		lpm temp, Z+
		cpi temp, 0
		breq gm_done
		st Y+, temp
		rjmp gm_loop	

	; remove protected registers from the stack
	gm_done:
		st Y, temp; 0 terminates string
		pop temp
		pop YL
		pop YH
		pop ZL
		pop ZH
		ret

display:
	;protecting registers
	push YH
	push YL
	push ZH
	push ZL
	push XH
	push XL
	push temp
	pushSW(ZH)
	pushSW(ZL)
	pushSW(XH)
	pushSW(XL)
	pushSW(temp)

	ldd ZH, Y+5+3 ; line1
	ldd ZL, Y+5+2 ; line1

	ldi XH, high(LCDCacheTopLine) ; destination
	ldi XL, low(LCDCacheTopLine) ; destination
		
	loop:
		ld temp, Z+
		cpi temp, 0
		breq loop2
		st X+, temp
		rjmp loop	

	loop2:	
		st X+, temp
		ldd ZH, Y+5+1 ; line2
		ldd ZL, Y+5 ; line2

		ldi XH, high(LCDCacheBottom) ; destination
		ldi XL, low(LCDCacheBottom) ; destination
	
	loop2_b:
		ld temp, Z+
		cpi temp, 0
		breq display_done
		st X+, temp
		rjmp loop2_b	

	display_done:
		st X+, temp; 0 terminates reversed string
		popSW(temp)
		popSW(XL)
		popSW(XH)
		popSW(ZL)
		popSW(ZH)
		pop temp 
		pop XL
		pop XH
		pop ZL
		pop ZH	
		pop YL
		pop YH
		ret

reverse:
	;protecting registers
	push ZH
	push ZL
	push YH
	push YL
	push XH
	push XL
	push r16
	push r19
	
	in YH, SPH ; stack pointer
	in YL, SPL ; stack pointer

	ldd ZH, Y+15 ; message
	ldd ZL, Y+14 ; message

	ldd XH, Y+13 ; destination
	ldd XL, Y+12 ; destination
	
	clr r16; buffers for extra pop required for compare
	push r16; buffers for extra pop required for compare
	rev_loop:
		ld r16, Z+
		cpi r16, 0
		breq pop_stack_init
		push r16
		rjmp rev_loop	
	pop_stack_init:
		pop r19
		cpi r19, 0
		breq rev_done
		st X+, r19
		rjmp pop_stack_init

	rev_done:
		;popping protected registers
		st X+, r19; 0 terminates reversed string

		pop r19
		pop r16
		pop XL
		pop XH
		pop YL
		pop YH
		pop ZL
		pop ZH	
	
	ret

; The following code is modified from CSC 230 Lab 9, authors detailed above
.equ TIMER1_DELAY = 208
;.equ TIMER1_DELAY = 15625 ; for one second - obtained from calculator defined in Lab 9 resources
.equ TIMER1_MAX_COUNT = 0xFFFF
.equ TIMER1_COUNTER_INIT=TIMER1_MAX_COUNT-TIMER1_DELAY + 1
timer1_setup:	
	; timer mode	
	push r16
	ldi r16, 0x00		; normal operation
	sts TCCR1A, r16

	; prescale 
	; Our clock is 16 MHz, which is 16,000,000 per second
	;
	; scale values are the last 3 bits of TCCR1B:
	;
	; 000 - timer disabled
	; 001 - clock (no scaling)
	; 010 - clock / 8
	; 011 - clock / 64
	; 100 - clock / 256
	; 101 - clock / 1024
	; 110 - external pin Tx falling edge
	; 111 - external pin Tx rising edge
	;ldi r16, (1<<CS12)|(1<<CS10)	; clock / 1024
	ldi r16, (1<<CS10)				; clock / 1
	sts TCCR1B, r16
	
	; allow timer to interrupt the CPU when it's counter overflows
	ldi r16, 1<<TOIE1
	sts TIMSK1, r16

	; set timer counter to TIMER1_COUNTER_INIT (defined above)
	ldi r16, high(TIMER1_COUNTER_INIT)
	sts TCNT1H, r16 	; must WRITE high byte first 
	ldi r16, low(TIMER1_COUNTER_INIT)
	sts TCNT1L, r16		; low byte
	
	; enable interrupts (the I bit in SREG)
	pop r16
	sei	

	ret

;A modulus-like function
modulus:
	push msg_counter
	mov temp, msg_counter
	cpi msg_counter, 4
	brsh lp
	rjmp done_mod
	lp:
	subi msg_counter, 4
	cpi msg_counter, 4
	brsh lp
	done_mod:
	mov temp, msg_counter ; temp has the mod 4 value of the current msg_counter
	pop msg_counter; restore msg_counter
	ret

; timer interrupt flag is automatically
; cleared when this ISR is executed
; per page 168 ATmega datasheet
timer1_ISR:
	push YH
	push YL
	push r16
	push r17
	push r18
	
	lds r16, SREG
	push r16

	; RESET timer counter to TIMER1_COUNTER_INIT (defined above)
	ldi r16, high(TIMER1_COUNTER_INIT)
	sts TCNT1H, r16 	; must WRITE high byte first 
	ldi r16, low(TIMER1_COUNTER_INIT)
	sts TCNT1L, r16		; low byte


	ldi YH, high(RAMEND - 64 - 1)
	ldi YL, low(RAMEND - 64 - 1)

	;Checking if it is the starting msgs
	cpi msg_counter, 101
	breq starting
	
	;checking if its been 10 counters
	cpi msg_counter, 10
	breq switch_on
	cpi msg_counter, 1
	breq switch_on
	rjmp switch_return

	;turns on the switch to decrease/increase count/ direction of scrolling
	switch_on:
	push temp
	ldi temp, 1
	eor switch, temp
	pop temp
	rjmp switch_return

	;first scrolling occurs
	starting:
	ldi msg_counter, 1
	ldi temp, high(line1)
	pushSW(temp)
	ldi temp, low(line1)
	pushSW(temp)
	ldi temp, high(msg1)
	pushSW(temp)
	ldi temp, low(msg1)
	pushSW(temp)
	rjmp increase

	switch_return:	
	call modulus; remainder 4 
	rjmp main1

	; compares the modulus (temp) to determine what will be displayed
	main0:
	cpi temp, 0
	breq main0_display
	rjmp main1
	
	main1:
	cpi temp, 1
	breq main1_display
	rjmp main2

	main2:
	cpi temp, 2
	breq main2_display
	rjmp main3

	main3:
	cpi temp, 3
	breq main3_display
	rjmp main0
	
	; Load the addresses for display
	main0_display:
	ldi temp, high(msg3)
	pushSW(temp)
	ldi temp, low(msg3)
	pushSW(temp)
	ldi temp, high(msg4)
	pushSW(temp)
	ldi temp, low(msg4)
	pushSW(temp)
	rjmp switch_check

	main1_display:
	ldi temp, high(msg4)
	pushSW(temp)
	ldi temp, low(msg4)
	pushSW(temp)
	ldi temp, high(msg1)
	pushSW(temp)
	ldi temp, low(msg1)
	pushSW(temp)
	rjmp switch_check

	main2_display:
	ldi temp, high(msg1)
	pushSW(temp)
	ldi temp, low(msg1)
	pushSW(temp)
	ldi temp, high(msg2)
	pushSW(temp)
	ldi temp, low(msg2)
	pushSW(temp)
	rjmp switch_check

	main3_display:
	ldi temp, high(msg2)
	pushSW(temp)
	ldi temp, low(msg2)
	pushSW(temp)
	ldi temp, high(msg3)
	pushSW(temp)
	ldi temp, low(msg3)
	pushSW(temp)
	rjmp switch_check
	
	;checks direction of scrolling to determine decrease/increase count
	switch_check:
	cpi switch, 1
	breq decrease
	rjmp increase

	increase:
	inc msg_counter
	rjmp msg_change
	decrease:
	dec msg_counter
	rjmp msg_change

	;calls display with loaded addresses
	msg_change:
	call display
	popSW(temp)
	popSW(temp)
	popSW(temp)
	popSW(temp)
	
	end:
	pop r16

	sts SREG, r16
	pop r18
	pop r17
	pop r16
	pop YL
	pop YH
	reti

; end code modified from CSC 230 Lab 9

;program memory
startString: .db "*****************", 0
msg1_p:      .db "Cameron Lindsay  ", 0
msg2_p:      .db "Learning CSC 230 ", 0

.undef temp
.undef msg_counter
.undef switch

;other
.dseg
.org 0x200
line1: .byte msg_length
line2: .byte msg_length
line3: .byte msg_length
line4: .byte msg_length
msg1: .byte msg_length
msg2: .byte msg_length
msg3: .byte msg_length
msg4: .byte msg_length
LCDCacheTopLine: .byte msg_length
LCDCacheBottom: .byte msg_length

