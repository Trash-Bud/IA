:- use_module(library(lists)).

slots(4).
disciplines(12).
students(12).
discipline(1, [1,2,3,4,5]). 
discipline(2, [6,7,8,9]).
discipline(3, [10,11,12]).
discipline(4, [1,2,3,4]).
discipline(5, [5,6,7,8]).
discipline(6, [9,10,11,12]).
discipline(7, [1,2,3,5]).
discipline(8, [6,7,8]).
discipline(9, [4,9,10,11,12]).
discipline(10, [1,2,4,5]).
discipline(11, [3,6,7,8]).
discipline(12, [9,10,11,12]).

find_disciplines_in_slot([],_,_,[]).
find_disciplines_in_slot([H|T], SlotNum, Index, Disciplines) :-
    Index1 is Index + 1,
    find_disciplines_in_slot(T,SlotNum,Index1, Disciplines1),
    ((H = SlotNum) -> 
        append(Disciplines1,[Index],Disciplines);
        append(Disciplines1,[],Disciplines)
    ).


calc_colisions(List, Num) :-
    findall(N, (discipline(D,M),member(D,List),nth0(X,M,N)),Num).
    
    





%hill_climbing(Initial, Solution, Solution_Max) :-
