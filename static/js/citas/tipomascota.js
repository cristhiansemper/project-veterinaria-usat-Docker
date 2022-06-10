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
///////////////////////////////////////////////////////////////////////////
let inptDescripcion=document.querySelector('#id_descripcion');

const btnGuardarTipoMascota=document.querySelector('#registrar-tipomascota');
const btnModificarTipoMascota=document.querySelector('#modificar-tipomascota');

const btnModalTipoMascota=document.querySelector('#btn-modal-tipomascota');
btnModalTipoMascota.addEventListener('click',cleanData);
///////////////////////////////////////////////////////////////////////////

$(document).ready(function(){
    listarTipoMascota();
});

async function listarTipoMascota(){
    
    try {
        const response = await fetch("/citas/listar_tipo_mascota/");
        const result = await response.json();
        let resultado = JSON.parse(result.tipo_mascota)
        console.log(resultado);
        if ($.fn.DataTable.isDataTable('#table-tipomascota')) {
            $('#table-tipomascota').DataTable().destroy();
        }
        $('#table-tipomascota tbody').html("");
        for (i = 0; i < resultado.length; i++) {
            let fila = `<tr>`;
            fila += `<td>` + resultado[i].pk + `</td>`;
            fila += `<td>` + resultado[i].fields.descripcion + `</td>`;
            if (resultado[i].fields.estado) {
                fila += `<td><span class="badge bg-success">Activo</span></td>`;  
                
            } else {
                fila += `<td><span class="badge bg-danger">Inactivo</span></td>`;
            }
            fila += `<td>
                            <div class="row">
                                <div class="form-group col-sm-4">
                                    <a href="#" class="btn-cargarDatos-modificar" data-toggle="modal" data-target="#modal-xl" onclick="cargarDatos('${resultado[i].pk}','${resultado[i].fields.descripcion}',${resultado[i].fields.estado})">
                                        <i class="bi bi-pencil-square"></i>
                                    </a>                                   
                                </div>
                                <div class="form-group col-sm-4">
                                    <a href="#" class="btn-eliminar" onclick="eliminarTipoMascota('${resultado[i].pk}')">
                                        <i class="bi bi-trash"></i>
                                    </a>
                                </div>
                            </div>
                   </td>`;

            fila += `</tr>`;
            $('#table-tipomascota tbody').append(fila);
        }
        $('#table-tipomascota').DataTable({
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
///////////////////////////////////////////////////////////////////////////

btnGuardarTipoMascota.addEventListener('click',registroTipoMascota);
async function registroTipoMascota(){
    const form = new FormData(document.querySelector('#form-tipomascota'));
    form.set('descripcion',form.get('descripcion').trim());
    try {
        const response = await fetch('/citas/tipo_mascota/',{
            method:'POST',
            body:form,
            headers:{'X-CSRFToken':getCookie('csrftoken')}
        });
        const result = await response.json()
        const {status} = result;
        const {mensaje} = result;
        if (status){
            listarTipoMascota();
            imprimirMessage('Éxito',mensaje,'success');
            cleanData();
        }else{
            imprimirMessage('Sistema',mensaje,'info');
        }
    } catch (error) {
        console.log(error)
    }
}

///////////////////////////////////////////////////////////////////////////

let pk_tp=0;
function cargarDatos(pk, descripcion, estado){
    pk_tp=pk;
    inptDescripcion.value=descripcion;
    if(estado){
        $("#id_estado").prop('checked', true);
    }else{
        $("#id_estado").prop('checked', false);
    }
    btnGuardarTipoMascota.disabled=true;
    btnModificarTipoMascota.disabled=false;

}

btnModificarTipoMascota.addEventListener('click',modificarTipoMascota);
async function modificarTipoMascota(){
    const form = new FormData(document.querySelector('#form-tipomascota'));
    form.set('descripcion',form.get('descripcion').trim());
    form.append('id_tipo_mascota',pk_tp);
    try {
        const response = await fetch('/citas/modificar_tipo_mascota/',{
            method:'POST',
            body:form,
            headers:{'X-CSRFToken':getCookie('csrftoken')}
        });
        const result = await response.json()
        const {status} = result;
        const {mensaje} = result;
        if (status){
            listarTipoMascota();
            imprimirMessage('Éxito',mensaje,'success');
            cleanData();
        }else{
            imprimirMessage('Sistema',mensaje,'info');
        }
    } catch (error) {
        console.log(error)
    }
}



function cleanData(){
    pk_tp=0;
    inptDescripcion.value='';
    btnGuardarTipoMascota.disabled=false;
    btnModificarTipoMascota.disabled=true;
}

function eliminarTipoMascota(id) {

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
        console.log(id)
        const response = await fetch("/citas/eliminar_tipo_mascota/" + id + "/");
        const result = await response.json();
        const {status}=result;
        if (status){
            const{mensaje}=result;
            listarTipoMascota();
            imprimirMessage("Éxito",mensaje,"success");
        }
    } catch (error) {
        console.log(error)
        imprimirMessage("Sistema","Error al eliminar animal","error");
    }
}

///////////////////////////////////////////////////////////////////////////

async function registrarTipoMascota(){
    const form = new FormData(document.querySelector('#form-productos'));
    form.set('nombre',form.get('nombre').trim());
    form.set('descripcion',form.get('descripcion').trim());
    try {
        const response = await fetch('/producto/productos/',{
            method:'POST',
            body:form,
            headers:{'X-CSRFToken':getCookie('csrftoken')}
        });
        const result = await response.json()
        console.log(result)
        const {status} = result;
        const {mensaje} = result;
        if (status){
            listarProductos();
            imprimirMessage('Éxito',mensaje,'success');
            cleanData();
        }else{
            imprimirMessage('Sistmea',mensaje,'info');
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