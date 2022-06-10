///////////////////////////////////////////////////////////////////////////
let inptDescripcion=document.querySelector('#id_descripcion');
let inptPrecio = document.querySelector("#id_precio");
let inptTipoServicio = document.querySelector("#id_id_tipo_servicio")
let pk_s = 0;

const btnGuardarServicio=document.querySelector('#registrar-servicio');
const btnModificarServicio=document.querySelector('#modificar-servicio');
const btnModalServicio=document.querySelector('#btn-modal-servicio');

btnModalServicio.addEventListener('click',cleanData);
btnGuardarServicio.addEventListener('click',registrarServicio);
btnModificarServicio.addEventListener('click', modificarServicio)

$(document).ready(function(){
    listarServicios();
})
///////////////////////////////////////////////////////////////////////////

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function listarServicios() {
    try {
        const response = await fetch("/citas/listar_servicio/");
        const result = await response.json();

        console.log(result) // 
        let resultado = result.servicio
        if ($.fn.DataTable.isDataTable('#table-servicio')) {
            $('#table-servicio').DataTable().destroy();
        }
        $('#table-servicio tbody').html("");
        for (i = 0; i < resultado.length; i++) {
            let fila = `<tr>`;
            fila += `<td>` + resultado[i][0] + `</td>`;
            fila += `<td>` + resultado[i][1] + `</td>`;
            fila += `<td>` + resultado[i][2] + `</td>`;
            fila += `<td>` + resultado[i][5] + `</td>`;
            if (resultado[i][3]) {
                fila += `<td><span class="badge bg-success">Activo</span></td>`;
            } else {
                fila += `<td><span class="badge bg-danger">Inactivo</span></td>`;
            }
            fila += `<td>
                            <div class="row">
                                <div class="form-group col-sm-4">
                                    <a href="#" class="btn-cargarDatos-modificar" data-toggle="modal" data-target="#modal-xl" onclick="cargarDatos('${resultado[i][0]}','${resultado[i][1]}','${resultado[i][2]}','${resultado[i][3]}','${resultado[i][4]}')">
                                        <i class="bi bi-pencil-square"></i>
                                    </a>                                   
                                </div>
                                <div class="form-group col-sm-4">
                                    <a href="#" class="btn-eliminar" onclick="eliminarServicio('${resultado[i][0]}')">
                                        <i class="bi bi-trash"></i>
                                    </a>
                                </div>
                            </div>
                   </td>`;

            fila += `</tr>`;
            $('#table-servicio tbody').append(fila);
        }
        $('#table-servicio').DataTable({
            language: {
                decimal: "",
                emptyTable: "No hay información",
                info: "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                infoEmpty: "Mostrando 0 to 0 of 0 Entradas",
                infoFiltered: "(Filtrado de _MAX_ total entradas)",
                infoPostFix: "",
                thousands: ",",
                lengthMenu: "Mostrar _MENU_ Entradas",
                loadingRecords: "Cargando...",
                processing: "Procesando...",
                search: "Buscar:",
                zeroRecords: "Sin resultados encontrados",
                paginate: {
                    first: "Primero",
                    last: "Ultimo",
                    next: "Siguiente",
                    previous: "Anterior",
                },
            },
            lengthMenu: [5, 10, 20],
        })

    } catch (error) {
        console.log(error)
    }
}

function eliminarServicio(id) {
    Swal.fire({
        "title": "¿Estás seguro?",
        "text": "Esta acción no se puede revertir",
        "icon": "question",
        "showCancelButton": true,
        "cancelButtonText": "No, cancelar",
        "confirmButtonText": "Sí, eliminar",
        "confirmButtonColor": "#dc3545"
    }).then(function (result){
        if (result.isConfirmed){
            confirmarEliminar(id);
        }
    })
}

async function confirmarEliminar(id){
    try {
        const response = await fetch("/citas/eliminar_servicio/" + id + "/");
        const result = await response.json();
        const {status}=result;
        if (status){
            const{mensaje}=result;
            listarServicios();
            imprimirMessage("Éxito",mensaje,"success");
        }
    } catch (error) {
        console.log(error)
        imprimirMessage("Sistema","Error al eliminar servicio","error");
    }
}


async function registrarServicio(){
    const form = new FormData(document.querySelector('#form-servicio'));
    form.set('descripcion',form.get('descripcion').trim());
    form.set('precio',form.get('precio').trim());
    form.set('id_tipo_servicio', form.get('id_tipo_servicio').trim())
    
    try {
        const response = await fetch('/citas/servicio/',{
            method:'POST',
            body:form,
            headers:{'X-CSRFToken':getCookie('csrftoken')}
        });
        const result = await response.json()
        const {status} = result;
        const {mensaje} = result;
        if (status){
            listarServicios();
            imprimirMessage('Éxito',mensaje,'success');
            cleanData();
        }else{
            imprimirMessage('Sistema',mensaje,'info');
        }
    } catch (error) {
        console.log(error)
    }
}

async function modificarServicio(){
    const form = new FormData(document.querySelector('#form-servicio'));
    form.set('descripcion',form.get('descripcion').trim());
    form.set('precio',form.get('precio').trim());
    form.append('id_servicio', pk_s);
    try {
        const response = await fetch('/citas/modificar_servicio/',{
            method:'POST',
            body:form,
            headers:{'X-CSRFToken':getCookie('csrftoken')}
        });
        const result = await response.json()
        const {status} = result;
        const {mensaje} = result;
        if (status){
            listarServicios();
            imprimirMessage('Éxito',mensaje,'success');
            cleanData();
        }else{
            imprimirMessage('Sistema',mensaje,'info');
        }
    } catch (error) {
        console.log(error)
    }
}

function imprimirMessage(title, message, icon) {
    Swal.fire({
        "title": title,
        "text": message,
        "icon": icon
    })
}

function cargarDatos(pk,descripcion, precio, estado,tipoServicioId){
    pk_s=pk;
    inptDescripcion.value=descripcion;
    inptPrecio.value = precio;
    inptTipoServicio.value = tipoServicioId
    if(estado){
        $("#id_estado").prop('checked', true);
    }else{
        $("#id_estado").prop('checked', false);
    }
    btnGuardarServicio.disabled=true;
    btnModificarServicio.disabled=false;
}

function cleanData(){
    pk_s=0;
    inptDescripcion.value='';
    inptPrecio.value = '';
    inptTipoServicio.value = ''
    btnGuardarServicio.disabled=false;
    btnModificarServicio.disabled=true;
}