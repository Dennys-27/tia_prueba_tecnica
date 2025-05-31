// main.js completo

function cargarDatos() {
  const fecha_inicio = document.getElementById('fecha_inicio').value;
  const fecha_fin = document.getElementById('fecha_fin').value;
  const categoria = document.getElementById('categoria').value;
  const subcategoria = document.getElementById('subcategoria').value;
  const estado = document.getElementById('estado')?.value || ''; // Manejo de estado opcional
  const ciudad = document.getElementById('ciudad')?.value || ''; // Manejo de ciudad opcional

  const url = new URL('/get_datos/', window.location.origin);
  url.searchParams.append('fecha_inicio', fecha_inicio);
  url.searchParams.append('fecha_fin', fecha_fin);
  url.searchParams.append('categoria', categoria);
  url.searchParams.append('subcategoria', subcategoria);
  url.searchParams.append('estado', estado);
  url.searchParams.append('ciudad', ciudad);

  fetch(url)
    .then(response => response.json())
    .then(data => {
      console.log(data);

      // Indicadores
      const indicadoresDiv = document.getElementById('indicadores');
      /* indicadoresDiv.innerHTML = `
        <div class="card p-3 mb-3">
          <h5>Total Ventas</h5>
          <p>$${parseFloat(data.total_ventas).toFixed(2)}</p>
        </div>
        <div class="card p-3">
          <h5>Ventas por Segmento</h5>
          <ul>
            ${data.ventas_segmento.map(item => `
              <li>${item.segmento}: $${parseFloat(item.ventas).toFixed(2)}</li>
            `).join('')}
          </ul>
        </div>
      `; */

      //MEJORANDO ESTILOS DE LOS INDICADORES
      indicadoresDiv.innerHTML = `
        <div class="card mb-4" style="background-color: #1c1c1c; color: #f8f9fa; border-radius: 8px; border: 1.5px solid #e55353;">
          <div class="card-body">
            <div class="row">
              <div class="col-md-6 mb-3">
                <h5 class="card-title" style="color: #e55353; font-weight: 600;">
                  <i class="fas fa-dollar-sign me-2"></i>Total Ventas (DINERO)
                </h5>
                <p class="card-text fs-4">$${parseFloat(data.total_ventas).toFixed(2)}</p>
              </div>
              <div class="col-md-6 mb-3">
                <h5 class="card-title" style="color: #e55353; font-weight: 600;">
                  <i class="fas fa-shopping-cart me-2"></i>N° Ventas Realizadas
                </h5>
                <p class="card-text fs-4">#${parseInt(data.numeber_ventas)}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="card mb-4" style="background-color: #1c1c1c; color: #f8f9fa; border-radius: 8px; border: 1.5px solid #e55353;">
          <div class="row">
            <div class="col-md-6 mb-3">
              <div class="card-body">
                <h5 class="card-title mb-3" style="color: #e55353; font-weight: 600;">
                  <i class="fas fa-dollar-sign me-2"></i>Ventas por Segmento (Monto $)
                </h5>
                <ul class="list-group list-group-flush">
                  ${data.ventas_segmento.map(item => `
                    <li class="list-group-item d-flex justify-content-between align-items-center" style="background-color: #2a2a2a; border: none; color: #f8f9fa;">
                      <span>${item.segmento}</span>
                      <span class="badge rounded-pill" style="background-color: #e55353;">$${parseFloat(item.ventas).toFixed(2)}</span>
                    </li>
                  `).join('')}
                </ul>
              </div>
            </div>

            <div class="col-md-6 mb-3">
              <div class="card-body">
                <h5 class="card-title mb-3" style="color: #e55353; font-weight: 600;">
                  <i class="fas fa-shopping-cart me-2"></i>Ventas por Segmento (Cantidad)
                </h5>
                <ul class="list-group list-group-flush">
                  ${data.ventas_segmento_number_ventas.map(item => `
                    <li class="list-group-item d-flex justify-content-between align-items-center" style="background-color: #2a2a2a; border: none; color: #f8f9fa;">
                      <span>${item.segmento}</span>
                      <span class="badge rounded-pill" style="background-color: #4a90e2;">${parseInt(item.ventas)}</span>
                    </li>
                  `).join('')}
                </ul>
              </div>
            </div>
          </div>
        </div>
      `;


      // Tabla Clientes
      const tablaClientesDiv = document.getElementById('tabla_clientes');
      tablaClientesDiv.innerHTML = `
        <h5 style="color:#e55353; font-weight: 600;"><i class="fas fa-users me-2"></i> Top Clientes</h5>
        <table id="tablaClientesDT" class="table table-striped" style="background-color:#1c1c1c; color:#f8f9fa;">
          <thead style="background-color:#2a2a2a; color:#e55353;">
            <tr>
              <th>Cliente</th>
              <th>Segmento</th>
              <th>Ciudad</th>
              <th>Estado</th>
              <th>Total Ventas</th>
            </tr>
          </thead>
          <tbody>
            ${data.top_clientes.map(item => `
              <tr style="color:#f8f9fa;">
                <td>${item.cliente}</td>
                <td>${item.segmento}</td>
                <td>${item.ciudad}</td>
                <td>${item.estado}</td>
                <td>$${parseFloat(item.total).toFixed(2)}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
      new DataTable('#tablaClientesDT', {
        dom: 'Bfrtip',
        buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
      });

      // Tabla Productos
      const tablaProductosDiv = document.getElementById('tabla_productos');
      tablaProductosDiv.innerHTML = `
        <h5 style="color:#e55353; font-weight: 600;"><i class="fas fa-box-open me-2"></i> Top Productos</h5>
        <table id="tablaProductosDT" class="table table-striped" style="background-color:#1c1c1c; color:#f8f9fa;">
          <thead style="background-color:#2a2a2a; color:#e55353;">
            <tr>
              <th>ID Producto</th>
              <th>Categoría</th>
              <th>Subcategoría</th>
              <th>Nombre Producto</th>
              <th>Vendidos</th>
            </tr>
          </thead>
          <tbody>
            ${data.top_productos.map(item => `
              <tr style="color:#f8f9fa;">
                <td>${item.producto_id}</td>
                <td>${item.categoria}</td>
                <td>${item.subcategoria}</td>
                <td>${item.nombre}</td>
                <td>${item.vendidos}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;
      new DataTable('#tablaProductosDT', {
        dom: 'Bfrtip',
        buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
      });


      // Gráficos
      graficarLineas(data.linea_tiempo);
      graficarBarras(data.barras_categoria);
      graficarBarrasVentasNumber(data.barras_categoria_ventas_number);
      graficarLineasVentasNumber(data.linea_tiempo_ventas_number);
    })
    .catch(error => {
      console.error('Error al obtener datos:', error);
    });
} 






function graficarLineas(datos) {
  const ctx = document.getElementById("grafico_linea").getContext("2d");
  const labels = datos.map(d => d.fecha);
  const valores = datos.map(d => d.ventas);

  if (window.graficoLineaInstance) {
    window.graficoLineaInstance.destroy();
  }

  window.graficoLineaInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Ventas",
        data: valores,
        borderColor: "blue",
        fill: false,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        title: { display: true, text: "Ventas por Línea de Tiempo (Dinero en Efectivo)" }
      }
    }
  });
}

function graficarLineasVentasNumber(datos) {
  const ctx = document.getElementById("grafico_linea_ventas_number").getContext("2d");
  const labels = datos.map(d => d.fecha);
  const valores = datos.map(d => d.ventas);

  if (window.graficoLineaVentasNumberInstance) {
    window.graficoLineaVentasNumberInstance.destroy();
  }

  window.graficoLineaVentasNumberInstance = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Ventas",
        data: valores,
        borderColor: "blue",
        fill: false,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: "top" },
        title: { display: true, text: "Ventas por Línea de Tiempo (Numero de Ventas)" }
      }
    }
  });
}



function graficarBarras(datos) {
  const ctx = document.getElementById("grafico_barras").getContext("2d");
  const labels = datos.map(d => d.categoria);
  const valores = datos.map(d => d.ventas);

  if (window.graficoBarrasInstance) {
    window.graficoBarrasInstance.destroy();
  }

  window.graficoBarrasInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Ventas por Categoría",
        data: valores,
        backgroundColor: "rgba(54, 162, 235, 0.6)"
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: "Ventas por Categoría (Dinero en Efectivo)" }
      }
    }
  });
}


function graficarBarrasVentasNumber(datos) {
  const ctx = document.getElementById("grafico_barras_ventas_number").getContext("2d");
  const labels = datos.map(d => d.categoria);
  const valores = datos.map(d => d.ventas);

  if (window.graficoBarrasVentasNumberInstance) {
    window.graficoBarrasVentasNumberInstance.destroy();
  }

  window.graficoBarrasVentasNumberInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Ventas por Categoría",
        data: valores,
        backgroundColor: "rgba(54, 162, 235, 0.6)"
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: "Ventas por Categoría (Numero de Ventas)" }
      }
    }
  });
}



//USO DE MIS BOTONES ANTIGUO
/* function cargarCategorias() {
  fetch('/categorias/')
    .then(res => res.json())
    .then(data => {
      const selectCategoria = document.getElementById('categoria');
      data.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        selectCategoria.appendChild(option);
      });
    })
    .catch(err => console.error('Error al cargar categorías:', err));
}

window.addEventListener('DOMContentLoaded', cargarCategorias);


function cargarSubCategorias() {
  fetch('/sub_categorias/')
    .then(res => res.json())
    .then(data => {
      const selectSubCategoria = document.getElementById('subcategoria');
      data.forEach(cat => {
        const option = document.createElement('option');
        option.value = cat;
        option.textContent = cat;
        selectSubCategoria.appendChild(option);
      });
    })
    .catch(err => console.error('Error al cargar categorías:', err));
}

window.addEventListener('DOMContentLoaded', cargarSubCategorias); */



//USO DE MIS BOTONES NUEVO OPTIMIZADO
function cargarOpciones(url, selectId) {
  fetch(url)
    .then(res => res.json())
    .then(data => {
      const select = document.getElementById(selectId);
      select.innerHTML = '<option value="">Seleccione</option>';
      data.forEach(item => {
        const option = document.createElement('option');
        option.value = item;
        option.textContent = item;
        select.appendChild(option);
      });
    })
    .catch(err => console.error(`Error al cargar datos de ${selectId}:`, err));
}

window.addEventListener('DOMContentLoaded', () => {
  cargarOpciones('/categorias/', 'categoria');
  cargarOpciones('/sub_categorias/', 'subcategoria');
  cargarOpciones('/estado/', 'estado');
  cargarOpciones('/ciudad/', 'ciudad');
});
