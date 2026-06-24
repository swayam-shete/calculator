from flask import Flask, request, jsonify, send_from_directory
import ast
import operator

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')

# Supported AST operators mapping
SUPPORTED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def safe_eval(expr_str):
    """
    Safely evaluate a mathematical expression using Python's AST parser.
    Supports numbers, +, -, *, /, ^ (handled as **), unary operators, and parentheses.
    Throws ValueError or ZeroDivisionError on failure.
    """
    if not expr_str:
        raise ValueError("Expression is empty.")
        
    if len(expr_str) > 1000:
        raise ValueError("Expression length exceeds maximum limit of 1000 characters.")
        
    # Replace '^' with '**' for exponentiation
    expr_str = expr_str.replace('^', '**')
    
    try:
        node = ast.parse(expr_str.strip(), mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}")

    def _eval(n):
        if isinstance(n, ast.Expression):
            return _eval(n.body)
        elif isinstance(n, ast.Constant):
            if isinstance(n.value, (int, float)):
                return n.value
            raise ValueError(f"Unsupported constant type: {type(n.value).__name__}")
        elif hasattr(ast, 'Num') and isinstance(n, getattr(ast, 'Num')):  # Fallback for Python < 3.8
            return n.n
        elif isinstance(n, ast.BinOp):
            left = _eval(n.left)
            right = _eval(n.right)
            op_type = type(n.op)
            if op_type not in SUPPORTED_OPERATORS:
                raise ValueError(f"Unsupported binary operator: {op_type.__name__}")
            if op_type is ast.Div and right == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            # Prevent potential MemoryError or CPU exhaustion with huge powers
            if op_type is ast.Pow:
                if abs(right) > 1000:
                    raise ValueError("Exponent is too large.")
            return SUPPORTED_OPERATORS[op_type](left, right)
        elif isinstance(n, ast.UnaryOp):
            operand = _eval(n.operand)
            op_type = type(n.op)
            if op_type not in SUPPORTED_OPERATORS:
                raise ValueError(f"Unsupported unary operator: {op_type.__name__}")
            return SUPPORTED_OPERATORS[op_type](operand)
        else:
            raise ValueError(f"Unsupported syntax structure: {type(n).__name__}")

    return _eval(node)

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    # 1. Extract parameters from GET or POST requests
    if request.method == 'GET':
        data = request.args
    else:
        data = request.get_json(silent=True) or request.form or {}

    # Check for direct 'expression' or 'expr' field
    expression = data.get('expression') or data.get('expr')

    # If no direct expression, check if legacy parameters are provided
    if not expression:
        num1_raw = data.get('num1') if data.get('num1') is not None else data.get('number1')
        num2_raw = data.get('num2') if data.get('num2') is not None else data.get('number2')
        op_raw = data.get('operation') if data.get('operation') is not None else data.get('operator')
        if op_raw is None:
            op_raw = data.get('op')

        if num1_raw is not None and num2_raw is not None and op_raw is not None:
            # Map the operation name to the corresponding operator symbol
            op_str = str(op_raw).strip().lower()
            if op_str in ('add', 'addition', '+'):
                op_symbol = '+'
            elif op_str in ('subtract', 'subtraction', 'sub', '-'):
                op_symbol = '-'
            elif op_str in ('multiply', 'multiplication', 'mul', '*'):
                op_symbol = '*'
            elif op_str in ('divide', 'division', 'div', '/'):
                op_symbol = '/'
            else:
                return jsonify({"error": f"Invalid operator '{op_raw}'."}), 400
                
            expression = f"({num1_raw}) {op_symbol} ({num2_raw})"
            
    if not expression:
        return jsonify({"error": "Missing parameter. 'expression' or mathematical inputs (num1, num2, operation) are required."}), 400

    # 2. Evaluate the expression safely
    try:
        result = safe_eval(str(expression))
    except ZeroDivisionError as e:
        return jsonify({"error": str(e)}), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to evaluate expression: {str(e)}"}), 400

    # 3. Format result (convert float to int if it's a whole number)
    if isinstance(result, float) and result.is_integer():
        result = int(result)

    return jsonify({"result": result}), 200

if __name__ == '__main__':
    # Running on local port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
