
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'rightEXPONENTleftPLUSMINUSleftTIMESDIVIDEMODrightUMINUSnonassocLPARENRPARENDICE DIVIDE EXPONENT LPAREN MINUS MOD NUMBER PARAMETER PLUS RPAREN TIMES UMINUSexpression : expression PLUS expression\n        | expression MINUS expression\n        | expression TIMES expression\n        | expression DIVIDE expression\n        | expression MOD expressionexpression : expression EXPONENT expressionexpression : MINUS expression %prec UMINUSexpression : LPAREN expression RPARENexpression : DICEexpression : NUMBERexpression : PARAMETER'
    
_lr_action_items = {'MINUS':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,],[2,8,2,2,-9,-10,-11,2,2,2,2,2,2,-7,8,-1,-2,-3,-4,-5,8,-8,]),'LPAREN':([0,2,3,7,8,9,10,11,12,],[3,3,3,3,3,3,3,3,3,]),'DICE':([0,2,3,7,8,9,10,11,12,],[4,4,4,4,4,4,4,4,4,]),'NUMBER':([0,2,3,7,8,9,10,11,12,],[5,5,5,5,5,5,5,5,5,]),'PARAMETER':([0,2,3,7,8,9,10,11,12,],[6,6,6,6,6,6,6,6,6,]),'$end':([1,4,5,6,13,15,16,17,18,19,20,21,],[0,-9,-10,-11,-7,-1,-2,-3,-4,-5,-6,-8,]),'PLUS':([1,4,5,6,13,14,15,16,17,18,19,20,21,],[7,-9,-10,-11,-7,7,-1,-2,-3,-4,-5,7,-8,]),'TIMES':([1,4,5,6,13,14,15,16,17,18,19,20,21,],[9,-9,-10,-11,-7,9,9,9,-3,-4,-5,9,-8,]),'DIVIDE':([1,4,5,6,13,14,15,16,17,18,19,20,21,],[10,-9,-10,-11,-7,10,10,10,-3,-4,-5,10,-8,]),'MOD':([1,4,5,6,13,14,15,16,17,18,19,20,21,],[11,-9,-10,-11,-7,11,11,11,-3,-4,-5,11,-8,]),'EXPONENT':([1,4,5,6,13,14,15,16,17,18,19,20,21,],[12,-9,-10,-11,-7,12,-1,-2,-3,-4,-5,12,-8,]),'RPAREN':([4,5,6,13,14,15,16,17,18,19,20,21,],[-9,-10,-11,-7,21,-1,-2,-3,-4,-5,-6,-8,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,2,3,7,8,9,10,11,12,],[1,13,14,15,16,17,18,19,20,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','dice.py',64),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','dice.py',65),
  ('expression -> expression TIMES expression','expression',3,'p_expression_binop','dice.py',66),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','dice.py',67),
  ('expression -> expression MOD expression','expression',3,'p_expression_binop','dice.py',68),
  ('expression -> expression EXPONENT expression','expression',3,'p_expression_exponent','dice.py',81),
  ('expression -> MINUS expression','expression',2,'p_expression_uminus','dice.py',85),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','dice.py',89),
  ('expression -> DICE','expression',1,'p_expression_dice','dice.py',93),
  ('expression -> NUMBER','expression',1,'p_expression_number','dice.py',97),
  ('expression -> PARAMETER','expression',1,'p_expression_parameter','dice.py',101),
]
