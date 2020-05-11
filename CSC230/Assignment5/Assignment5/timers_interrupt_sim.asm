; Cameron Lindsay
; V00927778
; Lab 9
; All Lines EXCEPT 113-116 by CSC 230 Lab Team/ Dr. LillAnne Jackson




.org 0x0000
	jmp setup

.org 0x0028
	jmp timer1_ISR
    
.org 0x0072

main_loop:	
	call delay

	lds r16, PORTL
	ldi r17, 0b10100000
	eor r16, r17
	sts PORTL, r16

	rjmp main_loop


setup:
	; initialize the stack pointer (we are using functions!)
	ldi r16, high(RAMEND)
	out SPH, r16
	ldi r16, low(RAMEND)
	out SPL, r16

	; setup the output pins on Port L and Port B
	ldi r16, 0b10101010
	sts DDRL, r16
	ldi r16, 0b00001010
	out DDRB, r16

	; turn on one of the LEDs on port B
	ldi r16, 0b00001000
	out PORTB, r16

	; turn on one of the LEDs on port L
	ldi r16, 0b10000000
	sts PORTL, r16

	call timer1_setup

	jmp main_loop


.equ TIMER1_DELAY = 208
.equ TIMER1_MAX_COUNT = 0xFFFF
.equ TIMER1_COUNTER_INIT=TIMER1_MAX_COUNT-TIMER1_DELAY + 1
timer1_setup:	
	; timer mode	
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
	sei	

	ret


; timer interrupt flag is automatically
; cleared when this ISR is executed
; per page 168 ATmega datasheet
timer1_ISR:
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

	;Write your code here: toggle the bits which control the bottom two LEDs, 
	;which will make them flash alternately -- hint PORTB and EOR instruction
	in r17, PORTB
	ldi r16, 0b00001010
	eor r17, r16
	out PORTB, r17

	pop r16
	sts SREG, r16
	pop r18
	pop r17
	pop r16
	reti


; Function that delays for a period of time using busy-loop
delay:
	push r20
	push r21
	push r22
	nop
	; Nested delay loop
	ldi r20, 0x03
x1:
		ldi r21, 0x02
x2:
			ldi r22, 0x08
x3:
				dec r22
				brne x3
			nop
			dec r21
			brne x2
		dec r20
		brne x1

	pop r22
	pop r21
	pop r20
	ret	