
# =====================================================================
# ACT 3: PATRONES DE DISEÑO PARA OPTIMIZAR NAVEGACIÓN
# =====================================================================

# --- 1. PATRÓN STRATEGY (Filtrado Inteligente en Base de Datos) ---
class FiltroStrategy:
    def filtrar(self, queryset, valor_busqueda):
        pass

class FiltroHistoriasInteligente(FiltroStrategy):
    def filtrar(self, queryset, valor_busqueda):
        if valor_busqueda:
            # Buscamos en las tablas relacionadas (Paciente e Ingreso)
            return queryset.filter(
                Q(Pacientes_idPacientesDoc__idPacientesDoc__icontains=valor_busqueda) |
                Q(Pacientes_idPacientesDoc__Nombre__icontains=valor_busqueda) |
                Q(Pacientes_idPacientesDoc__Apellido__icontains=valor_busqueda) |
                Q(ingresosPacientes_idingresosPacientes__estudio1__icontains=valor_busqueda) |
                Q(ingresosPacientes_idingresosPacientes__sede__icontains=valor_busqueda)
            )
        return queryset

# --- 2. PATRÓN ITERATOR (Recorrido Óptimo por Fragmentos) ---
class IteradorHistorias:
    def __init__(self, queryset, start, length):
        # Evita error si length es -1 (mostrar todos)
        length = length if length > 0 else queryset.count()
        self.paginator = Paginator(queryset, length)
        # DataTables envía "start" (índice 0, 10, 20...), calculamos la página (1, 2, 3...)
        self.numero_pagina = (int(start) // int(length)) + 1

    def obtener_bloque(self):
        return self.paginator.page(self.numero_pagina).object_list

# =====================================================================
# VISTA OPTIMIZADA (Server-Side Processing)
# =====================================================================
@login_required    
def historias_clinicas(request):
    try:
        # 1. Recibir parámetros de DataTables
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')

        # 2. Obtener QuerySet base (Aún no ejecuta SQL, solo prepara la consulta)
        historias_base = HistoriaClinica.objects.all().order_by('-idhistoriaClinica')
        records_total = historias_base.count()

        # 3. Aplicar Patrón Strategy para Filtrar
        estrategia = FiltroHistoriasInteligente()
        historias_filtradas = estrategia.filtrar(historias_base, search_value)
        records_filtered = historias_filtradas.count()

        # 4. Aplicar Patrón Iterator para Paginar (Solo trae de SQL los 10 registros necesarios)
        iterador = IteradorHistorias(historias_filtradas, start, length)
        historias_bloque = iterador.obtener_bloque()

        # 5. Formatear la respuesta JSON (Igual que tu código original, pero optimizado)
        data_list = []
        for historia in historias_bloque:
            ingreso = historia.ingresosPacientes_idingresosPacientes
            paciente = historia.Pacientes_idPacientesDoc

            if ingreso:
                archivo_adjunto = historia.Adicionales if historia.Adicionales else None
                archivo_url = None
                if archivo_adjunto:
                    archivo_url = generar_token_seguro(archivo_adjunto, request.user.id)

                data_list.append({
                    'ID': historia.idhistoriaClinica,
                    'ID Ingreso': ingreso.idingresosPacientes,
                    'Fecha': ingreso.fechaIngreso.strftime('%Y-%m-%d %H:%M:%S'),
                    'Cedula': paciente.idPacientesDoc,
                    'Paciente': paciente.nombre_completo(),
                    'Estudio': ingreso.estudio1,
                    'Sede': ingreso.sede,
                    'Archivo': archivo_url,
                    'estado_archivo': historia.estado_archivo
                })

        # Estructura JSON estricta que exige DataTables Server-Side
        return JsonResponse({
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data_list
        })

    except ObjectDoesNotExist:
        return JsonResponse({'error': 'No hay registros de historias clínicas'}, status=404)
    except Exception as e:
        # Imprime el error en la consola si algo falla para facilitar correcciones
        print(f"Error en historias_clinicas: {e}") 
        return JsonResponse({'error': str(e)}, status=500)
