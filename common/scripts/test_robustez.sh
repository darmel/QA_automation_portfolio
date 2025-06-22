#!/usr/bin/env bash
# ------------------------------------------------------------------
#  robustez.sh – Ejecuta una suite pytest N veces y contabiliza
#                PASSED / FAILED / ERROR por cada test.
#  Uso: ./robustez.sh <argumento para pytest> [iteraciones]
# ------------------------------------------------------------------

set -euo pipefail
set +o pipefail

#hora de inicio
START_TIME=$(date +%s)

# --------- Validación de argumentos ----------
if [[ $# -lt 1 ]]; then
  echo "Uso: $0 <carpeta_de_tests> [runs]"
  exit 1
fi

SUITE="$1"
echo "$SUITE"
RUNS="${2:-100}"                   # por defecto 100 iteraciones
OUTFILE="resultados_robustez_${SUITE//\//_}.txt"

# --------- Diccionarios para contadores ----------
declare -A PASSED_COUNT
declare -A FAILED_COUNT
declare -A ERROR_COUNT

# --------- Función helper para imprimir tabla ----------
print_table () {
  printf '%-110s %7s %7s %7s\n' "Test" "PASSED" "FAILED" "ERROR"
  printf -- '%.0s-' {1..115}; echo

  for t in "${!PASSED_COUNT[@]}" "${!FAILED_COUNT[@]}" "${!ERROR_COUNT[@]}"; do :; done # expandir arrays

  for test in "${!PASSED_COUNT[@]}"; do
    printf '%-110s %7d %7d %7d\n' \
      "$test" \
      "${PASSED_COUNT[$test]:-0}" \
      "${FAILED_COUNT[$test]:-0}" \
      "${ERROR_COUNT[$test]:-0}"
  done | sort -k3 -r -k4 -r
}

echo "🔁  Ejecutando suite '${SUITE}' ${RUNS} veces"
echo "——————————————————————————————————————————————————————————————"

for ((i = 1; i <= RUNS; i++)); do
  echo -e "\n# Iteración $i / $RUNS"

  TMP=$(mktemp)
# mostrar salida en runtime y gudarla en TMP, sin salir del bucle for

  eval "python -m pytest $SUITE -rA | tee \"$TMP\" || true"


# Debug muestra el contenido de TMP
#  echo -e "\n# Contenido del resumen (TMP):"
# grep -E '^(PASSED|FAILED|ERROR) ' "$TMP" || echo "(sin resumen encontrado)"

  # Procesar líneas del resumen corto
  # wrap this part with {} in order to avoid abortion due to errors inside the while
    {
      while read -r status rest; do
        [[ "$status" =~ ^(PASSED|FAILED|ERROR)$ ]] || continue
        #test_name="$rest"
        test_name=$(awk '{print $2}' <<< "$status $rest")


        : "${PASSED_COUNT["$test_name"]:=0}"
        : "${FAILED_COUNT["$test_name"]:=0}"
        : "${ERROR_COUNT["$test_name"]:=0}"

        case "$status" in
          PASSED) ((PASSED_COUNT["$test_name"]++)) ;;
          FAILED) ((FAILED_COUNT["$test_name"]++)) ;;
          ERROR)  ((ERROR_COUNT["$test_name"]++)) ;;
        esac


      done
    } < <(grep -E '^(PASSED|FAILED|ERROR) ' "$TMP") || true

        echo -e "\n # Estado parcial tras $i ejecuciones"
        print_table

  rm -f "$TMP"
done

#hora de finalizacion
END_TIME=$(date +%s)

#calcular duracion
DURATION_S=$((END_TIME - START_TIME))

#calcular min y seg
DURATION_MIN=$((DURATION_S / 60))
DURATION_SEC=$((DURATION_S % 60))


# --------- Resumen final en pantalla ----------
echo -e "\n ###--- Resumen de robustez – ${RUNS} ejecuciones ---###"
print_table
#duracion:
echo ""
echo "Duración total: $DURATION_MIN min $DURATION_SEC seg"

# --------- Guardar a archivo ----------
{
  echo "Resumen de robustez – suite: ${SUITE} – ejecuciones: ${RUNS}"
  echo
  print_table
  echo ""
  echo "Duración total: $DURATION_MIN min $DURATION_SEC seg"
} > "$OUTFILE"

echo -e "\n# Resultado guardado en: $OUTFILE"
