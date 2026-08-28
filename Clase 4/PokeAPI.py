import requests
import pandas as pd
def buscar_pokemon(nombre = input("Introduzca el nombre del pokemon: ")):
  nombre = nombre.lower()
  url = f"https://pokeapi.co/api/v2/pokemon/{nombre}"
  try:
    respuesta = requests.get(url)
    respuesta.raise_for_status()
    datos = respuesta.json()
  except requests.exceptions.RequestException as e:
    print(f"Error al realizar la solicitud: {e}")
  for dato in datos:
    datos_pokemon = []
    datos_pokemon.append({
        "Nombre": datos["name"],
        "Altura": datos["height"],
        "Peso": datos["weight"],
        "Tipo1": datos["types"][0]["type"]["name"],
        "Tipo2": datos["types"][1]["type"]["name"] if len(datos["types"]) > 1 else "N/A",
        "Vida": datos["stats"][0]["base_stat"],
        "Ataque": datos["stats"][1]["base_stat"],
        "Defensa": datos["stats"][2]["base_stat"],
        "Ataque Especial": datos["stats"][3]["base_stat"],
        "Defensa Especial": datos["stats"][4]["base_stat"],
        "Velocidad": datos["stats"][5]["base_stat"],
    })
  datos_pokemon = pd.DataFrame(datos_pokemon)
  return datos_pokemon
if __name__ == "__main__":
    mi_pokemon = buscar_pokemon()
    pokemon = mi_pokemon.iloc[0]
    print("\n" + "=" * 36)
    print(f"Información de {pokemon['Nombre'].title()}")
    print("=" * 36)
    for atributo, valor in pokemon.items():
        print(f"{atributo:<18}: {valor}")
    print("=" * 36)