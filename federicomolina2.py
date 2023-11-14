import mysql.connector

conex = mysql.connector.connect(# conecta python con mysql
    host = "localhost",
    user = "root",
    password = "",
    port = "3306",
    database = "cajero_automatico",
)
conexion = conex.cursor()

def crear_usuario():
    try:
        while True:
            try:
                num_usuario = int(input("Ingrese su usuario: "))
                conexion.execute('SELECT * FROM cajero_automatico.usuario WHERE num_usuario = %s', (num_usuario,))
                result_usuario = conexion.fetchone()#trae el registro de la base de datos
                if result_usuario is not None:
                    print(f'El usuario {num_usuario} ya existe')
                else:
                    break
            except:
                print("Debe ingresar numeros")
        while True:
            contraseña = input("Ingrese su contraseña o PIN: ")
            if 3 < len(contraseña) < 5:
                break
            else:
                print("La contraseña debe tener 10 o mas caracteres")
        while True:
            nombre = input("Ingrese su nombre: ")
            if nombre.isalpha() and nombre !="":
                break
            else:
                print("Debe ingresar su nombre")
        while True:
            apellido = input("Ingrese su apellido: ")
            if apellido.isalpha() and apellido !="":
                break
            else:
                print("Debe ingresar su apellido")
        while True:
            cuil = input("Ingrese su cuil: ")
            if cuil.isdigit() and len(cuil) <=11:
                break
            else:
                print("Dato incorrecto.")
        direccion = input("Ingrese su direccion: ")
        while True:            
            try:
                dni = int(input("Ingrese su dni: "))
                conexion.execute('SELECT id_clientes FROM cajero_automatico.clientes WHERE dni = %s', (dni,))
                result = conexion.fetchone()#trae el registro de la base de datos
                if 10000000 <= dni <= 99999999:
                    if result is not None:
                        # El cliente ya existe, obtén su ID
                        id_clientes = result[0]
                    else:
                        # El cliente no existe, créalo y obtén su ID
                        conexion.execute("INSERT INTO cajero_automatico.clientes (nombre, direccion, apellido, dni, cuil) VALUES (%s, %s, %s, %s, %s)", (nombre, direccion, apellido, dni, cuil))
                        id_clientes = conexion.lastrowid
                        conex.commit()

                # Inserta el nuevo usuario asociado al ClienteID
                conexion.execute("INSERT INTO cajero_automatico.usuario (num_usuario, contraseña, id_clientes, saldo) VALUES (%s, %s, %s, %s)", (num_usuario, contraseña, id_clientes, 50000))
                conex.commit()
                print("El usuario ha sido creado correctamente!")
                break
            except ValueError:
                print("El DNI debe contener entre 7 y 8 dígitos. Intenta de nuevo.")
        
    except ValueError:
        print("El dato ingresado es incorrecto")
    


def ingreso():
    while True:
        try:
            num_usuario = int(input("Ingrese su numero de usuario o para volver ingrese 0: "))
            if num_usuario == 0:
                break
            contraseña = input("Ingrese su contraseña: ")
            conexion.execute("SELECT * FROM cajero_automatico.usuario WHERE num_usuario = %s AND contraseña = %s", (num_usuario, contraseña))
            resultado = conexion.fetchone()
            if resultado is not None:
                print("Acceso concedido. ¡Bienvenido!")
                while True:
                    print("""a. Consulta de saldo  
b. Retiro de dinero 
c. Depósito de efectivo
d. Consulta últimas diez operaciones 
e. Volver
                        """)
                    opcion = input("Ingrese la operacion a realizar: ").lower()
                    if opcion =="a":
                        conexion.execute ("SELECT saldo FROM cajero_automatico.usuario WHERE num_usuario = %s AND contraseña = %s", (num_usuario, contraseña))
                        resultad = conexion.fetchone()
                        print(f"Su saldo es: {resultad}")
                    elif opcion =="b":
                        while True:
                            try:
                                conexion.execute ("SELECT saldo FROM cajero_automatico.usuario WHERE num_usuario = %s AND contraseña = %s", (num_usuario, contraseña))
                                resultad_retiro = conexion.fetchone()
                                resultad_retiro = resultad_retiro[0]
                                print("""a. $1.000 
b. $5.000 
c. $10.000 
d. $20.000 
e. Otro monto 
f. Volver al menú anterior""")
                                opc=input("Ingrese la opcion: ")
                                if opc == "a" and 1000 <= resultad_retiro:
                                    conexion.execute("UPDATE cajero_automatico.usuario SET saldo = saldo - %s WHERE num_usuario = %s AND contraseña = %s", (1000, num_usuario, contraseña))
                                    print("Operacion exitosa!")
                                    conex.commit()
                                elif opc == "b" and 5000 <= resultad_retiro:
                                    conexion.execute("UPDATE cajero_automatico.usuario SET saldo = saldo - %s WHERE num_usuario = %s AND contraseña = %s", (5000, num_usuario, contraseña))
                                    print("Operacion exitosa!")
                                    conex.commit()
                                elif opc == "c" and 10000 <= resultad_retiro:
                                    conexion.execute("UPDATE cajero_automatico.usuario SET saldo = saldo - %s WHERE num_usuario = %s AND contraseña = %s", (10000, num_usuario, contraseña))
                                    print("Operacion exitosa!")
                                    conex.commit()
                                elif opc == "d" and 20000 <= resultad_retiro:
                                    conexion.execute("UPDATE cajero_automatico.usuario SET saldo = saldo - %s WHERE num_usuario = %s AND contraseña = %s", (20000, num_usuario, contraseña))
                                    print("Operacion exitosa!")
                                    conex.commit()
                                elif opc =="e":
                                    retirar = int(input("Ingrese el monto a retirar: "))
                                    if retirar <= resultad_retiro:
                                        conexion.execute("UPDATE cajero_automatico.usuario SET saldo = saldo - %s WHERE num_usuario = %s AND contraseña = %s", (retirar, num_usuario, contraseña))
                                        print("Operacion exitosa!")
                                        conex.commit()
                                    else:
                                        print("No tiene ese monto!")
                                elif opc == "f":
                                    break
                                else:
                                    print("No tiene ese monto!")
                            except:
                                print("Error: debe ingresar numeros")
                    elif opcion =="c":
                        pass
                    elif opcion =="d":
                        pass
                    elif opcion =="e":
                        break
                    else:
                        print("La opcion ingresada es incorrecta")
            else:
                print("Usuario o contraseña incorrectos. Inténtelo nuevamente.")
                print("Para salir ingrese 0")
        except ValueError:
            print("El dato ingresado es incorrecto. Debe ingresar un número como usuario.")
            



while True:
    print("""a. Ingresar b. Crear nuevo cliente c. Salir""")
    opcionn = input("Ingrese la opcion a realizar: ").lower()
    if opcionn == "a":
        ingreso()
    elif opcionn == "b":
        crear_usuario()
        conex.commit()
    elif opcionn == "c":
        print("Hasta luego!")
        break
    else:
        print("La opcion ingresada no es valida")
        
        
        
conexion.close()



"""conexion.execute("SELECT * FROM cajero_automatico.clientes WHERE usuario = %s AND contraseña = %s", (usuario, contraseña))
resultados = conexion.fetchall()
# Imprime cada resultado
for resultad in resultados:
    print(resultad)
    
    
    else:
            print("El dato ingresado es incorrecto")
                if 10000000 <= dni <=99999999:
                    if result is not None:
                        # El cliente ya existe, obtén su ID
                        cliente_id = result_cliente[0]
                    else:
                        conexion.execute("INSERT INTO cajero_automatico.clientes (nombre, direccion, apellido, dni, cuil) VALUES (%s, %s, %s, %s, %s)",(nombre, direccion, apellido, dni, cuil))
                        conexion.execute("INSERT INTO cajero_automatico.usuario (num_usuario, contraseña, saldo) VALUES (%s, %s, %s)",(num_usuario,contraseña,50000))
                        print("El usuario a sido creado correctamente!")
                        conex.commit()
                        # Esto confirma los cambios en la base de datos
                        # Esto cierra la conexión
                        break
                else:
                    print("El dato ingresado es incorrecto")
            except ValueError:
                print("El DNI debe contener entre 7 y 8 dígitos. Intenta de nuevo.")"""
