operators = {'+', '-', '*', '/', '(', ')', '^'}
priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
variables = {}
help_text = """
///////////////////////////////////////////////////////////////////////////////////////////
// This program calculates the value of the mathematical expression entered.             //
// Operations like "+", "-", "*", "/" and "^" are supported.                             //
// It also supports in-bracket calculations. Eg. 3 * (5 + 4)                             //
// You can assign numbers and already assigned variables to new variables                //
// You can call the variable to get its value in expression or alone. Eg. a = 5, b = a   //
// In the expression there should be a space between numbers and operators.              //
// Incomplete expressions eg. "4 * (2 + 3 " and multiple operators eg. "+++" and similar //
// will be considered as Invalid expression.                                             //
// Commands like "/exit" will exit program and "/help" will bring this text.             //  
///////////////////////////////////////////////////////////////////////////////////////////
"""


def operate(a, operator, b):
    a = int(a)
    b = int(b)
    if operator == '+':
        return a + b
    if operator == '-':
        return b - a
    if operator == '*':
        return a * b
    if operator == '/':
        return b / a
    if operator == '^':
        return b ** a


def post_fix(expression):
    """

    :type expression: str
    """
    stack = []
    output = ''

    for index, char in enumerate(expression):
        if char not in operators:
            output += char
        elif char == "(":
            stack.append(char)
        elif char == ")":
            while stack and stack[-1] != "(":
                output += f" {stack.pop()}"
            stack.pop()
        elif char == " ":
            continue
        else:
            if expression[index + 1] in operators:
                print("Invalid expression")
            else:
                while stack and stack[-1] != "(" and priority[char] <= priority[stack[-1]]:
                    output += stack.pop()
                stack.append(char)
    while stack:
        output += f" {stack.pop()}"
    return output


def calculate(postfix):
    stack = []
    postfix = list(filter(lambda x: len(x) != 0, postfix.split(" ")))
    for i in postfix:
        if i.isnumeric():
            stack.append(i)
        elif i.isalpha() and i in variables:
            stack.append(variables[i])
        elif i in operators:
            stack.append(operate(stack.pop(), i, stack.pop()))
    return stack[0]


def get_value(var):
    while True:
        try:
            var = variables[var]
        except KeyError:
            break
    return var


if __name__ == "__main__":
    print("!---- Smart Calculator ----!")
    while True:
        get = input("> ").strip()
        if get.startswith("/"):
            if get == '/exit':
                print("Bye!")
                break
            elif get == "/help":
                print(help_text)
            else:
                print("Unknown command")
        elif get == "" or get is None:
            continue
        elif get in variables:
            print(get_value(get))
        elif get.isalpha() and get not in variables:
            print("Unknown variable")
        elif "=" in get:
            variable = list(map(lambda x: x.strip(), get.split("=")))
            if len(variable) > 2:
                print("Invalid identifier")
            elif variable[0].isalpha():
                if variable[1].isalpha() and variable[1] in variables:
                    variables[variable[0]] = variable[1]
                elif variable[1].isnumeric():
                    variables[variable[0]] = variable[1]
                else:
                    print("Invalid identifier")
            else:
                print("Invalid identifier")

        else:
            try:
                print(calculate(post_fix(get)))
            except IndexError:
                print("Invalid expression")
