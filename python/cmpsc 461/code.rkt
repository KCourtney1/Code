#lang racket/base

#| Problem 1: Working with Data |#
(define (clamp-bounds ub lb data)
    (map (lambda (x)(cond
        [(> x ub) ub]
        [(< x lb) lb]
        [else x]))
        data)
)

; (clamp-bounds 9 -9 '())
; (clamp-bounds -3 -7 '(-4 -5))
; (clamp-bounds 1 1 '(1 2 3))
; (clamp-bounds 2 -1'(2 -4 3))

(define (cleanup-data data)
    (cond
        [(null? data) '()]
        [(boolean? (car data))(cleanup-data (cdr data))]
        [(string? (car data))
            (cons (string-upcase(car data))
                (cleanup-data (cdr data))
            )
        ]

        [(number? (car data))
            (define n (car data))
            (define check (if (even? n) 
                                (/ n 2)
                                (- (* n 3) 1)
                            )
            )
            (cons check(cleanup-data (cdr data)))
        ]

        ;if list then recurse inside and append.
        [(list? (car data))
            (append (cleanup-data (car data))
                    (cleanup-data (cdr data))
            )
        ]
    )
)

; (cleanup-data '(((()))))
; (cleanup-data '(#t "2" 3))
; (cleanup-data '(1 (2 (3 (4)))))
; (cleanup-data '(2 "we" (#f 1 "are" #t) 6))

(define (lesser-decadents data)
    (if (null? data) '()
        (let* ([x (car data)]
                [remaining (cdr data)]
                [lessers (filter (lambda (y) (< y x)) remaining)])
            (cons (list x lessers)(lesser-decadents (cdr data)))
        )
    )
)

; (lesser-decadents '())
; (lesser-decadents '(1 2 3))
; (lesser-decadents '(-2 5 0))
; (lesser-decadents '(1 3 4 2 3))

(define (windowed-average size data)
    (define (sum-list k lst)
                    (if (or (zero? k) (null? lst))
                        0
                        (+ (car lst) (sum-list (- k 1) (cdr lst)))
                    )
                )

    ;checks if list has k elements left (in this case [recursive call pos, rest of the list]). 
    (define (has-n? k lst)
        (cond
            [(zero? k) #t]
            [(null? lst) #f]
            [else (has-n? (- k 1) (cdr lst))]
        )
    )

    (if (< size 1) '()
        (begin
            (if (has-n? size data)
                (cons (exact->inexact (/ (sum-list size data) size))
                    (windowed-average size (cdr data)))
                '()
            )
        )
    )
)

; (windowed-average 4 '())
; (windowed-average 4 '(1 2 3))
; (windowed-average 2 '(1 2 3))
; (windowed-average 4 '(1 3 4 2 3))
(windowed-average 4 '(1 2 3 4 5 6))
(windowed-average 1 '(10 -3 8))
;(windowed-average 0 '(1 2 3))
;(windowed-average 3 '(1 2 3 4 5 6))

; #| Problem 2: Dealing with Duration |#
(define (pad-duration duration)
    (cond
        [(null? duration) '(0 0 0)]
        [(= (length duration)1) (list 0 0 (car duration))]
        [(= (length duration)2) (list 0 (car duration) (cadr duration))]
        [(= (length duration)3) duration]
        [else duration]
    )
)

; (pad-duration '())
; (pad-duration '(123))
; (pad-duration '(45 67))
; (pad-duration '(1 2 3))
; (pad-duration '(0 0 0))
; (pad-duration '(10 20))
; (pad-duration '(0 0 0 0))

(define (fmt-duration duration)
    (define pad_dur (pad-duration duration))
    (define hours(car pad_dur))
    (define minutes(cadr pad_dur))
    (define seconds(caddr pad_dur))
    
    ;converts number into string and decides unit descriptor.
    (define (formater value singular plural)
        (cond
            [(zero? value) ""]
            [(= value 1) (string-append (number->string value) " " singular)]
            [else (string-append (number->string value) " " plural)]
        )
    )

    ;sets up string list with unit.
    (define parts
        (filter (lambda(s) (not (string=? s "")))
            (list
                (formater hours "Hour" "Hours")
                (formater minutes "Minute" "Minutes")
                (formater seconds "Second" "Seconds")
            )
        )    
    )

    ;adds strings together. 
    (cond
        [(null? parts) "0 Seconds"]
        [(= (length parts) 1) (car parts)]
        [(= (length parts) 2) (string-append (car parts) " and " (cadr parts))]
        [else (string-append (car parts) ", " (cadr parts) ", and " (caddr parts))]
    )
)

; (fmt-duration '(99))
; (fmt-duration '(1 0 0))
; (fmt-duration '(9 1))
; (fmt-duration '(1 2 3))
; (fmt-duration '(0 0 0))

(define (add-durations leftDuration rightDuration)
    (define pad_dur_L (pad-duration leftDuration))
    (define pad_dur_R (pad-duration rightDuration))

    (define total_seconds (+ (caddr pad_dur_L) (caddr pad_dur_R)))
    (define total_minutes (+ (cadr pad_dur_L) (cadr pad_dur_R)))
    (define total_hours (+ (car pad_dur_L) (car pad_dur_R)))

    (define carry_minutes (+ total_minutes (quotient total_seconds 60)))
    (define remaining_seconds (remainder total_seconds 60))

    (define remaining_hours (+ total_hours (quotient carry_minutes 60)))
    (define remaining_minutes (remainder carry_minutes 60))

    ;formating
    (cond 
        [(> remaining_hours 0) (list remaining_hours remaining_minutes remaining_seconds)]
        [(> remaining_minutes 0) (list remaining_minutes remaining_seconds)]
        [else (list remaining_seconds)]    
    )
)

; (add-durations '(0 0 0) '(0 0 0)) 
; (add-durations '(0 0 0) '(10))   
; (add-durations '(123) '(1 0 0))  
; (add-durations '(45 67) '(8 9))  
; (add-durations '(0 30 0) '(30 0))
; (add-durations '(23 59 59) '(23 59 59))

#| Problem 4: Curried Calculations |#
(define menu
    '(("vegetable samosa" 4.99)
    ("aloo tikki" 5.35)
    ("paneer pakora" 6.50)
    ("fish curry" 16.99)
    ("tikka masala" 16.35)
    ("chicken saag" 15.00)
    ("daal tadka" 13.10)
    ("malai kofta" 14.35)
    ("mango lassi" 5.00)
    ("spiced tea" 3.50)
    ("coffee" 3.50))
)

;find item on menu.
(define (lookup item alist)
        (cond
            [(null? alist) #f] ;base case
            [(string=? item (car (car alist))) (cadr (car alist))] ;compare item to first element in list, if match get the price and return it.
            [else (lookup item (cdr alist))] ;no match, skip.
        )
)

;get order in pair in a list (("food1", quantiy) ("food2", quantiy))...
(define (parse_order lst)
  (cond
        [(null? lst) '()] ;base case
        [(and 
            (number? (car lst))
            (pair? (cdr lst))
            (string? (car (cdr lst)))
         )
         (cons (list (car (cdr lst)) (car lst))
               (parse_order (cddr lst))
         )] ;number followed by a string
        [(string? (car lst))
         (cons (list (car lst) 1)
               (parse_order (cdr lst)))] ;just string no int
        [else (parse_order (cdr lst))] ;skip invalid entries
    )
)


;get cost of each item in ordered items discounted then add all together.
(define (calc_items ordered_items discounts)
    (if (null? ordered_items) 0
        (let* (
                [entry (car ordered_items)]
                [item (car entry)]
                [qty (cadr entry)]
                [price (lookup item menu)]
                [discount (or (lookup item discounts) 0)]
                [cost (* qty price (- 1 (/ discount 100.0)))]
            )
            (+ cost (calc_items (cdr ordered_items) discounts))
        )
    )
)

;rounding
(define (round2 num)
    (/ (round (* num 100)) 100.0)
)

(define (calculate-subtotal order discounts)
    (define parsed (parse_order order))
    (define subtotal (calc_items parsed discounts))
    (round2 subtotal)
)

; ;/empty orders check
; (calculate-subtotal '(0 0 0) '()) ; => 0.00
; (calculate-subtotal '() '()) ; => 0.00
; (calculate-subtotal '(0 "coffee") '()) ; => 0.00

; ;/quantiy, /repeated items, /no int quantiy check
; (calculate-subtotal '(2 "coffee" "mango lassi") '()) ; => 12.00
; (calculate-subtotal '("coffee" "coffee" "coffee") '()); => 10.50
; (calculate-subtotal '(2 "coffee" 2 "coffee" 2 "coffee") '()); => 21.00

; ;/discounts that don't apply, /%100 off orders
; (calculate-subtotal '(2 "coffee") '(("mango lassi" 10))) ; => 7.00
; (calculate-subtotal '(50000 "coffee") '(("coffee" 100))) ; => 0.00, out of bounds for assigment but still cool
; ;(calculate-subtotal '(0 "coffee") '(("coffee") 50)) ; => 0.00, out of bounds but dosen't work... not cool

; ;/floating point rounding
; (calculate-subtotal '(1 "coffee" 1 "mango lassi") '()) ;=> 8.5 not 8.49

; ;/'normal' orders
; (calculate-subtotal '(1 "aloo tikki" 2 "chicken saag" 1 "malai kofta" 2 "spiced tea") '()) ; => 56.7
; (calculate-subtotal '(1 "aloo tikki" 2 "chicken saag" 1 "malai kofta" 2 "spiced tea") '(("malai kofta" 10))) ; => 55.26
; (calculate-subtotal '("aloo tikki" 2 "chicken saag" "malai kofta" "spiced tea") '(("malai kofta" 10))) ; => 55.76