def encontrar_salas(nombre_archivo):
    archivo=open(nombre_archivo)
    flag=False
    dicc={}
    for linea in archivo:
        if not flag:
            flag=True
        else:
            if "x" in linea:
                lista=linea.strip().split(",")
                flag1=False
                i=1
                j=2
                for hora in lista:
                    if not flag1:
                        sala=hora
                        flag1=True
                        dicc[sala]=[]
                    else:
                        if hora!="x":
                            dicc[sala].append(str(i)+"-"+str(j))
                        i+=2
                        j+=2
    archivo.close()
    return dicc
salida=encontrar_salas("Salas Lunes - Salas F.csv")
print(salida)
                        
                    
                
                
                
                
            
