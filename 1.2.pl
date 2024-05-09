:- use_module(library(lists)).


replace_nth(N,I,V,O) :-
    nth1(N,I,_,T),
    nth1(N,O,V,T).

replace_row_col(M,Row,Col,Cell,N) :-
    nth1(Row,M,Old),
    replace_nth(Col,Old,Cell,Upd),
    replace_nth(Row,M,Upd,N).


%up
operation(Matrix, NewMatrix, Size, (X,Y), (X1,Y1)) :-
    Y > 1,
    X1 is X,
    Y1 is Y - 1,
    nth1(Y1,Matrix,Row),
    nth1(X1,Row,Element),
    replace_row_col(Matrix,Y,X,Element,NewMatrix1),
    replace_row_col(NewMatrix1,Y1,X1,0,NewMatrix).


%down
operation(Matrix, NewMatrix, Size, (X,Y), (X1,Y1)) :-
    Y < Size,
    X1 is X,
    Y1 is Y + 1,
    nth1(Y1,Matrix,Row),
    nth1(X1,Row,Element),
    replace_row_col(Matrix,Y,X,Element,NewMatrix1),
    replace_row_col(NewMatrix1,Y1,X1,0,NewMatrix).