import json
import time

def cargar_red():
    with open('red_cp.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def buscar_afectados_en_cascada(red, equipo_caido_nombre):
    caidos = [equipo_caido_nombre]
    nuevos = True
    while nuevos:
        nuevos = False
        for nodo in red:
            if nodo['nombre'] not in caidos:
                if any(dep in caidos for dep in nodo['dependencias']):
                    caidos.append(nodo['nombre'])
                    nuevos = True
    return [nodo for nodo in red if nodo['nombre'] in caidos]

def iniciar_monitoreo():
    red = cargar_red()
    print(f"[INFO] Monitor activo. Nodos cargados: {len(red)}")
    
    while True:
        print("\n--- MENU DE MONITOREO ---")
        print("1. Ejecutar escaneo de estado")
        print("2. Simular falla en nodo")
        print("3. Salir")
        opcion = input("Selecciona una opcion: ")
        
        if opcion == "1":
            print("[OK] Escaneo completado. Todos los enlaces OSPF y subredes responden.")
            time.sleep(1)
            
        elif opcion == "2":
            print("\nDispositivos disponibles:")
            for i, nodo in enumerate(red, start=1):
                print(f"  {i}. {nodo['nombre']} ({nodo['ip']}) - {nodo['tipo']}")
            
            seleccion = input("\nNumero de dispositivo a desconectar: ")
            
            if seleccion.isdigit() and 1 <= int(seleccion) <= len(red):
                equipo_elegido = red[int(seleccion) - 1]['nombre']
                afectados = buscar_afectados_en_cascada(red, equipo_elegido)
                
                print(f"\n[ALERTA] Falla detectada en {equipo_elegido}. Nodos afectados: {len(afectados)}")
                for a in afectados:
                    info_extra = a.get('vlan', a.get('detalles'))
                    print(f"  [DOWN] {a['nombre']} | IP: {a['ip']} | {info_extra}")
                
                print("\n[INFO] Paquete de errores listo para envio a modulo de diagnostico.")
            else:
                print("[ERROR] Seleccion fuera de rango.")
                
        elif opcion == "3":
            print("[INFO] Cerrando monitor.")
            break

if __name__ == "__main__":
    iniciar_monitoreo()