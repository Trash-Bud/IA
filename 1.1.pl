
%FillB1
operation(X, Y, X1, Y) :-
    X < 4,
    X1 is 4.

%FillB2
operation(X, Y, X, Y1) :-
    Y < 3,
    Y1 is 3.

%EmptyB1
operation(X, Y, 0, Y) :-
    X > 0.

%EmptyB2
operation(X, Y, X, 0) :-
    Y > 0.

%PourB1B2FillB2    
operation(X,Y,X1,Y1) :-
    X + Y >= 3,
    Y < 3,
    X1 is X - (3-Y),
    Y1 is 3.

%PourB1B2EmptyB1   
operation(X,Y,X1,Y1) :-
    X + Y < 3,
    X > 0,
    Y1 is Y + X,
    X1 is 0.

%PourB2B1FillB1    
operation(X,Y,X1,Y1) :-
    X + Y >= 4,
    X < 4,
    X1 is 4,
    Y1 is Y - (4 - X).

%PourB2B1EmptyB2   
operation(X,Y,X1,Y1) :-
    X + Y < 4,
    Y > 0,
    Y1 is 0,
    X1 is Y + X.


solve_bucket_problem(Origin, N, Iteration, Result) :-
    bucket_problem_aux([Origin-1], N, [], Iteration, Result).


bucket_problem_aux([(N,Y)-I|_],N,_, I, (N,Y)).

bucket_problem_aux([(X,Y)-I|Queue], N, Visited, Iteration, Result) :-
    I1 is I + 1,
    findall((X1,Y1)-I1,
        (operation(X,Y,X1,Y1),
            \+ member((X1,Y1), Visited),
            \+ member((X1,Y1), Queue)),
        List
    ),
    append(Queue,List,NewQueue),
    append(Visited,[(X,Y)],NewVisited),
    bucket_problem_aux(NewQueue, N, NewVisited, Iteration, Result).