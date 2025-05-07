'''
Desarrollado por:
- Alyson Melissa Sánchez Serratos
- Miguel Ángel Pérez Ávila

Fecha de realización: 04/04/2024
'''

global token_tipo, variables
token_tipo = {'operacion':["+", "-", "*", "/", "^"]
                }
variables=[]

output_tokens=[]
output_types=[]

error=[]



#/////////////////// Tools

#Registrar output -> "Token":"Evento"
def write_output(token, tipo):
    output_tokens.append(token)
    output_types.append(tipo)


#/////////////////// Estados



# char ∈ { 0-9 } -> Estado Número Entero
def qNumeroEntero(cad, concat_entero):
    
    if(cad == "\n" or cad==""):
       write_output(concat_entero, "Entero")
       qTerminal()
    else:
        char = cad[0]

        if(char.isnumeric()):
            concat_entero+=char
            qNumeroEntero(cad[1:],concat_entero)
        elif(char == "."):
            concat_entero+=char
            qNumeroReal(cad[1:], concat_entero)
        elif(char in token_tipo.get('operacion')):
            write_output(concat_entero, "Entero")
            if(char=="+"):
                qSuma(cad[1:])
            if(char=="-"):
                qResta(cad[1:])
            if(char=="*"):
                qMultiplicacion(cad[1:])
            if(char=="/"):
                qDivision(cad[1:])
            if(char=="^"):
                qPotencia(cad[1:])
        elif(char == ")"):
            write_output(concat_entero, "Entero")
            qParentesisC(cad[1:])
        else:
            error.append("Error en estado: qNumeroEntero, símbolo: "+char+" incomprensible para valor Entero.")
        
   
# char ∈ { "." } -> Estado Número Real
def qNumeroReal(cad, concat_real):

    if(cad == "\n" or cad==""):
       write_output(concat_real, "Entero")
       qTerminal()
    else:
        char = cad[0]

        if(char.isnumeric()):
            concat_real+=char
            qNumeroReal(cad[1:], concat_real)
        elif(char == "E" or char == "e"):
            concat_real+=char
            qNumeroPositivoExponencial(cad[1:], concat_real)
        elif(char in token_tipo.get('operacion')):
            write_output(concat_real, "Real")
            if(char=="+"):
                qSuma(cad[1:])
            if(char=="-"):
                qResta(cad[1:])
            if(char=="*"):
                qMultiplicacion(cad[1:])
            if(char=="/"):
                qDivision(cad[1:])
            if(char=="^"):
                qPotencia(cad[1:])
        elif(char == ")"):
            write_output(concat_real, "Real")
            qParentesisC(cad[1:])
        else:
            error.append("Error en estado: qNumeroReal, símbolo: "+char+" incomprensible para valor Real.")


# char ∈ { .E | .e } -> Estado Número Real
def qNumeroPositivoExponencial(cad, concat_pos_exp):
    char= cad[0]

    if(char.isnumeric() or char=="-"):
        concat_pos_exp+=char
        qEntero_exp(cad[1:], concat_pos_exp)
    else:
        error.append("Error en estado: qNumeroPositivoExponencial, símbolo: "+char+" incomprensible para valor Real Exponencial")

# 
def qEntero_exp(cad, concat):
    if(cad == "\n" or cad==""):
       write_output(concat, "Real")
       qTerminal()
    else:
        char= cad[0]

        if(char.isnumeric()):
            concat+=char
            qEntero_exp(cad[1:], concat)
        elif(char in token_tipo.get('operacion')):
            write_output(concat, "Real")
            if(char=="+"):
                qSuma(cad[1:])
            if(char=="-"):
                qResta(cad[1:])
            if(char=="*"):
                qMultiplicacion(cad[1:])
            if(char=="/"):
                qDivision(cad[1:])
            if(char=="^"):
                qPotencia(cad[1:])
        elif(char == ")"):
            write_output(concat, "Real")
            qParentesisC(cad[1:])
        else:
            error.append("Error en estado: qEntero_exp, símbolo: "+char+" incomprensible para valor Real Exponencial")

    

#---

# char = "-" -> Estado Signo Negativo
def qSignoNegativo(cad):
    #cad no incluye signo "-"
    char= cad[0]
    
    if(char.isnumeric()):
        qNumeroEntero(cad, "-")
    elif(char.isalpha()):
        qVariable(cad, "-")
    elif(char == "("):
        write_output("-", "Resta.")
        qParentesisA(cad[1:])
    else:
        error.append("Error en estado: qSignoNegativo, uso de signo negativo incorrecto para: "+char)


#---


# char = "(" -> Estado Parentesis Abre
def qParentesisA(cad):
    #cad llega con el puto parentesis
    write_output("(", "Paréntesis que Abre.")
    char= cad[0]

    if(char.isnumeric()):
        qNumeroEntero(cad[1:], char)
    elif(char.isalpha()):
        qVariable(cad[1:], char)
    elif(char == "-"):
        qSignoNegativo(cad[1:])
    elif(char == "("):
        qParentesisA(cad[1:])
    else:
        error.append("Error en estado: qParentesisA, operación incomprensible: "+char)

    

# char = ")" -> Estado Parentesis Cierra
def qParentesisC(cad):
    write_output(")", "Paréntesis que Cierra.")

    if(cad == "\n" or cad == ""):
       qTerminal()
    else:
        char= cad[0]

        if(char in token_tipo.get('operacion')):
            if(char=="+"):
                qSuma(cad[1:])
            if(char=="-"):
                qResta(cad[1:])
            if(char=="*"):
                qMultiplicacion(cad[1:])
            if(char=="/"):
                qDivision(cad[1:])
            if(char=="^"):
                qPotencia(cad[1:])
        elif(char == ")"):
            qParentesisC(cad[1:])
        else:
            error.append("Error en estado: qParentesisC, operación incomprensible: "+char)
   


#---


# char = "+" -> Estado Suma
def qSuma(cad):
    write_output("+", "Suma")
    char= cad[0]

    if(char.isnumeric()):
        qNumeroEntero(cad[1:], char)
    elif(char.isalpha()):
        qVariable(cad[1:], char)
    elif(char == "("):
        qParentesisA(cad[1:])
    else:
        error.append("Error en estado: qSuma, operando de Suma inválido : "+char)

    
# char = "-" -> Estado Resta
def qResta(cad):
    write_output("-", "Resta")
    char= cad[0]
    
    if(char.isnumeric()):
        qNumeroEntero(cad[1:], char)
    elif(char.isalpha()):
        qVariable(cad[1:], char)
    elif(char == "("):
        qParentesisA(cad[1:])
    else:
        error.append("Error en estado: qResta, operando de Resta inválido : "+char)
    

# char = "*" -> Estado Multiplicación
def qMultiplicacion(cad):
    write_output("*", "Multiplicación")
    char= cad[0]
    
    if(char.isnumeric()):
        qNumeroEntero(cad[1:], char)
    elif(char.isalpha()):
        qVariable(cad[1:], char)
    elif(char == "("):
        qParentesisA(cad[1:])
    else:
        error.append("Error en estado: qMultiplicacion, operando de Multiplicacion inválido : "+char)


# char = "/" -> Estado División
def qDivision(cad):
    char= cad[0]
    
    if(char.isnumeric()):
        write_output("/", "División")
        qNumeroEntero(cad[1:], char)
    elif(char.isalpha()):
        write_output("/", "División")
        qVariable(cad[1:], char)
    elif(char == "("):
        write_output("/", "División")
        qParentesisA(cad[1:])
    elif(char == "/"):
        qComentario(cad[1:], "//")
    else:
        error.append("Error en estado: qDivision, operando de División inválido : "+char)
    

# char = "^" -> Estado Potencia
def qPotencia(cad):
    write_output("^", "Potencia")
    char= cad[0]
    
    if(char.isnumeric()):
        qNumeroEntero(cad[1:], char)
    elif(char.isalpha()):
        qVariable(cad[1:], char)
    elif(char == "("):
        qParentesisA(cad[1:])
    else:
        error.append("Error en estado: qPotencia, operando de Potencia inválido : "+char)
   

def qConstructorComentario(cad, concat):
    char= cad[0]

    if(concat == "//"): #Viene de qDivisión
        concat+=char
        qComentario(cad[1:], concat)
    else:
        if(char=="/"):
            concat+=char
            qComentario(cad[1:], concat)
        else:
            error.append("Error en estado: QConstructorComentario, error al comenzar comentario.")
        

def qComentario(cad, concat):
    if(cad == "\n" or cad==""):
       concat= concat.replace("@"," ")
       write_output(concat, "Comentario")
       qTerminal()
    else:
        char=cad[0]
        concat+=char
        qComentario(cad[1:], concat)


def qTerminal():
    #write_output("salto de linea", "TERMINAL ---")
    pass
    


# char = "=" -> Estado Asignación
def qVarAsignacion(cad):
    write_output("=", "Asignación")
    char =cad[0] #Caracter actual

    if(char == "-"):
        qSignoNegativo(cad[1:])
    elif(char.isalpha()):
        qVariable(cad[1:], char)
    elif(char.isnumeric()):
        qNumeroEntero(cad[1:], char)
    elif(char == "("):
        qParentesisA(cad[1:])
    else:
        error.append("Error en estado: QVarAsignación, variable no reconocida o con errores de sintáxis")
        

# char ∈ { a-z | A-Z | "_" | 0-9 } -> Estado Variable
def qVariable(cad, concat_var):
    if(cad == "\n" or cad==""):
       write_output(concat_var, "Variable")
       qTerminal()
    else:

        char =cad[0] #Caracter actual

        if(char.isalpha() or char.isnumeric() or char=="_"):
            concat_var+=char
            qVariable(cad[1:], concat_var)

        elif(char=="="):
            if(concat_var not in variables):
                variables.append(concat_var)
            write_output(concat_var, "Variable")
            qVarAsignacion(cad[1:])

        elif(char in token_tipo.get('operacion')):
            if(concat_var in variables):
                write_output(concat_var, "Variable")
                if(char=="+"):
                    qSuma(cad[1:])
                if(char=="-"):
                    qResta(cad[1:])
                if(char=="*"):
                    qMultiplicacion(cad[1:])
                if(char=="/"):
                    qDivision(cad[1:])
                if(char=="^"):
                    qPotencia(cad[1:])
            else:
                error.append("Error en estado: QVariable, variable: '"+concat_var+"' indefinida")
        
        elif(char == ")"):
            if(concat_var in variables):
                write_output(concat_var, "Variable")
                qParentesisC(cad[1:])
            else:
                error.append("Error en estado: QVariable, variable: '"+concat_var+"' indefinida")
        
        else:
            error.append("Error en estado: QVariable, variable no reconocida o con errores de sintáxis")

            
def q0(cad):
    char =cad[0] #Caracter actual

    if(cad == "\n" or cad==""):
       qTerminal()
    else:
        if(char.isalpha()): 
            qVariable(cad[1:], char) # char ∈ {a-z} -> Estado Variable
        elif(char.isnumeric()):
            qNumeroEntero(cad[1:], char) # char ∈ {0-9} -> Estado Número Entero
        elif(char == "-"):
            qSignoNegativo(cad[1:]) # char = "-" -> Estado Signo Negativo
        elif(char == "/"):
            qConstructorComentario(cad[1:], char) # char = "/" -> Estado Comentario
        elif(char == "("):
            qParentesisA(cad[1:]) # char = "(" -> Estado Parentesis Abre
        else:
            error.append("Error en estado: Q0, no se puede iniciar la línea con: "+char)
    



#///////////////////////////////

def lexerAritmetico(file):
    
    #Lectura de archivo.txt en modo lectura
    arch= open(file, "r")
    lines= arch.readlines()

    #Iteración para análisis por línea
    for line in lines:
        
        ind= line.find("//")
        comments= line[ind:]
        comments= comments.replace(" ","@")
        line=line[0:ind]+comments
        
        #Remplazo de espacios (" " -> "")
        line=line.replace(" ","")
        q0(line)
    
    
    if(len(error)==0):
        #Validación parentesis
        pA=0
        pC=0
        for i in output_types:
            if(i == "Paréntesis que Abre."):
                pA+=1
            if(i == "Paréntesis que Cierra."):
                pC+=1

        if(pA!=pC):
            print("Error, Inconsistencia en el uso de Paréntesis...")
        else:   
            #Impresión de SALIDAS
            print("Token   |   Tipo")
            print("==============================================")
            for i,j in zip(output_tokens, output_types):
                print(i,"         ", j)
    else:
        for err in error:
            print(err)
    print("\n")

    '''
    print("=======   Variables:  =======")
    for var in variables:
        print(var)
    
    '''
    

print("\n"*45)
file= "input.txt"
lexerAritmetico(file)
