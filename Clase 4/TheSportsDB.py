import requests

def buscar_equipo(equipo):
  equipo = equipo.strip().replace(" ", "_")
  url = f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={equipo}"
  try:
    respuesta = requests.get(url)
    respuesta.raise_for_status()
    datos = respuesta.json()
  except requests.exceptions.RequestException as e:
    print(f"Error al realizar la solicitud: {e}")
    return None

  equipos = datos.get("teams") or []
  if not equipos:
    print("No se encontró el equipo.")
    return None

  dato = equipos[0]
  return {
      "Nombre": dato["strTeam"],
      "Fundación": dato["intFormedYear"],
      "Estadio": dato["strStadium"],
      "Liga": dato["strLeague"],
      "Descripción": dato["strDescriptionES"]
  }

if __name__ == "__main__":
    equipo = input("Ingrese el nombre del equipo que desea buscar: ")
    mi_equipo = buscar_equipo(equipo)
    if mi_equipo:
        print(f"El equipo {mi_equipo['Nombre']} fue fundado el año {mi_equipo['Fundación']}, juega en la {mi_equipo['Liga']} y su estadio es el {mi_equipo['Estadio']}")
        print("Una breve descripción del equipo:")
        print(mi_equipo["Descripción"])