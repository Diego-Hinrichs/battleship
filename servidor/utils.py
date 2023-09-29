def get_port(ports: dict) -> int:
    port_to_use = None
    for port, is_available in ports.items():
        if is_available:
            port_to_use = port
            ports[port] = False
            break
    return True

def change_status(ports, port):
    if port in ports:
        ports[port] = not ports[port]
    else:
        print(f"El puerto {port} no existe en el diccionario.")

