# vim:fdm=marker:

templates = {

'main' : # {{{
"""
%%include "lib/x86asm/asm_io.inc"

; initialized data
segment .data
%s

; constants
%s


; uninitialized data
segment .bss
%s

; code
segment .text
%%ifdef ELF_TYPE
        global  main
%%else
        global  _main
%%endif

; entry point
%%ifdef ELF_TYPE
main:
%%else
_main:
%%endif
        enter   0, 0            ; setup routine
        pusha

%s

        popa
        mov     eax, 0          ; return
        leave                     
        ret
""", # }}}

'const' : # {{{
"""
%s equ %s
""", # }}}

'var' : # {{{
"""
%s resd 1
""", # }}}

'proc' : # {{{
"""
        jmp     %s              ; circumvent the procedure definition below
%s:                             ; procedure name
        push    ebp
        mov     ebp, esp        ; procedure prologue
%s
        pop     ebp             ; procedure epilogue
        ret
%s:                             ; procedure end
""", # }}}

'assign' : # {{{
# the value to be assigned is in EAX
"""
; assignment
%s 
        mov     [%s], eax
""", # }}}

'call' : # {{{
# if we want to support procedures with parameters
# we need to push arguments on stack before calling
# and move ESP back to remove them from stack after calling
"""
        call    %s
""", # }}}

'if' : # {{{
# the condition must set the flags correctly
# and generate the right "jxx endif#" instruction
"""
; if condition
%s
; if statement
%s
; if label
%s:
""", # }}}

'while' : # {{{
# the condition must set the flags correctly
# and generate the right "jxx endwhile#" instruction
"""
; while label
%s:
; while condition
%s
; while statement
%s
; while next turn
        jmp     %s
; while endlabel
%s:
""", # }}}

'print' : # {{{
# the value to be printed is in EAX
"""
; print
%s
        call    print_int
""", # }}}

'oddcond' : # {{{
# the value of the expression is in EAX
# if EAX > 0, we do NOT jump (so we enter the if clause)
# ergo, if EAX <= 0, we jump (jle or jng)
"""
; odd condition
%s
        cmp     eax, 0
        jle     %s
""", # }}}

'bincond' : # {{{
# we first calculate the left one, and push the result (in EAX) on stack
# then we calculate the right one, leave its value in EAX,
# pop the left one into EBX, compare EBX with EAX (that is, left with right)
"""
; binary condition
; left is pushed on stack
%s
        push    eax
; right is popped into eax
%s
        pop     ebx       ; left
        cmp     ebx, eax
        %s      %s
""", # }}}

'exprfirst' : # {{{
# the value of the first term is in EAX
# then if the first sign is minus, we do a negation
"""
; first term in the expression
%s
%s                        ; negation if the first sign is minus
        push    eax       ; push the result of the first term on stack
""", # }}}

'negate' : # {{{
# negates EAX mathmatically
"""
; negate
        not     eax
        inc     eax
""", # }}}

'expr' : # {{{
# previous value is on stack
"""
; another term in the expression, value in EAX
%s
        pop    ebx
        %s    ebx, eax   ; accumulate each term to top of the stack
        push   ebx
""", # }}}

'exprend' : # {{{
"""
        pop     eax       ; pop the expression value into EAX
""", # }}}

'termfirst' : # {{{
# the value of the first factor is in EAX
"""
; first factor in the term
%s
        push    eax       ; push the result of the first factor on stack
""", # }}}

'termmul' : # {{{
# previous value is on stack
"""
; another factor in the term: multiplication, value in EAX
%s
        pop     ebx
        imul    ebx, eax
        push    ebx       ; accumulate each factor to top of the stack
""", # }}}

'termdiv' : # {{{
# previous value is on stack
"""
; another factor in the term: division, value in EAX
%s
        mov     ebx, eax  ; divider
        pop     eax       ; EDX:EAX is the dividend
        xor     edx, edx  ; initialize EDX before division
        idiv    ebx       ; the quotient is in EAX
        push    eax       ; accumulate each factor to top of the stack
""", # }}}

'termend' : # {{{
"""
        pop     eax       ; put the term value in EAX
""", # }}}

'idfacconst' : # {{{
"""
; idfactor: const
        mov     eax, %s   ; use the const name directly
""", # }}}

'idfacvar' : # {{{
"""
; idfactor: variable
        mov     eax, [%s]
""", # }}}

'numfac' : # {{{
"""
; numfactor
        mov     eax, %s
""", # }}}

}
