import json

departamentos = [
    {"nombre": "Estadistica", "octeto": 1},
    {"nombre": "Fitologia", "octeto": 2},
    {"nombre": "Almacen", "octeto": 3},
    {"nombre": "Biologia", "octeto": 4},
    {"nombre": "U_C", "octeto": 5}
]

red_total = [
    {
        "id": "CORE-L3",
        "nombre": "Switch-Capa-3",
        "tipo": "Switch-L3",
        "ip": "10.0.0.1",
        "detalles": "Núcleo central - Enlaces Gig1/0/x - OSPF Area 0",
        "dependencias": []
    },
    {
        "id": "RTR-GOBIERNO",
        "nombre": "Router-de-Gobierno",
        "tipo": "Router",
        "ip": "10.0.0.2",
        "detalles": "Gateway exterior y Servidor DHCP Centralizado",
        "dependencias": ["Switch-Capa-3"]
    }
]

for dep in departamentos:
    x = dep["octeto"]
    rtr_nombre = f"Router-{dep['nombre']}"
    
    red_total.append({
        "id": f"RTR-{dep['nombre'].upper()}",
        "nombre": rtr_nombre,
        "tipo": "Router",
        "ip": f"10.0.0.{10 + x}",
        "detalles": "Gig0/0/0 | Subinterfaces .10, .20, .30 (dot1Q) | DHCP Relay + OSPF",
        "dependencias": ["Switch-Capa-3"]
    })
    
    sw_nombre = f"Switch-{dep['nombre']}-Acceso"
    red_total.append({
        "id": f"SW-{dep['nombre'].upper()}",
        "nombre": sw_nombre,
        "tipo": "Switch-L2",
        "ip": f"192.168.{x}.2",
        "detalles": "Trunk en fa0/1-3",
        "dependencias": [rtr_nombre]
    })
    
    vlans = [
        {"vlan": "VLAN 10", "ip": f"192.168.{x}.10/25", "puertos": "fa0/2-6", "tipo": "Host-Trabajadores"},
        {"vlan": "VLAN 20", "ip": f"192.168.{x}.130/26", "puertos": "fa0/7-11", "tipo": "Host-Estudiantes"},
        {"vlan": "VLAN 30", "ip": f"192.168.{x}.194/29", "puertos": "fa0/12-17", "tipo": "Impresora"}
    ]
    
    for v in vlans:
        red_total.append({
            "id": f"{v['tipo']}-{dep['nombre']}",
            "nombre": f"Equipo-{v['vlan'].replace(' ', '')}-{dep['nombre']}",
            "tipo": v["tipo"],
            "ip": v["ip"],
            "vlan": f"{v['vlan']} (Puertos {v['puertos']})",
            "dependencias": [sw_nombre]
        })

with open('red_cp.json', 'w', encoding='utf-8') as f:
    json.dump(red_total, f, indent=4, ensure_ascii=False)

print(" 'red_cp.json' generado con éxito.")