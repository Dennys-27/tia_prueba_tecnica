from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import login, VentasForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'dashboard/index.html')

@login_required
def categorias(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT Category FROM superstore_data")
        categorias = [row[0] for row in cursor.fetchall()]

    return JsonResponse(categorias, safe=False)


@login_required
def subcategorias(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT sub_category FROM superstore_data")
        sub_categorias = [row[0] for row in cursor.fetchall()]

    return JsonResponse(sub_categorias, safe=False)

@login_required
def subcategorias(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT sub_category FROM superstore_data")
        sub_categorias = [row[0] for row in cursor.fetchall()]

    return JsonResponse(sub_categorias, safe=False)

@login_required
def estado(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT state FROM superstore_data")
        estado = [row[0] for row in cursor.fetchall()]

    return JsonResponse(estado, safe=False)

@login_required
def ciudad(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT city FROM superstore_data")
        ciudad = [row[0] for row in cursor.fetchall()]

    return JsonResponse(ciudad, safe=False)


# FUNCION PRONCIPAL PARA OBTENER LOS DATOS DEL DASHBOARD
@login_required
def get_datos(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    categoria = request.GET.get('categoria')
    subcategoria = request.GET.get('subcategoria')
    estado = request.GET.get('estado')
    ciudad = request.GET.get('ciudad')

    where = []
    params = []

    if fecha_inicio and fecha_fin:
        if fecha_fin < fecha_inicio:
            return JsonResponse({'error': 'La fecha fin debe ser mayor o igual a la fecha inicio'}, status=400)
        where.append("Order_Date BETWEEN %s AND %s")
        params += [fecha_inicio, fecha_fin]

    if categoria:
        where.append("Category = %s")
        params.append(categoria)

    if subcategoria:
        where.append("Sub_Category = %s")
        params.append(subcategoria)

    if estado:
        where.append("State = %s")
        params.append(estado)

    if ciudad:
        where.append("City = %s")
        params.append(ciudad)

    filtro = " AND ".join(where)
    if filtro:
        filtro = "WHERE " + filtro

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT SUM(Sales) FROM superstore_data {filtro}", params)
        total_ventas = cursor.fetchone()[0] or 0


        cursor.execute(f"SELECT COUNT(Sales) FROM superstore_data {filtro}", params)
        numeber_ventas = cursor.fetchone()[0] or 0


        cursor.execute(f"""
            SELECT Segment, SUM(Sales)
            FROM superstore_data {filtro}
            GROUP BY Segment
        """, params)
        ventas_segmento = [{'segmento': row[0], 'ventas': row[1]} for row in cursor.fetchall()]



        cursor.execute(f"""
            SELECT Segment, COUNT(Sales)
            FROM superstore_data {filtro}
            GROUP BY Segment
        """, params)
        ventas_segmento_number_ventas = [{'segmento': row[0], 'ventas': row[1]} for row in cursor.fetchall()]

        cursor.execute(f"""
            SELECT Customer_Name, Segment, City, State, SUM(Sales) as total
            FROM superstore_data {filtro}
            GROUP BY Customer_Name, Segment, City, State
            ORDER BY total DESC
            LIMIT 10
        """, params)
        top_clientes = [
            {
                'cliente': row[0],
                'segmento': row[1],
                'ciudad': row[2],
                'estado': row[3],
                'total': row[4]
            }
            for row in cursor.fetchall()
        ]

        cursor.execute(f"""
            SELECT Product_ID, Category, Sub_Category, Product_Name, COUNT(*) as vendidos
            FROM superstore_data {filtro}
            GROUP BY Product_ID, Category, Sub_Category, Product_Name
            ORDER BY vendidos DESC
            LIMIT 20
        """, params)
        top_productos = [
            {
                'producto_id': row[0],
                'categoria': row[1],
                'subcategoria': row[2],
                'nombre': row[3],
                'vendidos': row[4]
            }
            for row in cursor.fetchall()
        ]

        cursor.execute(f"""
            SELECT Order_Date, SUM(Sales)
            FROM superstore_data {filtro}
            GROUP BY Order_Date
            ORDER BY Order_Date
        """, params)
        linea_tiempo = [{'fecha': row[0], 'ventas': row[1]} for row in cursor.fetchall()]

        cursor.execute(f"""
            SELECT Category, SUM(Sales)
            FROM superstore_data {filtro}
            GROUP BY Category
        """, params)
        barras_categoria = [{'categoria': row[0], 'ventas': row[1]} for row in cursor.fetchall()]


        cursor.execute(f"""
            SELECT Order_Date, COUNT(Sales)
            FROM superstore_data {filtro}
            GROUP BY Order_Date
            ORDER BY Order_Date
        """, params)
        linea_tiempo_ventas_number = [{'fecha': row[0], 'ventas': row[1]} for row in cursor.fetchall()]

        cursor.execute(f"""
            SELECT Category, COUNT(Sales)
            FROM superstore_data {filtro}
            GROUP BY Category
        """, params)
        barras_categoria_ventas_number = [{'categoria': row[0], 'ventas': row[1]} for row in cursor.fetchall()]

    return JsonResponse({
        'total_ventas': total_ventas,
        'ventas_segmento': ventas_segmento,
        'top_clientes': top_clientes,
        'top_productos': top_productos,
        'linea_tiempo': linea_tiempo,
        'barras_categoria': barras_categoria,
        'linea_tiempo_ventas_number': linea_tiempo_ventas_number,
        'barras_categoria_ventas_number': barras_categoria_ventas_number,
        'numeber_ventas': numeber_ventas,
        'ventas_segmento_number_ventas': ventas_segmento_number_ventas
    })




# funcion login plus para que sepan que se manejar autentificacion proteccion de rutas y creacion formularios dinamicos en python
def login(request):
    if request.method == 'POST':
        form  = login(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                form.add_error(None, 'Usuario o contraseña incorrectos')
    else:
        form = login()
    return render(request, 'dashboard/index.html', {'form': form})



def listar_ventas(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM superstore_data ORDER BY Order_Date DESC LIMIT 100")
        ventas = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    return render(request, 'dashboard/crud/index.html', {'ventas': ventas})


def create(request):
    if request.method == 'POST':
        form = VentasForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO superstore_data (
                        id, row_id, order_id, order_date, ship_date,
                        ship_mode, customer_id, customer_name, segment,
                        country, city, state, postal_code, region,
                        product_id, category, sub_category, product_name, sales
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                              %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, [
                    form.cleaned_data['id'],
                    form.cleaned_data['row_id'],
                    form.cleaned_data['order_id'],
                    form.cleaned_data['order_date'],
                    form.cleaned_data['ship_date'],
                    form.cleaned_data['ship_mode'],
                    form.cleaned_data['customer_id'],
                    form.cleaned_data['customer_name'],
                    form.cleaned_data['segment'],
                    form.cleaned_data['country'],
                    form.cleaned_data['city'],
                    form.cleaned_data['state'],
                    form.cleaned_data['postal_code'],
                    form.cleaned_data['region'],
                    form.cleaned_data['product_id'],
                    form.cleaned_data['category'],
                    form.cleaned_data['sub_category'],
                    form.cleaned_data['product_name'],
                    form.cleaned_data['sales'],
                ])
            return redirect('ventas')
    else:
        form = VentasForm()
    return render(request, 'dashboard/crud/create.html', {'form': form})


def edit(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM superstore_data WHERE id = %s", [id])
        row = cursor.fetchone()
        if not row:
            return redirect('ventas')

        form = VentasForm(request.POST or None, initial=dict(zip([col[0] for col in cursor.description], row)))

        if form.is_valid():
            cursor.execute("""
                UPDATE superstore_data SET
                    row_id = %s, order_id = %s, order_date = %s, ship_date = %s,
                    ship_mode = %s, customer_id = %s, customer_name = %s, segment = %s,
                    country = %s, city = %s, state = %s, postal_code = %s, region = %s,
                    product_id = %s, category = %s, sub_category = %s, product_name = %s,
                    sales = %s
                WHERE id = %s
            """, [
                form.cleaned_data['row_id'],
                form.cleaned_data['order_id'],
                form.cleaned_data['order_date'],
                form.cleaned_data['ship_date'],
                form.cleaned_data['ship_mode'],
                form.cleaned_data['customer_id'],
                form.cleaned_data['customer_name'],
                form.cleaned_data['segment'],
                form.cleaned_data['country'],
                form.cleaned_data['city'],
                form.cleaned_data['state'],
                form.cleaned_data['postal_code'],
                form.cleaned_data['region'],
                form.cleaned_data['product_id'],
                form.cleaned_data['category'],
                form.cleaned_data['sub_category'],
                form.cleaned_data['product_name'],
                form.cleaned_data['sales'],
                id
            ])
            return redirect('ventas')

    return render(request, 'dashboard/crud/edit.html', {'form': form})

def delete(request, id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM superstore_data WHERE id = %s", [id])
    return redirect('ventas')