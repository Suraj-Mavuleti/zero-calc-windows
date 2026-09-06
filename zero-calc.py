#!/usr/bin/env python3
import ast
import operator
import math
from decimal import Decimal, getcontext
import sys

# Configure ultra-high precision (100 decimal places)
getcontext().prec = 100

class ZeroCalcEvaluator(ast.NodeVisitor):
    def __init__(self):
        self.variables = {
            'pi': Decimal(str(math.pi)),
            'e': Decimal(str(math.e)),
            'tau': Decimal(str(math.tau))
        }
        self.ops = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.BitXor: operator.pow,  # Support ^ for power
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }
        self.funcs = {
            'sin': lambda x: Decimal(str(math.sin(float(x)))),
            'cos': lambda x: Decimal(str(math.cos(float(x)))),
            'tan': lambda x: Decimal(str(math.tan(float(x)))),
            'sqrt': lambda x: x.sqrt(),
            'log': lambda x: Decimal(str(math.log(float(x)))),
            'abs': abs
        }

    def eval(self, expr):
        # Handle assignments (e.g. x = 10)
        if '=' in expr and '==' not in expr:
            var_name, val_expr = expr.split('=', 1)
            var_name = var_name.strip()
            if not var_name.isidentifier():
                raise SyntaxError(f"Invalid variable name: {var_name}")
            val = self._eval_node(ast.parse(val_expr.strip(), mode='eval').body)
            self.variables[var_name] = val
            return val
        
        # Parse and evaluate standard math expressions safely
        node = ast.parse(expr, mode='eval').body
        return self._eval_node(node)

    def _eval_node(self, node):
        if isinstance(node, ast.Constant):
            return Decimal(str(node.value))
        elif isinstance(node, ast.BinOp):
            op = type(node.op)
            if op == ast.BitXor:
                op = ast.Pow
            return self.ops[op](self._eval_node(node.left), self._eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return self.ops[type(node.op)](self._eval_node(node.operand))
        elif isinstance(node, ast.Name):
            if node.id in self.variables:
                return self.variables[node.id]
            raise NameError(f"Undefined variable: {node.id}")
        elif isinstance(node, ast.Call):
            func_name = node.func.id
            if func_name in self.funcs:
                args = [self._eval_node(arg) for arg in node.args]
                return self.funcs[func_name](*args)
            raise ValueError(f"Unknown function: {func_name}")
        else:
            raise TypeError(f"Unsupported operation or syntax error.")

def main():
    print("[1;36m" + "="*50 + "[0m")
    print("[1;36m          ZERO-CALC: ARBITRARY PRECISION ENGINE[0m")
    print("[1;36m" + "="*50 + "[0m")
    print("[3mType 'help' for commands, 'exit' to quit.[0m
")
    
    evaluator = ZeroCalcEvaluator()
    
    while True:
        try:
            # Try to use readline for history if available
            import readline
        except ImportError:
            pass
            
        try:
            expr = input("[1;32mzero-calc > [0m").strip()
        except (EOFError, KeyboardInterrupt):
            print("
Exiting...")
            sys.exit(0)
            
        if not expr:
            continue
        if expr.lower() in ('exit', 'quit'):
            break
        if expr.lower() == 'help':
            print("
  [1;33mCommands:[0m")
            print("  Variables: [36mmass = 55.5[0m (assign variables easily)")
            print("  Functions: [36msin(x), cos(x), sqrt(x), abs(x), log(x)[0m")
            print("  Math Ops:  [36m+, -, *, /, ^ (power)[0m")
            print("  Precision: [32mArbitrary (Calculates up to 100 decimal places)[0m
")
            continue
            
        try:
            result = evaluator.eval(expr)
            res_str = f"{result:f}"
            if '.' in res_str:
                res_str = res_str.rstrip('0').rstrip('.')
            print(f"[1;33m[Result]: {res_str}[0m
")
        except Exception as e:
            print(f"[1;31m[Error]: {str(e)}[0m
")

if __name__ == '__main__':
    main()
