import json
from solana.rpc.api import Client

# Configuración del cliente de Solana
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"  # URL del nodo RPC
client = Client(SOLANA_RPC_URL)

def obtener_info_slot(slot_num, cuenta):
    # Obtener información del bloque para el slot
    slot_info = client.get_block(slot_num, encoding='jsonParsed')

    # Verificar si se obtuvo información del slot
    if slot_info is None or slot_info.value is None:
        print("No se pudo obtener información del slot.")
        return None

    # Verificar si la cuenta participó en el slot
    participacion = False
    transacciones_serializables = []

    for transaction in slot_info.value.transactions:
        # Convertir cada transacción en un formato serializable
        instrucciones_serializables = []
        for ix in transaction.transaction.message.instructions:
            # Verificar si la instrucción es del tipo ParsedInstruction
            if hasattr(ix, 'parsed'):
                instrucciones_serializables.append({
                    "program_id": str(ix.program_id),
                    "accounts": ix.parsed['info']['accounts'] if 'accounts' in ix.parsed['info'] else [],
                    "data": str(ix.parsed)  # Serializar todo el contenido parseado si no tiene cuentas
                })
            else:
                # Instrucciones no parseadas
                instrucciones_serializables.append({
                    "program_id": str(ix.program_id),
                    "accounts": [str(account) for account in ix.accounts],
                    "data": str(ix.data)
                })

        transaccion_info = {
            "signatures": [str(sig) for sig in transaction.transaction.signatures],  # Convertir firmas a string
            "account_keys": [str(key) for key in transaction.transaction.message.account_keys],  # Convertir claves a string
            "instructions": instrucciones_serializables  # Instrucciones serializadas
        }
        transacciones_serializables.append(transaccion_info)

        # Verificar si la cuenta participó en esta transacción
        if cuenta in transaccion_info["account_keys"]:
            participacion = True

    # Crear un diccionario con la información del slot
    info_slot = {
        "slot": slot_num,
        "participacion": participacion,
        "transacciones": transacciones_serializables  # Usar la versión serializable de las transacciones
    }

    return info_slot

def guardar_info_json(info_slot, nombre_archivo):
    # Guardar información en formato JSON
    with open(nombre_archivo, 'w') as archivo:
        json.dump(info_slot, archivo, indent=4)
    print(f"Información guardada en {nombre_archivo}")

if __name__ == "__main__":
    slot_num = int(input("Ingrese el número de Slot: "))
    cuenta = input("Ingrese la dirección de la cuenta: ")

    info_slot = obtener_info_slot(slot_num, cuenta)
    if info_slot:
        guardar_info_json(info_slot, f"slot_{slot_num}.json")



